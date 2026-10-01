# PDP renovadas — 1 de octubre de 2026 (L31)

| Ruta | Contenido |
|---|---|
| `src/pdp.css` | Estilos de las dos PDP (las reglas antiguas de PDP se retiraron de `src/catalog.css` y `src/ahorrador.css`) |
| `src/pdp.js` | Galería (scroll-snap, flechas, miniaturas, contador), zoom a pantalla completa (`<dialog>` por galería) y aparición del botón fijo; variantes, precios y rutas siguen en `src/catalog.js`. `src/inertia.js` deja la rueda a la foto ampliada (`.lb-open`) |
| `scripts/prepare-pdp-assets.py` | Prepara desde `audit/source/`: mapa oficial con la paleta de la demo, foto oficial en la montaña, bolsas de 1 kg de Villa Rica y Cusco, y las dos imágenes generadas |
| `audit/source/pdp-*-original.*`, `audit/source/ahorrador-{villa-rica,cusco}-1kg-original.jpg`, `audit/source/pdp-generation.json` | Originales oficiales y generados; registro de generación con prompts, costes y el descarte |
| `qa/2026-10-01-pdp-pack/` | El Ahorrador como cuarta opción de tamaño en Amazonas, la línea de 1 kg y la sección inferior de descubrimiento; `checks.json` (20/20) |
| `qa/2026-10-01-pdp-ajustes/` | Ajustes tras la prueba en iPhone: título sin recuadro de foco y margen del carrusel mobile; `checks.json` (4/4) |
| `qa/2026-10-01-pdp/` | `verify.py`, `checks.json` (50/50) y capturas de las dos PDP, con el zoom |

`src/catalog.js` añade el precio por tamaño, las tazas por bolsa, los selectores por bolsa del pack, la sincronización del botón fijo, la carga de las imágenes de cada PDP al abrirla y la clase `on-pdp`. Regresiones ejecutadas fuera del repo: home 154/154 y precios 15/15.

# Precios al día — 1 de octubre de 2026 (L31)

| Ruta | Contenido |
|---|---|
| `audit/source/prices-2026-10-01.json` | Snapshot de `/products/<handle>.js` de los nueve productos con precio en la home y las PDP |
| `scripts/prepare-prices.py` | Reescribe `src/amazonas-variants.json` y `src/ahorrador-variants.json` desde ese snapshot, sin red |
| `qa/2026-10-01-precios/` | `verify.py`, `checks.json` (15/15) y capturas: cada precio mostrado frente al snapshot; sin precios anteriores en el documento |

Precios fijos en `index.html` (hero, 02, 05, PDP del pack) corregidos a mano contra el snapshot; `public/assets/og-share.jpg` regenerado con `scripts/prepare-og-image.py`. Regresión completa de `qa/2026-10-01-orden/verify.py` ejecutada en una copia fuera del repo: 154/154.

# Revisión de la home — 1 de octubre de 2026 (L29)

| Ruta | Contenido |
|---|---|
| `qa/2026-10-01-revision/` | `verify.py` (regresión de L28 adaptada más los controles de esta ronda), `checks.json` (143/143), capturas y README |
| `qa/2026-10-01-orden/` | P4: la misma verificación más orden de secciones, anclas y carga de fotos de los bloques de cierre; `checks.json` (154/154), capturas y README |
| `audit/source/locales-2026-10-01.txt` | Extracto literal de la página oficial de locales (direcciones, horarios y enlaces de mapa de Tarata y La Mar) |

Cambios en `index.html`, `src/home.css`, `src/catalog.css`, `src/catalog.js` (P4: las fotos de 05 y de los mosaicos también se piden al acercarse a los bloques de cierre), `src/origin.css`, `src/origin.js`, `src/peru.css` y `src/scenes.js`; sin assets nuevos ni dependencias.

# Hero «Del cafetal a tu bolsa», 03 «De la bolsa a tu taza» y mejoras generales — 30 de septiembre de 2026 (L28)

