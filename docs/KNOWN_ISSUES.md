# Known issues — registro de observaciones técnicas

**Este archivo NO es un backlog.** Registra lo que se observó, con su evidencia y sus condiciones.

- Un issue observado **no autoriza** a ningún agente a corregirlo.
- Cada corrección requiere seguir las *change classes* de [AGENTS.md](../AGENTS.md) (aprobación explícita del usuario para las clases 3–5, consulta previa para la clase 2).
- Ninguna entrada está aprobada como tarea. Ninguna resuelve una decisión OPEN de [DECISIONS.md](DECISIONS.md).
- Este registro no elige entre A y B ni valora el mérito creativo de ninguna dirección.

## Origen y mantenimiento

Observaciones de la auditoría del 23 de septiembre de 2026, sobre el commit `9961e26` (el código no ha cambiado desde `5e77ef1`). Las capturas exploratorias y los scripts de verificación se hicieron fuera del repositorio y no se conservaron en él.

- Toda entrada nueva se añade como clase 1 (describir).
- Los issues históricos materialmente relevantes no se borran en silencio: pueden marcarse `RESOLVED` o `SUPERSEDED`, con referencia a la corrección aprobada por el usuario que los respalda. Los duplicados y las afirmaciones incorrectas pueden consolidarse o corregirse, dejando una referencia cuando tenga valor histórico. Los IDs no se reutilizan.
- La existencia de un issue nunca lo convierte en tarea aprobada.
- **Basis** indica cómo se obtuvo el dato: *observed* (visto o medido), *computed* (calculado de archivos o CSS), *read* (leído en código o documentos), *inferred* (deducido, no comprobado).
- **Alcance:** *baseline contract* (afecta a los viewports de referencia de L09), *exploratory* (fuera de ellos), *environment* o *documentation*.

## 1. Environment / reproducibility

**KI-01 · Node local por debajo del requisito de Vite**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `node --version` → v18.20.1; `node_modules/vite/package.json` declara `engines.node` `^20.19.0 || >=22.12.0`; `typeof require('crypto').hash` → `undefined`. README e IMPLEMENTATION_STATUS piden Node 20.19+ / 22.12+. `package.json` no declara `engines` ni hay archivo de versión de Node.
- Condiciones: máquina de la auditoría, Windows 10 Pro, 2026-09-23. Basis: observed (versiones); inferred (que `npm run dev` y `npm run build` fallen; no se ejecutaron).

**KI-02 · `export-standalone.py` no puede leer `index.html` con la codificación por defecto de Windows**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `scripts/export-standalone.py:14` usa `read_text()` sin `encoding`. Con Python 3.10.0 la codificación preferida es cp1252; una lectura equivalente de `index.html` lanza `UnicodeDecodeError` (byte 0x81, posición 3576; corresponde a «Á» en «MÁS CERCA DEL ORIGEN»).
- Condiciones: misma máquina. Basis: observed (la lectura equivalente); el script no se ejecutó.

**KI-03 · La detección de MIME del exportador depende del registro del sistema**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `scripts/export-standalone.py:11`. En la máquina de la auditoría `mimetypes.guess_type` devuelve `None` para `.webp`, `.woff2` y `.ttf`, con lo que caería en `application/octet-stream`. Los HTML entregados incrustan `image/webp`, `font/woff2` y `font/ttf`. Una regeneración en memoria (con UTF-8 explícito) dio texto idéntico y payloads binarios idénticos; solo cambian los prefijos MIME (+100 bytes).
- Condiciones: misma máquina. Basis: observed. No se probó si los data URLs con `octet-stream` se renderizan igual.

**KI-04 · Scripts que escriben sobre archivos del baseline**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `export-standalone.py` escribe en `deliverables/`; `prepare-assets.py` escribe en `public/assets/` y `audit/source/otorongo-extract.webp`; `trace-otorongo.py` escribe `public/assets/otorongo-traced.svg`. Ejecutarlos sobreescribe archivos tracked que L13 conserva como baseline.
- Basis: read. No es un defecto: es un riesgo de uso.

