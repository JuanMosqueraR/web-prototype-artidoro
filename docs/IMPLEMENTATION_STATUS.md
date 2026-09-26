# Estado actual — home 01–05, 25 de septiembre de 2026

La fase autorizada L18 ya está implementada sobre `0a1da04`, sin commit final. A es ahora la home; B conserva su hero. El snapshot del 23/24 de septiembre, los HTML autónomos anteriores y las capturas antiguas se conservan como evidencia histórica y **no representan la home actual**. El exportador autónomo anterior no se ejecutó ni se adaptó a esta home con video.

Stack actual: HTML/CSS/JS, Vite 7.1.3, videos H.264 silenciosos con posters WebP y fuentes locales. Sin librería de animación, WebGL, backend ni checkout propio. Los enlaces de compra conducen a las fichas oficiales, donde se elige molienda/tamaño.

| Ruta | Responsabilidad / producción |
|---|---|
| `index.html` | A 01–05, navegación, cinco productos y compra; B retenido |
| `src/home.css`, `src/home.js` | Composición responsive, 04/05, navegación y preferencia de motion |
| `src/sensory.css`, `src/sensory.js` | 03, scroll reversible, carga diferida, cambio de composición y fallbacks |
| `src/origin.js` | Selección local de cinco orígenes, carga de bolsas bajo demanda |
| `src/main.js` | Cambio A/B explícito; anchors de home no cambian la dirección |
| `src/common.css` | Mismos glifos Barlow en WOFF2 en vez de TTF |
| `src/seat.css`, `src/seat.js` | Archivos anteriores conservados, ya no importados por la home |
| `audit/source/home-catalog-2026-09-25.json` | Snapshot de cinco productos oficiales con variantes y fuentes |
| `audit/source/scene03-generation.json` | Seis tareas generativas, prompts, parámetros, costes, hashes y fuentes guardadas; generación no determinista |
| `audit/source/scene03-*.jpg`, `scene03-*-original.mp4` | Originales de cuatro stills y dos videos; no reconstruibles de forma determinista solo con el prompt |
| `audit/source/{villa-rica,cusco,puno}-original.jpg` | Tres fotos reales adicionales del catálogo |
| `audit/source/barlow-condensed-800-original.ttf` | Fuente original retenida para conversión local de formato |
| `scripts/prepare-home-assets.py` | Pillow/fontTools: tres recortes de bolsa, cuatro posters, dos paisajes, Tarata y WOFF2; fuentes guardadas |
| `scripts/produce-scene03.cjs` | Orquestación específica de los dos videos mediante el cliente APIMart existente; generar tiene coste, consultar estado no regenera |
| `scripts/prepare-scene03-video.py` | FFmpeg: H.264, faststart y GOP corto para seek; seis frames de revisión |
| `public/assets/scene03-*` | Dos MP4 y cuatro WebP preparados; la home usa el poster final como fallback |
| `public/assets/{villa-rica,cusco,puno}-250g.webp` | Recortes reales preparados, sin redibujar packaging |
| `public/assets/cafetal-home-*.webp`, `tarata-mesa-home.webp`, `barlow-condensed-800.woff2` | Derivados optimizados; conservan las limitaciones de sus fuentes |
| `qa/2026-09-25-home/` | Capturas, frames, comprobaciones y medición local; scripts Playwright reproducibles |
| `deliverables/home-review.html`, `docs/HOME_REVIEW.md` | Galería visual local y entrega de esta fase |

**Entorno verificado:** Windows PowerShell 5.1, locale es-PE, Python 3.10, Node aislado 22.23.1. El Node 18 global no satisface Vite 7.1.3. Se utilizó el binario compatible ya existente en `C:/tmp/node22/node-v22.23.1-win-x64/node.exe`; no se cambió Node global, package.json, lockfile ni configuración de Vite.

```powershell
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js build
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js preview --host 127.0.0.1 --port 4174
```

Build correcto. Evidencia de 117 comprobaciones en Chromium 148, desktop/mobile, keyframes on/off, fallbacks y navegación. Condiciones y límites completos: [QA](../qa/2026-09-25-home/README.md). La medición local no es una auditoría de campo ni un resultado CRO comercial. Aún faltan pruebas en Safari/iOS y dispositivos físicos; el paisaje continúa sin localización confirmada y Tarata tiene limitación de autoría en su material de referencia.

---

## Snapshot histórico del Hero Lab — 23/24 de septiembre de 2026

# Implementation status — Hero Lab

