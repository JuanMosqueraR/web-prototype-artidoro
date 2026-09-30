"""Prepare the L28 stills of 03 «De la bolsa a tu taza» (grind, bloom, drip, still life).

Python + Pillow; generated sources in audit/source (see audit/source/hero-generation.json).
Desktop: 1600 px wide WebP. Mobile: rectangular 9:16 crops of the same landscape frames,
centred on the subject, except the still life, which has its own vertical composition.
Only resizing and rectangular crops; no retouching.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'audit/source'
OUT = ROOT / 'public/assets'
# Horizontal centre of the subject in each landscape frame (share of the width), for the 9:16 crop.
MOBILE_CENTRE = {'grind': 0.65, 'bloom': 0.71, 'drip': 0.69}


def save(image, name, width):
    image = image.copy()
    image.thumbnail((width, width * 2), Image.Resampling.LANCZOS)
    dest = OUT / name
    image.save(dest, quality=80, method=6)
    print(dest.name, image.size, dest.stat().st_size)


for key in ['grind', 'bloom', 'drip']:
    image = Image.open(SRC / f'cup03-{key}.jpg').convert('RGB')
    assert image.size == (2752, 1536), 'Review crops if a source changes.'
    save(image, f'cup03-{key}-desktop.webp', 1600)
    w = round(image.height * 9 / 16)
    left = min(image.width - w, max(0, round(image.width * MOBILE_CENTRE[key] - w / 2)))
    save(image.crop((left, 0, left + w, image.height)), f'cup03-{key}-mobile.webp', 720)
save(Image.open(SRC / 'cup03-still-desktop.jpg').convert('RGB'), 'cup03-still-desktop.webp', 1600)
save(Image.open(SRC / 'cup03-still-mobile.jpg').convert('RGB'), 'cup03-still-mobile.webp', 720)
