# Auditoría y corrección de la home 01–05 — 30 de septiembre de 2026

Autorización L24 sobre checkpoint `0b33580`, sin commit final de este cambio. Alcance: dirección A únicamente; B, PDPs y assets quedan fuera. Plan aprobado íntegro salvo dos opcionales explícitamente no aprobados (ahorro visible en el hero, estrellas en reseñas).

## Qué cambió

**Batch A — bugs, responsive, higiene de contenido.**

- **Iconografía (todas las secciones de A).** Los glifos de texto `↗`/`⌄` se sustituyen por iconos SVG vía `mask` y `currentColor` (`.icon-ext`, `.icon-arrow`, `.icon-chevron` en `common.css`). Ninguna fuente local (Chivo, Barlow) contiene esos glifos; en iOS, `↗` se renderiza como emoji de color en vez de flecha de texto. Se distingue destino externo (tienda oficial, Maps) de destino interno (anclas de la propia demo, incluidas las que la interceptación de `catalog.js` convierte en navegación interna aunque el `href` estático apunte a la tienda). B y las dos PDP conservan sus glifos originales sin cambios.
- **Solape hero mobile.** La anotación de origen y el botón «Alejar origen» dejaban 4 px de solape en 390 px de ancho (medido: notas terminaban en y=533, botón empezaba en y=529). Se reposicionó el botón (holgura existente antes de `.commerce`) y se recortaron márgenes de la anotación; ahora dejan ≥12 px de separación en 390×844, 390×664 y 360×740.
- **CTA bajo el pliegue real.** A 390×664 (área visible real de un iPhone con barras, según la captura del usuario), «Comprar Amazonas» terminaba en y=691. Se recompuso la pila del hero mobile (aprovechando el espacio liberado al quitar la fila «01 / PERÚ, EN PROFUNDIDAD») para que el CTA termine en y=639.
- **Fila del pack en el hero.** De dos líneas apiladas («El Ahorrador · 3 kg / S/280» y «Armar mi pack →» por separado) a una sola fila «Pack El Ahorrador · 3 × 1 kg — S/280 →», con tipografía ≥13 px.
- **Etiquetas de laboratorio.** Se retira la fila «01 / PERÚ, EN PROFUNDIDAD · AMAZONAS, PERÚ» del hero y el enlace público «Ver dirección B del laboratorio» del pie (B sigue accesible por `/b/` o `#b`, solo deja de anunciarse en la demo pública).
- **Avisos de procedencia (D1-a).** Mismo lugar, mismo aviso, texto humano sin token de laboratorio: «Paisaje referencial · ubicación por confirmar» (hero), «Escena conceptual generada para esta demo.» (03), «Fotografías de referencia · autoría por confirmar.» (Tarata). La divulgación completa se conserva íntegra en «Acerca de esta demo» del pie. Ninguna clasificación de `audit/assets.json` cambia.
- **Suelo tipográfico.** Por precisión del usuario: 11 px queda para labels muy secundarios (kickers, créditos de procedencia, «EN TAZA»); el texto informativo (confianza, datos de origen, captions, atribuciones, pistas de 03, enlaces de fuente, fila del footer) sube a 12–14 px. Aplicado en `common.css`, `home.css`, `peru.css`, `origin.css`, `sensory.css`, `catalog.css`, `ahorrador.css`, siempre bajo selectores propios de A (`html[data-direction="a"]`, `.hero-peru`, o clases exclusivas de las secciones `home-only`) para no tocar B.
- **Touch targets.** Se llevaron a ≥44 px el CTA del header mobile, «Llévalo a tu taza», los enlaces «Comprar pack/miel» de 05, el control «Sin movimiento»/«Activar movimiento» de 03, el resumen «Acerca de esta demo», el enlace «Sigue el origen» y el logo/«Tarata» del header. Quedan dos excepciones aceptadas (enlace dentro de una frase; bolsas lejanas del carrusel sin `pointer-events`), documentadas en el QA.
- **Tablet exploratorio (761–1000 px).** El botón y la anotación del hero quedaban detrás de la bolsa (por ejemplo, a 768 px, el botón invadía 76 px del área de la bolsa). Se reubicó la bolsa (más pequeña y a la derecha) y el botón/anotación entre el bloque de texto y la bolsa, sin solape en 768, 900 y 1000 px.

