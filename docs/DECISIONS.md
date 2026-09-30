# Alcance autorizado — home y revisión de Tarata

Actualización del 26 de septiembre: L19, al final de este registro, documenta la nueva composición de 04. L18 conserva el alcance de la home.

**L18 — Registro de la autorización explícita de la fase actual.** La instrucción del usuario es: «Continúa directamente con la fase de producción e implementación ya autorizada». Fuentes de verdad indicadas por el usuario: checkpoint `0a1da04`, dirección A — «Perú, en profundidad», referencias cinematográficas/motion y condiciones CRO del PDF existente.

La autorización incluye estas instrucciones literales:

- «La dirección base sigue siendo A — “Perú, en profundidad”.»
- «La selección de origen en 02 NO debe gobernar toda la narrativa posterior.»
- «Quiero terminar con una demo navegable de la home: 01 → 02 → 03 → 04 → 05».
- «03 debe convertirse en el gran momento wow de la home.»
- «04 debe quedar reducido y mejor proporcionado.»
- «05 debe cerrar claramente en clave ecommerce.»
- «Puedes generar los assets y videos necesarios.»
- «Para el problema Node/Vite usa la solución aislada compatible que propones.»
- «No hagas commit final.»

Alcance: ejecutar esta fase de la demo A, con composiciones desktop/mobile, media, preparación de assets, implementación y QA. El usuario autoriza criterio de ejecución y no pide otra ronda de planning. No autoriza una publicación, checkout nuevo, migración Shopify ni una nueva fase posterior. Deben conservarse `reference/`, el PDF CRO y los cambios preexistentes ajenos de `tools/apimart/*`. El checkpoint indicado ya existe y se preserva sin reescribir historial.

**Relación con el registro anterior:** para esta fase, L18 sustituye las restricciones de alcance de L02/L14 y los límites de media de L06/L10/L11 en aquello que la home y su 03 autorizado requieren. La simplificación aprobada de 04 sustituye el selector de dos estados de L16/L17 por una sola presencia «Desde la mesa»; se conservan las fuentes anteriores. A es la base expresamente indicada para continuar; no se declara una victoria experimental sobre B ni se realiza una comparación de conversión. Los cuadros LOCKED/OPEN de abajo quedan como registro histórico del Hero Lab, sin reclasificación documental de sus filas. Las referencias O01/O05/O06 de ese snapshot no describen la autorización actual. Las incertidumbres sobre paisaje, autoría y arte maestro siguen abiertas; ninguna generación es material oficial.

Implementación y evidencia de esta fase: [HOME_REVIEW.md](HOME_REVIEW.md). La implementación es revisable, no una aprobación creativa final inferida por el agente.

---

## Snapshot histórico — 23/24 de septiembre de 2026

# Decisions — cierre del checkpoint Hero Lab

Registro de decisiones efectivamente tomadas y asuntos aún abiertos. Fecha de corte: 23 de septiembre de 2026. LOCKED se refiere al contrato del experimento actual, no a una aprobación irrevocable para producción.

## LOCKED

