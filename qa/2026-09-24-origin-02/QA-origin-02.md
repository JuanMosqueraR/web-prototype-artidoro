# QA — escena 02 “Encontrar tu origen” (A → 02)

24 de septiembre de 2026. Evidencia nueva; no sobrescribe `qa/QA.md`, `qa/measurements.json` ni las capturas de `deliverables/`. Estado revisado: HEAD `e5a0b9e` + cambios sin commit de este checkpoint.

## Condiciones

- **Navegador:** Chrome 153 headless (Windows 10), controlado por Chrome DevTools Protocol desde un script Python temporal. Píxel ratio 1, sin zoom.
- **Viewport:** iframe de ancho exacto (envoltorio temporal, escala 1:1) dentro de una ventana emulada del mismo tamaño. Todas las mediciones (`innerWidth/innerHeight`, `scrollY`, `scrollHeight`, `clientWidth`, rectángulos) se toman **dentro del documento del iframe**, que es el que contiene la escena. Confirmado en cada captura: 1440 × 900 y 390 × 844. Las capturas históricas de desktop usaron escala 0.9; estas son 1:1.
- **Servidor:** servidor estático temporal fuera del repo (Node 18, `127.0.0.1`, sin dependencias, sirviendo los archivos actuales sin transformarlos). **No es Vite y no sustituye su validación.** `npm run dev`, `npm run build` y `export-standalone.py` **no se ejecutaron** (Node v18.20.1 < requisito de Vite 7.1.3; KI-01). Build real: **NO VERIFICADO**.
- **Barras de desplazamiento:** las pasadas de regresión usan barras ocultas/superpuestas (equivalente al baseline, donde A no desbordaba). Una pasada exploratoria usa barra clásica de 15 px (ver KI-80).
- **Motion:** “on” = predeterminado; “off” = `?motion=off` (casilla Sin motion); además, `prefers-reduced-motion` emulado en las pruebas de 02 y en un filmstrip.
- **Entrada:** teclado real (`Input.dispatchKeyEvent`), ratón real (`dispatchMouseEvent`) y **toque simulado** (`dispatchTouchEvent` con emulación táctil). No hay dispositivo físico.
- **Antes/después:** HEAD se exportó con `git archive` a un directorio temporal y se midió con el mismo procedimiento (`data/hero-regression-before-HEAD.json`); el estado modificado, en `data/hero-regression-after.json`.

## 1. Regresión de heroes (A y B × inicial/desplegado × 1440 × 900 y 390 × 844 × motion on/off = 16 casos)

- **Antes → después:** las únicas diferencias son `scrollHeight` del documento en A (intencional): desktop 900 → 1861 (hero y barra 900 · 02 900 · nota de laboratorio 61) y mobile 844 → 1797 (844 · 844 · 109). Bolsa, CTA, confianza y botón de interacción de A y B: **0 px de diferencia** en los 16 casos; B sin cambios en absoluto (documento de un viewport).
- **Contra `qa/measurements.json`:** 0 deltas > 0,6 px en bolsa, CTA, confianza e interacción (8 casos comparables); no se asumió delta cero de antemano.
- **Sin desbordamiento horizontal:** `scrollWidth == clientWidth` en todos; sin scroll interno del hero en A. En B, `hero.scrollWidth` (1454/425) supera `clientWidth` por el recorte de diseño (`overflow: clip`), igual que antes.
- **B:** 02 y la nota de laboratorio son `display:none`, sin caja de layout; 30 pulsaciones de Tab (con y sin Sin motion) no entran nunca en `#origin-scene` ni en la nota (16/16 comprobaciones de `data/B-hidden-and-independence.json`).
- **Hero A y estado de 02 son independientes:** Acercar/Alejar no reinicia 02 y elegir Cajamarca no cambia el hero; A → B → A conserva Cajamarca.
- **Observación fuera del contrato (KI-80):** con barra clásica, A cambia de geometría (ancho útil 1425 / 375). Es consecuencia de la altura nueva de A. No se corrigió ni se ocultó la barra; **requiere decisión del usuario**.

## 2. Escena 02

