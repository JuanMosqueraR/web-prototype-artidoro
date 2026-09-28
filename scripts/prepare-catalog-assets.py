"""Prepare only the three approved catalog photos and the static Amazonas variants.

Python + Pillow; original pixels, rectangular whitespace crops, no artwork edits.
Reads audit/source; writes the named WebP files and src/amazonas-variants.json.
Sources and crop coordinates are recorded in audit/assets.json.
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RECIPES = {
    'travel': ('.png', (90, 385, 980, 825), 1100),
    'explorador': ('.jpg', (90, 330, 960, 870), 700),
    'miel': ('.jpg', (335, 385, 750, 910), 460),
}

def main():
    for name, (ext, crop, maximum) in RECIPES.items():
        image = Image.open(ROOT / f'audit/source/catalog-{name}-original{ext}').convert('RGB')
        assert image.size == (1080, 1080), 'Review crop if source changes.'
        image = image.crop(crop)
        image.thumbnail((maximum, maximum), Image.Resampling.LANCZOS)
        dest = ROOT / f'public/assets/catalog-{name}.webp'
        image.save(dest, quality=90, method=6)
        print(dest.name, image.size, dest.stat().st_size)
    snapshot = json.loads((ROOT / 'audit/source/catalog-pdp-2026-09-28.json').read_text(encoding='utf-8'))
    item = snapshot['products']['amazonas']
    data = {'checked': snapshot['retrieved'], 'source': item['source'], 'variants': [
        {key: v[key] for key in ['id', 'option1', 'option2', 'price', 'available']}
        for v in item['product']['variants']
    ]}
    (ROOT / 'src/amazonas-variants.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