| ID | Decisión vigente | Alcance / referencia |
|---|---|---|
| L01 | Comparar únicamente A — Perú, en profundidad y B — Fuera de la lata | Ambas aprobadas para prueba; sin mezclar. “Un nombre, muchas manos” fuera de esta fase. |
| L02 | Construir solo un Hero Lab aislado | Un hero y dos keyframes por dirección. No home ni secciones adicionales; no Shopify, PLP, PDP o tienda. |
| L03 | Usar el mismo café Amazonas 250 g | Rodríguez de Mendoza, naranja y melaza; bolsa habitual y misma foto en ambas variantes. |
| L04 | Comparación con condiciones comerciales comunes | Categoría clara, propuesta de valor, CTA inmediato y confianza temprana. Mismo CTA y mensaje de confianza; acceso al producto sin completar el efecto. |
| L05 | Mantener producto, CTA y confianza fijos entre keyframes | Verificado en ambos tamaños. La composición puede ser distinta entre direcciones; no se igualan artificialmente sus posiciones de producto. |
| L06 | A aproxima el origen sin desplazar la bolsa | Paisaje por pocos planos, copy a la izquierda y bolsa a la derecha en desktop; revelado de procedencia/altura/notas. No mapa, recorrido turístico o video. |
| L07 | B despliega el mismo lenguaje ilustrado sobre fondo gráfico | AMAZONAS monumental, bolsa habitual protagonista y otorongo como gráfica, no mascota. No landing exclusiva de Travel Line, stickers o campaña temporal. |
| L08 | Usar interacción explícita y reversible | Acercar/Alejar y Desplegar/Plegar. Sin scroll obligatorio, espera o introducción automática. Parámetros reales en [CREATIVE_DIRECTIONS.md](CREATIVE_DIRECTIONS.md). |
| L09 | Mobile tiene composición propia | Referencia 390 × 844; desktop 1440 × 900. Selector de laboratorio fuera del diseño final. |
| L10 | Priorizar ligereza y reduced motion | HTML/CSS/JS, transforms simples y fuentes locales. Implementación actual sin video, WebGL o dependencias pesadas de animación. |
| L11 | No generar imágenes IA en esta fase | Ningún asset generado mediante IA. El trazado del otorongo deriva del material real y permanece provisional. Excepción solo para CP04: ver L15. |
| L12 | Identificar incertidumbres de los assets | Paisaje sin localización confirmada y otorongo sin maestro original. No presentarlos como material oficial definitivo ni retirar los avisos mientras persistan los gaps. |
| L13 | Conservar el estado final como baseline de revisión | Fuentes, dos HTML autónomos, seis capturas y QA entregados. El scroll interno de B fue corregido; no se debe reintroducir al alterar el recorte. |
| L14 | Detener el trabajo en este checkpoint | La tarea actual es documental. No modificar implementación, rediseñar, elegir ganadora ni continuar hacia home. |
| L15 | Para CP04 de Artidoro se permite explícitamente utilizar IA generativa y edición avanzada para producir assets conceptuales de la demo. La excepción es únicamente para CP04. Distingue REAL_ASSET, AI_PREPARED_ASSET y CONCEPTUAL_ASSET. Se mantienen estas protecciones: no inventar otro local; no sustituir la arquitectura esencial; no inventar branding; no cambiar logo; no falsificar packaging; no inventar productos; no inventar servicios; no inventar claims; no convertir Artidoro en una cafetería temática de motos. Los assets intervenidos con IA no son evidencia documental del local y deben permanecer identificados como conceptuales/provisionales. | CP04 only; 2026-09-24; approved explicitly by the user on 2026-09-24. |
| L16 | CP04 — “Tomar asiento” (dirección A) usa dos estados: “Desde la entrada” y “Desde la mesa”. Luz de la escena: final de tarde, con las lámparas encendidas. La luz la eligió el agente por delegación explícita del usuario; el usuario podrá revisarla una vez vista implementada en la web (por ejemplo, cambiar a luz de mañana). Esa revisión queda para después. | CP04; 2026-09-24; aprobado explícitamente por el usuario el 2026-09-24. |
| L17 | CP04: estado 1 = `02-facade.webp`; estado 2 = `03-counter-perspective-3.webp`, versión A. El guiño visible a los cascos NO aparece en CP04. El posible guiño motero queda pendiente para otra sección y no se resuelve ahora. Ambas imágenes se adoptan como `CONCEPTUAL_ASSET` para esta demo (`public/assets/cp04-entrada.jpg`, `public/assets/cp04-mesa.jpg`; registro en `audit/assets.json`). | CP04; 2026-09-24; aprobado explícitamente por el usuario el 2026-09-24. CP04 no está implementado. |

Las decisiones de composición, copy, fuentes, colores y tiempos presentes en el código se registran como baseline implementado en [CREATIVE_DIRECTIONS.md](CREATIVE_DIRECTIONS.md). No se reinterpretan silenciosamente al retomar el proyecto. Los valores aproximados de assets no se convierten por ello en especificaciones oficiales de marca.

## OPEN

