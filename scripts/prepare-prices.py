"""Rebuild the two variant snapshots the PDPs read from the dated official price snapshot (L31).

Reads audit/source/prices-2026-10-01.json (official /products/<handle>.js, fetched 2026-10-01).
Writes src/amazonas-variants.json and src/ahorrador-variants.json in the format catalog.js expects. No network access.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'audit/source/prices-2026-10-01.json'
snap = json.loads(SOURCE.read_text(encoding='utf-8'))
day = snap['retrieved'][:10]
products = snap['products']

amazonas = products['cafe-amazonas']
data = {'checked': day, 'source': 'https://www.artidororodriguez.com/products/cafe-amazonas.js', 'variants': [
    {'id': v['id'], 'option1': v['options'][0], 'option2': v['options'][1], 'price': v['price'], 'available': v['available']}
    for v in amazonas['variants']]}
(ROOT / 'src/amazonas-variants.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

pack = products['pack-3kg-origenes-1']
data = {'checked': day, 'source': 'https://www.artidororodriguez.com/products/pack-3kg-origenes-1.js', 'options': pack['options'], 'variants': [
    {'id': v['id'], 'options': v['options'], 'price': v['price'], 'available': v['available']} for v in pack['variants']]}
(ROOT / 'src/ahorrador-variants.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('amazonas', sorted({v['price'] for v in amazonas['variants']}), '| pack', sorted({v['price'] for v in pack['variants']}),
      'compare_at', sorted({v['compare_at_price'] for v in pack['variants']}))