| Archivo | Qué es / cómo se produce |
|---|---|
| `index.html` | Nuevo marcado del hero A (`#direction-a`, mismas clases e id), nueva 03 (`#sensory-scene`, se conserva el id por los enlaces externos), franja `.grinds`, cuarto punto de confianza en 05, `data-reveal-lines`, canvas `.hs-seq` en títulos, scripts `scenes.js` e `inertia.js`, texto de «Acerca de esta demo» |
| `src/scenes.js` (nuevo) | Motor de las dos escenas: progreso amortiguado, video del hero por scroll en todos los dispositivos (pedido tras la carga) con la secuencia AVIF/WebP en canvas (ventana de bitmaps, liberación de memoria) como respaldo si el video no está listo en 3,5 s, y 03 con cruces, textos y bolsa ligados al scroll (variables CSS `--f2..4`, `--z1..4`, `--t1..3`, `--cbag`); el video y la secuencia se liberan cuando el hero queda lejos, pasos de 03 disparados por scroll con transición de tiempo fijo, modo estático sin movimiento. Sustituye a `src/sensory.js` (eliminado) |
| `src/inertia.js` (nuevo) | Scroll con inercia solo con rueda en desktop; cede ante teclado, barra, anclas y zonas con scroll propio; desactivado con movimiento reducido o táctil. Sin dependencias (no hay npm para el Node 22 aislado y no se tocó `node_modules`) |
| `src/peru.css` (reescrito), `src/sensory.css` (reescrito), `src/home.css`, `src/catalog.css`, `src/home.js`, `src/origin.js` y `src/origin.css` (solo el gesto de swipe de 02, reescrito al estilo de un drag de Framer) | Estilos del hero y de 03/moliendas; header transparente, revelado de títulos; icono `icon-fair`; lógica de header, revelado y saltos que cruzan escenas (la barra de compra de mobile se retiró tras la prueba en iPhone) |
| `scripts/produce-hero.cjs` | Orquesta los cuatro clips del hero con el cliente APIMart existente (primer y último fotograma por tarea); generar tiene coste, `status` no regenera |
| `scripts/prepare-hero-video.py` | FFmpeg (imageio-ffmpeg): une los dos clips por formato, H.264 CRF 28/29, GOP 8, faststart; pósters inicial y final como WebP; secuencia de 121 AVIF a 12 fps (calidad máxima dentro de 1,5 MB mobile / 2,4 MB desktop, desde los clips originales) y de 61 WebP a 6 fps de respaldo. Salidas `public/assets/hero-{desktop,mobile}.mp4` (24 fps constantes, escala 12288, GOP 4 sin fotogramas B, con hqdn3d + Lanczos + unsharp; 3,26 y 3,44 MB), `hero-*-{start,end}.webp` (de los originales) y `hero-seq/{device}-{avif,webp}/` (mobile 1,41 y 1,45 MB; desktop 2,24 y 1,50 MB) |
| `scripts/prepare-og-image.py`, `public/assets/og-share.jpg` | Imagen de previsualización 1200 × 630 (135 KB): captura del hero final con `?motion=off` sobre un build servido; las etiquetas `og:`/`twitter:` están en el `<head>` de `index.html` (URL absoluta del host de Pages, título marcado «Demo») |
| `scripts/prepare-cup03.py` | Pillow: WebP desktop de 1600 px y recortes 9:16 mobile de los fotogramas de 03; el bodegón mobile tiene composición propia. Salidas `public/assets/cup03-*` |
| `audit/source/hero-generation.json`, `hero-*`, `cup03-*` | Registro de las 18 tareas (15 adoptadas, 3 descartadas; US$ 1,76), prompts y parámetros sin URLs firmadas; originales de imágenes y clips |
| `qa/2026-09-30-l28/` | `verify.py`, `checks.json` (107/107), capturas y README con condiciones y rendimiento de laboratorio |

