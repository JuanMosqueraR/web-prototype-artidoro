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
| `public/assets/cajamarca-250g.webp` / `scripts/prepare-cajamarca.py` | Bolsa Cajamarca derivada del original en `audit/source/cajamarca-original.jpg`; Pillow |
| `qa/2026-09-24-origin-02/` | Evidencia fechada de 02 y regresión de heroes (capturas + mediciones + `QA-origin-02.md`) |
| `public/assets/` | Recursos visuales y tipográficos utilizados por la web |
| `audit/` | Fuentes, clasificación y materiales de preparación conservados |
| `qa.html` | Contenedor de revisión con iframe de dimensiones fijas |
| `qa/QA.md` / `qa/measurements.json` | Informe y mediciones del QA realizado |
| `deliverables/` | Dos HTML autónomos y seis capturas finales |
| `scripts/export-standalone.py` | Exportación HTML con CSS, JS y assets embebidos; Python estándar |
| `scripts/prepare-assets.py` / `scripts/trace-otorongo.py` | Preparación determinista opcional; requieren Pillow y NumPy |
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
