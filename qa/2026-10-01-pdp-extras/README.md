# QA — medios de pago, video en la galería y atajo del pack (L31), 1 de octubre de 2026

**Resultado: 25/25** (`checks.json`). Script: `verify.py`. Capturas: `after/`.

**Condiciones.** Chromium 148 (Python Playwright), DPR 1, build de producción servido por HTTP. Recorrido en 1440 × 900 y 390 × 844 (táctil), en las dos PDP. Un caso con `prefers-reduced-motion`.

**Qué cubre.**
- **Medios de pago:** los iconos bajo el botón son exactamente la lista oficial (`audit/source/payment-methods-2026-10-01.html`) y cargan.
- **Galería:**
  - 7 fotos en Amazonas y 5 en el pack, con sus miniaturas;
  - botón de zoom en todas menos el video;
  - 4 y 3 avisos de imagen conceptual, respectivamente.
- **Video:**
  - el clip no se pide hasta llegar a su foto;
  - allí se reproduce en bucle sin sonido y se pausa al salir;
  - la vista ampliada (zoom) se lo salta;
  - con movimiento reducido queda en pausa con controles.
- **Atajo del pack:** «Las tres bolsas de Cusco» llena las tres bolsas, actualiza la variante y la imagen, y se oculta.
- **Resto:**
  - en desktop las miniaturas no se cortan (pasan a dos filas cuando no caben);
  - sin desbordamiento ni errores.
- **Regresión fuera del repo:**
  - home: 154/154;
  - precios: 15/15;
  - pack en la decisión: 20/20;
  - ajustes: 4/4.
- **QA anterior de las PDP:** `qa/2026-10-01-pdp/verify.py` da 46/50. Las cuatro diferencias son los recuentos que este cambio modifica (fotos, avisos, zoom); esta carpeta los sustituye.

**No cubre.**
- Safari/iOS instrumental. El usuario lo probó en su iPhone: «probé en iPhone, todo ok» (user-reported). No se registró si el teléfono estaba en modo de bajo consumo, donde el código muestra los controles nativos.
- Peso del clip en datos móviles. Son 3,3 MB y se piden solo al llegar a esa foto. Si se entra directo a una PDP, el hero de la home también pide su video; es un comportamiento anterior, no corregido.