**Batch B — refactor acotado de 05.**

- **Cola de 05.** Se elimina la fila huérfana «¿Prefieres una sola bolsa? · Elige entre cinco orígenes ↑» y se sustituye por una tarjeta «Café de origen» con el mismo formato que El Explorador y Miel de abeja (imagen, etiqueta, precio S/39.90, enlace «Elegir origen» a `#origin-scene`), usando el asset ya existente `amazonas-250g.webp`. La fila de complementos pasa de 2 a 3 columnas iguales desde 1024 px (2 columnas se conservan en la franja 761–1023, con la tercera tarjeta pasando a su propia fila).
- **Reseñas.** Se añade «Reseñas de clientes en la tienda oficial» antes de las citas (antes, la fuente solo se indicaba en un enlace al final). El nombre del producto de cada reseña («Café Origen Amazonas», «Pack «El Ahorrador» 3 kg») pasa de texto plano a enlace: abre la PDP interna correspondiente (`#producto-amazonas` / `#producto-ahorrador`) reutilizando la interceptación ya existente de `catalog.js` (`[data-pdp]` / `[data-pack-pdp]`), sin JS nuevo. En mobile, las reseñas pasan de 2 columnas a 1, con la cita a 16 px (antes 12 px).

<a id="l28"></a>
## Iteración L28 (mismo día): hero «Del cafetal a tu bolsa», 03 «De la bolsa a tu taza» y mejoras generales

El usuario pidió un hero más impactante a partir de referencias externas (enlazu.com, scrolltide.co), aprobó el concepto sobre un boceto fuera del repo y decidió que el momento wow pase del 03 al hero (literal en [DECISIONS L28](DECISIONS.md)).

- **Hero.** Video generado de 10 s (en mobile, la misma toma como secuencia de 121 imágenes AVIF a 12 fps en canvas: tras la prueba en iPhone el video no se preparaba en Safari/Chrome de iOS) que avanza con el scroll dentro de un escenario fijo (280 svh desktop, 250 svh mobile), con avance amortiguado: vista aérea → cerezas que se vuelven granos → cascada; la bolsa real sube al final. Tres pasos de texto verificado, índice 01–03 en desktop y línea compacta por paso en mobile. Titular, precio, CTA, confianza y pack visibles durante todo el recorrido (también en 390 × 664). Header transparente sobre el hero. Póster = primer fotograma (1280 × 714, 28 KB); video pedido tras la carga (1,60 MB desktop, 1,34 MB mobile, dentro del límite de 2,5/1,5 MB).
- **03.** Cuatro imágenes fijas generadas; el scroll dispara cada paso (moler, preparar, servir) y la transición dura un tiempo fijo, para que un deslizamiento rápido no la salte (observación del usuario sobre el boceto). Final en bodegón con vaso de doble pared y la bolsa real a escala. Se conserva el id `#sensory-scene` por los enlaces existentes.
- **Moliendas.** Franja informativa con cuatro iconos propios y texto de las preguntas frecuentes oficiales; el selector interactivo se reserva para la PDP.
- **05.** «Precio justo al caficultor» en la franja de confianza.
- **Séptima ronda (cierre).** El swipe de 02 funciona en iOS según el usuario. Revisión de Forno: se adoptan la estructura de video GOP 4 sin fotogramas B (picos de seek ~30–45 % menores en Chromium; el usuario debe revalidar el hero) y las etiquetas de previsualización (Open Graph/Twitter, título «Demo», imagen 1200 × 630 generada con `scripts/prepare-og-image.py`); no se adoptan la carga como `blob` ni el todo-intra.
- **Sexta ronda (iPhone).** El swipe de 02 era igual en la versión anterior a L28 (no es una regresión). Comparado con Forno: gesto reescrito (listeners en la ventana, sin captura de puntero, la tira sigue al dedo, confirma por distancia o velocidad y también tras `pointercancel`); en Chromium el flick corto pasa de 0/8 a 8/8 y el gesto cancelado por el sistema de 0/8 a 8/8. Por confirmar en el iPhone.
- **Quinta ronda (iPhone).** Filmación de las transiciones de 03: se eliminan la superposición de textos y la bolsa que flotaba al subir, y se suavizan barridos y apertura circular. Batería con el MCP de Playwright (26 posiciones de reposo, vaivenes, deslizamientos bruscos, scroll continuo, recorrido aleatorio, PDP, anclas, giro, recarga) sin más bugs. Swipe de 02: no reproducible en Chromium (24/24 en la versión anterior y en la nueva); la versión previa a L28 se sirve en `/old/` para compararla en el iPhone.
- **Cuarta ronda (iPhone).** Hero aprobado por el usuario. Bug de la 03 localizado con el MCP de Playwright: la cola de esperas por fotograma mostraba el último paso después de salir de la sección a ~1 000 px/s; ahora el último paso queda completo con la sección en pantalla 3,0 s (500 px/s), 1,75 s (800 px/s) y 1,15 s (1 000 px/s). Limpieza de ruido y afinado del hero antes de codificar. El «hueco inferior» de Chrome iOS era el degradado oscuro del hero, no una franja sin contenido.
- **Tercera ronda (iPhone).** El hero vuelve a usar video en mobile (24 fps constantes y escala 12288 como el video de la 03 que sí funcionaba; 3,2 MB, límite subido a 3,5 MB) con la secuencia solo como respaldo; la 03 retiene 2,3 s cada fotograma intermedio; diagnóstico de viewport y de video en una página aparte para el iPhone.
- **Segunda corrección tras iPhone (versión publicada).** Secuencia a 12 fps desde los originales en AVIF (más nítida; el techo sigue siendo el 720p de los clips), viewport alto para evitar la franja inferior al ocultarse las barras del navegador, espera mínima de 1,7 s por paso en 03. El swipe del carrusel de 02 no se reprodujo en Chromium: pendiente de diagnóstico en el dispositivo.
- **Corrección tras iPhone.** Se retira la barra de compra fija (doble CTA con el header); 03 reparte sus pasos a 20/40/60 % en 300/280 svh; en mobile el cierre de 03 queda debajo de la bolsa.
- **General.** Títulos que suben línea a línea una vez; scroll con inercia solo con rueda en desktop (módulo propio, sin dependencias); grano de película en ambas escenas.
- **Sin movimiento** (sistema, «Reducir movimiento», Save-Data): sin fijación ni video; composiciones finales estáticas; títulos visibles.

