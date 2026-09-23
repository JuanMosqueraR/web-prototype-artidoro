# Artidoro — Project brief

Handoff del checkpoint Hero Lab. Fecha de corte: 23 de septiembre de 2026. Colocar estos cinco documentos en `/docs` de la raíz del proyecto extraído.

## Marca y contexto

Artidoro Rodríguez es una marca peruana de café de especialidad con tienda online y cafeterías físicas. Su procedencia, los productos identificados por origen y el lenguaje ilustrado de su packaging son activos centrales de esta exploración. Los cinco orígenes considerados en la sesión son Amazonas, Cajamarca, Villa Rica, Cusco y Puno.

Referencias de la sesión: [web oficial](https://www.artidororodriguez.com/) e [Instagram](https://www.instagram.com/artidorocoffee). Instagram tuvo acceso limitado por login; no se realizó una auditoría completa del feed. Las fuentes verificadas y utilizadas se conservan en [audit/assets.json](../audit/assets.json).

## Objetivo

Comparar en igualdad de condiciones dos direcciones aprobadas **para una prueba**:

- A — Perú, en profundidad: origen como aproximación espacial a un territorio.
- B — Fuera de la lata: universo ilustrado del packaging convertido en lenguaje digital.

El Hero Lab convierte cada tesis en un primer viewport y una interacción reversible entre dos keyframes. Busca comprobar si cada dirección tiene suficiente fuerza visual y continuidad digital para justificar una siguiente inversión de producción, manteniendo claridad comercial desde el inicio.

No es un experimento estadístico de conversión ni una aprobación del diseño definitivo. No hay dirección ganadora.

## Producto común y control de la comparación

| Campo | Valor del experimento |
|---|---|
| Producto | Café Amazonas 250 g |
| Procedencia del producto | Rodríguez de Mendoza |
| Notas | Naranja y melaza |
| Presentación | Bolsa habitual; no lata Travel Line |
| Fotografía | Mismo `public/assets/amazonas-250g.webp` en A y B |
| CTA | Comprar café de Amazonas |
| Confianza | Tostamos cada semana · Cafeterías en Miraflores |

El CTA abre la ficha real del producto en otra pestaña. No existe compra simulada, carrito ni checkout dentro del laboratorio. La procedencia del producto **no confirma** la ubicación del fotograma que ilustra A.

## Restricciones comerciales

El diagnóstico previo aportado por el usuario señaló fricciones de claridad, acceso al producto, confianza y rendimiento. El hero debe comunicar café peruano de especialidad, dar una propuesta entendible, mostrar producto y CTA desde el primer frame e incorporar confianza temprana. La interacción nunca debe funcionar como una barrera para comprar.

La creatividad y el comercio se integran en la composición: el producto no desaparece ni cambia de posición al revelar origen o notas. La señal de confianza y el CTA permanecen disponibles. No se pretende convertir las direcciones en una landing CRO genérica.

## Mobile y rendimiento

Mobile tiene una composición propia de referencia en **390 × 844**, no un desktop reducido. Se priorizan jerarquía, producto, legibilidad y botones utilizables sin hover. Desktop de referencia: **1440 × 900**.

Se usan HTML, CSS, JavaScript y transforms simples. No hay video, WebGL ni imágenes generadas por IA. El contenido comercial está visible antes de interactuar; el movimiento es una mejora opcional. El laboratorio respeta reduced motion. Los alcances reales del QA y sus límites están en [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md), con evidencia en [qa/QA.md](../qa/QA.md).

## Fuera del alcance actual

No se están construyendo la nueva web ni una home completa. No hay secciones adicionales, navbar o footer de producción, PLP, PDP, integración Shopify, arquitectura ecommerce, despliegue público ni optimización de una tienda en producción. “Un nombre, muchas manos” está fuera de esta fase. Las dos direcciones no se mezclan.

## Estado y lectura del handoff

Implementación entregada, seis capturas y dos HTML autónomos disponibles; build y QA del checkpoint completados. La revisión visual del usuario y la elección A/B siguen pendientes. Esta entrega documental no modifica implementación, assets, exportaciones ni documentación anterior.

- [CREATIVE_DIRECTIONS.md](CREATIVE_DIRECTIONS.md): comportamiento visual realmente implementado.
- [ASSET_AUDIT.md](ASSET_AUDIT.md): inventario consolidado y provisionalidad.
- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md): ejecución local, controles y límites técnicos.
- [DECISIONS.md](DECISIONS.md): LOCKED y OPEN.
- [README](../README.md): entrada operativa original; no se sustituye.

La siguiente sesión de Codex debe comenzar leyendo este handoff y el código local actual. El checkpoint no autoriza continuar automáticamente hacia una home.
