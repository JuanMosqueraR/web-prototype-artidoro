"""Prepare real 1 kg bag crops and the pack's 125 variant snapshot; no generation.
Reads the retained official sources. Writes three WebP files and one JSON table.
The official group photo has 454 g labels and is retained as unused discrepancy evidence.
"""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for origin in ['amazonas','cajamarca','puno']:
    image=Image.open(ROOT/f'audit/source/ahorrador-{origin}-1kg-original.jpg').convert('RGB')
    assert image.size==(1080,1080)
    image=image.crop((325,140,735,980))
    image.thumbnail((410,840),Image.Resampling.LANCZOS)
    out=ROOT/f'public/assets/ahorrador-{origin}-1kg.webp'
    image.save(out,quality=90,method=6)
    print(out.name,out.stat().st_size)
source=json.loads((ROOT/'audit/source/ahorrador-2026-09-28.json').read_text(encoding='utf-8'))
data={'checked':source['retrieved'],'source':source['source'],'options':source['product']['options'],'variants':[
    {k:v[k] for k in ['id','options','price','available']} for v in source['product']['variants']]}
(ROOT/'src/ahorrador-variants.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