| ID | Cuestión pendiente | Estado al cierre |
|---|---|---|
| O01 | Elección A vs B | Pendiente de revisión visual del usuario. No hay ganadora ni aprobación para producción. |
| O02 | Paisaje definitivo de A | Falta confirmar/producir u obtener material atribuido a Rodríguez de Mendoza / Amazonas. No se ha elegido un reemplazo. |
| O03 | Otorongo definitivo de B | Falta arte maestro completo. La extracción trazada no sustituye esa decisión ni la validación del acabado final. |
| O04 | Paleta y acabado definitivos | El verde se aproxima desde packaging; no hay homologación oficial. La adecuación final de tipografía y tratamiento visual permanece sujeta a revisión, conservando entretanto el baseline. |
| O05 | Posible generación IA posterior | No decidida. No hay aprobación de uso, proveedor, presupuesto, prompts ni plan de generación. La restricción de no generar sigue vigente en el checkpoint actual. Excepción solo para CP04: ver L15. |
| O06 | Siguiente alcance | No definido. No se ha autorizado una home, arquitectura completa, nuevas secciones, adaptación Shopify, publicación o una fase de producción. |
| O07 | Validación perceptiva de las tesis | QA geométrico/funcional completado; fuerza creativa, carácter de marca y mérito para avanzar pendientes. No se han hecho pruebas con usuarios ni un test de conversión. |
| O08 | Material de marca adicional | Acceso completo a Instagram, arte botánico independiente y otros originales no obtenidos. No se ha decidido incorporarlos ni producir mapas/texturas. |

No se resuelve ninguna cuestión OPEN en este handoff. Los límites técnicos registrados en [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) describen deuda y cobertura de prueba, no constituyen un backlog aprobado para ejecutar automáticamente.

## Fuentes del registro

El contrato de alcance proviene de las instrucciones de la sesión. El baseline concreto se contrastó con `index.html`, `src/`, `README.md`, `audit/`, `qa/`, `deliverables/` y el ZIP final. Las referencias operativas y de evidencia permanecen en sus archivos originales; estos cinco documentos aportan contexto para retomar la conversación en VS Code.


## L19 — Tarata editorial, 26 de septiembre de 2026

El usuario aprobó explícitamente la opción 1 propuesta —interior grande y fachada con moto como fotografía secundaria superpuesta, con composición propia mobile—: «de acuerdo con la primera, aporta tener el guiño a la moto y cascos ya que el dueño es motero y aficionado por las motos». Tras concretar motion sobre fotografías reales, sin generar video para 04, confirmó: «de acuerdo. go!».

Alcance: revisar únicamente 04 dentro de la home A; dos fotografías existentes, titular expresivo, copy breve, dirección y Cómo llegar. Entrada suave una vez, con desfase entre interior/fachada/titular; después reposo, scroll libre y reduced motion. Desktop prioriza interior; mobile prioriza fachada y conserva el detalle interior. 03 mantiene el video central y 05 el cierre comercial. Se conservan los archivos originales de reference/ y no se modifican herramientas APIMart ni el PDF CRO.

Esta aprobación sustituye para 04 la exclusión anterior del guiño a cascos en L17 y la resolución con una sola imagen de L18. No autoriza transformar la cafetería en un concepto temático de motos ni inventar nuevos elementos del local. El interés del dueño es contexto aportado por el usuario, no un claim añadido a la web.

Checkpoint previo de la implementación actual: `3830028`, continuando la autorización de conservar un estado recuperable antes de cambios. Esta revisión queda sin commit final. Clasificación/fuentes: audit/assets.json. Evidencia: qa/2026-09-26-tarata/.

## L20 — Catálogo y PDP, 28 de septiembre de 2026

**L20 — Catálogo y PDP, 28 de septiembre de 2026.** Tras el plan «Completar el recorrido comercial: 05, confianza y una PDP», el usuario instruye: «mejor encargate tu de implementar el plan». Alcance de ese plan: renovar 05 con entrada compacta a cafés de origen, Travel Line, Pack El Explorador y Miel Perfil Frutal; accesos a categorías mediante Tienda; dos reseñas publicadas y cuatro FAQ con fuentes; una PDP representativa de Amazonas con las variantes reales y continuación a la tienda oficial. Rama `feat/catalogo-pdp` desde `38a209f`; conservar 01–04, incluido 03 sin otra iteración, y el estado local de 02. Sin generación de media, carrito/checkout propio, publicación, merge ni commit final. Se mantienen las exclusiones preexistentes. Esta autorización permite la PDP nombrada frente al límite anterior de L02; no amplía el alcance a otras PDP o a una migración de tienda. Implementación y límites: [CATALOG_PDP_REVIEW.md](CATALOG_PDP_REVIEW.md). Los registros históricos inferiores no se reclasifican.

