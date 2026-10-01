# QA — El Ahorrador en la decisión de Amazonas (L31), 1 de octubre de 2026

**Resultado: 20/20** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, 1440 × 900 y 390 × 844 (táctil), build de producción servido por HTTP, con la PDP abierta desde el botón del hero.

**Qué cubre (desktop y mobile).**
- **Opción del pack en «Tamaño»:** precio, precio normal tachado, precio por kilo y «El kilo más barato», calculados de `src/ahorrador-variants.json` y `src/amazonas-variants.json`.
- **Línea de 1 kg:** aparece solo con 1 kg y muestra el ahorro oficial.
- **Al elegir el pack:**
  - cambian precio y tazas;
  - se oculta la molienda y aparece su nota;
  - el botón pasa a «Armar mi pack» con ruta interna e icono de flecha;
  - cambian la barra fija y el texto bajo el botón.
- **Sin problemas de lectura:** ningún texto por debajo de 11 px ni desbordamiento con el pack elegido.
- **Navegación al pack:**
  - «Armar mi pack» abre la PDP del pack con Amazonas en la bolsa 1, aunque antes hubiera otra;
  - «Volver» regresa a Amazonas con el pack aún elegido.
- **Al volver a 250 g:** el botón vuelve a ser externo, con la variante oficial; reaparece la molienda y se restaura la barra.
- **Sección inferior:** solo descubrimiento (sin tarjeta del pack, con El Explorador y los cuatro orígenes).
- **Sin errores de página.**
- **Regresión fuera del repo:**
  - `qa/2026-10-01-pdp/verify.py`: 50/50;
  - `qa/2026-10-01-orden/verify.py`: 154/154;
  - `qa/2026-10-01-precios/verify.py`: 15/15;
  - `qa/2026-10-01-pdp-ajustes/verify.py`: 4/4.

**No cubre.**
- Safari/iOS instrumental.
- iPhone físico solo según el usuario («Probé en iOS y está ok»), sin registro instrumental.