Estado de publicación (1 de octubre, tras L29): `master` va 13 commits por delante de `origin/master` (`cf45646`, L29 publicada en Pages); L30 y L31 (precios al día, PDP renovadas y el pack en la decisión de Amazonas) aún no están publicadas. Build de verificación con la Vite 7.1.3 del repo y Node 22.23.1 aislado. Los assets de la 03 anterior (`scene03-*`) siguen en `public/assets/` sin uso.

---

# Medición de rendimiento de la home publicada — 30 de septiembre de 2026

*Describe la home publicada antes de L28; histórico. Por L30 no se vuelve a medir hasta la fase de Shopify.* Clase 0/1, solo lectura. Script y resultados en `qa/2026-09-30-performance/` (`perf.py`, `perf.json`, README): mediana de 3 corridas, LCP 1,67 s en mobile con Slow 4G y CPU 4× (0,21 s en desktop), CLS 0, sin peticiones fallidas; la primera corrida en frío tarda ~4 s. Laboratorio, no de campo ni Lighthouse; no es comparable 1:1 con el 12,1 s del diagnóstico CRO (otra herramienta y otro sitio). Detalle y límites en el README de esa carpeta.

---

# Cierre gráfico de 05 — 30 de septiembre de 2026 (L27)

`index.html` (nueva sección `#close-bands`), `src/catalog.css` (bloque de bandas; se retiran las reglas del bloque antiguo de reseñas/categorías), `src/catalog.js` (selector de carga diferida ampliado). Evidencia: `qa/2026-09-30-cierre-05/`. Un asset nuevo: `public/assets/nanolote-tin.webp` (derivado de `audit/source/nanolote-original.jpg` con `scripts/prepare-nanolotes.py`). Build de verificación con Vite 6.4.3 externo.

---

# Hero automático y ajustes de 05 — 30 de septiembre de 2026 (L25)

Cambia `index.html`, `src/peru.css`, `src/home.css`, `src/home.js`, `src/sensory.js`, `src/sensory.css`, `src/main.js` (guard sin botón), `src/ahorrador.css`; evidencia en `qa/2026-09-30-hero-auto/`. Sin assets nuevos. Build de verificación con Vite 6.4.3 externo (el `node_modules/vite` del repo está incompleto; sin reparar, Class 2).

---

# Auditoría y corrección de la home 01–05 — 30 de septiembre de 2026

Autorización L24, sobre checkpoint `0b33580`. Sin commit final de este cambio. Solo dirección A; B, PDPs y assets sin tocar.

| Ruta nueva o afectada | Función / producción |
|---|---|
| `index.html`, `src/common.css`, `src/home.css`, `src/peru.css`, `src/origin.css`, `src/sensory.css`, `src/catalog.css`, `src/ahorrador.css` | Iconos SVG por `mask` (sin fuente, corrige el emoji de iOS); corrección del solape y del CTA del hero mobile; suelo tipográfico y touch targets; retiro de etiquetas de laboratorio; reescritura de avisos de procedencia (mismo lugar, mismo gap, texto humano); tarjeta «Café de origen» en 05 en lugar de la fila huérfana; reseñas con nota de fuente y producto enlazado a su PDP |
| `qa/2026-09-30-home-audit/` | Script Playwright, `checks.json` (39/39) y capturas; regresión de B (8/8 estados, 0 px) |
| `docs/HOME_AUDIT_2026_09_30.md` | Entrega, alcance, validación y límites de esta revisión |

Entorno: Node 22.23.1 aislado, Vite 7.1.3, Python 3.10, Playwright Chromium 148.0.7778.96, Windows. Sin cambios de dependencias ni de assets/`audit/source`.

---

# Ahorro visible, propuesta y script de publicación — 29 de septiembre de 2026

Autorización L23. Checkpoint previo `41d0cf1`. El usuario confirma que la iteración del 28 de septiembre funciona en un iPhone físico y que la publicó en GitHub Pages; Pages no incluye estos cambios. Las menciones de las secciones inferiores a una prueba de iPhone pendiente o a que no hubo publicación quedan superadas.

