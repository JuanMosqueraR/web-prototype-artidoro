# QA — ahorro visible de El Ahorrador, 29 de septiembre de 2026

Cambio (L23): precio normal tachado S/ 330.00 y «Ahorras S/ 50» en la tarjeta del pack de 05 y en su PDP (junto al precio y en el total). Checkpoint previo `41d0cf1`. Referencia anterior: `../2026-09-28-ahorrador/`, que no se sobrescribe.

Condiciones: Windows, Node 22.23.1 aislado, Vite 7.1.3 (`vite build`), preview de producción en `http://127.0.0.1:4175`, Python 3.10, Playwright Chromium 148.0.7778.96, DPR 1. Contrato 1440 × 900 y 390 × 844, A y B, keyframes inicial/expandido, movimiento on/off.

- `verify.py` → `checks.json`: **211/211**. Copia del script del 28 de septiembre; solo cambian la fecha del informe y la referencia de píxeles del hero, que ahora es `../2026-09-28-ahorrador/after/`. Hero A y B: 0 píxeles distintos en los 16 estados. Altura de 05: 1998,30 px en 390 × 844 (antes 1993,70; +4,60 px); 1674,38 px en 1440 × 900.
- `pack-checks.py` → `pack-checks.json`: **316/316**. Copia sin cambios de lógica. La primera ejecución dio 315/316: a 390 × 700 el botón «Continuar con mi pack» terminaba en y = 704,28 px por la nueva línea de ahorro. Se compactó la línea en móvil (12 px) y el margen de la introducción; ahora termina en y = 697,48 px (antes del cambio, 676,69 px).
- `saving-checks.py` → `saving-checks.json`: **20/20**, nuevo. Texto, tachado y etiqueta para lectores de pantalla en 05 y PDP; ahorro en combinaciones repetidas y mixtas; se oculta con una combinación inexistente; sin errores JS. La primera ejecución falló en 4 comprobaciones por la expectativa: `innerText` incluye la etiqueta «Precio normal» oculta a la vista; se corrigió comparando el texto normalizado.

Capturas `after/`: mismas vistas que la entrega anterior (A/B, home, 05, PDP de Amazonas y del pack).

Reproducir desde la raíz, con el build y el preview activos:

```powershell
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js build
python qa/2026-09-29-ahorro/verify.py
python qa/2026-09-29-ahorro/pack-checks.py
python qa/2026-09-29-ahorro/saving-checks.py
```

No cubre: Safari/iOS físico para este cambio, Android, lectores de pantalla reales, GitHub Pages (no se republicó), checkout ni conversión. `verify-external.py` no se repitió: los destinos oficiales no cambian.