## L21 — El Ahorrador, 28 de septiembre de 2026

El usuario elige «asumamos que el pack sera: https://www.artidororodriguez.com/products/pack-3kg-origenes-1 es el que tiene ads activas» y aprueba la propuesta siguiente con «ok, go!»: acceso al pack en 01 conservando composición y compra individual; acceso desde 02 sin heredar su selección; El Ahorrador principal en 05, Travel Line como segunda propuesta y Explorador/miel complementarios; PDP propia con tres bolsas de 1 kg configurables y continuación a la variante oficial. Molienda en la tienda oficial. Conservar la PDP de Amazonas, 03 y Tarata; sin nuevos caminos por origen, carrito o checkout. La autorización permite esta PDP adicional respecto de L20, sin extenderse a otras. No se autoriza un commit final, merge o publicación en esta instrucción. Checkpoint `87ea725`; ejecución sobre `feat/catalogo-pdp`. La premisa publicitaria es información del usuario, no una verificación de campañas. [Implementación y límites](AHORRADOR_REVIEW.md).

## L22 — Cierre, integración y handoff comercial, 28 de septiembre de 2026

Instrucción literal del usuario: «actualiza docs, commitea, has merge a master, has handoff y dame un prompt para hacer con claude la presentacion(Un argumento breve que conecte diseño y negocio. ), otro prompt(o incluyelo en el anterior si lo crees adecuado) para ropuesta concreta para contratar el siguiente trabajo(lcance, entregables, plazo, inversión y lo que necesitamos de Artidoro: materiales definitivos, información comercial y acceso a su tienda ...)».

Autoriza actualizar documentación, versionar los cambios pendientes propios de la demo, integrarlos en `master`, cerrar el handoff y preparar el prompt para la presentación y propuesta. Sustituye para este cierre la prohibición de commit/merge de L20/L21; el alcance implementado no cambia. No autoriza push, publicación, trabajo en la tienda de producción ni una aceptación contractual de la futura propuesta. Se preservan fuera del commit los cambios ajenos de `tools/apimart/*`, `reference/` y el PDF CRO. No se infiere una nueva confirmación física de iPhone ni resultados de conversión. Ninguna fila histórica LOCKED/OPEN cambia de estado.

## L23 — Ahorro visible, propuesta y script de publicación, 29 de septiembre de 2026

Instrucción literal del usuario, en respuesta a la lista de pendientes propuesta por el agente: «guarda la propuesta en el repo / muestra el ahorro / script de publicacion en el repo / actualiza docs».

- **Ahorro visible (Clase 3 y 4).** En la tarjeta de El Ahorrador de 05 y en su PDP se muestra el precio normal tachado S/ 330.00 y «Ahorras S/ 50» junto al precio de S/ 280.00; en la PDP también en la fila del total. El precio normal procede del snapshot oficial del 29 de septiembre (`audit/source/ahorrador-2026-09-29.json`; registro en `verified_copy.ahorrador_saving_2026_09_29`). 01 y 02 conservan solo S/ 280, sin cambios en el hero ni en el selector. Sustituye para la demo la exclusión de precio tachado registrada el 28 de septiembre. Checkpoint previo `41d0cf1`; QA en `qa/2026-09-29-ahorro/`.
- **Script de publicación (Clase 2).** `scripts/build-presentation-artifact.py` genera la copia publicable de la presentación en `dist/` (ignorado por Git). No publica: la publicación del Artifact sigue siendo una acción manual.
- **Propuesta.** Se guarda como borrador en `docs/PROPUESTA_ETAPA1.md`, con su nota interna en `docs/PROPUESTA_NOTA_INTERNA.md`. No es una cotización cerrada ni un alcance contratado; tarifa, capacidad, impuestos y fecha siguen pendientes del usuario.

