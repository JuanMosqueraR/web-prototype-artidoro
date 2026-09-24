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

## Condiciones compartidas de revisión

Mantener el producto, CTA y confianza comunes y un nivel de acabado comparable. No penalizar ni validar definitivamente una tesis solo por la calidad de sus assets provisionales. Las capturas mobile entregadas muestran Keyframe B. El modo sin movimiento debe mantener los dos estados utilizables. Ninguna dirección está elegida para producción.