**Validación.** [qa/2026-09-30-l28](../qa/2026-09-30-l28/README.md): 107/107 en Chromium DPR 1 sobre build de producción (1440 × 900, 390 × 844, 390 × 664, 768 × 1024; movimiento activo, «Reducir movimiento» y `prefers-reduced-motion`), PDPs abiertas desde hero y pack, B sin cambios frente a `qa/2026-09-29-ahorro/after/`. Rendimiento de laboratorio en local (mediana de 3): LCP mobile 2,02 s frente a 2,09 s del build anterior a L28 en las mismas condiciones; el video pesa 3,2–3,5 MB y se pide después de la carga; el video (desktop) y la secuencia (mobile) se piden después de la carga.

**No cubierto.** Safari/iOS instrumental (la corrección se hizo tras la prueba física del usuario en Chrome de iPhone y debe confirmarse allí); Firefox; datos de campo; lectores de pantalla más allá de la estructura. La medición de la home publicada y la presentación en `deliverables/` quedan desactualizadas tras el próximo despliegue.

## Iteración L27 (mismo día): cierre gráfico de 05

El tramo final pasa de una franja plana a cuatro bandas: confianza con iconos («Tostamos cada semana», «Cafeterías en Miraflores», «Envíos a Lima y provincias»), reseñas en banda oscura con estrellas y comilla, FAQ en dos columnas con controles circulares y mosaicos «Sigue explorando» con producto. Cuerpo ≥ 19 px en citas y ≥ 15 px en la FAQ; una sola mención de fuente. El mosaico de Nanolotes usa una foto oficial de la colección (`nanolote-tin`, registrada en `audit/assets.json`). Evidencia: [qa/2026-09-30-cierre-05](../qa/2026-09-30-cierre-05/checks.json) (49/49, B 0 px). FAQ de las PDP sin cambios.

## Rendimiento medido (mismo día)

Tras la publicación en Pages, medición de laboratorio en Chromium (3 corridas, mediana): LCP 1,67 s en mobile con Slow 4G y CPU 4×, 0,21 s en desktop, CLS 0, sin peticiones fallidas; el arranque en frío tarda ~4 s. Cambia el estado de rendimiento del informe CRO de «no medido» a «medido en laboratorio, sin datos de campo». [Método, resultados y límites](../qa/2026-09-30-performance/README.md).