**KI-05 · Repositorio sin remoto**
- Estado: `SUPERSEDED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `git remote -v` vacío; una sola rama (`master`); sin tags. El único respaldo es el `.git` local.
- Condiciones: 2026-09-23. Basis: observed.
- Actualización 2026-09-26: el usuario informa que subió el repositorio a `https://github.com/JuanMosqueraR/web-prototype-artidoro` y que publicó una rama `gh-pages` con el build (ver IMPLEMENTATION_STATUS). El agente no hizo esos push y no verificó el remoto. Ya no es cierto que el `.git` local sea el único respaldo.
- Actualización 2026-09-30: el repositorio es público (`gh repo view`, `visibility: PUBLIC`). La publicación en Pages pasó de la rama `gh-pages` a GitHub Actions; ver IMPLEMENTATION_STATUS y KI-90. `gh-pages` quedó sin actualizar desde el 26 de septiembre.

## 2. Documentation ↔ implementation discrepancies

**KI-10 · `artifact-build/` no aparece en la documentación**
- Estado: `OBSERVED` · Afecta: shared · Alcance: documentation · Tarea: no aprobada
- Evidencia: commit `18b122d` añade `artifact-build/hero-lab-artifact.html`. No figura en README, en la tabla de estructura de IMPLEMENTATION_STATUS, en PROJECT_BRIEF ni en DECISIONS. IMPLEMENTATION_STATUS afirma que la entrega agrega únicamente cinco Markdown y habla de «39 archivos del ZIP». No existe script que lo genere. Tampoco constan `AGENTS.md` y `CLAUDE.md` en esa tabla.
- Basis: read.

**KI-11 · «Rodríguez de Mendoza» ya está visible en el Keyframe A de ambas direcciones**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: `index.html:55` y `index.html:72` (leyenda `origin-caption`, visible desde el inicio). CREATIVE_DIRECTIONS describe el Keyframe B de A como el momento en que «se revela» «Rodríguez de Mendoza». Lo que aparece de nuevo en A es el kicker, la altitud y las notas; en B, solo las notas.
- Condiciones: capturas entregadas en `deliverables/` y lectura del HTML. Basis: observed, read.

**KI-12 · Reglas responsive sin describir en los docs**
- Estado: `OBSERVED` · Afecta: shared · Alcance: documentation · Tarea: no aprobada
- Evidencia: `src/common.css:18` (`min-width:761px` y `max-height:790px`: `min-height` del hero 690 px, `.commerce` a `top:74%`, propuesta de valor a 14 px), `common.css:19`, `peru.css:8` y `lata.css:6` (rango 761–1000 px). Los documentos leídos describen desktop 1440 × 900 y mobile 390 × 844; no mencionan estas reglas ni el `min-height` de 720 px de desktop.
- Basis: read.

## 3. Responsive / layout observations

Las entradas KI-20 a KI-23 vienen de capturas exploratorias de los HTML autónomos de `deliverables/` (idénticos a `src/` en esa fecha, ver *Verification notes*): Chrome headless, pixel ratio 1, sin conservar en el repo. Salvo indicación, solo se capturó el **Keyframe A**. Ninguna redefine la especificación.

**KI-20 · B: el texto «Café con carácter propio.» queda solapado por AMAZONAS**
- Estado: `OBSERVED` · Afecta: B · Alcance: exploratory · Tarea: no aprobada
- Evidencia: solapamiento visible en 1536 × 730, 1366 × 650 y 1920 × 950. En 1440 × 900 (baseline) el texto queda pegado bajo la palabra, sin solapar.
- Causa probable (no aislada): `lata.css:4` coloca `.lata-copy` en `top:51%` del alto del hero, mientras `lata.css:2` dimensiona `.monument` en `vw`; la regla de `common.css:18` no ajusta `.lata-copy`. Basis: observed (solapamiento); read (causa).

**KI-21 · A: la propuesta de valor toca el CTA en 1536 × 730**
- Estado: `OBSERVED` · Afecta: A · Alcance: exploratory · Tarea: no aprobada
- Evidencia: la segunda línea de la propuesta de valor queda pegada a la parte superior del botón, sin espacio visible.
- Condiciones: solo 1536 × 730, Keyframe A. A no se capturó en 1920 × 950 ni en 1366 × 650, y el Keyframe B no se capturó en ningún viewport exploratorio. Basis: observed.