| Ruta nueva o afectada | Función / producción |
|---|---|
| `index.html`, `src/catalog.js`, `src/ahorrador.css` | Precio normal tachado y ahorro en la tarjeta del pack de 05 y en su PDP; el cálculo usa `data-compare-at` y el precio de la variante elegida |
| `audit/source/ahorrador-2026-09-29.json`, `audit/assets.json` | Snapshot oficial con `compare_at_price` y registro `verified_copy.ahorrador_saving_2026_09_29` |
| `qa/2026-09-29-ahorro/` | Regresión 211/211, pack 316/316, ahorro 20/20 y capturas; condiciones en su README |
| `scripts/build-presentation-artifact.py` | Herramienta (Clase 2, L23). Python estándar: quita el esqueleto HTML, incrusta las fuentes y copia las imágenes referenciadas. Escribe solo en `--out` (por defecto `dist/presentation-artifact/`, ignorado por Git) y no publica |
| `deliverables/presentacion-artidoro.html` | Capturas de `qa/2026-09-29-ahorro/after/` y referencia al ahorro en la parada 2 y la tabla de estrategia |
| `docs/PROPUESTA_ETAPA1.md`, `docs/PROPUESTA_NOTA_INTERNA.md` | Propuesta en borrador y su nota interna, escritas manualmente; no son una cotización aprobada |

Entorno: Node 22.23.1 aislado, Vite 7.1.3, Python 3.10, Playwright Chromium 148, Windows. Sin cambios de dependencias.

---

# El Ahorrador — revisión del 28 de septiembre de 2026

Desarrollada en `feat/catalogo-pdp` desde checkpoint `87ea725`; versionada e integrada localmente en `master` por fast-forward hasta `a5512e2`, por instrucción del usuario (L22). Sin push ni nueva publicación. [Handoff actual](HANDOFF.md) · [Entrega](AHORRADOR_REVIEW.md). Home local `http://127.0.0.1:4175/`; ficha `http://127.0.0.1:4175/#producto-ahorrador`. La confirmación anterior de iPhone corresponde al checkpoint, no a esta iteración.

| Ruta nueva o afectada | Función / producción |
|---|---|
| `index.html`, `src/catalog.js`, `src/ahorrador.css` | Accesos al pack, jerarquía de 05 y segunda PDP; CSS/JS propios, sin librerías |
| `src/ahorrador-variants.json` | 125 variantes, generadas desde el snapshot oficial |
| `audit/source/ahorrador-*.json`, `audit/source/ahorrador-*-original.jpg`, `audit/source/ahorrador-original.jpg` | Respuestas oficiales, tres fotos individuales y foto grupal descartada por discrepancia de gramaje |
| `public/assets/ahorrador-*-1kg.webp`, `scripts/prepare-ahorrador.py` | Tres recortes WebP reproducibles; script también genera variantes |
| `qa/2026-09-28-ahorrador/` | Regresión, pruebas de combinación, destinos oficiales y capturas directas |
| `dist/ahorrador-pages/` | Build local ignorado, generado por `scripts/build-pages.py --allow-dirty --out dist/ahorrador-pages`; sin staging de rama ni publicación |
| `docs/HANDOFF.md`, `docs/CLAUDE_PRESENTACION_PROMPT.md` | Handoff escrito manualmente y prompt para redactar presentación/propuesta; no son una cotización aprobada |
| `deliverables/presentacion-artidoro.html` | Presentación de 12 diapositivas para la reunión con el dueño (29 de septiembre), escrita manualmente; incluye la revisión propia de la tienda (evidencia exploratoria en `qa/draft-2026-09-29-tienda-actual/`, ignorada por Git). Sin assets nuevos: usa `public/assets/` y capturas de `qa/2026-09-28-ahorrador/after/` por ruta relativa y recorte CSS; abrir desde el repositorio. Enlaza a la demo en GitHub Pages; imprimible a PDF (una diapositiva por página). Copia publicable generada con `scripts/build-presentation-artifact.py` y publicada como Artifact (enlace en `docs/HANDOFF.md`) |

