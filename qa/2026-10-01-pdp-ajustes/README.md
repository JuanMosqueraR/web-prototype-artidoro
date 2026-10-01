# QA — ajustes de las PDP tras la prueba en iPhone (L31), 1 de octubre de 2026

**Resultado: 4/4** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, 390 × 844 táctil, build de producción servido por HTTP.

**Qué cubre.**
- **Título de la PDP.** Al abrir la ficha recibe el foco, para que el lector de pantalla anuncie el cambio, pero sin recuadro. El recuadro azul que se veía en Chrome iOS era ese indicador de foco, no texto seleccionado. El siguiente control conserva su indicador de foco con teclado.
- **Carrusel mobile «Del cafetal a tu taza» (Amazonas y pack).** La primera tarjeta empieza en el margen de 22 px y el ajuste magnético alinea las tarjetas en ese margen (`scroll-padding-inline`); antes quedaban pegadas al borde.
- **Regresión.** Fuera del repo se ejecutaron `qa/2026-10-01-pdp/verify.py` (50/50) y `qa/2026-10-01-orden/verify.py` (154/154).

**No cubre.** Safari/iOS instrumental. El usuario lo probó en iOS: «Probé en iOS y está ok» (user-reported).