**KI-22 · Mobile: el CTA y lo que le sigue dependen del alto útil**
- Estado: `OBSERVED` · Afecta: shared · Alcance: exploratory · Tarea: no aprobada
- Evidencia: con la barra de laboratorio de 44 px y el `min-height` de 790 px del hero en mobile, en 390 × 664 el CTA queda cortado por el borde inferior y la línea de confianza fuera de vista; en 360 × 740 la leyenda y el aviso provisional quedan bajo el pliegue. En 430 × 932 el contenido queda anclado arriba con espacio vacío debajo. CTA a y = 629 px según medición del baseline; sin la barra de laboratorio estaría 44 px más arriba.
- Condiciones: iframe de ancho exacto, Keyframe A, ambas direcciones. Basis: observed.

**KI-23 · Anchos intermedios fuera de la especificación**
- Estado: `OBSERVED` · Afecta: A y B (uno por caso) · Alcance: exploratory · Tarea: no aprobada
- Evidencia: a 600 × 900 la bolsa tapa «AM» de AMAZONAS en B; a 768 × 1024 el botón «Acercar origen» de A se solapa con la bolsa. Los anchos 360, 390 y 430 no mostraron solapamientos en el Keyframe A de ninguna dirección.
- Basis: observed.

**KI-24 · El layout mezcla unidades**
- Estado: `OBSERVED` · Afecta: shared · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: posiciones en `%` del alto del hero, tamaños en `vw` y, en mobile, posiciones en `px` fijos (`peru.css:10-14`, `lata.css:8-11`). Solo hay mediciones en 1440 × 900 y 390 × 844 (`qa/measurements.json`).
- Basis: read.

**KI-25 · Tipografía de 7–8 px**
- Estado: `OBSERVED` · Afecta: shared · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: `src/*.css` declara `font-size:7px` en 5 lugares y `8px` en 10 (anotaciones, kicker, aviso `PROVISIONAL_ASSET`, altitud en mobile). No se evaluó su legibilidad frente a ningún criterio.
- Basis: computed.

## 4. A/B comparison confounds

Diferencias entre A y B que la documentación no clasifica como parte de la tesis de cada dirección. Son *potential confounds* hasta que el usuario o la documentación las clasifiquen (ver AGENTS.md, A/B comparison integrity); no se corrigen ni se explotan automáticamente. Ver también KI-11.

**KI-30 · Duración del movimiento distinta y sin clasificar**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: A usa 800 ms (`--motion-time` heredado de `.hero`); B usa 650 ms (`lata.css:1`). CREATIVE_DIRECTIONS registra ambos valores y la misma curva, pero no dice si la diferencia de duración forma parte de la tesis de cada dirección. La naturaleza del movimiento (zoom del paisaje frente a desplazamiento y máscara) sí está descrita como parte de cada concepto y no se anota aquí.
- Basis: read.

**KI-32 · Copy distinta entre direcciones**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: propuesta de valor de A: «Cinco orígenes peruanos. Recién tostados, con molienda a tu medida.»; de B: «Cinco orígenes. Tostado semanal y molienda a tu medida.» (`index.html:38` y `index.html:65`). L04 exige el mismo CTA y el mismo mensaje de confianza; no exige igualar la propuesta de valor.
- Basis: read.

**KI-33 · Recursos de la escena oculta**
- Estado: `OBSERVED` · Afecta: shared · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: las dos escenas están en el mismo HTML, sin `loading="lazy"`; la no visible queda con `hidden`. `index.html:29` marca el paisaje de A con `fetchpriority="high"`. Los tamaños de archivo suman ≈ 445 KiB en total (A ≈ 397 KiB y B ≈ 253 KiB si se cargaran por separado, con fuentes y bolsa compartidas).
- Basis: computed (tamaños de archivo); inferred (que el navegador cargue las imágenes de la escena oculta; no se midió con una traza de red).

