# Hero «Del cafetal a tu bolsa» y 03 «De la bolsa a tu taza» — 30 de septiembre de 2026 (L28)

Sustituye, para la home de A, el hero automático de L25 (sección siguiente, ahora histórica) y la escena de video de 03 descrita en la revisión del 26 de septiembre. B no cambia.

- **01 — momento wow.** Escenario fijo (sticky) de 280 svh en desktop y 250 svh en mobile (~1,8 y ~1,5 pantallas de scroll) bajo un header transparente que se vuelve sólido al salir del hero. El scroll recorre un video generado de 10 s (dos clips de 5 s; en mobile, la misma toma como secuencia de 60 imágenes en un canvas, y en desktop la secuencia es el respaldo si el video no está listo): vista aérea del cafetal → cerezas que se vuelven granos → cascada de granos; la bolsa real de Amazonas sube al final como capa propia. Tres pasos con texto verificado (Rodríguez de Mendoza · 1 700–1 900 m s. n. m.; notas de naranja y melaza; Amazonas 250 g) y un índice 01–03 en desktop; en mobile cada paso es una línea compacta arriba. Titular, precio, CTA, confianza y pack quedan visibles durante todo el recorrido, también en 390 × 664. El avance está amortiguado (la escena sigue al scroll con un retardo corto). El póster es el primer fotograma del video; el video se pide tras la carga.
- **03 — deseo y uso.** Cuatro imágenes fijas generadas (molido, primer chorro en V60, goteo, bodegón con vaso de doble pared y la bolsa real a escala) en un escenario fijo de 300/280 svh. El scroll solo dispara cada paso (moler, preparar, servir; a 20/40/60 % del recorrido) y la transición se reproduce en tiempo fijo (barrido, apertura circular, fundido), con un acercamiento lento que sigue al scroll. Cierre: «Un mundo. Una taza.» y «Tu bolsa de 250 g: unas 16 tazas». El motor admite pasar a video sin cambiar el diseño.
- **Moliendas.** Franja informativa tras 03 con cuatro iconos propios y texto de las preguntas frecuentes oficiales.
- **General.** Titulares de sección que suben línea a línea una vez; scroll con inercia solo con rueda en desktop; grano de película en las dos escenas; «Precio justo al caficultor» en la franja de confianza de 05.
- **Sin movimiento** (preferencia del sistema, «Reducir movimiento», Save-Data): sin fijación ni video; hero en su composición final (último fotograma, bolsa, origen y notas) y 03 en el bodegón final; titulares visibles.

