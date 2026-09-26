"""Prepare delivery copies of the two user-approved Tarata reference photographs.

Python + Pillow; resize and WebP encoding only. No generative edits, retouching,
cropped source, invented details, text changes, or writes to reference/.
Original bytes are retained in audit/source. Layout cropping lives in CSS.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
for source, output, width in [
    ('tarata-facade-motorcycle-original.jpg', 'tarata-facade.webp', 780),
    ('tarata-counter-staff-original.jpg', 'tarata-interior.webp', 765),
    ('tarata-counter-staff-original.jpg', 'tarata-interior-mobile.webp', 420),
]:
    with Image.open(ROOT / 'audit/source' / source) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        image.thumbnail((width, 1400), Image.Resampling.LANCZOS)
        path = ROOT / 'public/assets' / output
        image.save(path, quality=83, method=6)
        print(f'{output}: {image.width}x{image.height}, {path.stat().st_size} bytes')