**KI-35 · Cobertura exploratoria insuficiente para comparar la sensibilidad responsive de A y B**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: exploratory · Tarea: no aprobada
- Evidencia: las capturas exploratorias fueron desiguales: B se capturó en 1536 × 730, 1366 × 650 y 1920 × 950, y A solo en 1536 × 730; el Keyframe B no se capturó en ningún viewport exploratorio. Sin paridad de evidencia no se extrae ninguna conclusión comparativa. KI-20 a KI-23 siguen siendo observaciones independientes de cada dirección.
- Basis: observed.

## 5. Asset quality / provenance gaps

Ya clasificados en [ASSET_AUDIT.md](ASSET_AUDIT.md) y [audit/assets.json](../audit/assets.json) (L12, O02, O03). Aquí solo se añaden observaciones de calidad.

**KI-40 · Otorongo trazado a partir de un recorte muy pequeño**
- Estado: `OBSERVED` · Afecta: B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: fuente de 164 × 195 px (`audit/source/otorongo-curved-tin-detail.png`); en 1440 px de ancho se muestra a ≈ 45 % del ancho (≈ 650 px CSS), es decir ≈ 4× de ampliación. Contornos con aspecto de manchas en las capturas entregadas. `otorongo-traced.svg`: un solo `<path>` con 56 subtrazados, 42 KB.
- Basis: computed, observed.

**KI-41 · Paisaje: fotograma de video de baja resolución con tratamiento oscuro**
- Estado: `OBSERVED` · Afecta: A · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: fotograma de 1280 × 720 de un video 720p (`audit/source/artidoro-landscape-still.jpg`). En el hero se muestra con `object-fit: cover` y `brightness(.69) saturate(.7)` más degradados; al acercar, la ampliación efectiva ronda 1,33× a 1440 × 900. La fuente muestra hileras de café; en la captura del hero el paisaje se lee sobre todo como ladera boscosa. El plano cercano es un recorte de 470 × 440 px del mismo fotograma.
- Basis: computed, observed.

**KI-42 · Resolución de la bolsa en pantallas de alta densidad**
- Estado: `OBSERVED` · Afecta: shared · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: `amazonas-250g.webp` mide 326 × 761 px (la bolsa ocupa ≈ 310 × 747 px en la fuente). Se muestra a 496 px CSS de alto en desktop y 273–277 px en mobile: a pixel ratio 2 en desktop se necesitarían 992 px (≈ 1,3× de ampliación).
- Basis: computed. No se inspeccionó en una pantalla de alta densidad.

**KI-43 · Tres registros solapados de assets**
- Estado: `OBSERVED` · Afecta: shared · Alcance: documentation · Tarea: no aprobada
- Evidencia: `audit/ASSETS.md`, `audit/assets.json` y `docs/ASSET_AUDIT.md` recogen información parcialmente coincidente; `docs/ASSET_AUDIT.md` repite valores estructurados (tamaños, orígenes, preparación) que también constan en `assets.json`. AGENTS.md designa ahora `audit/assets.json` como registro canónico de los hechos estructurados y `docs/ASSET_AUDIT.md` como resumen; los documentos existentes no se han reconciliado con esa regla.
- Basis: read.

## 6. Copy / factual provenance gaps

**KI-50 · «Naranja y melaza» frente a la etiqueta de la bolsa**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: PROJECT_BRIEF, DECISIONS y las anotaciones del HTML dicen «Naranja y melaza» (singular). La etiqueta de la bolsa fotografiada, visible en ambos heroes, dice «NARANJAS Y MELAZAS / ORANGES AND MOLASSES» (`audit/source/amazonas-original.jpg`).
- Basis: observed.

**KI-51 · Altitud sin registro de procedencia**
- Estado: `OBSERVED` · Afecta: A · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: «1 700–1 900 m s. n. m.» (`index.html:50`). La etiqueta de la bolsa muestra «MSNM / MASL 1700 - 1900», pero el dato no figura en `verified_copy` de `audit/assets.json`.
- Basis: observed, read.

