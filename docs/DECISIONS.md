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
