"""Create self-contained review files. No hosting or external asset requests required."""
import base64,mimetypes,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'deliverables'
DEST.mkdir(exist_ok=True)
cache={}
def data_url(name):
 if name not in cache:
  p=ROOT/'public/assets'/name
  mime=mimetypes.guess_type(p)[0] or 'application/octet-stream'
  cache[name]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
 return cache[name]
html=(ROOT/'index.html').read_text()
css='\n'.join((ROOT/'src'/p).read_text() for p in ['common.css','peru.css','lata.css'])
css=re.sub(r'/assets/([^\'\"\)\s]+)',lambda m:data_url(m[1]),css)
html=re.sub(r'\s*<link rel="preload"[^>]*>', '',html)
html=re.sub(r'\s*<link rel="stylesheet"[^>]*>', '',html)
html=html.replace('</head>','<style>\n'+css+'\n</style>\n</head>')
js=(ROOT/'src/main.js').read_text()
html=re.sub(r'\s*<script type="module" src="/src/main.js"></script>','',html)
html=html.replace('</body>','<script>\n'+js+'\n</script>\n</body>')
html=re.sub(r'/assets/([^\'\"\s>]+)',lambda m:data_url(m[1]),html)
for key,name in [('a','A-peru-en-profundidad.html'),('b','B-fuera-de-la-lata.html')]:
 out=html.replace('data-direction="a"','data-direction="'+key+'"',1)
 if key=='b':
  out=out.replace('id="direction-a" aria-labelledby="title-a" data-expanded="false"','id="direction-a" aria-labelledby="title-a" data-expanded="false" hidden')
  out=out.replace('id="direction-b" aria-labelledby="title-b" data-expanded="false" hidden','id="direction-b" aria-labelledby="title-b" data-expanded="false"')
  out=out.replace('data-direction-link="a" aria-current="page"','data-direction-link="a"')
  out=out.replace('data-direction-link="b"','data-direction-link="b" aria-current="page"')
 (DEST/name).write_text(out)
 print(name,len(out.encode()),'bytes')