**KI-52 · Afirmaciones sin fuente registrada por afirmación**
- Estado: `OBSERVED` · Afecta: A y B · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: «molienda a tu medida» y «Cinco orígenes» aparecen en ambos heroes sin entrada en `verified_copy`. «Rodríguez de Mendoza» no se ve en la etiqueta fotografiada; `verified_copy.product` apunta a la ficha del producto, sin registrar la afirmación concreta. «Tostamos cada semana» y «Cafeterías en Miraflores» sí tienen fuente (`weekly_roast`, `physical_stores`). Ninguna se volvió a comprobar contra el sitio durante la auditoría.
- Basis: read.

## 7. Artifact / export observations

**KI-60 · `artifact-build/`: una tercera copia manual con dependencias frágiles**
- Estado: `OBSERVED` · Afecta: shared · Alcance: documentation · Tarea: no aprobada
- Evidencia: el fragmento elimina `<!doctype>`, `<html>`, `<head>` y `<body>`; un script inicial fija `lang` y `data-direction` (por defecto A). `<meta name="theme-color">`, `<title>` y `<link rel="icon">` quedan como etiquetas sueltas fuera de `<head>`. `src/main.js:18` accede a `meta[name="theme-color"]` sin comprobar `null`; si el anfitrión lo elimina, `setDirection()` lanzaría un `TypeError` tras conmutar las escenas y antes de `updateIndicator()` y de aplicar `?frame=b`. La URL del Artifact publicado no consta en el repo.
- Basis: read. No se probó en el anfitrión del Artifact.
- Actualización 2026-09-26: el Artifact publicado a partir de esta copia (y sus versiones posteriores) se retiró por decisión del usuario; ver KI-61. El archivo se conserva como histórico y figura ahora en la tabla de IMPLEMENTATION_STATUS.

**KI-61 · El video 03 no arrancaba en Chrome/Safari de iPhone dentro del contenedor del Artifact**
- Estado: `OBSERVED` · Afecta: A (03) · Alcance: environment · Tarea: no aprobada
- Evidencia: el usuario reporta que en el Artifact (v3, con la recuperación de `891bbc4`) Chrome y Safari de iPhone mostraban solo el póster con «Reintentar movimiento», y que el reintento no lo resolvía; el mismo Artifact funcionaba en el app de Claude y en la web de escritorio. Una página de diagnóstico publicada como Artifact aparte y abierta en Chrome iOS (CriOS 154, iOS 26.6.2; la batería de la captura sugiere modo de bajo consumo) mostró: origen `*.frame.claudeusercontent.com/_f/<versión>/`; una petición Range a `scene03-mobile.mp4` devolvió 206; `<video src>` con el archivo llegó a `readyState` 4 y avanzó (1,48 s); `fetch → Blob`, `data:` URI y base64 → Blob llegaron a `readyState` 2 pero `play()` fue rechazado con `NotAllowedError`; ningún bloqueo de CSP registrado. Una petición anónima directa con `curl` a un archivo del mismo origen devolvió 403 (2026-09-26). Una v4 con adaptador `fetch → Blob` (solo en el Artifact, no en este repo) aún exigía tocar «Activar movimiento» en Chrome iPhone, según el usuario. Con el build del repo en GitHub Pages el usuario reporta que funciona en Chrome y Safari de iPhone y que el video arranca solo.
- Condiciones: capturas y textos del usuario; sin acceso al host del Artifact ni a sus registros. No se conservan las capturas. La página de diagnóstico se borró el 2026-09-26 y su código no está en el repo. Basis: observed (resultados de la sonda), user-reported (comportamiento por navegador y resultado en Pages). La causa dentro del contenedor no se aisló: el 403 anónimo no demuestra fallo de la petición contextual del reproductor.

**KI-62 · El build de Pages publica assets de `public/` que la home no usa**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: Vite copia todo `public/` a la salida. Siete de los 28 archivos copiados de `public/assets/` no están referenciados por `index.html`, el CSS ni el JS compilados: `barlow-condensed-800.ttf`, `cafetal-provisional.webp`, `cp04-entrada.jpg`, `cp04-mesa.jpg`, `scene03-desktop-start.webp`, `scene03-mobile-start.webp` y `tarata-mesa-home.webp`; suman 2 653 633 bytes de 7 881 945 publicados. `cp04-*` y `cafetal-provisional.webp` son de fases anteriores; los `cp04-*` son `CONCEPTUAL_ASSET`.
- Basis: computed (comparación de nombres de archivo con el texto compilado sobre `581e24f`). No se evaluó el efecto en la carga real, ni si conviene publicarlos.