Estado revisado contra código, documentación y paquete final el 23 de septiembre de 2026. Los 39 archivos del ZIP entregado coinciden byte a byte con sus originales locales antes de añadir este handoff. Esta entrega agrega únicamente cinco Markdown en `/docs`; no reconstruye ni modifica el laboratorio.

## Stack y estructura

HTML semántico, CSS y JavaScript vanilla, con **Vite 7.1.3** como dependencia de desarrollo. Sin React, router, librería de animación, backend, Shopify, video ni WebGL. Las fuentes se sirven localmente. Build configurado para ES2020.

| Ruta desde la raíz | Responsabilidad |
|---|---|
| `index.html` | Dos heroes independientes y barra de laboratorio; copy, imágenes, enlaces y botones reales |
| `src/common.css` | Tipografía, controles, CTA/confianza, estilos compartidos y reduced motion |
| `src/peru.css` / `src/lata.css` | Composición y transición específicas de cada dirección |
| `src/main.js` | Cambio de dirección, estado desplegado y casilla Sin motion |
| `src/origin.css` / `src/origin.js` | Escena 02 “Encontrar tu origen” (solo visible en A): estilos aislados y estado propio de origen (Amazonas/Cajamarca). No comparten estado con el hero |
| `src/seat.css` / `src/seat.js` | Escena 04 “Toma asiento” / CP04 (solo visible en A): estilos aislados y estado propio de vista (entrada/mesa). No comparten estado con el hero ni con 02 |
| `public/assets/cp04-entrada.jpg` / `cp04-mesa.jpg` | `CONCEPTUAL_ASSET` de CP04 (L15–L17). Producción manual/no reproducible (edición con IA + restauración de rótulos con píxeles reales); procedencia, modelo, task_id y prompts en `audit/assets.json` |
| `qa/2026-09-24-seat-04/` | Evidencia fechada de CP04 y regresión contra HEAD (capturas + `data/*.json`) |
| `public/assets/cajamarca-250g.webp` / `scripts/prepare-cajamarca.py` | Bolsa Cajamarca derivada del original en `audit/source/cajamarca-original.jpg`; Pillow |
| `qa/2026-09-24-origin-02/` | Evidencia fechada de 02 y regresión de heroes (capturas + mediciones + `QA-origin-02.md`) |
| `public/assets/` | Recursos visuales y tipográficos utilizados por la web |
| `audit/` | Fuentes, clasificación y materiales de preparación conservados |
| `qa.html` | Contenedor de revisión con iframe de dimensiones fijas |
| `qa/QA.md` / `qa/measurements.json` | Informe y mediciones del QA realizado |
| `deliverables/` | Dos HTML autónomos y seis capturas finales |
| `scripts/export-standalone.py` | Exportación HTML con CSS, JS y assets embebidos; Python estándar |
| `scripts/prepare-assets.py` / `scripts/trace-otorongo.py` | Preparación determinista opcional; requieren Pillow y NumPy |
| `tools/apimart/` | Tooling local reutilizable para generar assets vía APIMart; Node core, sin dependencias; `.env` y `data/` ignorados. Ver su [README](../tools/apimart/README.md). |
| `package.json`, `package-lock.json`, `vite.config.js` | Scripts, dependencias y configuración de desarrollo |

El [README original](../README.md) sigue siendo la referencia operativa general. Los enlaces relativos de este handoff asumen `/docs` directamente dentro de la raíz del proyecto.

## Traslado a VS Code y ejecución

Extraer `artidoro-hero-lab.zip`, abrir su carpeta de proyecto en VS Code y colocar estos cinco archivos en `docs/`. El ZIP contiene las fuentes; los HTML autónomos por sí solos no sustituyen el proyecto editable. No se necesita la integración Sites del entorno anterior para ejecutar localmente.

Según el README, usar Node 20.19+ o 22.12+ y npm. En la terminal situada en la raíz que contiene `package.json`:

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4173
```

| Vista | URL local con el servidor en marcha |
|---|---|
| A | http://localhost:4173/a/ |
| B | http://localhost:4173/b/ |
| A, Keyframe B al cargar | http://localhost:4173/a/?frame=b |
| B, Keyframe B al cargar | http://localhost:4173/b/?frame=b |
| Ejemplo sin motion | http://localhost:4173/b/?frame=b&motion=off |

`/a/` y `/b/` son entradas sobre la misma aplicación; no hay dos páginas ni un router instalado. Alternativamente funcionan `/?direction=a` y `/?direction=b`.

Para revisar sin servidor, abrir `deliverables/A-peru-en-profundidad.html` o `deliverables/B-fuera-de-la-lata.html` en el navegador. Incluyen los recursos y el selector. No abrir el `index.html` de desarrollo por `file://`: utiliza rutas servidas por Vite.

