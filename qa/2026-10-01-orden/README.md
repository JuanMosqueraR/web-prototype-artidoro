# QA — nuevo orden de secciones (L29, P4), 1 de octubre de 2026

**Resultado: 154/154** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Las mismas que [qa/2026-10-01-revision](../2026-10-01-revision/README.md):
- Chromium 148.0.7778.96 (Python Playwright), DPR 1.
- Build de producción servido por HTTP con Range.
- Viewports de baseline 1440 × 900 y 390 × 844, más los anchos exploratorios de esa carpeta.

**Qué cubre.**

- **Toda la verificación de `qa/2026-10-01-revision/`:** regresión de L28, controles de P1–P3 y B sin cambios.
- **Controles de P4, en desktop y mobile:**
  - orden real en pantalla: hero, 02, 03, moliendas, tienda, confianza, reseñas, cafeterías, FAQ, explorar;
  - fotos de los mosaicos pedidas al saltar directamente a 04;
  - fotos de Tarata decodificadas en su nueva posición;
  - «Cafeterías» del header (solo desktop; en mobile ese enlace no se muestra) y «Llévalo a tu taza» llegan a su sección, justo bajo el header;
  - sin errores de página.
- **Bug corregido.** El control de los mosaicos fallaba antes de la corrección de `src/catalog.js`.

**No cubre.**
- Safari/iOS instrumental, Firefox, Android.
- iPhone físico solo según el usuario («ya probe, todo ok»), sin registro instrumental.
- Lectores de pantalla más allá de la estructura de títulos.
