# QA — auditoría y corrección de la home 01–05, 30 de septiembre de 2026

Autorización L24. Checkpoint previo `0b33580` (sin commit de este cambio). Condiciones: Windows, Node 22.23.1 aislado, Vite 7.1.3 (`vite build` + `vite preview`), Python 3.10, Playwright Chromium 148.0.7778.96, DPR 1. Contrato 1440 × 900 y 390 × 844, más exploratorios 390 × 664 (área visible real de un iPhone con barras), 768 × 1024 (tablet/iPad).

`verify.py` → `checks.json`: **39/39**.

- **Iconografía.** Ningún icono con tamaño cero en las secciones auditadas; se sustituyó `↗`/`⌄` por iconos SVG vía `mask` solo en la dirección A (home, hero A, 02, 03, 04, 05, pie). B y las PDP conservan sus glifos de texto originales, sin tocar.
- **Solape hero mobile.** La anotación de origen termina al menos 12 px por encima de «Alejar origen» en 390 × 844, 390 × 664 y tablet — antes, la medición mostraba 4 px de solape.
- **CTA visible.** «Comprar Amazonas» termina en y = 639 px a 390 × 664 (antes 691, fuera del área visible real reportada por el usuario).
- **Tipografía.** Ningún texto visible por debajo de 11 px en la dirección A, en ningún viewport comprobado. Por precisión del usuario, 11 px queda reservado a labels muy secundarios (kickers, créditos de procedencia); el texto informativo se elevó a 12–14 px y las citas de reseñas a 16 px (mobile) / 16 px (desktop, sin cambios).
- **Touch targets.** Sin objetivos por debajo de 44 px salvo dos excepciones aceptadas y documentadas abajo.
- **Overflow.** 0 px de desbordamiento horizontal en los cuatro viewports.
- **Dirección B.** 8/8 estados (desktop/mobile × motion/reduced × inicial/expandido) sin diferencia de píxeles frente a `qa/2026-09-29-ahorro/after/b-*`. No se tocó ningún archivo de B.
- **Barrido funcional.** Sin errores de página en consola; la nueva tarjeta «Café de origen» de 05 decodifica su imagen; el selector de 02 recorre los cinco orígenes; los enlaces de producto en las reseñas abren la PDP de Amazonas y la de El Ahorrador correctamente y el botón de volver funciona.

## Excepciones aceptadas en touch targets (no son defectos)

- **Enlaces dentro de una frase** («Consultar envíos», dentro del párrafo de la FAQ de envíos): WCAG 2.5.8 excluye explícitamente los enlaces en medio de una línea de texto corrido, cuyo alto lo determina la tipografía del párrafo, no el autor del control. 118×15 (desktop) / 109×14 (mobile).
- **Bolsas vecinas lejanas del carrusel de 02** (offset ±2, ej. «Ver café de Villa Rica»/«Ver café de Cusco» a 390 × 664): no tienen `pointer-events` habilitado hasta que el carrusel avanza (solo offset ±1 es interactivo); no son objetivos de toque reales en su posición actual. 42×99.

## Capturas

`after/{desktop,mobile,mobile664,tablet}-{initial,expanded}.png`: hero en ambos keyframes en los cuatro viewports. `after/{1440x900,390x844,390x664,768x1024}-full.png`/`-expanded-hero.png` (donde aplica): página completa y detalle del hero expandido, usadas para la revisión visual final. `after/b-*.png`: los 8 estados de regresión de B.

## No cubierto

Safari/iOS físico (el hallazgo original del emoji `↗` viene de una captura de iPhone real; Chromium no puede reproducir ese bug de renderizado, así que la corrección se verifica por ausencia de la fuente de texto, no visualmente en iOS). Android, lectores de pantalla, Core Web Vitals de campo o en GitHub Pages, conversión. PDPs no auditadas en este cambio (solo se tocaron dos enlaces de reseña que abren PDPs ya existentes, sin modificar su interior). El paisaje, la autoría de Tarata y la naturaleza generada de 03 siguen como gaps abiertos; solo cambió el texto del aviso (ver `docs/ASSET_AUDIT.md`).

Reproducir con el build y preview activos:

```powershell
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js build
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js preview --host 127.0.0.1 --port 4175
python qa/2026-09-30-home-audit/verify.py
```