El CTA abre la ficha pública del café Amazonas en una pestaña nueva. No agrega una variante al carrito ni ejecuta una compra dentro del lab.

## Escena 02 (checkpoint del 24 de septiembre de 2026)

Tras el Hero A, `index.html` incluye la sección `#origin-scene` con `aside.origin-lab-note`. Solo se muestran con la dirección A; con B se ocultan por CSS (`display:none`) y quedan fuera del orden de tabulación. Su origen (Amazonas/Cajamarca) es independiente del estado Acercar/Alejar. Villa Rica, Cusco y Puno son filas informativas sin selección. La altura del documento en A ahora es la del hero más la de 02 (más la nota de laboratorio). Descripción y evidencia: [CREATIVE_DIRECTIONS.md](CREATIVE_DIRECTIONS.md) y [qa/2026-09-24-origin-02/QA-origin-02.md](../qa/2026-09-24-origin-02/QA-origin-02.md). Para abrir A → 02: la URL de A (`/a/`) y bajar; `?motion=off` inicia sin movimiento. Con el hero desplegado, `/a/?frame=b`.

El build y el servidor de Vite **no se verificaron** en este entorno (Node 18; ver KI-01). La escena se comprobó con un servidor estático temporal fuera del repo, que no sustituye esa validación.

## Escena 04 — CP04 “Toma asiento” (checkpoint del 24 de septiembre de 2026)

Tras la escena 02 y su nota de laboratorio, `index.html` incluye `#seat-scene` y `aside.seat-lab-note` (esta reutiliza la clase `origin-lab-note`). Solo se muestran con la dirección A; con B se ocultan por CSS (`display:none`) y sus imágenes no se solicitan. Estado propio (`data-view`: `entrada` / `mesa`), independiente del hero y de 02. `seat.js` repite el flujo de 02 (imagen decodificada → desvanecer ~90 ms → cambio síncrono → volver), con una diferencia: una imagen rota se vuelve a pedir al empezar cada intento, de modo que el primer reintento tras un fallo funciona. 02 no se tocó ni se refactorizó.

