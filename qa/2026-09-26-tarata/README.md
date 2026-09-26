# QA de Tarata — 26 de septiembre de 2026

Build local de producción en http://127.0.0.1:4174/. Python 3.10/Playwright, Chromium 148.0.7778.96, DPR 1. Desktop 1440×900 y mobile 390×844 emulados; viewport comprobado. No prueba de dispositivo físico ni Safari/iOS.

- `verify-tarata.py` → `tarata-checks.json`: **30/30**. Motion de entrada y reposo, no repetición, cambio de preferencia, sistema reduced motion, fotos responsive, carga diferida, sin JS, mapa conservado y scroll libre.
- `verify-journey.py` → `checks.json`: **117/117**, repetición de la cobertura del 25 con nuevas capturas. Ambos heroes, ambos keyframes, motion on/off, cinco orígenes, compra y video03 con avance/retroceso/fallback. Incluye viewport exploratorio adicional y ausencia de overflow.
- `regression.json`: comparación de las 16 capturas de hero con septiembre 25 y delta cero en los 16 bounding boxes de CTA. Quince capturas idénticas; B desktop expandida/reduced difiere 409 píxeles del titular, máximo 14/255, con geometría idéntica. Observación fuera de la modificación de 04; no se cambió B.
- `captures/*-04-motion-rest.png`: viewport completo con entrada terminada después de 1.35 s; todas las fotos decodificadas.
- `captures/*-04-section.png`: captura de elemento completo; viewport de origen es el declarado, alto del archivo depende de la sección.
- `captures/*-04-reduced.png`: movimiento reducido del sistema.
- `captures/*-03-to-04.png`, `*-04-to-05.png`: límites de sección con preferencia reduced motion; 03 muestra poster.
- `captures/*-home-complete.png`: home completa con reduced motion; recorrido previo a 04 para solicitar y decodificar sus fotos, regreso al principio, captura completa. Los archivos viejos no se sobrescriben.

Repetir, con el build servido y Playwright/Chromium instalado:

```powershell
python qa/2026-09-26-tarata/verify-tarata.py
python qa/2026-09-26-tarata/verify-journey.py
```

No se ejecutó compra ni navegación al mapa, ni una auditoría Lighthouse, medición de conversión, lector de pantalla o prueba en dispositivos físicos. La medición de rendimiento del 25 pertenece a aquel snapshot; para esta revisión se comprobó ausencia de descarga inicial de las fotos de 04.