Node aislado 22.23.1/Vite 7.1.3, sin cambio de tooling. Las entregas inferiores y sus evidencias se conservan como históricas.

---

# Revisión catálogo/PDP — 28 de septiembre de 2026

Rama `feat/catalogo-pdp` desde `38a209f`, versionada por petición del usuario y sin merge ni publicación desde esta revisión. [Entrega actual](CATALOG_PDP_REVIEW.md). Home local `http://127.0.0.1:4175/`; PDP `http://127.0.0.1:4175/#producto-amazonas`. Las URLs requieren el servidor de preview activo. El 28 de septiembre el usuario confirma que esta versión se ve bien en iPhone, sin especificar navegador o versión; no es una validación instrumental completa de iOS.

| Ruta nueva o afectada | Función / producción |
|---|---|
| `index.html`, `src/catalog.css`, `src/catalog.js` | 05, menú Tienda, FAQ/reseñas y PDP de Amazonas con navegación por hash; sin dependencias nuevas |
| `src/amazonas-variants.json` | Doce variantes estáticas; generado por `scripts/prepare-catalog-assets.py` desde el snapshot oficial |
| `audit/source/catalog-pdp-2026-09-28.json` | Respuestas originales de cuatro endpoints públicos `.js` de producto, guardadas el 28 de septiembre |
| `audit/source/catalog-reviews-2026-09-28.json` | Dos reseñas publicadas; texto, HTML fuente, URL y fecha capturados mediante Playwright |
| `audit/source/catalog-*-original.*` | Tres fotografías originales descargadas sin alteración de los productos oficiales |
| `public/assets/catalog-*.webp`, `scripts/prepare-catalog-assets.py` | Recortes/compresión reproducibles desde originales; no generación ni redibujo |
| `qa/2026-09-28-catalog-pdp/` | Capturas directas antes/después, QA principal, comprobaciones adicionales y lecturas de destinos oficiales |

Build verificado con Node aislado 22.23.1, Vite 7.1.3. QA Chromium 148, DPR 1: 211/211 + cinco comprobaciones adicionales y dos destinos externos. Fuentes y clasificación en `audit/assets.json`. Las entregas inferiores son históricas; no se sobrescribieron sus capturas ni se generó otra galería.

---

# Selector horizontal de 02 — rama de revisión, 26 de septiembre de 2026

Implementado en `feat/origin-selector` desde `7b122b9`, por aprobación explícita del plan del usuario. Solo 02 cambia: cinco nombres y carrusel de bolsas, composición mobile compacta y dos columnas desde 1024 px. Sin dependencias ni assets nuevos. Versionado en esa rama por petición del usuario, sin merge a `master`; la publicación en Pages la hace el usuario con `scripts/build-pages.py` y este documento no registra si ya ocurrió. [Entrega y QA](ORIGIN_SELECTOR_REVIEW.md).

| Ruta nueva o afectada | Función / producción |
|---|---|
| `index.html`, `src/origin.css`, `src/origin.js` | HTML comercial de 02, estilos propios, selección atómica, preparación de vecinos y gestos |
| `src/home.css` | Retira únicamente los overrides anteriores de 02; las reglas nuevas están en origin.css |
| `qa/2026-09-26-origin-selector/` | Capturas antes/después del contrato, secuencia, geometría, fallos de carga y regresión; Python Playwright/Chromium, scripts incluidos |
| `deliverables/origin-selector-review.html` | Galería escrita manualmente sobre las capturas del nuevo QA; servir desde Vite dev para resolver rutas relativas |
| `docs/ORIGIN_SELECTOR_REVIEW.md` | Resultado, condiciones, comandos y límites de esta iteración |

