"""Encode the two approved generated clips for responsive scroll seeking.

Requires imageio-ffmpeg (or pass an ffmpeg executable as argv[1]). No regeneration.
Sources stay unchanged in audit/source. Outputs: public/assets/scene03-*.mp4 and
qa/2026-09-25-home/frames/*.jpg (three actual decoded frames per composition).
"""
from pathlib import Path
import subprocess
import sys
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = sys.argv[1] if len(sys.argv) > 1 else imageio_ffmpeg.get_ffmpeg_exe()
FRAMES = ROOT / 'qa/2026-09-25-home/frames'
FRAMES.mkdir(parents=True,exist_ok=True)
for device in ['desktop','mobile']:
    source = ROOT / f'audit/source/scene03-{device}-original.mp4'
    target = ROOT / f'public/assets/scene03-{device}.mp4'
    subprocess.run([FFMPEG,'-y','-hide_banner','-loglevel','error','-i',str(source),
        '-an','-vf','fps=24','-c:v','libx264','-preset','slow','-crf','21',
        '-pix_fmt','yuv420p','-g','8','-keyint_min','8','-sc_threshold','0',
        '-movflags','+faststart',str(target)],check=True)
    for name,second in [('start',0),('middle',3.5),('end',6.9)]:
        subprocess.run([FFMPEG,'-y','-hide_banner','-loglevel','error','-ss',str(second),
            '-i',str(target),'-frames:v','1','-q:v','2',str(FRAMES/f'{device}-{name}.jpg')],check=True)
    print(target.name, target.stat().st_size, flush=True)