Contenido factual (local Tarata, dirección, horarios, destino de «Cómo llegar») verificado el 24 de septiembre de 2026 en la [página oficial de locales](https://www.artidororodriguez.com/pages/locales); textos y enlace exactos en `audit/assets.json` (`verified_copy.cp04_tarata`). El enlace de «Cómo llegar» es el `href` de esa tarjeta y no se resolvió ni se siguió. Cafetería La Mar, que la misma página lista, no se usa.

Para abrir A → 02 → 04: la URL de A (`/a/`) y bajar; `?motion=off` inicia sin movimiento. La altura del documento en A pasa de 1861 a 2822 px (desktop) y de 1797 a 2959 px (mobile).

**Validación:** servidor estático temporal fuera del repo (no Vite); `npm run dev`, `npm run build` y `export-standalone.py` **no se ejecutaron** (Node 18; KI-01), por lo que el build real de CP04 no está verificado. `deliverables/*.html` no incluyen CP04: son snapshots anteriores. QA en Chrome 153 headless, dpr 1, viewports emulados 1440 × 900 y 390 × 844: 54 comprobaciones de CP04 y 12 casos de regresión contra HEAD en `qa/2026-09-24-seat-04/data/`. No hubo dispositivo táctil físico, Safari/iOS ni lectores de pantalla.

## Direcciones, keyframes y estado

- El selector superior usa `#a` / `#b`. En mobile muestra las letras; los nombres completos y el indicador FRAME están ocultos visualmente.
- A empieza con **Acercar origen** (Keyframe A). Al pulsarlo pasa a **Alejar origen** (Keyframe B). Otro clic regresa.
- B empieza con **Desplegar origen** (Keyframe A). Al pulsarlo pasa a **Plegar origen** (Keyframe B). Otro clic regresa.
- Cada escena conserva su propio estado mientras se alterna dentro de la misma página. La dirección B no equivale a Keyframe B.
- El estado de keyframe no se escribe en la URL ni en almacenamiento persistente. `?frame=b` solo inicializa desplegada la dirección activa al cargar. Para reiniciar, abrir una URL limpia sin ese parámetro ni hash previo.
- No hay interacción por scroll, autoplay ni seguimiento del pointer. Los botones actualizan `data-expanded`, `aria-expanded`, `aria-hidden` y su texto.

## Reduced motion y mejora progresiva

La casilla **Sin motion** aplica `.no-motion`, que elimina transiciones y animaciones. `?motion=off` permite inicializarla. La preferencia del sistema `prefers-reduced-motion: reduce` también elimina movimiento mediante CSS, y se consulta al inicializar la casilla.

Si el sistema solicita movimiento reducido, desmarcar la casilla no anula esa regla CSS. No hay un listener que mantenga la casilla sincronizada con cambios posteriores de la preferencia del sistema; la media query sí sigue siendo CSS reactivo.

Los keyframes siguen siendo accesibles con cambios instantáneos. El contenido comercial y la bolsa ya existen en el HTML inicial; JS mejora la comparación y el revelado. Esto no equivale a un selector A/B funcional sin JavaScript: esa interacción sí depende del script.

## QA realizado y evidencia

El informe completo está en [qa/QA.md](../qa/QA.md); las coordenadas, en [qa/measurements.json](../qa/measurements.json). No se repiten aquí las tablas de medidas completas.

Se revisaron A y B, estados inicial y desplegado, en Chrome con viewports CSS **1440 × 900** y **390 × 844**. Se comprobó ausencia de overflow del documento en esos tamaños, jerarquía, legibilidad, tamaño del producto, contraste, continuidad, reversibilidad y permanencia del CTA. Bolsa, CTA y confianza conservaron exactamente sus coordenadas entre keyframes. Ambos modos sin movimiento se probaron con duración calculada de transición de 0 s.

Se corrigió durante la implementación un scroll interno de 34 px en B desktop. El estado final usa `overflow: clip` en el hero y una leyenda de origen con fondo verde. Las mediciones finales acreditan la corrección; no debe registrarse como defecto pendiente.

El build final completó correctamente. Se verificó carga de imágenes embebidas, selector y revelado en la exportación autónoma. No se observaron errores de aplicación en el origen local. No se realizó ninguna compra.

**Alcance de las capturas:** el QA empleó un iframe con el viewport CSS exacto. Desktop se proyectó al 90%, por lo que las imágenes entregadas son **1296 × 810**, representando layout 1440 × 900. Mobile está a escala 1:1, **390 × 844**. Se recortó únicamente el margen de la superficie de revisión. Las dos capturas mobile muestran Keyframe B.

Para reproducir el encuadre con el servidor iniciado: `/qa.html?direction=a&size=desktop` o `/qa.html?direction=b&size=mobile`; añadir `&frame=b` abre el estado desplegado. Este contenedor facilita revisión, no es una suite automatizada.

## Limitaciones y deuda deliberada

- Laboratorio de un producto: contenido y posiciones están definidos directamente en HTML/CSS. No hay CMS, catálogo, datos dinámicos, analítica de experimento ni arquitectura ecommerce.
- Las dos variantes están en el mismo HTML y comparten JavaScript. Sus CSS están separados; eliminar una dirección requeriría retirar su markup y referencias de estado, no solo borrar un CSS. No se construyó un sistema de componentes de producción.
- Assets provisionales y límites de resolución/procedencia: ver [ASSET_AUDIT.md](ASSET_AUDIT.md). El SVG del otorongo no resuelve la ausencia del maestro.
- Mobile usa posiciones específicas y un mínimo de 790 px de alto para el hero, además de 44 px de barra. Pantallas más bajas pueden necesitar scroll vertical. La validación no se extiende automáticamente a todas las resoluciones, orientación horizontal, zoom o tamaños de texto.
- No hubo pruebas en teléfonos físicos, Safari/iOS, matriz de navegadores, lectores de pantalla ni una auditoría integral de accesibilidad. La interacción móvil se comprobó por clic en viewport simulado; no se acredita una prueba táctil física.
- No hubo Lighthouse/Core Web Vitals, red móvil simulada, test de conversión o medición de producción. Los ~445 KiB de assets servidos y ~730 KiB por HTML autónomo son tamaños de archivos, no resultados de carga real.
- No hay suite E2E/CI instalada. Se conservan QA manual, mediciones y capturas, no un runner automatizado del entorno anterior.
- Las exportaciones HTML y capturas son snapshots: no se actualizan al editar CSS/JS. La configuración conserva un host permitido del entorno previo; el comando local fuerza `127.0.0.1`. No se modificó esa configuración en el handoff.

## Comandos existentes para una futura revisión autorizada

```sh
npm run build
python scripts/export-standalone.py
```

El README utiliza `python3`; en Windows puede usarse el intérprete Python disponible (`python` o `py`). El exportador usa biblioteca estándar y no requiere ejecutar los scripts de preparación. Ninguno de estos comandos se ejecutó para cambiar el resultado durante este handoff. Una siguiente fase requiere definición de alcance; no se debe iniciar la home a partir de estas instrucciones.