Node aislado 22.23.1, Vite 7.1.3, Python 3.10 y Windows. Preview local de esta sesión en `http://127.0.0.1:4175/`. Los snapshots anteriores conservan el listado vertical de 02: son históricos y no se sobrescriben. La publicación y la validación física de iPhone descritas debajo corresponden a la versión anterior, no a esta rama.

---

# Despliegue automático con GitHub Actions — 30 de septiembre de 2026

Sobre `2e93f2f`. La publicación en Pages deja de ser manual: `.github/workflows/pages.yml` compila y despliega en cada push a `master`, sin build local, sin clon aparte de `gh-pages` y sin segundo `git push`. La rama `gh-pages` del remoto (fuente de la sección anterior) queda sin actualizar desde el 26 de septiembre; ya no es la fuente que sirve Pages.

| Ruta | Función / producción |
|---|---|
| `.github/workflows/pages.yml` | Herramienta (Clase 2, aprobada por el usuario). `push` a `master` → job `build` (Node 22 del runner, `npm ci`, `python3 scripts/build-pages.py --node node --out dist/pages`) → `upload-pages-artifact` → job `deploy` (`deploy-pages`) |
| `scripts/build-pages.py` | Sin cambios de comportamiento salvo lo de abajo; ahora lo ejecuta también el workflow, no solo el uso local |

**Cambio en `build-pages.py`** (mismo commit `ce2e56d`, antes de este despliegue): los enlaces `/b/` y `/?motion=off` del pie dejaron de existir en `index.html` (cambio de contenido de L24-L27, no de este commit). El script exigía exactamente una ocurrencia de cada uno y se detenía si no la encontraba; ahora los reescribe solo si aparecen (0 o 1 vez) y sigue deteniéndose si aparecen 2+ veces (caso ambiguo). El resto de comprobaciones (ninguna ruta raíz-absoluta sin resolver en el HTML/CSS/JS compilado) no cambió.

**Hallazgo de entorno, no de código:** el primer despliegue con Actions falló en el job `deploy` — GitHub crea automáticamente un ambiente `github-pages` con una regla de qué ramas pueden desplegar ahí, y por defecto no incluía `master`. Se corrigió agregando `master` en Settings → Environments → `github-pages` → *Deployment branches and tags*; no requirió cambios en el repo. Detalle y condiciones en KI-90.

**Validación:** el job `build` corrió `scripts/build-pages.py` sin intervención y sin errores (39 archivos). Tras corregir la regla de ambiente, el job `deploy` terminó en verde y la URL pública respondió con el contenido esperado (título, los cinco orígenes, El Ahorrador, Travel Line, Tarata, FAQ) verificado por fetch externo. **No cubierto:** capturas visuales de la página desplegada, comparación píxel a píxel contra el build local, ni revisión en iPhone de esta ronda.

---

# Publicación en GitHub Pages — 26 de septiembre de 2026

Sobre `581e24f`. La revisión pública pasa del Artifact a GitHub Pages. El Artifact se retiró por decisión del usuario (borrado; enlace inválido, historial no recuperable) tras fallar el video 03 en Chrome y Safari de iPhone dentro de su contenedor; ver KI-61 y [VIDEO_RECOVERY](VIDEO_RECOVERY.md). Según el usuario, el sitio en Pages funciona en Chrome y Safari de iPhone y el video arranca solo.

| Ruta | Función / producción |
|---|---|
| `scripts/build-pages.py` | Herramienta (Clase 2, aprobada por el usuario). Python estándar más el Node de Vite: compila, hace relativas las rutas `/assets/…` (también los `data-*` que lee el JS), cambia `/b/` y `/?motion=off` del pie por `#b` y `?motion=off`, añade `.nojekyll`. Se detiene si `index.html`, `src/`, `public/` o los archivos de paquete tienen cambios sin commit (`--allow-dirty`). Con `--branch-dir` prepara un commit `gh-pages` en un repositorio local fuera de este. No añade remotos ni hace push |
| `dist/pages/` | Salida generada; ignorada por git (`dist/`) |
| rama `gh-pages` (remoto) | Build publicado por el usuario; no forma parte del historial de `master`. El árbol que produce el script coincide con el del commit preparado en la sesión (`f35b4d7`); no se verificó el remoto |
| `artifact-build/hero-lab-artifact.html` | Histórico: primera exportación como Artifact (`18b122d`). No representa la home actual (KI-82) y el Artifact asociado se retiró |

