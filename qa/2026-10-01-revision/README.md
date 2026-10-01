# QA — revisión de la home, 1 de octubre de 2026 (L29)

**Resultado: 143/143** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148.0.7778.96 (Python Playwright), DPR 1, build de producción servido por HTTP con soporte de Range (Vite y Node aislados, fuera del repo), Windows 10. Viewports de baseline 1440 × 900 y 390 × 844, más 390 × 664 y 768 × 1024; anchos exploratorios 320, 360, 900, 1024, 1051, 1280 y 1920 solo para la geometría de 04 y el desbordamiento.

**Qué cubre.**

- **Regresión de L28.** Es el script de `qa/2026-09-30-l28/` con un cambio: el hero ya no tiene texto en el paso 3, así que el control comprueba que termina en el paso 3 con la bolsa colocada y ningún texto de paso visible. Incluye:
  - video y secuencias de respaldo;
  - ritmo de 03;
  - movimiento desactivado y `prefers-reduced-motion`;
  - inercia de la rueda y barras del navegador móvil;
  - swipe de 02;
  - etiquetas para compartir;
  - PDP desde el hero;
  - B sin cambios frente a `qa/2026-09-29-ahorro/after/`.
- **Esta ronda (desktop y mobile, con `?motion=off`):**
  - ningún texto visible por debajo de 11 px en header, secciones y pie;
  - iconos ↗ del pie dentro de su enlace y en la misma línea;
  - sin numeración de secciones (el contador «01 / 05» del carrusel no cuenta);
  - «justo antes de enviarlo» una sola vez, sin «Para tus días», y «¿Qué molienda elijo?» presente;
  - reseñas, FAQ y explorar como `h2`;
  - el enlace de reseñas apunta a la ficha oficial de Amazonas;
  - 04 con Tarata y La Mar, con dirección, horarios y enlace de mapa idénticos a `audit/source/locales-2026-10-01.txt`;
  - subtítulo «Nos vemos en Miraflores»;
  - icono del CTA de 02: flecha interna para Amazonas e icono externo para Cajamarca;
  - sin errores de página.
- **Geometría de 04 (por encima de 760 px):**
  - ninguna foto tapa la última línea del titular;
  - la fachada termina antes de las fichas de las cafeterías;
  - sin desbordamiento horizontal en ningún ancho probado.

**No cubre.**

- Safari/iOS instrumental, Firefox, Android.
- iPhone físico solo según el usuario («ya probe en iphone, todo ok»), sin registro instrumental.
- Lectores de pantalla más allá de la estructura de títulos.
- No se siguieron los enlaces de mapa ni el de reseñas.
- No se comprobó que los horarios sigan vigentes después del 1 de octubre.
