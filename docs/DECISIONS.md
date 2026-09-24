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
