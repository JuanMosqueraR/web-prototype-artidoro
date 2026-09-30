"""Encode the approved L28 hero clips for scroll seeking (desktop 16:9, mobile 9:16).

Requires imageio-ffmpeg (or pass an ffmpeg executable as argv[1]). No regeneration.
Sources stay unchanged in audit/source (two 5 s clips per format, origin then beans).
Outputs: public/assets/hero-{desktop,mobile}.mp4 plus the decoded first and last frames
as posters public/assets/hero-{desktop,mobile}-{start,end}.webp, so the poster never
jumps when the video takes over.
"""
from pathlib import Path
import subprocess
import sys
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = sys.argv[1] if len(sys.argv) > 1 else imageio_ffmpeg.get_ffmpeg_exe()
TMP = ROOT / 'dist' / 'hero-frames'
TMP.mkdir(parents=True, exist_ok=True)
# Short GOP so scroll seeking lands on a nearby keyframe; CRF chosen to stay within the L28 weight budget.
SETTINGS = {'desktop': ('1280:-2', '28'), 'mobile': ('-2:1280', '29')}


def run(*args):
    subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', *args], check=True)


for device, (scale, crf) in SETTINGS.items():
    origin = ROOT / f'audit/source/hero-{device}-origin-original.mp4'
    beans = ROOT / f'audit/source/hero-{device}-beans-original.mp4'
    target = ROOT / f'public/assets/hero-{device}.mp4'
    # The beans clip starts on the frame the origin clip ends on: drop its first frame to avoid a hold.
    run('-i', str(origin), '-i', str(beans), '-an', '-filter_complex',
        f'[0:v]fps=24,scale={scale},setsar=1[a];[1:v]fps=24,scale={scale},setsar=1,trim=start_frame=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]',
        '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', crf, '-pix_fmt', 'yuv420p',
        '-g', '8', '-keyint_min', '8', '-sc_threshold', '0', '-movflags', '+faststart', str(target))
    for name, where in [('start', ['-ss', '0']), ('end', ['-sseof', '-0.05'])]:
        png = TMP / f'{device}-{name}.png'
        run(*where, '-i', str(target), '-frames:v', '1', str(png))
        from PIL import Image
        Image.open(png).convert('RGB').save(ROOT / f'public/assets/hero-{device}-{name}.webp', quality=80, method=6)
    print(target.name, target.stat().st_size, flush=True)
    # Image sequence for browsers that refuse to prepare the video (iOS Low Power Mode blocks even muted
    # inline playback): 6 fps from the same encode, drawn on a canvas by scenes.js.
    seq = ROOT / f'public/assets/hero-seq/{device}'
    seq.mkdir(parents=True, exist_ok=True)
    for old in seq.glob('*.webp'):
        old.unlink()
    for old in TMP.glob(f'{device}-seq-*.png'):
        old.unlink()
    run('-i', str(target), '-vf', 'fps=6', str(TMP / f'{device}-seq-%03d.png'))
    from PIL import Image
    frames = sorted(TMP.glob(f'{device}-seq-*.png'))
    for i, png in enumerate(frames):
        Image.open(png).convert('RGB').save(seq / f'f{i:03d}.webp', quality=52, method=6)
    total = sum(f.stat().st_size for f in seq.glob('*.webp'))
    print(f'hero-seq/{device}', len(frames), 'frames', total, flush=True)
