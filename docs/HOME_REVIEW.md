# Home Artidoro — entrega para revisión visual

25 de septiembre de 2026. Dirección A — «Perú, en profundidad». Implementación sobre el checkpoint recuperable `0a1da04`, sin commit final.

## Abrir y ver

- **Demo navegable:** [http://127.0.0.1:4174/](http://127.0.0.1:4174/) — build de producción servido localmente.
- **Galería visual:** [videos, frames y home completa](../deliverables/home-review.html). Se puede abrir como archivo local.
- **Captura desktop completa:** [1440 × 900 de viewport](../qa/2026-09-25-home/captures/desktop-home-complete.png).
- **Captura mobile completa:** [390 × 844 de viewport](../qa/2026-09-25-home/captures/mobile-home-complete.png).
- **03 con interfaz:** [desktop](../qa/2026-09-25-home/captures/desktop-03-middle.png) · [mobile](../qa/2026-09-25-home/captures/mobile-03-end.png).
- **Clips:** [horizontal](../public/assets/scene03-desktop.mp4) · [vertical](../public/assets/scene03-mobile.mp4).

Las capturas completas usan movimiento reducido para mostrar todo el contenido con el poster de 03. Los clips, frames y capturas específicas de 03 muestran la media en movimiento. Condiciones: Chromium 148.0.7778.96, DPR 1; los tamaños mobile son emulados.

## Qué está resuelto

01 mantiene presencia, producto y acercamiento al cafetal, con precio y compra desde el primer viewport. 02 permite explorar **cinco** cafés; su selección es local. 03 concentra la ambición visual: de la superficie del café a la taza, con dos composiciones generadas y control reversible mediante scroll. 04 queda reducido a un momento de Tarata. 05 presenta los cinco productos reales, notas, gramaje, precio y compra, y abre el catálogo completo.

La marca, las bolsas, el copy y los enlaces viven en HTML fuera del video. Los botones de compra abren las fichas oficiales; no hay carrito ni checkout simulados. El precio mostrado corresponde a 250 g; la molienda y otros tamaños se eligen en la tienda oficial.

**Ritmo:** solo 03 permanece durante un tramo corto de scroll. 01/02 mantienen transiciones CSS/JS; 04 es una pausa estática y breve. El paso a 05 vuelve a las bolsas y al fondo editorial claro. No hay librería pesada de motion ni toda una home de scroll fijado.

## CRO y performance

Se revisó el PDF CRO existente, sin modificarlo. Las respuestas implementadas son precio/producto/CTA en el hero, decisión por origen con notas y compra, enlace permanente de compra en navegación, atajo comercial dentro de 03 y cierre con cinco productos, precios y CTA individuales. Envíos y preguntas frecuentes enlazan a información oficial. No se inventaron reseñas, valoraciones, descuentos, garantías o promesas de entrega.

El video **no se solicita en la carga inicial**. Se carga una sola composición al acercarse a 03. Poster, fallo de red, límite de espera, movimiento reducido y ahorro de datos conservan el contenido y la compra. Los paisajes y la tipografía se comprimieron sin cambiar sus fuentes; los assets de B no se cargan por adelantado en A.

Medición local sobre el build, una corrida por tamaño, caché desactivada, red 1.6 Mbps/150 ms y CPU 4×:

| Observación | Desktop | Mobile |
|---|---:|---:|
| LCP | 2.20 s | 1.62 s |
| FCP | 1.65 s | 1.60 s |
| CLS | 0.00012 | 0.00046 |
| Recursos transferidos observados | 391 KB | 347 KB |
| Video solicitado al iniciar | No | No |

Son observaciones de laboratorio, no Core Web Vitals de campo ni Lighthouse. No son directamente comparables con las cifras de la web anterior en el PDF, y no prueban un aumento de conversión. [Datos y condiciones](../qa/2026-09-25-home/performance.json).

## Media y coste

| Producción nueva | Modelo / proveedor | Coste registrado |
|---|---|---:|
| 4 stills, inicio/final desktop/mobile | Nano Banana Pro (`gemini-3-pro-image-preview`) / APIMart | US$0.1200 |
| 2 videos de 7 s, horizontal/vertical, sin audio | Kling V3 / APIMart | US$0.9408 |
| **Total de esta fase** | | **US$1.0608** |

Los MP4 preparados pesan 1.68 MB y 2.22 MB. Se conservan originales, prompts, tareas, costes y hashes en [scene03-generation.json](../audit/source/scene03-generation.json). Los posters y frames se prepararon localmente. No se incluye en el coste de esta fase la generación previa de CP04. Saldo del ledger APIMart tras la fase: US$1.586012 acumulados de un límite local de US$2; US$0.413988 restantes. No se alteraron esos límites.

03 es una escena conceptual, no documentación de un origen, método de elaboración o taza oficial. Su movimiento de líquido es estilizado, especialmente en mobile. Tarata reutiliza el asset conceptual aprobado; mantiene su aviso y limitación de autoría de las referencias. Ninguna imagen generada sustituye packaging o logo reales.

## QA crítico

**Build correcto y 117/117 comprobaciones pasan.** Desktop 1440 × 900 y mobile 390 × 844; A/B, ambos keyframes, motion on/off. Cinco selecciones correctas, independencia de 05, scroll reversible, video responsive diferido, posters decodificados, error de MP4, preferencia del sistema, CTA de salida hacia compra y contenido comercial sin JavaScript. Anchors, ausencia de errores JS y desbordamiento horizontal comprobados; además, revisión exploratoria en 320, 360, 768, 1024 y 1920 px.

Contra `qa/measurements.json`, el CTA de B no cambia de posición ni tamaño en ambos keyframes y viewports. En A conserva tamaño y posición horizontal: se desplaza −3.125 px en Y desktop y +8 px mobile por la nueva composición comercial; permanece dentro del primer viewport. [Deltas](../qa/2026-09-25-home/baseline-deltas.json).

B inicial con movimiento reducido coincide píxel a píxel con la captura previa a esta fase, en ambos tamaños. Conversión de fuente comprobada: mismos glifos, mapa Unicode y métricas. [Regresión](../qa/2026-09-25-home/regression-b.json). No es una nueva comparación creativa entre A y B.

Se inspeccionaron visualmente la home completa, 03 desktop/mobile y los frames. [Cobertura reproducible](../qa/2026-09-25-home/README.md). Los snapshots anteriores se conservaron; representan su checkpoint, no esta nueva home.

## Archivos modificados o nuevos

Implementación:

- `index.html`; `src/common.css`, `src/main.js`, `src/origin.js`.
- Nuevos `src/home.css`, `src/home.js`, `src/sensory.css`, `src/sensory.js`.
- Sin cambios en `package.json`, lockfile, configuración Vite, `src/peru.css`, `src/lata.css` ni los antiguos archivos `src/seat.*`.

Assets y trazabilidad:

- `audit/assets.json`; snapshot `audit/source/home-catalog-2026-09-25.json`.
- `audit/source/{villa-rica,cusco,puno}-original.jpg`, `barlow-condensed-800-original.ttf`.
- `audit/source/scene03-{desktop,mobile}-{start,end}.jpg`, `scene03-{desktop,mobile}-original.mp4`, `scene03-generation.json`.
- `public/assets/{villa-rica,cusco,puno}-250g.webp`, `barlow-condensed-800.woff2`, `cafetal-home-{desktop,mobile}.webp`, `tarata-mesa-home.webp`.
- `public/assets/scene03-{desktop,mobile}-{start,end}.webp`, `scene03-{desktop,mobile}.mp4`.
- Nuevos `scripts/prepare-home-assets.py`, `scripts/prepare-scene03-video.py`, `scripts/produce-scene03.cjs`.

Evidencia y documentación:

- `qa/2026-09-25-home/`: scripts QA, JSON de comprobaciones/medición/regresión, capturas y seis frames.
- `deliverables/home-review.html`; este informe.
- `README.md`, `docs/DECISIONS.md`, `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ASSET_AUDIT.md`. Se registra la autorización actual y se identifican los snapshots anteriores como históricos, sin reclasificar sus filas LOCKED/OPEN.

**Cambios ajenos preservados:** los cuatro archivos previamente modificados `tools/apimart/{README.md,cli.cjs,client.cjs,pricing.cjs}`, `reference/` y el PDF CRO no se editaron ni se añadieron a git. La generación autorizada sí actualizó el ledger local ignorado del cliente APIMart. El árbol queda con esta fase y aquellos cambios preexistentes sin commit. HEAD continúa en `0a1da04`.

## Pendientes reales y límites

- Validación visual del usuario de esta implementación y del acabado generado, incluido el movimiento más estilizado del líquido mobile.
- Safari/iOS y dispositivos físicos no probados; queda por validar la fluidez de seek con su decodificador y red real. El fallback está implementado y se probó con fallo de red en Chromium.
- Paisaje sin ubicación exacta confirmada; Tarata mantiene la limitación de autoría de su referencia. Ambos avisos siguen visibles. Se requieren materiales con derechos y atribución claros antes de convertirlos en entrega pública definitiva.
- No se implementaron Shopify, PDP/PLP nuevos, carrito, checkout ni analítica de conversión. Las observaciones del diagnóstico CRO relativas a esas páginas siguen fuera de esta fase.
- No se hicieron pruebas con usuarios, lectores de pantalla ni una auditoría completa de accesibilidad; tampoco se ejecutó una compra real.

No hay un bloqueo técnico conocido para revisar esta demo local. No se solicita otra aprobación de producción ni se inicia una fase adicional.