No autoriza push, publicación en GitHub Pages ni trabajo en la tienda de producción. Ninguna fila histórica LOCKED/OPEN cambia de estado.

## L24 — Auditoría y corrección de la home 01–05, 29–30 de septiembre de 2026

Instrucción literal del usuario: «Apruebo el plan. D1 = opción (a): mantener los avisos de procedencia en su ubicación actual, pero reemplazar los tokens internos de laboratorio por copy humano y discreto, con la divulgación completa consolidada en "Acerca de esta demo/propuesta". No apruebo por ahora los dos opcionales: no añadir "Ahorras S/50" al hero; no añadir estrellas a las reseñas. […] 11 px es mínimo absoluto solo para labels muy secundarios. No lo uses como tamaño objetivo para texto informativo normal; prioriza 12–14 px cuando la composición lo permita y ≥15 px para las reseñas según tu propio plan. Todo lo demás queda aprobado. […] Implementa: 1. Batch A completo; 2. verifica; 3. Batch B completo; 4. verifica la home completa. Mantén estrictamente WHAT NOT TO TOUCH. No regeneres assets. No toques PDPs. No toques dirección B. No publiques Pages. No hagas commit final sin mi revisión.»

Alcance aprobado (dirección A únicamente; B, PDPs y assets fuera de alcance): iconografía de flechas/chevron sustituida por SVG vía `mask` (corrige el emoji de iOS y separa flecha interna/externa); corrección del solape entre la anotación de origen y el botón «Alejar origen» en mobile; recomposición del hero mobile para que el CTA quede visible en 390×664 y la fila del pack sea una sola línea legible; suelo tipográfico de la home elevado según el criterio del usuario (11 px solo en labels muy secundarios, 12–14 px en texto informativo, ≥15 px en las citas de reseñas); objetivos de toque ≥44 px en los controles señalados; ajuste exploratorio del hero en la franja 761–1000 px para que la anotación no quede detrás de la bolsa; retiro de la fila interna «01 / PERÚ, EN PROFUNDIDAD» y del enlace público a la dirección B en el pie; reescritura de los tres avisos de procedencia a texto humano sin token de laboratorio (D1-a); sustitución de «¿Prefieres una sola bolsa?» por una tarjeta «Café de origen» con el mismo formato que El Explorador y Miel de abeja; en las reseñas, nota de fuente añadida antes de las citas y nombre de producto convertido en enlace a su ficha (interna para Amazonas y El Ahorrador).

No autoriza: precio tachado ni «Ahorras S/50» en el hero; estrellas en las reseñas; cambios en B, en las PDP, en 03/Tarata más allá de tamaños de texto, ni regeneración de ningún asset. No se hizo commit final; el checkpoint recuperable es `0b33580`. Implementación, condiciones de entorno y evidencia: [HOME_AUDIT_2026_09_30.md](HOME_AUDIT_2026_09_30.md); QA en `qa/2026-09-30-home-audit/`.

## L25 — Hero automático, pack y Travel Line, scroll y control de movimiento, 30 de septiembre de 2026

Instrucciones literales del usuario, respondiendo a la propuesta del agente: «1. acepto la propuesta 2. ok 3. acepto: botón secundario en el hero y Travel Line con más peso en 05; la franja entre 02 y 03 solo si el dueño lo pide. 4. el visitante puede que no entienda que es Naranja y Melaza, quiza nunca toque la opcion de acercar origen, alejar origen no tiene sentido. prefiero que se muestre la informacion con la misma aninmacion en automatico, pero informacion puntual que se entienda y no muestre el contenido sobrecargado. con respecto a Sin movimiento/Movimiento reducido, acepto recomendacion».

