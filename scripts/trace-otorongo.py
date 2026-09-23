"""Deterministic contour tracing of extracted packaging ink. No original artwork invented."""
from PIL import Image
from pathlib import Path
from collections import defaultdict
import numpy as np
root=Path(__file__).resolve().parents[1]
a=np.asarray(Image.open(root/'audit/source/otorongo-extract.webp').getchannel('A').resize((164,195),Image.Resampling.LANCZOS))>128
edges=defaultdict(list)
h,w=a.shape
for y,x in zip(*np.where(a)):
 if y==0 or not a[y-1,x]:edges[(x,y)].append((x+1,y))
 if x==w-1 or not a[y,x+1]:edges[(x+1,y)].append((x+1,y+1))
 if y==h-1 or not a[y+1,x]:edges[(x+1,y+1)].append((x,y+1))
 if x==0 or not a[y,x-1]:edges[(x,y+1)].append((x,y))
def simplify(p,t=.65):
 if len(p)<3:return p
 p0=np.array(p[0]); p1=np.array(p[-1]); v=p1-p0
 d=np.abs(np.cross(v,np.array(p)-p0))/max(np.linalg.norm(v),.001)
 i=int(np.argmax(d))
 return simplify(p[:i+1],t)[:-1]+simplify(p[i:],t) if d[i]>t else [p[0],p[-1]]
def fmt(p):return f'{float(p[0]):.2f},{float(p[1]):.2f}'
paths=[]
while edges:
 first=next(iter(edges));cur=first;p=[first]
 while cur in edges:
  nxt=edges[cur].pop()
  if not edges[cur]:del edges[cur]
  p.append(nxt);cur=nxt
  if cur==first:break
 if len(p)<6:continue
 area=abs(sum(p[i][0]*p[i+1][1]-p[i+1][0]*p[i][1] for i in range(len(p)-1))/2)
 if area<2.5:continue
 half=len(p)//2
 pts=simplify(p[:half+1])[:-1]+simplify(p[half:])[:-1]
 if len(pts)<3:continue
 mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 s='M'+fmt(mid(pts[-1],pts[0]))
 for i,pt in enumerate(pts):s+='Q'+fmt(pt)+' '+fmt(mid(pt,pts[(i+1)%len(pts)]))
 paths.append(s+'Z')
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 164 195"><title>Otorongo de Artidoro, extracción provisional de packaging</title><path fill="#0f1d12" fill-rule="evenodd" d="'+''.join(paths)+'"/></svg>'
(root/'public/assets/otorongo-traced.svg').write_text(svg)
print(len(paths),'contours,',len(svg),'bytes')
