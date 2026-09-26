"""Prepare the authorized home assets; preserve source artwork, resize/compress only.

Run with Python + Pillow. Sources remain in audit/source (and existing CP04 JPEG).
No source, previous prepared bag, or baseline capture is overwritten.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'audit/source'
ASSETS = ROOT / 'public/assets'
POLYGON = [(363,188),(653,186),(653,214),(656,219),(655,241),(660,283),
           (668,469),(668,725),(665,851),(666,917),(663,930),(370,931),
           (360,926),(361,886),(360,815),(361,580),(360,326),(365,246),
           (359,239),(358,220),(363,216)]

for origin in ['villa-rica', 'cusco', 'puno']:
    image = Image.open(SOURCE / f'{origin}-original.jpg').convert('RGBA')
    assert image.size == (1080, 1080), 'Check the silhouette against new source dimensions.'
    mask = Image.new('L', (4320,4320), 0)
    ImageDraw.Draw(mask).polygon([(x*4,y*4) for x,y in POLYGON], fill=255)
    image.putalpha(mask.resize(image.size, Image.Resampling.LANCZOS))
    image.crop((352,179,678,940)).save(ASSETS / f'{origin}-250g.webp', quality=92, method=6)

for device, width in [('desktop',1600),('mobile',900)]:
    for frame in ['start','end']:
        path = SOURCE / f'scene03-{device}-{frame}.jpg'
        if path.exists():
            image = Image.open(path).convert('RGB')
            image.thumbnail((width, 1600), Image.Resampling.LANCZOS)
            image.save(ASSETS / f'scene03-{device}-{frame}.webp', quality=84, method=6)

image = Image.open(ASSETS / 'cp04-mesa.jpg').convert('RGB')
image.thumbnail((1000,1340), Image.Resampling.LANCZOS)
image.save(ASSETS / 'tarata-mesa-home.webp', quality=80, method=6)

# Same source and geography uncertainty; responsive delivery, no new landscape.
for device, width in [('desktop',1280),('mobile',768)]:
    image = Image.open(SOURCE / 'artidoro-landscape-still.jpg').convert('RGB')
    image.thumbnail((width,720), Image.Resampling.LANCZOS)
    image.save(ASSETS / f'cafetal-home-{device}.webp', quality=75, method=6)

# Lossless font container conversion, all glyphs retained, no font redesign.
font_source = SOURCE / 'barlow-condensed-800-original.ttf'
if not font_source.exists():
    shutil.copyfile(ASSETS / 'barlow-condensed-800.ttf', font_source)
font = TTFont(font_source, recalcTimestamp=False)
font.flavor = 'woff2'
font.save(ASSETS / 'barlow-condensed-800.woff2')
print('Prepared bags, posters, Tarata, responsive landscape and WOFF2 font.')