Uso y comandos: [README](../README.md#publicar-en-github-pages). **Entorno:** con el Node 18 global el script se detiene; se usó el Node 22.23.1 aislado (`--node`), Vite 7.1.3, Python 3.10, Windows.

**Validación (Chromium 148, DPR 1, 1440×900 y 390×844, servidor estático con Range bajo `/web-prototype-artidoro/`; no es GitHub Pages ni se conserva en el repo):** 8 estados (A/B × keyframe A/B × desktop/mobile) idénticos píxel a píxel al build original; 0 peticiones fallidas; los cinco orígenes cargan bajo demanda; imágenes de Tarata cargadas; video 03 con `readyState` 4 en desktop y mobile; suite de recuperación 20/20. El script se ejecutó dos veces: mismos bytes que el sitio verificado y segunda ejecución sin commit nuevo. **No cubierto:** cabeceras reales de Pages (Range, caché), otras versiones de iOS, Android, modo de bajo consumo, capturas del iPhone (el resultado es lo que informa el usuario).

---

> **Corrección posterior de video03 (26 de septiembre):** recuperación tras carga lenta, activación/reintento por toque y eventos de disponibilidad alternativos. [Estado, QA y diferencias con el Artifact](VIDEO_RECOVERY.md). Checkpoint previo `8d24ed9`; corrección versionada en `891bbc4`, QA en `94fa987`, por petición explícita del usuario. No validado directamente en el host real de Artifacts; en iPhone solo consta el arranque automático que el usuario reporta en Pages, no las rutas «Activar» y «Reintentar movimiento». La v4 de Claude incorporaba un adaptador Blob que no estuvo en este repo; el Artifact se retiró el 26 de septiembre de 2026 (KI-61).

# Actualización de Tarata — 26 de septiembre de 2026

L19 implementado sobre el checkpoint `3830028` de la home, sin commit final de esta revisión. 04 ahora combina dos fotografías existentes, animación de entrada única, carga diferida a 800 px y fallback sin JS. Mobile prioriza fachada/moto; desktop, interior/personal/cascos. No se cambian 01/02/03/05 ni B. La documentación del 25 de septiembre de abajo es el estado anterior de 04.

| Ruta nueva o afectada | Función |
|---|---|
| `index.html`, `src/home.css`, `src/home.js` | Composición, fuentes responsive, motion y carga de 04; aviso de procedencia actualizado |
| `audit/source/tarata-*-original.jpg` | Copias exactas de las dos referencias seleccionadas; las originales no se modifican |
| `public/assets/tarata-facade.webp`, `tarata-interior.webp`, `tarata-interior-mobile.webp` | Derivados WebP sin generación ni retoque |
| `scripts/prepare-tarata-editorial.py` | Preparación reproducible con Pillow desde audit/source |
| `qa/2026-09-26-tarata/` | 117 comprobaciones del recorrido + 30 específicas, capturas y regresión |
| `deliverables/tarata-review.html`, `docs/TARATA_REVIEW.md` | Entrega visual vigente para 04 |

Build verificado con el mismo Node aislado 22.23.1 y Vite 7.1.3. Demo actual: http://127.0.0.1:4174/. Scripts de QA usan Python Playwright/Chromium148, DPR1, 1440×900 y390×844. Safari/iOS físico y autoría de referencias siguen pendientes. Los snapshots del 25 no se sobrescribieron y ya no describen la composición actual de 04.

---

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
