# Verificación del Hero Lab

23 de septiembre de 2026. Chrome. Dos composiciones de hero, sin secciones adicionales.

| Comprobación | A desktop | A mobile | B desktop | B mobile |
|---|---|---|---|---|
| Viewport CSS | 1440 × 900 | 390 × 844 | 1440 × 900 | 390 × 844 |
| Overflow de documento | Ninguno | Ninguno | Ninguno | Ninguno |
| Bolsa fija entre frames | Sí | Sí | Sí | Sí |
| CTA fijo entre frames | Sí | Sí | Sí | Sí |
| Confianza fija entre frames | Sí | Sí | Sí | Sí |
| Keyframes e interacción reversible | Revisados | Revisados | Revisados | Revisados |

## Evidencia

`measurements.json` registra dimensiones, posiciones y estado de ambos frames. La comparación de coordenadas confirmó que bolsa, CTA y confianza permanecen exactamente en su sitio.

CTA: 330 × 58 px desktop; 346 × 54 px mobile. Interacción secundaria: 190 × 48 px desktop; 168/170 × 46 px mobile. No se necesita hover, scroll ni animación de entrada.

El cafetal conserva la misma fotografía al acercarse (escala 1 → 1.12); el recorte de primer plano se mueve un poco más. La bolsa no cambia. El otorongo conserva la misma geometría; se desplaza y abre su máscara. No hay sustitución de imágenes ni crossfade entre escenas.

Se probó **Sin motion** en las dos direcciones: transición calculada de 0 s y estado final correcto. También hay una regla para `prefers-reduced-motion`. En A se comprobó escala final 1.12; en B, desplazamiento móvil de −38 px. Los controles siguen disponibles.

La revisión detectó y corrigió un desplazamiento de 34 px producido por el recorte de B desktop. `overflow: clip` elimina ese scroll interno; la nueva medición confirmó posiciones idénticas. Se protegió la leyenda de producto con el verde de fondo para mantener su lectura sobre el dibujo.

Contraste de colores sólidos: crema/verde oscuro A **12.81:1**; tinta/verde B **7.00:1**; CTA crema/tinta B **15.31:1**. El texto sobre fotografía se revisó visualmente con su degradado oscuro. El aviso de asset provisional es una anotación del laboratorio.

No se observaron errores de aplicación en el origen local. El build de Vite completó correctamente. Se comprobó la exportación HTML: todos los recursos visuales están embebidos, las imágenes cargan y funcionan el selector y la interacción. El CTA conduce a la ficha pública del café; no se ejecutó ninguna compra.

## Capturas

Los viewports se comprobaron en un iframe con las dimensiones CSS exactas. Desktop se proyectó al 90% para caber en la superficie de captura: archivos **1296 × 810**, correspondientes al layout **1440 × 900**. Mobile se capturó a escala 1:1, **390 × 844**. Se recortó únicamente el margen de la superficie de revisión. Las capturas finales están en `../deliverables/`; las dos capturas mobile muestran el frame desplegado.

Esto comprueba composición responsive e interacción por clic; no sustituye una prueba en dispositivos físicos ni una auditoría de rendimiento en producción.

## Rendimiento y alcance

Sin video, WebGL, librerías de animación, React ni servicios de fuentes remotos. CSS y transformaciones sencillas; JS de interacción pequeño. La imagen de producto es única y compartida entre variantes. Los assets servidos suman aproximadamente **445 KiB**. La versión estática inicial ya muestra producto, texto, CTA y confianza; la animación solo revela información adicional.

El tamaño mayor de los HTML autónomos (~730 KiB cada uno) corresponde a recursos embebidos para revisión sin servidor. El proyecto Vite sirve recursos por separado y permite caché compartida. No se ha medido un presupuesto de rendimiento de una tienda real.

## Límites visuales

- Fotograma real de la marca; falta confirmar que corresponda a Rodríguez de Mendoza.
- Otorongo trazado desde una extracción pequeña y curva; falta el original completo.
- Verde aproximado desde packaging; no equivale a una especificación oficial de color.
- Instagram limitado por acceso/login. No se afirma una revisión completa del feed.

No se selecciona una dirección ganadora. El trabajo se detiene en este checkpoint.
