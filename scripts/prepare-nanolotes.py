"""Prepare the Nanolotes tile photo (L27 follow-up, explicit user request).

Python + Pillow; original pixels, rectangular whitespace crop, no artwork edits.
Reads audit/source/nanolote-original.jpg; writes public/assets/nanolote-tin.webp.
Source and crop coordinates are recorded in audit/assets.json.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CROP = (306, 255, 795, 818)
MAXIMUM = 620


def main():
    image = Image.open(ROOT / 'audit/source/nanolote-original.jpg').convert('RGB')
    assert image.size == (1080, 1080), 'Review crop if source changes.'
    image = image.crop(CROP)
    image.thumbnail((MAXIMUM, MAXIMUM), Image.Resampling.LANCZOS)
    dest = ROOT / 'public/assets/nanolote-tin.webp'
    image.save(dest, quality=90, method=6)
    print(dest.name, image.size, dest.stat().st_size)


if __name__ == '__main__':
    main()