Alcance (solo dirección A; B, PDPs y assets sin tocar): se elimina el botón Acercar/Alejar origen del hero A y la aproximación al cafetal se reproduce una sola vez, automáticamente, con la misma animación; el detalle de origen se muestra sin pulsar nada (mobile: «Rodríguez de Mendoza» y «Notas de sabor: Naranja y melaza»; desktop conserva además kicker y altitud; «EN TAZA» pasa a «Notas de sabor»). Con movimiento reducido o `.no-motion` el detalle queda visible y estático. La fila del pack en el hero pasa a botón secundario con borde, sin «Ahorras S/ 50» (no aprobado). Travel Line recibe en 05 el mismo peso que El Ahorrador (tarjeta completa y CTA de botón, también en mobile). Scroll: suave solo cuando el trayecto no cruza 03; si lo cruza, salto instantáneo con un fundido breve de llegada; marca de sección activa para Tarata en el header. El control «Sin movimiento» de 03 y el botón del pie se sustituyen por un único control dentro de «Acerca de esta demo». No se añade la franja entre 02 y 03 (solo si el dueño la pide). Este cambio sustituye la interacción reversible de L06/L08 para A en la home; no toca la de B. Checkpoint: `0b33580` más el patch de L24 sin commit; sin commit final, sin publicar Pages. Evidencia: `qa/2026-09-30-hero-auto/`.

## L26 — Pack del hero: 3 kg y precio normal tachado, 30 de septiembre de 2026

Instrucción literal del usuario: «Pack el Ahorrador 3 x 1kg, me parece que puede que no se entienda, mejorar para que se entienda que son 3kg de cafe por S/280, seria buena idea mostrar el precio de comparacion(S/330) tachado en el hero?». El agente entendió la propuesta como aprobación y la implementó; el usuario puede revertirla. El botón del hero A muestra «Pack El Ahorrador · 3 kg», «3 bolsas de 1 kg, a tu elección», S/ 330 tachado (con «Precio normal» para lectores de pantalla) y S/ 280. Sustituye para el hero la exclusión de L23 («01 y 02 conservan solo S/ 280»); 02 sigue sin cambios y no se añade «Ahorras S/ 50». El precio normal procede de `audit/source/ahorrador-2026-09-29.json` (`verified_copy.ahorrador_saving_2026_09_29`); «a tu elección» refleja que cada bolsa se elige por separado (L21). Sin commit ni publicación.

## L27 — Cierre gráfico de 05: confianza, reseñas con estrellas, FAQ y mosaicos, 30 de septiembre de 2026

Instrucciones literales del usuario: «aún la ultimas secciones me parece que no se entienden, no tienen buena estructura, esta muy recargado, no es facil de leer. dame un plan para mejorarlo» y, ante el primer plan: «incluyamos algo mas grafico, estrellas o lo que tu consideres necesario para mejorar ui/ux, no nos limitemos por esto porque sino no podremos notar un cambio»; el plan revisado (franja de confianza con iconos, banda oscura de reseñas con estrellas, FAQ en dos columnas, mosaicos «Sigue explorando») fue aprobado.

Alcance (solo A; B, PDPs y assets sin tocar): el tramo posterior a las tarjetas de 05 pasa a una sección propia `#close-bands` con cuatro bandas. Estrellas: las dos reseñas reflejan las cinco estrellas guardadas en `audit/source/catalog-reviews-2026-09-28.json`; sin promedio, recuento ni «compra verificada». Los mosaicos reutilizan `amazonas-250g.webp`, `ahorrador-amazonas-1kg.webp` y `catalog-miel.webp`; **Nanolotes no tiene imagen (asset faltante)** y usa un mosaico tipográfico. Los iconos son SVG propios (interfaz, no sellos). Sustituye la exclusión de estrellas de `verified_copy.catalog_pdp_2026_09_28.reviews_usage` solo para la home. El único cambio de JS es ampliar el selector de carga diferida de imágenes a `#close-bands`. Sin commit ni publicación. Evidencia: `qa/2026-09-30-cierre-05/`.

**Complemento de L27 (30 de septiembre).** Instrucción literal del usuario: «extrae imagen para nanolotes». Se descarga la primera imagen de producto de la colección oficial de Nanolotes (NanoLote Typica, Bourbon y Caturra), original en `audit/source/nanolote-original.jpg`, derivado `public/assets/nanolote-tin.webp` con `scripts/prepare-nanolotes.py` (recorte rectangular, sin retoque) y registro `nanolote-tin` en `audit/assets.json` (`REAL_ASSET`, preparada `USABLE_WITH_PREPARATION`). Solo ilustra el mosaico de Nanolotes en la home; sustituye el mosaico tipográfico y el aviso de asset faltante de L27.