Capturas en `captures/` (`02-desktop-*`, `02-mobile-*`, `hero-regression-*`, `filmstrip-*`). Mediciones en `data/02-geometry.json` (coordenadas relativas al inicio de la sección; y = 0 es el inicio de 02).

**Desktop 1440 × 900** (referencia → medido): kicker y106 → 106 · titular y138 → 138 (Barlow 80, una línea) · instrucción y238 → 238 · índice x86 y284, 382 × 420 → 86,4 / 284 / 382 × 420 (filas de 84) · información x548 → 548,4: indicador 284, procedencia 336, EN TAZA 432, notas 456 (28 px, 2 líneas reservadas), línea 548 (145 px), 250 g 578, precio 606 (32 px) → todas iguales · bolsa centro x1080, inicio 270, alto 496 → 1080,05 / 270 / 496 (212,5 de ancho) · CTA x548 y676 330 × 58 → 548,4 / 676 / 330 × 58 · enlace de catálogo y796 → texto en 796 (caja táctil de 44 px desde 784) · altura de sección 900.

**Mobile 390 × 844:** márgenes 22 · kicker y52 → 52 · titular y76 (Barlow 48, interlínea 44) → 76 · índice 192–432 → 192–432 (filas de 48; nombre Barlow 26, nota Chivo 12, sin recortes) · panel y466 → 466; información 190 de ancho; bolsa 224 de alto, centro x292 → 292; precio termina en 689 (antes del CTA) · CTA x22 y724 346 × 54 → igual · enlace ≈ y798 → 798 · altura 844.

**Estabilidad entre orígenes:** 0 diferencias de rectángulo en escena, encabezado, índice, filas, campos de información, caja del producto, CTA, catálogo y altura, entre Amazonas y Cajamarca, en los cuatro casos viewport × motion. `scrollY` idéntico antes/después de seleccionar. Sin overflow horizontal ni contenido cortado ni solapamientos entre cajas de texto (comprobación geométrica en ambos viewports).

**Contenido y destinos** (`href` resueltos completos): CTA Amazonas → `https://www.artidororodriguez.com/products/cafe-amazonas`, texto “Comprar café de Amazonas ↗”; CTA Cajamarca → `https://www.artidororodriguez.com/products/cafe-cajamarca`, “Comprar café de Cajamarca ↗”; catálogo → `https://www.artidororodriguez.com/collections/cafe` (absoluto). Los tres con `target="_blank" rel="noopener"`. Precio S/ 39.90 en ambos, verificado hoy (sin diferencia con la referencia del checkpoint). Imágenes: 326 × 761, `complete`, `naturalWidth > 0` (Amazonas: la misma foto del hero; Cajamarca: foto oficial preparada, no placeholder).

**Filas informativas** (Villa Rica, Cusco, Puno): `<div>` sin `tabindex`, cursor por defecto; las filas funcionales son `<button>` con cursor pointer. Contraste: tinta/crema 12,81:1; notas y numeración del índice (`#3d564b`/crema) 7,01:1; CTA crema/verde 12,81:1 (hover 9,82:1).

## 3. Interacción (42/42 comprobaciones, `data/02-interaction.json`; ambos viewports)

Clic (desktop) y toque simulado (mobile): selección correcta, foco en el control activado, sin desplazamiento de página. Teclado: Tab salta las filas informativas, Enter y Espacio seleccionan, el foco permanece y es visible; el conjunto enfocable de 02 son 4 elementos (2 botones, CTA, catálogo). Casos de cambio rápido, con una invariante muestreada en cada `requestAnimationFrame` (registro visible = bolsa visible = `aria-pressed` = destino y texto del CTA = `data-origin`; 0 violaciones):

- Amazonas → Cajamarca → Amazonas antes del cambio de estado: resultado Amazonas, sin cambios de `data-origin` posteriores.
- Repetir el mismo origen ya mostrado: sin efecto; repetir el origen pedido con cambio pendiente: un solo cambio.
- Alternancias durante fases de salida y entrada; ráfagas de 12 (→ Amazonas) y 11 (→ Cajamarca) alternancias a ~30 ms: gana la última solicitud.
- Sin motion activado con la animación pendiente: commit inmediato coherente, opacidad 1, sin `is-out`; con Sin motion activo el cambio es inmediato; `prefers-reduced-motion` emulado: cambio inmediato.
- CTA operable durante la transición (clic a los ~40 ms abre el destino del origen mostrado en ese instante). No se usa `inert`.

