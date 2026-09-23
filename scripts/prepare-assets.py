"""Deterministic preparation of real public Artidoro assets; no generated imagery."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'audit/source'
OUT=ROOT/'public/assets'
# Source pixels are preserved. A hand-fitted silhouette removes the white studio background.
im=Image.open(RAW/'amazonas-original.jpg').convert('RGBA')
pts=[(363,188),(653,186),(653,214),(656,219),(655,241),(660,283),(668,469),(668,725),(665,851),(666,917),(663,930),(370,931),(360,926),(361,886),(360,815),(361,580),(360,326),(365,246),(359,239),(358,220),(363,216)]
mask=Image.new('L',(im.width*4,im.height*4),0)
ImageDraw.Draw(mask).polygon([(x*4,y*4) for x,y in pts],fill=255)
mask=mask.resize(im.size,Image.Resampling.LANCZOS)
im.putalpha(mask)
im.crop((352,179,678,940)).save(OUT/'amazonas-250g.webp',quality=92,method=6)
# Real ink from the curved Travel Line tin; no missing anatomy is reconstructed.
src=Image.open(RAW/'otorongo-curved-tin-detail.png').convert('RGB')
p=np.asarray(src,dtype=float)
g=p[:,:,1]
bg=np.percentile(g,92,axis=0)[None,:]
alpha=np.clip((bg*.69-g)/(bg*.28),0,1)
alpha[:,156:]=0
alpha[85:,147:]=0
alpha[-3:,:]=0
ink=np.zeros((p.shape[0],p.shape[1],4),dtype=np.uint8)
ink[:,:,:3]=[15,29,18]
ink[:,:,3]=(alpha*255).astype(np.uint8)
Image.fromarray(ink).resize((656,780),Image.Resampling.LANCZOS).save(RAW/'otorongo-extract.webp',lossless=True,method=6)
# One still from the brand's own video. Its precise geographic location is unverified.
land=Image.open(RAW/'artidoro-landscape-still.jpg').convert('RGB')
land.save(OUT/'cafetal-provisional.webp',quality=85,method=6)
# A small real foliage crop serves as a near plane, feathered rather than invented.
leaf=land.crop((0,280,470,720)).convert('RGBA')
w,h=leaf.size
y,x=np.mgrid[0:h,0:w]
a=(np.clip((y/h-.12)/.62,0,1)*np.clip((1-x/w)/.48,0,1)*220).astype('uint8')
leaf.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(9)))
leaf.save(OUT/'cafetal-foreground.webp',quality=80,method=6)
# Display font retained as a small local TTF; no runtime font service.
for f in sorted(OUT.iterdir()): print(f.name, f.stat().st_size)
