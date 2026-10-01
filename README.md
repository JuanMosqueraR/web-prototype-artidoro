# Artidoro — demo de la home 01–05

**Actualización — 1 de octubre de 2026 (L29):** revisión de la home con siete correcciones, limpieza de textos (sin numeración de secciones) y 04 «Nos vemos en Miraflores» con las dos cafeterías y su horario oficial. Detalle: [docs/HOME_AUDIT_2026_09_30.md](docs/HOME_AUDIT_2026_09_30.md#l29) · evidencia: [qa/2026-10-01-revision](qa/2026-10-01-revision/README.md). Después, nuevo orden (P4): tienda, confianza y reseñas antes de las cafeterías ([qa/2026-10-01-orden](qa/2026-10-01-orden/README.md)).

**Actualización — 1 de octubre de 2026 (L28):** la home de A estrena el hero «Del cafetal a tu bolsa» (video generado que avanza con el scroll, 24 fps constantes, con la misma toma como secuencia de imágenes AVIF/WebP de respaldo si el video no está listo), la sección 03 «De la bolsa a tu taza» (cuatro imágenes con cruces ligados al scroll, bolsa real a escala en el cierre), la franja «Elige tu molienda», «Precio justo al caficultor» en la confianza de 05, titulares que suben línea a línea, scroll con inercia solo con rueda en desktop, un swipe de 02 reescrito y etiquetas para compartir el enlace (título «Demo»). El usuario lo probó en un iPhone físico (hero, 03 y swipe). B y las PDP no cambian.
- Detalle y límites: [docs/HOME_AUDIT_2026_09_30.md](docs/HOME_AUDIT_2026_09_30.md#l28) · decisiones L28 y sus ocho complementos: [docs/DECISIONS.md](docs/DECISIONS.md) · evidencia: [qa/2026-09-30-l28](qa/2026-09-30-l28/README.md) (107 controles en Chromium; sin Safari/iOS instrumental).
- **Publicación (1 de octubre, tras L29):** `master` va 9 commits por delante de `origin/master` (`cf45646`, L29 publicada en Pages); L30 y L31 (precios al día y PDP renovadas) aún no están publicadas. Un `git push` a `master` dispara el despliegue. Rendimiento: no se vuelve a medir hasta la fase de Shopify (L30).
- Regenerar assets de L28 (requieren ffmpeg vía `imageio-ffmpeg` y Pillow con AVIF): `python scripts/prepare-hero-video.py` (`--video-only` para solo video y pósters), `python scripts/prepare-cup03.py`, `python scripts/prepare-og-image.py <url del build servido>`; la generación con APIMart está en `scripts/produce-hero.cjs` y cuesta dinero.
- Las menciones de más abajo al video de 03, a «Reintentar movimiento» o al hero con Acercar/Alejar origen están **superadas** para A.

**Actualización — 29 de septiembre:**
- La tarjeta del pack en 05 y la ficha de El Ahorrador muestran el precio normal tachado S/ 330.00 y «Ahorras S/ 50» (L23). QA: [qa/2026-09-29-ahorro](qa/2026-09-29-ahorro/README.md).
- El usuario confirmó la iteración anterior del pack en un iPhone físico y la publicó en GitHub Pages. Pages **no** incluye todavía el cambio del ahorro.
- Presentación para la reunión: [deliverables/presentacion-artidoro.html](deliverables/presentacion-artidoro.html); la copia publicable se genera con `python scripts/build-presentation-artifact.py`.
- Propuesta en borrador: [docs/PROPUESTA_ETAPA1.md](docs/PROPUESTA_ETAPA1.md).
- Menciones de más abajo a una prueba de iPhone pendiente o a que no hubo publicación: superadas.

**Estado actual — integrado en `master` (28 de septiembre):** selector 02, catálogo y ambas PDP, incluido El Ahorrador. Integración local por fast-forward hasta `a5512e2`, sin push ni nueva publicación. [Handoff para retomar](docs/HANDOFF.md) · [Prompt de presentación y propuesta para Claude](docs/CLAUDE_PRESENTACION_PROMPT.md).

**Revisión actual — El Ahorrador:** [demo, capturas y validación](docs/AHORRADOR_REVIEW.md). Acceso al pack desde 01/02/Tienda, protagonista en 05 y ficha con tres orígenes configurables: `http://127.0.0.1:4175/#producto-ahorrador`. Checkpoint previo `87ea725`; cambios versionados e integrados por petición del usuario. La prueba física de iPhone de esta última iteración sigue pendiente. Las revisiones inferiores son históricas.

**Revisión anterior — catálogo y PDP (28 de septiembre):** [entrega y capturas directas](docs/CATALOG_PDP_REVIEW.md). Rama `feat/catalogo-pdp` desde `38a209f`, versionada por petición del usuario tras confirmar que se ve bien en iPhone; sin merge ni publicación desde esta revisión. Home `http://127.0.0.1:4175/`; ficha Amazonas `http://127.0.0.1:4175/#producto-amazonas`. Incluye 05 renovado, categorías, reseñas, FAQ y una PDP con doce variantes reales y continuación a la tienda oficial. Las revisiones de abajo son históricas. La propuesta no implementa un carrito o checkout propio.

**Revisión local de 02 (26 de septiembre):** [selector horizontal — entrega y QA](docs/ORIGIN_SELECTOR_REVIEW.md) · [antes/después y secuencia](deliverables/origin-selector-review.html). Rama `feat/origin-selector` (checkpoint `7b122b9`), versionada por petición del usuario y sin merge a `master`. Preview de esta sesión: `http://127.0.0.1:4175/#origin-scene`. La publicación en Pages la hace el usuario con `scripts/build-pages.py`; este README no registra si ya ocurrió (hasta entonces Pages conserva el selector anterior).

**Publicación de revisión:** GitHub Pages ([cómo publicar](#publicar-en-github-pages)). El Artifact que se había publicado se retiró el 26 de septiembre de 2026; ver [recuperación de video y resultado](docs/VIDEO_RECOVERY.md).

**Actualización del 26 de septiembre:** [Tarata editorial — entrega y QA](docs/TARATA_REVIEW.md) · [Galería actual](deliverables/tarata-review.html). Checkpoint previo `3830028`; revisión sin commit final. La home sigue en `http://127.0.0.1:4174/`.

Estado actual, 25 de septiembre de 2026: dirección A «Perú, en profundidad», con cinco orígenes, momento cinematográfico 03, pausa breve en Tarata y cierre comercial. Checkpoint recuperable `0a1da04`; esta fase queda sin commit final para revisión.

- [Galería visual, videos y capturas](deliverables/home-review.html)
- [Entrega y límites](docs/HOME_REVIEW.md)
- [Implementación actual](docs/IMPLEMENTATION_STATUS.md)
- [QA y condiciones](qa/2026-09-25-home/README.md)

## Ejecutar la demo actual

Vite 7.1.3 requiere Node 20.19+ o 22.12+. En esta máquina se usó Node 22.23.1 aislado, sin actualizar el Node global:

```powershell
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js build
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js preview --host 127.0.0.1 --port 4174
```

Home: `http://127.0.0.1:4174/`. Hero B conservado: `/b/`. Con un Node compatible, también funcionan `npm run build` y `npm run preview -- --host 127.0.0.1 --port 4174`. Las dependencias ya estaban instaladas en el entorno revisado.

03 tiene video horizontal/vertical diferido, poster y reduced motion. Compra y catálogo enlazan a la tienda oficial; no hay checkout propio ni integración Shopify. La página `deliverables/home-review.html` se puede abrir como archivo local para revisar capturas y clips; la home interactiva requiere el servidor Vite.

## Publicar en GitHub Pages

Desde el 30 de septiembre de 2026 la publicación es automática: `.github/workflows/pages.yml` compila con Vite (Node 22 del runner) y despliega en cada push a `master`. Basta con:

```powershell
git push origin master
```

y revisar la pestaña **Actions** del repo (job `deploy`) hasta que quede en verde, un par de minutos. La URL es `https://juanmosquerar.github.io/web-prototype-artidoro/`, con la barra final.

**Configuración de Pages en GitHub (ya hecha, una sola vez):** Settings → Pages → Source → `GitHub Actions`. La primera vez el ambiente `github-pages` que crea GitHub puede traer una regla de protección que no incluya `master`; si el job `deploy` falla con *"Branch 'master' is not allowed to deploy..."*, se corrige en Settings → Environments → `github-pages` → *Deployment branches and tags* → agregar `master` (ver KI-90). No hace falta repetirlo en despliegues siguientes.

El workflow corre el mismo `scripts/build-pages.py` que compila localmente: hace relativas las rutas `/assets/…` (incluidos los atributos `data-*` que lee el JS) y, si existen, los enlaces `/b/` y `/?motion=off` del pie los cambia por `#b` y `?motion=off` — son opcionales; si la página no los tiene, el script sigue igual (ver `docs/IMPLEMENTATION_STATUS.md`). `#a`, `#b` y `?motion=off` siguen funcionando siempre vía `src/main.js`, tengan o no un enlace visible que apunte a ellos. No existen rutas `/a/` ni `/b/` en Pages. El build publica también los assets de `public/` que la home no usa (KI-62).

**Build local, para previsualizar sin publicar** (no es necesario para desplegar):

```powershell
python scripts/build-pages.py --node 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' --out 'dist/pages'
```

Con el Node 18 global el script se detiene con un aviso; usa `--node` con Node 20.19+ o 22.12+. `--branch-dir` (crea o actualiza un commit `gh-pages` en un repositorio local fuera de este) sigue disponible pero ya no hace falta: la rama `gh-pages` del remoto dejó de ser la fuente de Pages y no se actualiza sola.

**Las instrucciones, HTML autónomos y capturas del Hero Lab de abajo son históricos.** No representan esta home y su exportador no se ejecutó ni actualizó para incluir el video. No regenerar los baselines anteriores para revisar esta fase.

---

## Snapshot histórico del Hero Lab

# Artidoro — Hero Lab

Checkpoint de comparación. Solo dos heroes, con el mismo café Amazonas 250 g (Rodríguez de Mendoza; naranja y melaza). Sin home, Shopify, video, WebGL ni imágenes generadas mediante IA.

## Abrir sin instalar

Descargar y abrir cualquiera de estos archivos en el navegador:

- `deliverables/A-peru-en-profundidad.html`
- `deliverables/B-fuera-de-la-lata.html`

Ambos incluyen todos los assets y el selector A/B. No necesitan conexión para visualizarse. El CTA abre la ficha real de café Amazonas en una pestaña nueva; no simula un checkout.

## Ejecutar el proyecto

Node 20.19+ o 22.12+ y npm. Desde esta carpeta:

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4173
```

- A: `http://localhost:4173/a/`
- B: `http://localhost:4173/b/`

El selector de laboratorio queda fuera de la composición. Cada dirección conserva su estado al alternar. La casilla **Sin motion** elimina las transiciones; también se respeta la preferencia del sistema. Las interacciones son reversibles y no requieren scroll ni espera.

## Archivos

- `src/peru.css`: composición A y acercamiento del cafetal.
- `src/lata.css`: composición B y despliegue del otorongo.
- `src/common.css`: tipografía, producto, CTA y controles compartidos.
- `src/main.js`: selector, revelado y preferencia de movimiento.
- `src/origin.css` y `src/origin.js`: escena 02 “Encontrar tu origen” (solo con A).
- `audit/ASSETS.md` y `audit/assets.json`: clasificación, fuentes y gaps.
- `qa/QA.md` y `qa/measurements.json`: comprobaciones del checkpoint.
- `deliverables/*.jpg`: capturas finales.

La foto de cafetal y el otorongo se marcan **PROVISIONAL_ASSET**. La primera procede de la marca pero carece de atribución geográfica verificada. El segundo es un trazado determinista de una extracción pequeña del packaging; no es el arte maestro original.

## Construir / regenerar entregables

```sh
npm run build
python3 scripts/export-standalone.py
```

Las exportaciones HTML son archivos de revisión con recursos embebidos. El proyecto Vite sirve los recursos por separado y comparte la misma foto de producto entre variantes. No hay arquitectura de tienda ni integración de compra.

Las fuentes originales de fotografía usadas para la preparación están en `audit/source/`. Los scripts de preparación son utilidades opcionales de auditoría (Pillow y NumPy), no dependencias de ejecución del lab.