Detalle y evidencia: [HOME_AUDIT_2026_09_30.md](HOME_AUDIT_2026_09_30.md#l28), `qa/2026-09-30-l28/`.

---

# Hero automático — 30 de septiembre de 2026 (L25)

*Histórico desde L28 para el hero de A.* En A, 01 ya no ofrece Acercar/Alejar origen: al cargar, el cafetal se acerca una vez (misma animación de 1,4 s) y aparece el detalle de origen sin interacción. Mobile muestra solo procedencia y notas de sabor; desktop añade kicker y altitud. Con movimiento reducido el detalle es estático. El pack del hero es un botón secundario con borde; en 05 Travel Line iguala a El Ahorrador. La descripción de Acercar/Alejar más abajo queda como histórico de A y sigue vigente en B. [Detalle](HOME_AUDIT_2026_09_30.md).

---

# Auditoría y corrección de la home — 30 de septiembre de 2026

Autorización L24. Alcance: solo A. **01** conserva la tesis, el paisaje, la bolsa y Acercar/Alejar origen sin cambios de composición desktop; en mobile se corrige el solape entre la anotación y el botón (≥12 px de separación), el CTA queda visible dentro del área real de un iPhone (390×664), la fila del pack pasa a una sola línea legible y desaparece la fila interna «01 / PERÚ, EN PROFUNDIDAD». El aviso de procedencia del paisaje cambia de texto (sin token de laboratorio) pero sigue en el mismo lugar y sigue señalando el mismo gap. **05** conserva El Ahorrador, Travel Line, El Explorador y Miel de abeja; la fila «¿Prefieres una sola bolsa?» se sustituye por una tarjeta «Café de origen» con el mismo formato que sus vecinas, y la fila de complementos pasa a 3 columnas desde 1024 px. Las reseñas añaden una nota de fuente antes de las citas y enlazan el producto a su PDP. En todo el resto de la home (icono/tipografía/touch targets) se elevan mínimos sin cambiar composición. Detalle completo, condiciones y evidencia: [HOME_AUDIT_2026_09_30.md](HOME_AUDIT_2026_09_30.md). Las descripciones inferiores de 01 y 05 quedan como snapshot del 26 de septiembre; sus composiciones generales no cambiaron, solo lo aquí descrito.

---

# Ahorro visible del pack — 29 de septiembre de 2026

La tarjeta de El Ahorrador en 05 y su PDP muestran, bajo el precio de S/ 280.00, el precio normal tachado S/ 330.00 y «Ahorras S/ 50». En la PDP el ahorro también aparece en la fila del total y se oculta si la combinación no existe. Es una línea secundaria, más pequeña que el precio y en el verde apagado del texto de apoyo; en celular baja a 12 px para que «Continuar con mi pack» siga visible a 390 × 700. 01 y 02 conservan solo S/ 280, y el hero no cambia (0 píxeles distintos). Sin motion nuevo. Autorización L23; [QA](../qa/2026-09-29-ahorro/README.md).

---

# El Ahorrador — revisión descriptiva del 28 de septiembre de 2026

A incorpora acceso al pack de 3 kg desde 01, 02 y Tienda. Se conservan el CTA y el precio individual de Amazonas en 01 y toda la interacción de 02; la selección de origen no configura el pack. 05 da protagonismo a El Ahorrador, mantiene Travel Line como segunda propuesta y Explorador/miel como complementos. El bloque repetido de Amazonas en 05 se sustituye por un enlace a los cinco orígenes.

La PDP `#producto-ahorrador` permite elegir tres orígenes independientemente y repetirlos. Total y enlace corresponden a una de las 125 variantes del snapshot oficial; molienda y pago se completan allí. Imagen de combinación representativa, etiquetada. La PDP de Amazonas permanece. Sin motion nuevo, cambios en 03/Tarata o rediseño de B. [Entrega actual](AHORRADOR_REVIEW.md). Las descripciones inferiores son snapshots históricos.

---

# Actualización descriptiva — 28 de septiembre de 2026

A conserva 01–04 y renueva 05: entrada compacta a Amazonas/02, Travel Line protagonista, pack y miel complementarios, categorías explícitas, dos reseñas atribuidas y cuatro FAQ. Tienda es un desplegable accesible. La PDP de Amazonas usa `#producto-amazonas`, datos locales de variantes y continuación a la ficha oficial; mantiene la selección de 02 al volver. B conserva su hero. No se añade motion a 05/PDP ni se modifica el de 03. Composición, QA y límites actuales: [CATALOG_PDP_REVIEW.md](CATALOG_PDP_REVIEW.md). Las descripciones inferiores de cinco tarjetas en 05 y compra exclusivamente externa desde Amazonas son snapshots anteriores.

---

# Dirección A — home implementada, revisión del 26 de septiembre de 2026

La fase L18 desarrolla «Perú, en profundidad» desde el checkpoint `0a1da04`. El código actual prevalece sobre el snapshot del Hero Lab conservado más abajo. B continúa accesible en `/b/`; no recibe un rediseño y no se formula una nueva comparación A/B.

- **01 / presencia:** conserva el cafetal, la bolsa Amazonas y el acercamiento reversible. Añade navegación propia de home, precio visible y CTA comercial desde el primer viewport. Paisaje responsive y tipografía local comprimida; aviso de procedencia geográfica provisional conservado.
- **02 / elección (rama `feat/origin-selector`, 26 de septiembre):** carrusel circular de cinco bolsas, con acceso directo por nombre, flechas, toque en vecinos, swipe/arrastre y teclado. Mobile agrupa producto, notas, 250 g, precio y compra dentro de la primera vista de la sección; desde 1024 px, carrusel a la izquierda y ficha a la derecha. Las bolsas vecinas se preparan al aproximarse a 02; selección confirmada solo tras decodificar, transición de 320 ms y cambio inmediato con movimiento reducido. La última solicitud prevalece y un fallo conserva el producto anterior. La selección afecta únicamente a 02; 03 y 05 no heredan un origen. [Entrega y QA](ORIGIN_SELECTOR_REVIEW.md).
- **03 / deseo:** macro de la superficie del café que se abre hacia una taza, con clips propios horizontal y vertical de siete segundos. El scroll controla el tiempo de un video silencioso y reversible. Solo esta escena tiene permanencia sticky. La tipografía cambia de escala y aparecen dos bolsas reales al cerrar el movimiento; marca, packaging, textos y enlace comercial permanecen fuera del video. El enlace «Llévalo a la taza» salta directamente a 05.
- **04 / cercanía (L19):** composición editorial de dos fotografías de referencia existentes: interior con personal y cascos, y fachada con personas y moto. Interior grande en desktop y fachada secundaria superpuesta; en mobile la fachada es principal y el interior queda como inserto que deja visible la moto. «TOMA ASIENTO.» se integra con la composición. Una frase, dirección y Cómo llegar. Entrada de 850–1100 ms, desfase máximo de 140 ms, una sola vez; luego imágenes en reposo. Sin selector, video ni permanencia de scroll. Fotos diferidas a 800 px de la sección, fallback sin JS, motion reducido respetado.
- **05 / compra:** composición editorial de cinco bolsas en desktop; Amazonas abre y las otras cuatro forman dos columnas en mobile. Cada café tiene notas, gramaje, precio y enlace «Comprar» a su PDP oficial. El cierre conduce al catálogo completo y muestra enlaces de envíos y preguntas frecuentes.

**Motion y carga:** CSS/JS conservan las interacciones de 01/02; no se añadió una librería de animación. 03 solicita solo el MP4 correspondiente al viewport al acercarse a 450 px, sin autoplay ni descarga inicial. Scroll normal en el resto de la página. Preferencia del sistema, control de movimiento o ahorro de datos evitan el video; fallo o espera de 15 s muestran el poster y eliminan la permanencia. La carga lenta puede recuperarse posteriormente; se ofrece Activar movimiento o Reintentar movimiento para permitir arranque mediante un toque. El scroll retoma el control después de ese arranque. Ver VIDEO_RECOVERY.md. Los CTAs siguen disponibles. La transición a Tarata es la salida natural del tramo sticky y un cambio de superficie, sin otra secuencia de video.

**Mobile tiene composición propia:** clip vertical, titular superior, taza más baja, compra siempre enlazada; 04 prioriza la fachada con un inserto del interior y 05 organiza los productos de forma distinta. No es un recorte único del desktop.

Media de 03 conceptual; Tarata usa fotografías de referencia no generadas, de autoría pendiente de confirmar. Ambas condiciones están identificadas en la interfaz y en `audit/assets.json`. No representa un proceso documentado de un origen ni una taza oficial de la marca. [Galería de revisión](../deliverables/home-review.html) · [QA](../qa/2026-09-25-home/README.md).

---

## Snapshot histórico del Hero Lab — no describe la home actual

# Direcciones creativas — estado implementado

Este documento registra el Hero Lab entregado, no una evolución propuesta. **Dirección A/B** identifica un concepto; **Keyframe A/B** identifica el estado inicial/desplegado dentro de cualquiera de ellos.

La barra gris de laboratorio ocupa 44 px superiores y queda fuera del diseño final. Las posiciones CSS descritas son relativas al hero, salvo cuando se indica “viewport”. Los valores finales del código prevalecen sobre aproximaciones de la exploración escrita. Las mediciones completas no se duplican aquí: [qa/measurements.json](../qa/measurements.json).

## A — Perú, en profundidad

### Tesis

Entrar en la procedencia del café mediante una aproximación espacial. La geografía pertenece al producto y deja de ser solo una etiqueta. El prototipo demuestra un único origen, Amazonas; no implementa navegación entre los cinco orígenes.

### Primer viewport y desktop

Fondo verde oscuro `#102e25`, tipografía crema y cafetal fotográfico hacia la derecha, integrado con degradados oscuros. Logotipo blanco arriba a la izquierda; indicador de origen arriba a la derecha.

El bloque comercial ocupa el lado izquierdo, con margen de 6% y ancho aproximado de 43%. Incluye “Café peruano de especialidad”, el titular en dos líneas **EL ORIGEN / SE SIENTE.** y “Cinco orígenes peruanos. Recién tostados, con molienda a tu medida.” El titular usa Barlow Condensed, `clamp(90px, 8.6vw, 140px)`.

La bolsa frontal está centrada en el 75% del ancho y mide el 58% de la altura del hero; es un plano independiente de la fotografía. El paisaje lejano comienza en el 31% del ancho y un recorte de follaje de la misma foto ocupa el extremo inferior derecho. El CTA claro y la confianza quedan debajo del texto. “Acercar origen” se sitúa entre el bloque comercial y la bolsa. La leyenda de producto y el aviso `PROVISIONAL_ASSET` permanecen visibles.

### Keyframe A

La bolsa, el texto, el CTA, la confianza y la leyenda están presentes inmediatamente. El cafetal está a escala 1. La anotación detallada de origen está oculta. No hay introducción automática, espera, video ni dependencia del scroll.

### Interacción y Keyframe B

Clic o activación táctil de **Acercar origen**:

- La misma fotografía pasa de escala 1 a **1.12**.
- El plano cercano se desplaza **20 px en X y 38 px en Y**, a escala **1.1** en desktop.
- Se revela “Rodríguez de Mendoza”, “1 700–1 900 m s. n. m.” y “Naranja y melaza”, entre texto y bolsa.
- El botón pasa a **Alejar origen** y permite regresar al estado inicial.

La transición principal dura **800 ms**, con `cubic-bezier(.2,.7,.22,1)`. La anotación se abre mediante recorte, desplazamiento y opacidad. La continuidad proviene de transformar los mismos planos; no se intercambian imágenes de paisaje mediante crossfade. No hay parallax ligado al pointer ni secuencia de scroll.

### Mobile — 390 × 844

Logo, categoría, titular de 62 px y propuesta comercial se apilan arriba. La fotografía queda en una ventana de 305 px de altura, a partir de los 260 px del hero. La bolsa pasa al lado derecho: altura **273 px**, centro horizontal al 73%. La anotación se revela a la izquierda de la bolsa; el botón queda debajo de ella.

El CTA aparece a **y = 629 px del viewport**, con 346 × 54 px. Confianza debajo, seguida de la leyenda del producto y la advertencia provisional. El plano lejano conserva la escala final 1.12; el cercano reduce su desplazamiento a **10 px / 17 px** y escala **1.08**. Es una composición distinta de desktop.

### Elementos fijos

Bolsa, logo, titular, propuesta comercial, CTA, confianza, leyenda y posición del botón. Cambian los planos del paisaje, la anotación y el texto/icono del control. QA confirmó coordenadas idénticas de bolsa, CTA y confianza entre estados en los dos tamaños.

### Riesgos y criterio observable

Riesgos: parecer turismo, una web institucional peruana o una campaña genérica de origen; relegar la bolsa; atribuir el cafetal a Rodríguez de Mendoza sin evidencia. La bolsa persistente, el copy comercial y el acceso directo al producto sostienen el enfoque en café.

El criterio de lectura del concepto es que, al alternar estados, se perciba una aproximación al **mismo** cafetal mientras el producto permanece estable, y que el segundo frame conecte esa aproximación con Rodríguez de Mendoza y naranja/melaza. El primer frame debe poder entenderse comercialmente sin activar el efecto. El QA acredita geometría y funcionamiento; la fuerza perceptiva y la elección creativa siguen pendientes de revisión del usuario. No se ha fijado un umbral nuevo de investigación con usuarios.

### No alterar sin revisión

La bolsa habitual visible desde el inicio; su posición derecha en desktop; el texto comercial a la izquierda; el movimiento del paisaje sin arrastrar producto o CTA; la revelación de procedencia y notas; la reversibilidad y el tratamiento mobile específico. No introducir mapa del Perú, video cinematográfico, recorrido obligatorio ni assets falsamente atribuidos. El paisaje definitivo sigue OPEN.

Fuentes de implementación: [peru.css](../src/peru.css), [index.html](../index.html). Capturas: `deliverables/A-desktop-keyframe-A.jpg`, `A-desktop-keyframe-B.jpg` y `A-mobile.jpg`.

## B — Fuera de la lata

### Tesis

Liberar el lenguaje ilustrado del packaging y llevarlo a una composición gráfica digital. Travel Line aporta el vocabulario visual, pero el producto comercial sigue siendo la bolsa habitual de Amazonas. No se presenta como lanzamiento o colección temporal.

### Primer viewport y desktop

Fondo plano verde Amazonas aproximado `#30bc4e`, tinta `#0f1d12`, logotipo negro y categoría arriba. **AMAZONAS** ocupa aproximadamente el 90.6% del ancho, con Barlow Condensed a `23.4vw`.

La bolsa se superpone al gran titular, centrada al **54%** del ancho, desde el 25% de la altura del hero y con altura del 58%. El otorongo está detrás del producto, a la derecha: contenedor desde el 56% del ancho y 37% de la altura, ancho 45% y altura 67%, con recorte y partes fuera de campo.

Abajo a la izquierda aparecen “Café con / carácter propio.” y “Cinco orígenes. Tostado semanal y molienda a tu medida.” El CTA negro y la confianza ocupan las mismas coordenadas comerciales que en A. A la derecha está “Desplegar origen”. La leyenda del producto tiene fondo verde para mantener su lectura sobre el animal.

### Keyframe A

Fondo, palabra monumental, bolsa, copy, CTA y confianza aparecen inmediatamente. El animal es parcialmente visible, con máscara inicial `inset(0 0 0 10%)`. Las notas ampliadas están ocultas. El aviso identifica el otorongo como extracción provisional.

### Interacción y Keyframe B

Clic o activación táctil de **Desplegar origen**:

- El mismo contenedor del otorongo se desplaza **−7.5vw** en desktop.
- Su máscara pasa a `inset(0)`; la bolsa conserva su superposición sobre la ilustración.
- Aparecen **NOTAS EN TAZA / NARANJA / Y MELAZA** en el lado derecho.
- El control pasa a **Plegar origen**, que revierte la interacción.

La transición principal dura **650 ms**, con la misma curva de aceleración de A. El revelado de notas usa recorte, desplazamiento y opacidad. La geometría y la pose del animal no cambian: no hay animación de mascota, rebote ni cambio de ilustración. Abrir la máscara no reconstruye partes ausentes del arte original ni implica mostrar el animal completo.

### Mobile — 390 × 844

La palabra AMAZONAS se mantiene completa en una línea bajo logo y categoría (`23.05vw`). La bolsa se coloca a la izquierda, centrada al **25%**, desde los 181 px del hero, con altura **277 px**. El animal aparece detrás y a la derecha; su contenedor parte del 29% del ancho, mide 80% y tiene una ventana de 262 px de alto.

La máscara inicial móvil recorta 8% a la izquierda. Al desplegar, el animal se traslada **−38 px**, conservando su dibujo. Las notas aparecen a la derecha de la bolsa y encima del control. El copy comercial queda debajo de la escena. CTA y confianza conservan las mismas coordenadas que A: CTA a y = 629 px del viewport. No es una reducción de la distribución desktop.

### Elementos fijos

Bolsa, palabra AMAZONAS, logo, fondo, copy comercial, CTA, confianza, leyenda y posición del control. Cambian animal/máscara, notas y texto/icono del botón. QA confirmó inmovilidad de bolsa, CTA y confianza. El contenedor del hero usa `overflow: clip` para evitar el scroll interno detectado y corregido en desktop.

### Riesgos y criterio observable

Riesgos: parecer una landing exclusiva de Travel Line, una campaña temporal, un diseño infantil o una colección de ilustraciones sin producto. La bolsa habitual protagonista, el animal tratado como gráfica y el copy de marca sostienen el alcance comercial.

El criterio de lectura es poder reconocer la bolsa Amazonas como producto comprable desde el inicio y seguir **la misma ilustración** al abrirse la máscara y desplazarse, mientras se revelan naranja/melaza sin mover ni tapar el CTA y la confianza. La ampliación gráfica no debe confundirse con cambio de producto ni animación de personaje. La validación perceptiva sigue abierta; el trazado provisional limita el juicio sobre el acabado del dibujo.

### No alterar sin revisión

AMAZONAS monumental, fondo gráfico plano, bolsa habitual como protagonista, otorongo como gráfica parcialmente oculta al inicio, continuidad de la misma ilustración y revelado de notas. Mantener CTA y confianza inmóviles. No sustituir la bolsa por lata, mezclar paisaje de A, añadir stickers, campaña promocional o gestos de mascota. El arte maestro y la especificación final de color siguen OPEN.

Fuentes de implementación: [lata.css](../src/lata.css), [index.html](../index.html). Capturas: `deliverables/B-desktop-keyframe-A.jpg`, `B-desktop-keyframe-B.jpg` y `B-mobile.jpg`.

## Escena 02 — “Encontrar tu origen” (continuación de A, checkpoint del 24 de septiembre de 2026)

Sección independiente tras el Hero A; solo visible con A. No forma parte de la comparación A/B ni cambia el hero. Storyboard de trabajo: 01 El origen se siente (hero), **02 Encontrar tu origen**, 03–05 sin implementar.

- **Composición.** Franja verde `#102e25` (64 px desktop, 32 px mobile) que continúa el verde del hero, borde limpio a crema `#f4f0e5`, encabezado “ENCUENTRA TU ORIGEN.” (Barlow 80/48), índice de cinco filas, información del origen y bolsa. Desktop ≥ 1360 px: tres columnas ancladas a 1440 × 900 (índice x86 · información x548 · bolsa centrada en el 75%). Por debajo de 1360 px se reorganiza en la composición vertical de mobile (390 × 844).
- **Estados.** Solo Amazonas (inicial) y Cajamarca son seleccionables (botones con `aria-pressed`). Villa Rica, Cusco y Puno son filas informativas con sus notas. Un único CTA persistente cambia texto y destino con el origen, y el enlace “Ver todos los cafés ↗” apunta a la colección oficial. Datos comerciales y sus fuentes: `audit/assets.json` (`verified_copy.origin_scene_02`).
- **Cambio de origen.** Información y bolsa se desvanecen como un conjunto (≈ 90 ms + 90 ms); el commit (selección, información, bolsa, CTA) es síncrono y solo ocurre con la imagen entrante decodificada y la solicitud vigente. Sin motion / `prefers-reduced-motion`: cambio inmediato, sin saltarse la preparación de la imagen. Ante error o timeout de 4 s se conserva el origen mostrado y aparece un aviso breve.
- **Hero → 02.** Solo por scroll; sin sticky, parallax, video ni crossfade. La bolsa no viaja: reaparece en el mismo eje (desktop, 75%).

## Escena 04 — “Toma asiento” / CP04 (continuación de A, checkpoint del 24 de septiembre de 2026)

Sección independiente tras 02; solo visible con A. No forma parte de la comparación A/B ni cambia el hero ni 02. Con ella queda implementada la 04 del storyboard; 03 y 05 siguen sin implementar (el párrafo de 02 los lista como pendientes en su fecha). Función: pasar de territorio a producto a espacio físico; el visitante “entra” a Artidoro. Decisiones visuales: L16 y L17.

- **Composición.** Fondo verde `#102e25`, crema `#f4f0e5`, Barlow + Chivo. Desktop ≥ 1360 px, ancladas a 1440 × 900: texto a la izquierda (x86, columna de 560 px) — kicker “Cafetería Artidoro Rodríguez” (y106), titular “TOMA ASIENTO.” (Barlow 80), selector, “TARATA”, dirección, horarios y CTA cream de 330 × 58 — e imagen a sangre a la derecha (675 × 900, x765, proporción 3:4 de los assets) con un degradado suave hacia el verde por su borde izquierdo. Por debajo de 1360 px se usa la composición vertical de mobile.
- **Mobile 390 × 844 (composición propia).** Kicker, titular (Barlow 48), imagen a sangre de 390 × 430 (recorte CSS de los mismos assets, sin imágenes nuevas), selector de dos filas de 47 px, Tarata, dirección/horarios, CTA de 346 × 54 y el aviso. La sección mide 1021 px: el CTA queda en y = 903–957 de la sección, por debajo de la primera pantalla.
- **Estados.** “Desde la entrada” (`cp04-entrada.jpg`, inicial) y “Desde la mesa” (`cp04-mesa.jpg`): botones con `aria-pressed`, punto y subrayado en el activo y el inactivo atenuado. “TOMA ASIENTO.” es el título de la sección, no el rótulo del control. Al cambiar, la interfaz no se mueve (0 px de diferencia medida): solo cambian la imagen y el estado activo. Sin zoom, parallax ni movimiento de cámara.
- **Cambio de vista.** Imagen y estado se desvanecen ~90 ms + ~90 ms; el cambio es síncrono y solo ocurre con la imagen entrante decodificada y la solicitud vigente; la última solicitud gana. Sin motion / `prefers-reduced-motion`: cambio inmediato. Ante error o timeout de 4 s se conserva la vista mostrada y aparece “No se pudo cargar esta vista. Inténtalo de nuevo.”
- **Contenido factual.** Cafetería Tarata · Calle Tarata 285, Miraflores · Lunes a Sábado 08:00 a.m. – 09:00 p.m. y Domingo 09:00 a.m. – 03:00 p.m. · CTA “Cómo llegar ↗” con el enlace oficial de esa tarjeta (nueva pestaña). Fuente y fecha: `audit/assets.json` (`verified_copy.cp04_tarata`).
- **Aviso de procedencia.** Chip `CONCEPTUAL_ASSET` discreto en la propia sección (“Imagen conceptual con IA · no es un documento del local”) y nota de laboratorio con la procedencia de las imágenes, fuera del diseño final. Sin guiño de cascos ni de motos (L17).
- **No alterar sin revisión.** Los dos assets de L17, la interfaz fija entre estados y la ausencia de zoom/parallax. La luz de tarde (L16) puede revisarse tras verla en la web; cambiarla implicaría sustituir los dos archivos.

## Condiciones compartidas de revisión

Mantener el producto, CTA y confianza comunes y un nivel de acabado comparable. No penalizar ni validar definitivamente una tesis solo por la calidad de sus assets provisionales. Las capturas mobile entregadas muestran Keyframe B. El modo sin movimiento debe mantener los dos estados utilizables. Ninguna dirección está elegida para producción.
