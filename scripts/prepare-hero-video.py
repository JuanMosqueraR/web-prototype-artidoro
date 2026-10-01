"""Encode the approved L28 hero clips for scroll seeking (desktop 16:9, mobile 9:16).

Requires imageio-ffmpeg (or pass an ffmpeg executable as argv[1]) and Pillow with AVIF support. No regeneration.
Use --video-only to redo just the videos and posters (the AVIF/WebP sequences take several minutes).
Sources stay unchanged in audit/source (two 5 s clips per format, origin then beans).

Outputs in public/assets:
- hero-{desktop,mobile}.mp4        scroll-seekable video, constant 24 fps (lowest CRF that fits the weight budget)
- hero-{device}-{start,end}.webp   posters cut from the ORIGINAL clips (not from the compressed video)
- hero-seq/{device}-avif/f###.avif 12 fps image sequence drawn on a canvas (mobile always; desktop as fallback),
                                   highest AVIF quality that fits the weight budget
- hero-seq/{device}-webp/f###.webp 6 fps WebP sequence for browsers without AVIF (iOS < 16)
iOS Safari/Chrome do not reliably prepare a video that is never played (and Low Power Mode blocks inline
playback altogether), so the sequence is the dependable path there; see scenes.js.
"""
from pathlib import Path
import io
import shutil
import subprocess
import sys
import imageio_ffmpeg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
VIDEO_ONLY = '--video-only' in sys.argv  # re-encode the videos and posters only; skip the (slow) sequences
FFMPEG = ARGS[0] if ARGS else imageio_ffmpeg.get_ffmpeg_exe()
TMP = ROOT / 'dist' / 'hero-frames'
TMP.mkdir(parents=True, exist_ok=True)
ASSETS = ROOT / 'public/assets'
# Weight budgets: video 3.5 MB per format (raised from 2.5 MB after the user asked for more sharpness); the image
# sequences are fallbacks only (mobile <= 1.5 MB).
SCALE = {'desktop': '1280:-2', 'mobile': '-2:1280'}
VIDEO_BUDGET = {'desktop': 3_500_000, 'mobile': 3_500_000}  # the mobile videos of the reference sites weigh 2.4 and 3.5 MB
SEQ_BUDGET = {'desktop': 2_400_000, 'mobile': 1_500_000}
FPS = 12
# The generated clips carry grain and blocky noise. A light spatial/temporal denoise before scaling, and a mild
# sharpen after it, give a visibly cleaner picture at the same weight (checked by eye at 100 %).
CLEAN = 'hqdn3d=3:2.5:4:4,'
SHARPEN = 'unsharp=5:5:0.7:5:5:0.0,'


def run(*args):
    subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', *args], check=True)


def concat(device, scale, fps, extra):
    """Origin then beans clip. The beans clip starts on the frame the origin clip ends on: drop its first frame."""
    origin = ROOT / f'audit/source/hero-{device}-origin-original.mp4'
    beans = ROOT / f'audit/source/hero-{device}-beans-original.mp4'
    return ['-i', str(origin), '-i', str(beans), '-an', '-filter_complex',
            f'[0:v]fps={fps},{CLEAN}scale={scale}:flags=lanczos,{SHARPEN}setsar=1[a];[1:v]fps={fps},{CLEAN}scale={scale}:flags=lanczos,{SHARPEN}setsar=1,trim=start_frame=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]',
            '-map', '[v]', *extra]


def encode_video(device):
    target = ASSETS / f'hero-{device}.mp4'
    # Constant 24 fps and a 12288 time scale, like the 03 video that iPhones prepared and scrubbed: the concat/trim
    # output otherwise carries an irregular 24.10 fps / 1 000 000 time scale. GOP 4 without B-frames: a seek decodes at most
    # 3 frames and nothing is reordered (the reference sites use all-intra video; at our weight that costs too much quality).
    # Measured at equal size on one clip: p90 seek latency 27.6 -> 19.3 ms, max 42 -> 22 ms (4x CPU), SSIM 0.9895 -> 0.9875.
    for crf in (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30):
        run(*concat(device, SCALE[device], 24, ['-r', '24', '-fps_mode', 'cfr', '-video_track_timescale', '12288', '-c:v', 'libx264', '-preset', 'slow',
                                                  '-crf', str(crf), '-pix_fmt', 'yuv420p', '-g', '4', '-keyint_min', '4', '-sc_threshold', '0', '-bf', '0',
                                                  '-movflags', '+faststart', str(target)]))
        if target.stat().st_size <= VIDEO_BUDGET[device]:
            break
    print(target.name, 'crf', crf, target.stat().st_size, flush=True)


def posters(device):
    # First and last frame of the original footage, at poster quality.
    frames = TMP / f'{device}-poster'
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    run(*concat(device, SCALE[device], 12, ['-r', str(FPS), str(frames / 'p%03d.png')]))
    files = sorted(frames.glob('p*.png'))
    for name, png in [('start', files[0]), ('end', files[-1])]:
        Image.open(png).convert('RGB').save(ASSETS / f'hero-{device}-{name}.webp', quality=86, method=6)


def sequences(device):
    frames = TMP / f'{device}-seq'
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    run(*concat(device, SCALE[device], FPS, ['-r', str(FPS), str(frames / 's%03d.png')]))
    files = sorted(frames.glob('s*.png'))
    images = [Image.open(f).convert('RGB') for f in files]
    out = ASSETS / 'hero-seq' / f'{device}-avif'
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    # Highest quality that fits the budget: encode in memory, then write the winner.
    chosen = None
    for quality in range(70, 29, -3):
        blobs = []
        for image in images:
            buffer = io.BytesIO()
            image.save(buffer, 'AVIF', quality=quality, speed=5)
            blobs.append(buffer.getvalue())
        if sum(map(len, blobs)) <= SEQ_BUDGET[device]:
            chosen = (quality, blobs)
            break
    assert chosen, 'No AVIF quality fits the budget.'
    for i, blob in enumerate(chosen[1]):
        (out / f'f{i:03d}.avif').write_bytes(blob)
    print(f'hero-seq/{device}-avif', len(images), 'frames at', FPS, 'fps, q', chosen[0], sum(map(len, chosen[1])), flush=True)
    # WebP fallback at 6 fps, cut from the same decoded frames.
    fallback = ASSETS / 'hero-seq' / f'{device}-webp'
    shutil.rmtree(fallback, ignore_errors=True)
    fallback.mkdir(parents=True)
    for i, image in enumerate(images[::2]):
        image.save(fallback / f'f{i:03d}.webp', quality=60, method=6)
    total = sum(f.stat().st_size for f in fallback.glob('*.webp'))
    print(f'hero-seq/{device}-webp', len(images[::2]), 'frames at 6 fps', total, flush=True)


for device in SCALE:
    encode_video(device)
    posters(device)
    if not VIDEO_ONLY:
        sequences(device)
