# QA — PDP renovadas (L31), 1 de octubre de 2026

**Resultado: 50/50** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, build de producción servido por HTTP. Recorrido completo en 1440 × 900 y 390 × 844. Desbordamiento también en 320 × 640, 768 × 1024, 1024 × 768 y 1920 × 1080 (exploratorio).

**Qué cubre (desktop y mobile).**

- **Home:** al cargar no se pide ninguna imagen propia de las PDP.
- **Entrada a Amazonas:**
  - el botón del hero abre la PDP con foco en el título;
  - el header oculta «Comprar café».
- **Contenido de Amazonas:**
  - todas las imágenes cargan al abrir la PDP;
  - el rating «5,0 · 3 reseñas» enlaza al bloque de reseñas;
  - cada tamaño muestra su precio oficial;
  - con 1 kg y molienda media coinciden precio, «unas 65 tazas», variante del botón y botón fijo;
  - tres fotos con aviso de imagen conceptual más el crédito de la banda.
- **Galería:**
  - mobile: el swipe (scroll horizontal) mueve el contador;
  - desktop: flecha y miniatura cambian la foto y marcan la miniatura.
- **Zoom:** hay un botón en cada una de las 6 fotos; abre la foto a pantalla completa, un toque o clic acerca en ese punto (la foto queda desplazable), las flechas pasan de foto, Escape cierra y la galería queda en la última foto vista. En el pack, la foto ampliada muestra la combinación elegida.
- **Botón fijo:** se oculta con el botón principal en pantalla y aparece después.
- **Legibilidad:** sin texto por debajo de 11 px ni desbordamiento horizontal.
- **Retorno:** «Volver» lleva a la home y el header recupera «Comprar café».
- **Pack, abierto desde 05:**
  - 3 × 5 selectores en el orden oficial, con Amazonas, Cajamarca y Puno por defecto;
  - al elegir Villa Rica · Cusco · Cusco cambian imagen, texto de la foto, precio, ahorro, variante del botón y botón fijo;
  - todas las imágenes cargan;
  - sin texto por debajo de 11 px ni desbordamiento;
  - sin errores de página.
- **Regresión** (repetida tras tocar `src/inertia.js`): se ejecutaron fuera del repo `qa/2026-10-01-orden/verify.py` (154/154, incluye que B no cambia) y `qa/2026-10-01-precios/verify.py` (15/15).

**No cubre.**

- Safari/iOS instrumental, Firefox, Android.
- iPhone físico de esta ronda.
- Lectores de pantalla más allá de la estructura.
- No se siguieron los enlaces externos (tienda, políticas).
- No se verifica la vigencia de precios, rating y políticas después del 1 de octubre.
