# QA — video del hero al entrar directo a una PDP, 1 de octubre de 2026

**Resultado: 8/8** (`checks.json`). Script: `verify.py`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, 1440 × 900 y 390 × 844 (táctil), build de producción servido por HTTP, entrando directamente a `#producto-amazonas` y `#producto-ahorrador`.

**Qué cubre.**
- **En la PDP:** no se pide el video del hero ni su secuencia de imágenes, tampoco al hacer scroll. Antes se descargaba (unos 3,3 MB) aunque la home estuviera oculta.
- **Al volver a la home:** el hero pide su propio video (`hero-desktop.mp4` o `hero-mobile.mp4`) y lo usa, sin errores.
- **Regresión fuera del repo:**
  - home: 154/154;
  - precios: 15/15;
  - pack en la ficha: 20/20;
  - ajustes: 4/4;
  - medios de pago, video y atajo: 25/25.

**No cubre.**
- Safari/iOS.
- El póster del hero, que va en el HTML con prioridad alta, sigue cargándose en una visita directa a una PDP (es una imagen pequeña).
