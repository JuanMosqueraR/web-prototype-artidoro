"""Deterministic preparation of the official Cajamarca 250 g bag photo; no generated imagery.

Reads audit/source/cajamarca-original.jpg and writes only public/assets/cajamarca-250g.webp.
Same silhouette polygon and crop box as the Amazonas bag in prepare-assets.py: both official
photos share one bag template, and the polygon was validated against the Cajamarca photo
(see audit/assets.json, id cajamarca-bag). Source pixels are preserved; nothing is retouched.
"""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
im=Image.open(ROOT/'audit/source/cajamarca-original.jpg').convert('RGBA')
pts=[(363,188),(653,186),(653,214),(656,219),(655,241),(660,283),(668,469),(668,725),(665,851),(666,917),(663,930),(370,931),(360,926),(361,886),(360,815),(361,580),(360,326),(365,246),(359,239),(358,220),(363,216)]
mask=Image.new('L',(im.width*4,im.height*4),0)
ImageDraw.Draw(mask).polygon([(x*4,y*4) for x,y in pts],fill=255)
mask=mask.resize(im.size,Image.Resampling.LANCZOS)
im.putalpha(mask)
out=ROOT/'public/assets/cajamarca-250g.webp'
im.crop((352,179,678,940)).save(out,quality=92,method=6)
print(out.name,out.stat().st_size)
