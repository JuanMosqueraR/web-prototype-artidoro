# Catálogo y PDP — revisión del 28 de septiembre de 2026

Implementado por instrucción del usuario «mejor encargate tu de implementar el plan», en `feat/catalogo-pdp` desde `38a209f`. Versionado por petición posterior del usuario: «se ve bien en iphone, commitea». Sin merge ni publicación desde esta revisión. Los cambios ajenos de `tools/apimart/*`, `reference/` y el PDF CRO permanecen intactos.

## Demo y resultado

- Home: http://127.0.0.1:4175/ — 05: http://127.0.0.1:4175/#shop
- PDP: http://127.0.0.1:4175/#producto-amazonas
- Capturas directas: [desktop home](../qa/2026-09-28-catalog-pdp/after/desktop-home.png), [mobile home](../qa/2026-09-28-catalog-pdp/after/mobile-home.png), [05 desktop](../qa/2026-09-28-catalog-pdp/after/desktop-05.png), [05 mobile](../qa/2026-09-28-catalog-pdp/after/mobile-05.png), [PDP desktop](../qa/2026-09-28-catalog-pdp/after/desktop-pdp.png), [PDP mobile](../qa/2026-09-28-catalog-pdp/after/mobile-pdp.png).

05 reemplaza las cinco tarjetas repetidas por una entrada compacta a Amazonas y a 02, Travel Line como protagonista y dos piezas complementarias: Pack El Explorador y Miel Perfil Frutal. Precios, presentaciones y CTA individuales. La miel muestra y enlaza 300 g, coherente con la fotografía; no usa el precio mínimo de 175 g. Accesos explícitos a cafés, packs, nanolotes y otros productos, sin llamar «todo el catálogo» a una colección parcial. Dos reseñas atribuidas y cuatro FAQ nativas cierran la sección.

La navegación incorpora Tienda, con apertura por toque/teclado, cierre con Escape, foco fuera o pulsación exterior. No cambia la altura de la cabecera. La PDP de Amazonas se abre desde 01, 02 y 05, conserva el estado de 02 y permite volver al punto de entrada. Tamaño/molienda actualizan precio, anuncio y variante en una sola operación. El enlace final abre la ficha oficial con `?variant=`; no hay carrito propio, checkout, pedidos de prueba ni API comercial en tiempo de ejecución. El botón del encabezado puede devolver desde la PDP directamente a 05.

Foto de PDP: la bolsa existente de 250 g, identificada en el pie de imagen, también al configurar otras cantidades. No se representa ese envase como una fotografía de 454 g o 1 kg. Precios y disponibilidad proceden de un snapshot; la tienda oficial confirma sus valores vigentes. Las reseñas conservan su producto: la del pack corresponde a El Ahorrador, no se atribuye a El Explorador. La PDP solo incorpora la reseña de Amazonas.

## Media, ritmo y carga

Sin generación ni gasto en media. Tres fotografías comerciales reales, recortadas y comprimidas; fuentes, hashes y preparación en `audit/assets.json`. `scripts/prepare-catalog-assets.py` reproduce esos derivados y la tabla local de variantes desde las fuentes guardadas. La suma de los tres WebP es 180.126 bytes (unos 176 KiB).

Las fotos nuevas se preparan a 600 px de 05; no se solicitan al abrir el hero en la comprobación móvil. Tienen alternativa sin JS. No se añade carrusel, video, scroll retenido ni librería. 03 y Tarata conservan íntegros sus archivos de comportamiento y estilos. Los enlaces de Amazonas conservan un destino oficial funcional sin JS; con JS se intercepta únicamente la entrada normal a la PDP representativa. Abrir en otra pestaña mediante un gesto modificado conserva el destino oficial.

## Validación

Build Vite 7.1.3 con Node aislado 22.23.1; Windows, Python 3.10, Chromium 148.0.7778.96, DPR 1. **211/211 comprobaciones principales** y cinco comprobaciones adicionales; dos visitas de solo lectura confirman la variante seleccionada en las fichas oficiales de Amazonas y miel. No se ejecutó ninguna compra.

Contrato A/B: 1440 × 900 y 390 × 844, ambos keyframes y motion on/off. A conserva exactamente los píxeles del hero bajo la navegación contra este checkpoint; el cambio de texto de la navegación es intencional. B conserva composición y geometría; una captura registra 409 píxeles de antialias con delta máximo 14/255, dentro de la tolerancia previa (0,05 % y delta ≤16). Contra `qa/measurements.json`, B no cambia y A conserva sus deltas históricos anteriores a esta fase: CTA y −3,125 px desktop y +8 px mobile.

Se verificaron doce variantes en desktop y mobile, teclado, menú, enlaces, historial atrás/adelante, selección persistente de 02, acceso directo/recarga de PDP, FAQ, ausencia de desbordamiento, texto ampliado al 200 %, compra con fallo de video, poster, movimiento reducido y alternativa sin JS. 03 sigue buscando fotogramas en ambos sentidos después de visitar la PDP.

En 390 × 844: 05 mide 1.832,16 px con FAQ cerradas, frente a aproximadamente 1.833 px anteriores. El CTA de PDP termina en y=712,95 px. También queda completo en 390 × 700 y 360 × 740. Exploración adicional: 768 × 1024 y 1024 × 900. Texto ampliado y FAQ abiertas crecen naturalmente; el presupuesto de altura corresponde al texto normal y FAQ cerradas.

Evidencia y reproducción: [QA](../qa/2026-09-28-catalog-pdp/README.md). Capturas de home completa con movimiento reducido, imágenes decodificadas; capturas de PDP con selección inicial de 250 g/grano. No se creó otra galería.

## Archivos y límites

- Implementación: `index.html`, `src/catalog.css`, `src/catalog.js`, `src/amazonas-variants.json`.
- Fuentes y preparación: `audit/source/catalog-*`, `audit/assets.json`, `public/assets/catalog-*.webp`, `scripts/prepare-catalog-assets.py`.
- Evidencia: `qa/2026-09-28-catalog-pdp/`.
- Documentación descriptiva: este informe, `README.md`, `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ASSET_AUDIT.md`; autorización en `docs/DECISIONS.md`.

Validación del usuario, 28 de septiembre de 2026: «se ve bien en iphone». Se registra como conformidad visual en su dispositivo, sin navegador o versión especificados; no equivale a una prueba instrumental de todas las variantes o del checkout en iOS. No se publicaron estos cambios en Pages desde esta revisión ni se midió conversión, Core Web Vitals de campo, red móvil física o checkout completo. Los materiales provisionales anteriores conservan sus avisos y gaps. No se implementaron las recomendaciones posteriores de favicon/vista previa social ni una propuesta comercial: pertenecen al cierre de presentación, no a este alcance 05/PDP. Los snapshots y galerías anteriores siguen siendo históricos.
