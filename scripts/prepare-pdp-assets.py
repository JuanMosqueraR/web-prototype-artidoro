"""Prepare the PDP assets of L31 from the retained originals in audit/source (no network, no generation).

- pdp-amazonas-map.webp: the official origin map with its light grey and mint palette moved to the demo palette
  (cream background, sage province, gold district and label). Shapes, text and the black badge are not redrawn or recoloured:
  dark pixels keep their original colour, only the background and the mint tones change.
- pdp-amazonas-lifestyle.webp: the official photo of the bag held in front of mountains, resized only.
- ahorrador-villa-rica-1kg.webp / ahorrador-cusco-1kg.webp: the same crop as scripts/prepare-ahorrador.py uses for the other 1 kg bags.
- pdp-beans.webp / pdp-grinds.webp: the two generated images (CONCEPTUAL_ASSET), resized and encoded.
"""
import colorsys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / 'audit/source', ROOT / 'public/assets'


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


INK, CREAM = hexrgb('#12120c'), hexrgb('#ece6d6')
# saturation of the original mint tones -> demo colour
STOPS = [(0.28, hexrgb('#c9d2bf')), (0.47, hexrgb('#d1af7e')), (0.75, hexrgb('#8f6a33'))]


def remap(rgb):
    r, g, b = (c / 255 for c in rgb)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    grey = lerp(INK, CREAM, min(1, max(0, (v - 0.07) / (0.96 - 0.07))))  # dark stays dark, light grey -> cream
    if s < 0.06 or not (0.38 < h < 0.52):
        return grey
    if s <= STOPS[0][0]:
        return lerp(grey, STOPS[0][1], s / STOPS[0][0])
    for (s0, c0), (s1, c1) in zip(STOPS, STOPS[1:]):
        if s <= s1:
            return lerp(c0, c1, (s - s0) / (s1 - s0))
    return STOPS[-1][1]


def save(image, name, size, quality=84):
    image = image.convert('RGB')
    image.thumbnail(size, Image.Resampling.LANCZOS)
    out = OUT / name
    image.save(out, quality=quality, method=6)
    print(out.name, image.size, out.stat().st_size)


# Map: palette swap through a lookup of the distinct colours (the map is flat artwork with anti-aliasing).
m = Image.open(SRC / 'pdp-amazonas-map-original.png').convert('RGB')
lut = {c: remap(c) for _, c in m.getcolors(1 << 24)}
m.putdata([lut[p] for p in m.getdata()])
save(m, 'pdp-amazonas-map.webp', (1200, 1200), 88)

save(Image.open(SRC / 'pdp-amazonas-lifestyle-original.png'), 'pdp-amazonas-lifestyle.webp', (1080, 1080), 82)

for origin in ['villa-rica', 'cusco']:
    image = Image.open(SRC / f'ahorrador-{origin}-1kg-original.jpg').convert('RGB')
    assert image.size == (1080, 1080)
    image = image.crop((325, 140, 735, 980))
    image.thumbnail((410, 840), Image.Resampling.LANCZOS)
    out = OUT / f'ahorrador-{origin}-1kg.webp'
    image.save(out, quality=90, method=6)
    print(out.name, image.size, out.stat().st_size)

save(Image.open(SRC / 'pdp-beans-original.jpg'), 'pdp-beans.webp', (1080, 1080), 80)
# Crop to the board (the generated frame also shows a stool under it).
save(Image.open(SRC / 'pdp-grinds-original.jpg').crop((150, 130, 2600, 1380)), 'pdp-grinds.webp', (1400, 720), 82)
