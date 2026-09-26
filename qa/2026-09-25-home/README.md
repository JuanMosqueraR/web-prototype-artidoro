# Revisión de la home — 25 de septiembre de 2026

Evidencia de la fase autorizada desde el checkpoint `0a1da04`. Los originales del Hero Lab y los checkpoints del 24 de septiembre se conservan; no representan esta nueva home.

## Condiciones

Chromium 148.0.7778.96, Python Playwright, DPR 1. Desktop 1440 × 900 y mobile 390 × 844. Servidor de producción Vite en `http://127.0.0.1:4174/`. Las capturas mobile son emulación de viewport, no un dispositivo físico.

- `captures/desktop-home-complete.png` y `mobile-home-complete.png`: home completa, preferencia del sistema de movimiento reducido e imágenes decodificadas. Muestran el poster de 03, sin el espacio extra de scroll del video.
- `captures/{desktop,mobile}-03-{start,middle,end,reverse}.png`: escena 03 con movimiento activo; posiciones de scroll 0, 0.5, 1 y regreso a 0.25.
- `frames/`: inicio, mitad y final extraídos de los MP4 preparados mediante `scripts/prepare-scene03-video.py`. Son frames del video, sin UI.
- `captures/a-*` y `b-*`: ambos heroes, ambos keyframes, motion activado/desactivado y ambos tamaños. La home se desarrolla solo en A; no son una nueva comparación de méritos creativos entre A y B.
- `checks.json`: 117 comprobaciones funcionales y de geometría; 117 pasan. Incluye las cinco selecciones, independencia de 05, avance y retroceso del video, composición responsive, error de media, reduced motion, contenido sin JS y ausencia de errores JS.
- `baseline-deltas.json`: comparación de CTA con `qa/measurements.json`; B sin delta, A con nueva posición vertical (−3.125 px desktop, +8 px mobile), mismos tamaños y acceso dentro del viewport.
- `regression-b.json`: B inicial con movimiento reducido idéntico píxel a píxel al estado previo de esta fase en ambos tamaños; métricas, Unicode y glifos de la conversión WOFF2 iguales al TTF.
- `performance.json`: una observación por viewport con caché desactivada, latencia 150 ms, descarga 1.6 Mbps, subida 750 Kbps y CPU ralentizada 4× mediante CDP. Corrida separada del QA funcional. Son observaciones locales, no datos de campo ni puntuación Lighthouse. `observed_blocking_ms` suma el exceso sobre 50 ms de las tareas observadas; no equivale al TBT oficial de Lighthouse.

No se ejecutó una compra, no se probó checkout, ni Safari/iOS, dispositivos físicos, lector de pantalla o tráfico real. Los enlaces comerciales llevan a la tienda oficial. No se afirma una mejora medida de conversión ni una comparación de rendimiento equivalente con el PDF CRO.

## Repetir

Con el build actual servido en 4174 y Python con Playwright/Chromium instalado:

```powershell
python qa/2026-09-25-home/verify-home.py
python qa/2026-09-25-home/measure-performance.py
```

Ejecutarlos secuencialmente. Escriben solo la evidencia de esta carpeta fechada; no modifican los baselines anteriores. La preparación de frames usa FFmpeg a través de `imageio_ffmpeg` y escribe en `frames/`.