## 8. QA coverage / method

**KI-73 · Una captura headless estrecha dio un layout recortado en este entorno**
- Estado: `OBSERVED` · Afecta: shared · Alcance: exploratory · Tarea: no aprobada
- Evidencia: con `--window-size=390,844` en Chrome headless, el selector superior y la palabra «AMAZONAS» aparecieron recortados, como si el diseño se hubiera calculado más ancho que la captura. Un iframe de ancho exacto (como hace `qa.html`) renderizó correctamente. La hipótesis de un ancho mínimo de ventana de unos 500 px es una deducción específica de este entorno y de esta herramienta; no se midió y no debe tomarse como comportamiento general de Chromium.
- Condiciones: Chrome de escritorio en Windows 10, modo headless, 2026-09-23. Basis: observed (recorte); inferred (causa). Lo metodológico que se conserva: comprobar siempre que el viewport capturado es el previsto.

## 9. Escena 02 (A → 02)

Observaciones del 24 de septiembre de 2026 al implementar la escena 02 (ver [qa/2026-09-24-origin-02/QA-origin-02.md](../qa/2026-09-24-origin-02/QA-origin-02.md)). Chrome 153 headless, iframe de ancho exacto, píxel ratio 1, servidor estático temporal (no Vite). Ninguna es tarea aprobada.

**KI-80 · Con barra de desplazamiento clásica, el Hero A cambia de geometría**
- Estado: `OBSERVED` · Afecta: A · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: antes de 02, A medía exactamente el alto del viewport (sin scroll vertical). Con 02 el documento es más largo. Con barra clásica de 15 px (`Emulation.setScrollbarsHidden=false`), A pasa a 1425 px de ancho útil en 1440 × 900: bolsa x 962.41 (antes 973.66), CTA x 85.50 (antes 86.39). En 390 × 844 con barra clásica el ancho útil es 375 y el CTA mide 331 px (antes 346). Con barras superpuestas/ocultas (comportamiento del baseline y de móviles) no hay cambio. B no cambia (su documento sigue midiendo un viewport).
- Condiciones: 1440 × 900 y 390 × 844, motion on, hero inicial. No se ocultaron barras ni se cambió CSS compartido. Datos: `qa/2026-09-24-origin-02/data/exploratory-classic-scrollbar.json`. Basis: observed.

**KI-81 · `export-standalone.py` no incorpora la escena 02 completa**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia (por lectura del script, no ejecutado): lee el `index.html` actual, así que incluiría el markup de 02. Su lista de CSS es fija (`common.css`, `peru.css`, `lata.css`) y elimina todos los `<link rel="stylesheet">`, de modo que `origin.css` se descartaría sin embeberse; solo embebe `main.js`, y el `<script type="module" src="/src/origin.js">` quedaría como referencia externa sin resolver en `file://`. Basis: read.

**KI-82 · Entregables y `artifact-build/` no representan A → 02**
- Estado: `OBSERVED` · Afecta: shared · Alcance: documentation · Tarea: no aprobada
- Evidencia: `deliverables/*.html` y `artifact-build/hero-lab-artifact.html` no contienen 02. Las capturas y mediciones históricas del hero siguen siendo evidencia válida para el hero. Aparte, los HTML y capturas de B (baseline `59320ee`) son anteriores al commit `e5a0b9e` (`lata.css`); esa desactualización es previa a 02 (a 1440 × 900 y 390 × 844 las mediciones de B no cambiaron respecto a `qa/measurements.json`). Basis: read, observed.

**KI-83 · En A la bolsa de Cajamarca se pide al cargar**
- Estado: `OBSERVED` · Afecta: A · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: `cajamarca-250g.webp` (≈ 93 KiB) lleva `loading="lazy"`, pero en 1440 × 900 y 390 × 844 queda dentro de la distancia de carga diferida de Chrome y se solicita al abrir A. Abriendo B directamente, o pasando de A a B, no se solicita ni se genera ninguna petición nueva. Registro del servidor en `qa/2026-09-24-origin-02/data/network-*.json`. Basis: observed.

