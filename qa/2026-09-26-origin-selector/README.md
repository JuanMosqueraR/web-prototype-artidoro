# QA del selector horizontal — 26 de septiembre de 2026

Rama `feat/origin-selector`, checkpoint anterior `7b122b9`. Python 3.10, Playwright, Chromium 148.0.7778.96, DPR 1, Windows. Preview de producción en `http://127.0.0.1:4175/`; no es Pages ni un iPhone físico. No se ejecutó ninguna compra.

- `before/`: capturas inmutables del checkpoint anterior, Vite dev :4173, antes de editar. Baseline A/B × dos keyframes × motion on/off × desktop 1440×900 y mobile 390×844; capturas de 02 con Amazonas y motion on.
- `after/`: las mismas condiciones sobre el build nuevo; estados de 02 y secuencia Amazonas→Cajamarca. La secuencia usa esperas nominales de 110/110/220 ms más la duración de cada captura, no un muestreo de video de frecuencia fija.
- `checks.json`: **312/312**, geometría, datos comerciales, carga, fallos, gestos, texto, teclado, modos de movimiento y comparación de los heroes. Para aislar el hero, el comparador recorta la parte inferior si el viewport deja ver el comienzo de 02.
- `journey/`: **117/117** de la suite existente, con salida redirigida a este nuevo directorio. Incluye 03, 04, 05, sin JS, motion reducido y fallo del MP4.

Variación de raster observado en B desktop, keyframe expandido, motion off: tres recapturas del mismo código dieron 0, 320 y 189 píxeles distintos respecto a la referencia, delta máximo de canal 14/255. El resultado final registró 89 píxeles, máximo 7/255. Umbral de regresión: ≤0.05 % de píxeles y delta máximo ≤16; todas las otras capturas finales fueron idénticas. No se cambió el baseline para acomodar esa variación.

Pruebas exploratorias adicionales: 390×700, 360×740, 768×1024, 1023×900, 1024×768, 320×740, CDP touch (swipe y scroll vertical) y texto duplicado mediante CSS. Capturas exploratorias fuera del repo, en `C:/tmp/origin-selector/`. No definen nuevos viewports contractuales.

Para reproducir, con el build actual servido:

```powershell
python qa/2026-09-26-origin-selector/verify-selector.py
python qa/2026-09-26-origin-selector/run-home-regression.py
```

Ambos scripts aceptan `ARTIDORO_REVIEW_URL`. Escriben en este directorio, sin sobrescribir los QA históricos. `verify-selector.py` compara contra `before/` y consulta `qa/measurements.json`; no regenera esas referencias. El wrapper de home reutiliza las aserciones de `qa/2026-09-25-home/verify-home.py` con otra ruta de salida.

No cubierto: Safari/WebKit, dispositivo físico, preferencias de texto de iOS, condiciones reales de red móvil y publicación de esta rama. [Entrega](../../docs/ORIGIN_SELECTOR_REVIEW.md).
