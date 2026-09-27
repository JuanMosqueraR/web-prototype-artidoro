# Selector de orígenes — revisión del 26 de septiembre de 2026

Implementación del plan aprobado «02 — Selector horizontal de orígenes» en `feat/origin-selector`, desde el checkpoint `7b122b9`. Versionado en esa rama por petición del usuario, sin merge a `master`. La publicación en Pages la hace el usuario con `scripts/build-pages.py`; este informe no registra si ya ocurrió (hasta entonces Pages conserva la versión anterior).

**Demo local:** http://127.0.0.1:4175/#origin-scene · **Galería antes/después:** http://127.0.0.1:4173/deliverables/origin-selector-review.html (servidor Vite dev). [Archivo de la galería](../deliverables/origin-selector-review.html).

## Resultado

Cinco nombres siempre disponibles, bolsa central completa y vecinos al 72 % de escala. Carrusel circular mediante nombres, flechas, toque en vecinos, swipe, arrastre y teclado. Mobile prioriza una vista conjunta del producto y la compra; desde 1024 px, carrusel/ficha en proporción 60/40. Encabezado compacto, packaging, notas, gramaje, precios y enlaces oficiales conservados.

| Viewport CSS | Altura de 02 | Borde inferior del CTA en pantalla |
|---|---:|---:|
| 390 × 844 | 734.9 px | 706.9 px |
| 390 × 700 | 654.9 px | 626.9 px |
| 360 × 740 | 682.1 px | 654.1 px |
| 1440 × 900 | 781 px | 687.9 px |

Mediciones con 02 alineada bajo navegación de 64 px mobile / 72 px desktop, fuentes cargadas y tamaño de texto normal. Antes, a 390 × 844, 02 medía 953.8 px y el CTA empezaba en y=848.8 px. Ahora se ve completo junto al producto. En pantallas estrechas o con texto ampliado, la sección puede crecer sin scroll vertical interno. Desde 600 a 1023 px se mantiene una composición vertical más amplia.

## Motion, carga y accesibilidad

- Tras preparar y decodificar el café solicitado, bolsa, ficha, CTA y selección se actualizan conjuntamente. Las bolsas se desplazan y cambian de escala durante 320 ms; el texto hace un fundido de salida de 70 ms y entrada de 100 ms. Precio y CTA conservan su posición.
- Solo se cargan las bolsas vecinas al aproximarse a 200 px de 02 y después de cada selección. No hay imágenes generadas, nuevos derivados ni dependencias; se reutilizan las cinco bolsas existentes. Media generada/coste: ninguno.
- La última solicitud prevalece. Fallo o timeout de 4 s conserva el estado anterior y permite reintentar seleccionando el nombre. El retraso de una respuesta antigua no cambia la selección vigente.
- Swipe horizontal cambia un origen por gesto; movimiento vertical conserva el scroll normal. Se corrigió la transferencia de captura implícita de Pointer Events observada en la emulación táctil de Chromium.
- Flechas izquierda/derecha, Home/End, foco visible y anuncio accesible. Al seleccionar una bolsa vecina, el foco pasa al grupo del carrusel para poder seguir usando teclado.
- Movimiento reducido por sistema/control elimina las transiciones. Sin JavaScript se conserva Amazonas, su precio y compra; los controles interactivos quedan ocultos.
- La selección pertenece solo a 02. Los heroes A/B, video 03, Tarata y catálogo 05 conservan su implementación.

## Validación y límites

Build correcto con Node aislado 22.23.1 y Vite 7.1.3. **312/312 comprobaciones del selector + 117/117 del recorrido completo** en Chromium 148.0.7778.96, DPR 1. [Resultados y scripts](../qa/2026-09-26-origin-selector/README.md).

Baseline A/B, ambos keyframes, movimiento on/off, 1440 × 900 y 390 × 844. Capturas comparadas con las guardadas antes de editar; no hay diferencias de composición en los heroes. Un estado de B tiene 89 píxeles de antialias con diferencia máxima de 7/255; capturas repetidas de ese mismo estado sin cambios de código dieron entre 0 y 320 píxeles de diferencia. El comparador registra el delta y admite como máximo 0.05 % de píxeles con delta de canal ≤16; no se declara identidad estricta de bytes.

Contra `qa/measurements.json` histórico, B mantiene la geometría del CTA. A presenta los cambios previos de la home: y +8 px en mobile y −3.125 px en desktop. No son cambios de esta iteración; el hero actual se conserva contra el checkpoint previo. Deltas completos en `checks.json`.

Probados: cinco productos, enlaces y decodificación; estabilidad de precio/CTA; vuelta Puno→Amazonas; teclado; mouse y tacto emulado; gesto vertical; fallo, lentitud, timeout y reintento; carrera de solicitudes; reduced motion; sin JS; ampliación de texto al 200 % mediante estilos de prueba. El recorrido completo también verifica seek de 03 en ambos sentidos, poster/fallo, compra y autonomía de 05.

**Pendiente:** revisión física de esta rama en Safari y Chrome de iPhone. El éxito reportado por el usuario en Pages pertenece a la versión anterior. La emulación táctil y de texto no sustituye esa revisión. No se modificó ni se publicó Pages.

## Archivos y estado

Implementación: `index.html`, `src/origin.css`, `src/origin.js` y retirada de overrides de 02 en `src/home.css`. Documentación: este informe, `README.md`, `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`. Evidencia y galería: `qa/2026-09-26-origin-selector/`, `deliverables/origin-selector-review.html`.

Los snapshots anteriores de 02 son históricos. No se sobrescribieron. Permanecen aparte los cambios preexistentes en `tools/apimart/*`, `reference/` y el PDF CRO; no se tocaron ni se incluyeron en un commit. No se reclasificó ninguna decisión LOCKED/OPEN ni material provisional.