**KI-84 · Texto pequeño y filas informativas en 02**
- Estado: `OBSERVED` · Afecta: A (02) · Alcance: baseline contract · Tarea: no aprobada
- Evidencia: la especificación de 02 fija Chivo 10–13 px en etiquetas y notas (mobile: 10, 12; desktop: 11–14). Villa Rica, Cusco y Puno usan el mismo tratamiento tipográfico que las filas seleccionables y solo se distinguen por el cursor por defecto y la ausencia de foco; no se evaluó si un usuario las entiende como no interactivas. Basis: read, observed.

## 10. GitHub Pages / CI (30 de septiembre de 2026)

**KI-90 · El ambiente `github-pages` de Actions no permitía desplegar `master` por defecto**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: al cambiar Settings → Pages → Source a «GitHub Actions», GitHub crea un ambiente `github-pages` con una regla de «Deployment branches and tags». El primer `push` a `master` con `.github/workflows/pages.yml` completó el job `build` pero el job `deploy` falló: *"Branch 'master' is not allowed to deploy to github-pages due to environment protection rules."* Se corrigió en Settings → Environments → `github-pages` → *Deployment branches and tags* → agregar `master` a la lista (`gh-pages` ya figuraba). Tras el ajuste, un *re-run* del mismo job (sin nuevo commit) terminó en verde.
- Condiciones: primera activación de Pages vía Actions en este repositorio, 2026-09-30. No se determinó si el valor por defecto depende de la visibilidad del repo (es público) o de otro ajuste de la cuenta; no se probó en otro repositorio. Basis: observed.

**KI-91 · Procesos `esbuild.exe` huérfanos bloquean `npm ci` en Windows**
- Estado: `OBSERVED` · Afecta: shared · Alcance: environment · Tarea: no aprobada
- Evidencia: `npm ci` falló con `EPERM: operation not permitted, unlink '...@rollup\rollup-win32-x64-msvc\rollup.win32-x64-msvc.node'`, y dejó `node_modules` a medio borrar (4 carpetas en vez del árbol completo). Un `Remove-Item -Recurse -Force node_modules` posterior falló igual, ahora sobre `@esbuild\win32-x64\esbuild.exe`, con `UnauthorizedAccessException`. `Get-CimInstance Win32_Process -Filter "Name='esbuild.exe'"` mostró dos procesos ejecutando el `esbuild.exe` de este proyecto, hijos de dos procesos `node.exe` del Node 22 aislado con fecha de inicio de sesiones anteriores (26 y 29 de septiembre) — service processes de esbuild que Vite deja corriendo para acelerar builds repetidos, y que no terminaron cuando el comando `vite build` que los originó salió. Terminarlos (`Stop-Process -Force`) liberó los archivos; `Remove-Item` y `npm ci` funcionaron después sin cambios adicionales.
- Condiciones: Windows 10, varias invocaciones de `node_modules/vite/bin/vite.js build` en la misma sesión a lo largo de varios días. Basis: observed. No se determinó por qué esos procesos no terminaron con su comando padre (posible interacción con el entorno donde se ejecutó cada build), ni si ocurre también fuera de esa forma de invocar Vite.

## Verification notes

No son issues; se conservan para no repetir trabajo. Cada nota deja de valer cuando cambie lo que verifica.

- **Entregables frente a `src/`.** El 2026-09-23, sobre `9961e26`, una regeneración del export en memoria dio texto (HTML, CSS y JS) idéntico al de `deliverables/A-peru-en-profundidad.html` y `B-fuera-de-la-lata.html`, con payloads binarios también idénticos. Los dos archivos difieren entre sí solo en 5 líneas de atributos de dirección inicial. Vale mientras no cambien `src/` ni `index.html`.
- **Mediciones frente al CSS.** Las posiciones de `qa/measurements.json` son coherentes con el CSS actual.
- **Movimiento en la máquina de la auditoría.** Las animaciones de Windows estaban activas, así que `prefers-reduced-motion` no aplicaba ahí; un revisor con esa preferencia activa vería el movimiento eliminado por CSS (documentado en IMPLEMENTATION_STATUS).