## Iteración L25 (mismo día)

Tras probar en iPhone físico, con autorización L25: el hero A deja de tener botón Acercar/Alejar; la aproximación y el detalle de origen se muestran solos y con texto puntual; el pack del hero es un botón secundario con borde; Travel Line pasa a tarjeta completa en 05 (mobile incluido); scroll suave solo donde no cruza 03 (salto instantáneo con fundido breve si lo cruza); el control de movimiento se reduce a uno, dentro de «Acerca de esta demo». Evidencia: [qa/2026-09-30-hero-auto](../qa/2026-09-30-hero-auto/checks.json) (51/51, B 0 px). El script de `qa/2026-09-30-home-audit/verify.py` hacía clic en el botón retirado y ya no aplica a A; su evidencia queda como histórico. Entorno de esta iteración: `node_modules/vite` del repo estaba incompleto; el build de verificación usó Vite 6.4.3 de otro proyecto local y Node 22.23.1, sin modificar el repo (Vite 7.1.3 no verificado en esta iteración).

## No se tocó

02 (carrusel, gestos, estados, compra) salvo tamaños mínimos de texto; 03 (video, scroll, sticky, reduced motion, recuperación) salvo tamaños e icono; 04 (composición editorial L19); las tarjetas de El Ahorrador (con su ahorro L23) y Travel Line; la FAQ; ningún archivo de `public/assets/`, `audit/source/` ni los scripts de preparación; la dirección B completa; las dos PDP (Amazonas, El Ahorrador) más allá de dos enlaces nuevos que abren PDPs ya existentes.

## Validación

Build Vite 7.1.3 con Node aislado 22.23.1, Python 3.10, Chromium 148.0.7778.96, DPR 1. `qa/2026-09-30-home-audit/verify.py` → **39/39**: separación anotación/botón ≥12 px, CTA dentro del viewport en 390×664, cero texto <11 px, cero desbordamiento horizontal, iconos con tamaño no nulo, cero errores de página, B sin diferencia de píxeles en los 8 estados de regresión (desktop/mobile × motion/reducido × inicial/expandido), y barrido funcional (nueva tarjeta decodifica, selector de 02 recorre los cinco orígenes, enlaces de reseña abren sus PDP y el retorno funciona). Detalle, excepciones aceptadas y capturas: [QA](../qa/2026-09-30-home-audit/README.md).

## Pendiente / no cubierto

Confirmación física en iOS del icono corregido (el hallazgo original vino de una captura de iPhone; Chromium no reproduce el bug de renderizado de emoji, así que la corrección se verifica por ausencia de la fuente del problema — ningún glifo de texto en las fuentes locales — no visualmente en el dispositivo). Android, lectores de pantalla, Core Web Vitals de campo o en GitHub Pages. Los gaps de paisaje, autoría de Tarata y naturaleza generada de 03 siguen abiertos (`docs/ASSET_AUDIT.md`); no se resolvió ninguna decisión OPEN. No se implementaron los dos opcionales no aprobados por el usuario (ahorro visible en el hero, estrellas en reseñas). Pages no se republicó.

**Snapshots desactualizados por este cambio (no regenerados, requieren tu aprobación):** `deliverables/presentacion-artidoro.html` (usa capturas de `qa/2026-09-29-ahorro/after/`, que muestran el hero y 05 previos a esta revisión) y la propia evidencia de `qa/2026-09-29-ahorro/after/` para dirección A (no se sobrescribe; sigue siendo válida como historial y como línea base de comparación de B).

## Archivos

- Implementación: `index.html`, `src/common.css`, `src/home.css`, `src/peru.css`, `src/origin.css`, `src/sensory.css`, `src/catalog.css`, `src/ahorrador.css`.
- QA: `qa/2026-09-30-home-audit/` (script, `checks.json`, capturas).
- Documentación: este informe, `docs/ASSET_AUDIT.md` (nota de cambio de copy), `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`, autorización en `docs/DECISIONS.md` (L24).

Los cambios preexistentes de `tools/apimart/*`, `reference/` y el PDF CRO quedan intactos y excluidos. No se resuelve ninguna decisión LOCKED/OPEN con este cambio.
