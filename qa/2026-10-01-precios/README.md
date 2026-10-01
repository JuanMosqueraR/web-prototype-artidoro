# QA — precios al día (L31), 1 de octubre de 2026

**Resultado: 15/15** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, build de producción servido por HTTP, 1440 × 900 y 390 × 844, `?motion=off` en la home.

**Qué cubre.** Cada precio que muestran la home y las PDP frente a `audit/source/prices-2026-10-01.json`:
- **Hero:** Amazonas 250 g y el pack con precio normal tachado.
- **02:** los cinco orígenes y el enlace del pack.
- **05:** pack con su ahorro, Travel Line, café de origen, El Explorador y miel de 300 g.
- **PDP de Amazonas:** los tres tamaños.
- **PDP del pack:** precio, total y ahorro.
- **Sin precios anteriores:** ni «S/ 280», ni «Ahorras S/ 50», ni «S/ 180.00», ni «S/ 99.00» en ninguna parte del documento, incluidas las PDP ocultas.
- **Imagen para compartir:** existe; el precio nuevo se revisó a ojo en la imagen.
- **Regresión:** la verificación completa de `qa/2026-10-01-orden/` se ejecutó en una copia fuera del repo con 154/154; sus resultados no se guardan aquí.

**No cubre.**
- Safari/iOS.
- La vigencia de los precios después del 1 de octubre.
