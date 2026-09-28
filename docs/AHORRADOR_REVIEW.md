# El Ahorrador — revisión del 28 de septiembre de 2026

Demo local: http://127.0.0.1:4175/ · Ficha directa: http://127.0.0.1:4175/#producto-ahorrador

Rama `feat/catalogo-pdp`, checkpoint recuperable `87ea725`. Implementación sin commit final, merge ni publicación. Requiere el preview activo. Autorización L21; la confirmación anterior del usuario en iPhone correspondía al checkpoint, no a estos cambios.

## Qué cambió

El Ahorrador aparece desde 01 y 02, además del menú Tienda. 01 conserva su bolsa, precio y CTA de Amazonas. 02 conserva su selector; sus elecciones no configuran el pack. 05 abre con El Ahorrador y su precio de S/280, seguido de Travel Line, Explorador y miel. Categorías, reseñas y FAQ permanecen; la compra individual vuelve a 02 mediante un enlace. El enlace del hero al pack sustituye el enlace anterior a los cinco orígenes; estos siguen accesibles por scroll y Tienda.

La nueva PDP permite configurar tres bolsas de 1 kg, repitiendo o mezclando los cinco orígenes. Las 125 combinaciones corresponden a variantes oficiales. El enlace final conserva la selección mediante `?variant=`; molienda, disponibilidad final, envío y pago se completan en la tienda oficial. La configuración inicial es Amazonas/Cajamarca/Puno y se mantiene al regresar durante la visita; recargar restablece ese ejemplo. Amazonas conserva su propia PDP. No se añadieron carrito, API comercial en tiempo de ejecución ni nuevas animaciones. Los archivos de 03, Tarata y el selector no se modificaron.

## Capturas directas

| Vista | Desktop | Mobile |
|---|---|---|
| Home completa | [Abrir](../qa/2026-09-28-ahorrador/after/desktop-home.png) | [Abrir](../qa/2026-09-28-ahorrador/after/mobile-home.png) |
| 05 | [Abrir](../qa/2026-09-28-ahorrador/after/desktop-05.png) | [Abrir](../qa/2026-09-28-ahorrador/after/mobile-05.png) |
| PDP del pack | [Abrir](../qa/2026-09-28-ahorrador/after/desktop-pack.png) | [Abrir](../qa/2026-09-28-ahorrador/after/mobile-pack.png) |

Antes: `qa/2026-09-28-catalog-pdp/after/`, correspondiente al checkpoint. No se sobrescribió evidencia ni se creó otra galería.

## Media y ritmo

Tres fotografías oficiales de bolsas de 1 kg, preparadas como WebP: 155.580 bytes en total. Se solicitan al aproximarse a 05 o abrir la PDP; no se cargan al entrar al hero. El resto de media y su comportamiento permanecen. Sin generación ni coste de generación.

La fotografía grupal de la ficha oficial tiene etiquetas de 454 g aunque el pack vendido sea 3 × 1 kg. Se comunicó y conservó esa discrepancia; la demo usa fotografías individuales reales de 1 kg, sin reconstruir etiquetas. La composición es un ejemplo fijo de Amazonas/Cajamarca/Puno, identificado en la PDP; las selecciones y el resumen textual determinan la configuración, no la fotografía. Fuentes y reproducibilidad en `audit/assets.json` y `scripts/prepare-ahorrador.py`.

05 mide 1.993,70 px en 390 × 844, frente a 1.832,16 px anteriores: +161,55 px por la oferta adicional. El primer bloque ya permite configurar el pack. No se añadió permanencia de scroll. 02 crece solo 5 px (739,88 px) y conserva su compra dentro del viewport útil; el acceso al pack también cabe en las tres medidas móviles verificadas. En el hero, ese acceso cabe en 390 × 844; en 390 × 700 y 360 × 740 requiere un pequeño desplazamiento, mientras el CTA individual continúa disponible.

## Validación y límites

Build Vite 7.1.3 con Node aislado 22.23.1, Python 3.10, Chromium 148.0.7778.96, DPR 1. Regresión: 211/211; pack: 316/316; dos destinos oficiales y cuatro comprobaciones adicionales correctos. Las dos visitas externas fueron de solo lectura, sin carrito ni pago. El build para Pages funciona bajo subruta local y carga las tres imágenes; no se publicó.

Contrato A/B: 1440 × 900 y 390 × 844, ambos keyframes, movimiento on/off. B conserva todos los píxeles; A conserva todos los píxeles en el área comparada, excluyendo navegación y el nuevo acceso inferior. El CTA original conserva sus coordenadas respecto del checkpoint. Contra la medición histórica original, A mantiene los deltas ya existentes: y −3,125 px desktop / +8 px mobile; B sin delta.

Se verificaron las 125 combinaciones en desktop/mobile, las doce variantes de Amazonas, teclado, selección inválida y recuperación, independencia de 02, historial/foco, acceso directo y recarga, controles de FAQ, ausencia de errores JS y desbordamiento, texto ampliado al 200 %, sin JS, carga diferida, poster ante fallo y búsqueda reversible de frames de 03 tras visitar una PDP. Medidas adicionales: 390 × 700, 360 × 740, 768 × 1024 y 1024 × 900. En todas, el CTA del pack cabe sin desplazar la ficha; a 390 × 700 termina en y=676,69 px.

Pendiente: Safari/Chrome en iPhone físico para esta iteración. No hay medición de conversión, Core Web Vitals de campo ni checkout completo. Precios y disponibilidad son un snapshot del 28 de septiembre, no stock en vivo. La actividad publicitaria del pack es la premisa aportada por el usuario, no una auditoría de campañas. Los gaps previos de paisaje, autoría de Tarata y material conceptual siguen abiertos; no se reclasificaron.

## Archivos

- Implementación: `index.html`, `src/catalog.js`, `src/ahorrador.css`, `src/ahorrador-variants.json`.
- Assets y fuentes: `public/assets/ahorrador-*-1kg.webp`, `audit/source/ahorrador-*`, `audit/assets.json`, `scripts/prepare-ahorrador.py`.
- QA: `qa/2026-09-28-ahorrador/`; comandos y condiciones en su README.
- Documentación: este informe, `README.md`, `docs/ASSET_AUDIT.md`, `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`, autorización añadida en `docs/DECISIONS.md`.

Los cambios preexistentes de `tools/apimart/*`, `reference/` y el PDF CRO quedan intactos y excluidos. No hace falta resolver otra decisión LOCKED/OPEN para revisar esta entrega.