## 4. Coordinación carga ↔ selección (34/34, `data/02-image-load-tests.json`)

Método: `Fetch.enable` de CDP retiene o falla la petición de `cajamarca-250g.webp`. Comprobado en ambos viewports: carga lenta con vuelta a Amazonas (la carga tardía no cambia la selección; mientras espera siguen visibles y operables Amazonas, su información y su CTA); error de carga (se conserva el origen mostrado, opacidad normal, aviso “No se pudo cargar este origen. Inténtalo de nuevo.”, 0 rechazos sin gestionar, un nuevo clic reintenta y funciona); timeout de 4 s (a los 3,6 s sigue esperando; a los 4,6 s conserva el origen y muestra el aviso; la liberación tardía no cambia nada); C→A→C con la imagen pendiente (gana la última, un solo cambio); Sin motion activado con la imagen pendiente y con Sin motion ya activo (nunca una bolsa vacía; al llegar la imagen, cambio inmediato y coherente). Con la imagen ya cargada, el primer cambio en A no muestra hueco.

**Qué se solicitó** (registro del servidor, `data/network-*.json`; ambos viewports iguales): **(a)** `/b/` abierto directamente: no se pide `cajamarca-250g.webp`; **(b)** `/a/` abierto y luego cambio a B: cero peticiones nuevas al cambiar; **(c)** en A la imagen de Cajamarca se pide al abrir (queda dentro de la distancia de carga diferida de Chrome; KI-83). B sí carga los archivos `origin.css` y `origin.js`.

## 5. Hero → 02 (`captures/filmstrip-*`, `data/hero-to-02.json`)

Desktop y mobile, desde hero inicial y desplegado, y una pasada con movimiento reducido (Sin motion + `prefers-reduced-motion`): el hero asciende sin cambios, entran los 64 px verdes (32 mobile) que continúan el verde del hero, aparece el crema con un borde limpio, luego encabezado, índice con Amazonas y bolsa. Sin sticky, pinned, parallax, video, WebGL ni crossfade. Eje de la bolsa: desktop hero 1080,0 → 02 1080,05; mobile hero 284,7 → 02 292 (el 02 sigue la referencia de la especificación; diferencia de 7,3 px, no es un fallo de implementación). Sin overflow horizontal en ningún paso.

## Diferencias respecto a la especificación y decisiones de ejecución

- Las coordenadas “y” se interpretan como la parte superior de la caja de línea de cada texto.
- Desktop de tres columnas solo a partir de 1360 px: por debajo, la bolsa al 75% invadiría la columna de información. Por debajo de 1360 px (y ≥ 761) 02 usa la composición vertical de mobile, con franja verde de 64 px y kicker a 76 px para no quedar dentro de la franja.
- Se añadió una instrucción visible en mobile (“Elige un origen para conocer su café”, y170) porque la especificación mobile no la sitúa; y una línea de estado reservada bajo el índice para el aviso de error.
- La nota del laboratorio (`aside.origin-lab-note`) queda bajo la sección y no cuenta en su altura, pero sí en la del documento.
- Notas de la información en peso regular; precio en negrita.

## Exploratorio (no es contrato; capturas fuera del repo)

`data/exploratory-layout-widths.json`: 1920 × 1080, 1440 × 700, 1366 × 768, 1360, 1359, 1280, 1024, 768, 600, 430, 360 y 320: sin solapamientos ni contenido fuera del ancho ni overflow horizontal tras dos ajustes hechos durante la revisión (kicker sobre la franja verde en 761–1359 px; desborde a 320 px). El alto de la sección es 900 (≥ 761) u 844–860 (< 761). `data/exploratory-classic-scrollbar.json`: ver KI-80.

## No cubierto

Build/dev real de Vite (NO VERIFICADO), dispositivos táctiles físicos, Safari/iOS y otros navegadores, lectores de pantalla, pantallas de alta densidad, rendimiento (Lighthouse, red simulada), zoom o tamaños de texto ampliados, orientación horizontal en móviles, y los HTML de `deliverables/` (no incluyen 02; KI-81/KI-82).
