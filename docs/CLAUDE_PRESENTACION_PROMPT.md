# Prompt para Claude — presentación y siguiente encargo

Copia el bloque siguiente en una sesión nueva de Claude Code, abierta en este repositorio. Es una tarea de redacción comercial; no requiere generar un deck ni modificar la demo.

```text
Trabaja en D:\proyectos\artidoro\artidoro-hero-lab.

Quiero preparar una reunión con el dueño de Artidoro Rodríguez para mostrar la demo y proponer el siguiente trabajo. Necesito dos piezas breves y coherentes: una presentación que conecte diseño y negocio, y una propuesta concreta para contratar la implementación siguiente. Haz el trabajo; no me devuelvas otra ronda extensa de planificación.

Empieza con git status. Lee AGENTS.md, CLAUDE.md, docs/DECISIONS.md y docs/HANDOFF.md. Después consulta docs/AHORRADOR_REVIEW.md y las capturas actuales que necesites en qa/2026-09-28-ahorrador/after/. Usa el repositorio como memoria. Las autorizaciones posteriores al Hero Lab están en L18–L22; no confundas snapshots antiguos con el alcance actual. No necesitas leer todos los JSON, ejecutar QA ni investigar nuevamente toda la marca. Usa fuentes puntuales si hay algo que no puedas sostener.

Contexto que debes conservar:
- Ecommerce de café primero; la cafetería física es secundaria.
- Dirección A: Perú, en profundidad. 01 presencia, 02 elección, 03 deseo, 04 cercanía, 05 compra.
- 03 es el momento cinematográfico y no se va a iterar ahora. No gobierna el acceso a compra. 02 tampoco condiciona toda la narrativa.
- El Ahorrador lidera 05 y se ofrece desde 01/02. Travel Line es la segunda propuesta; hay otros cafés, packs y complementos.
- Hay dos PDP de demostración: Amazonas y El Ahorrador. Sus variantes llevan a la tienda oficial; no existe integración de carrito/checkout propia.
- La premisa de ads activas del pack viene de mí. No afirmes que es bestseller, que tiene mejor margen ni que conocemos el rendimiento de la campaña.
- Esta demo no es una tienda Shopify lista para lanzar. No prometas resultados de ventas, porcentajes de conversión ni performance de campo que no se han medido. Los materiales provisionales y la última prueba física de iPhone pendiente están en el handoff.

Entrega 1 — presentación para el dueño:
1. Un argumento central de 80–120 palabras, sencillo y específico de Artidoro.
2. Un guion hablado de 3–4 minutos con un máximo de cinco paradas de la demo. Indica qué mostrar y qué decir. En cada parada conecta una decisión visible con una necesidad comercial, sin atribuir causalidad ni resultados que no tenemos. Muestra pronto el pack y termina en la compra.
3. Un cierre de 30 segundos que invite a contratar el siguiente paso, sin presión artificial.
No hagas una exposición de herramientas/IA/código ni una crítica despectiva a su web actual. Usa las capturas o la demo existente; no produzcas slides, imágenes o video todavía.

Entrega 2 — propuesta comercial de una o dos páginas:
Recomienda UNA oferta acotada para convertir esta dirección en una experiencia operativa en su tienda actual. Considera Shopify, pero deja la solución técnica sujeta a revisar tema, apps y datos reales. Evita headless o desarrollos propios complejos sin necesidad comprobada.
Incluye objetivo; alcance con número de plantillas/páginas y productos a configurar; entregables verificables; exclusiones; revisiones incluidas; hitos y plazo estimado; inversión en soles; forma de pago; soporte posterior delimitado y tratamiento de cambios de alcance.
Aclara qué se reutiliza de la demo y qué requiere adaptación/producción. Delimita home, navegación/categorías, PDP estándar y packs, carrito e integración con el checkout existente, QA mobile, rendimiento, medición y puesta en marcha. Decide qué entra en esta oferta y qué queda fuera; no presupuestes una migración ilimitada ni todas las PDP a medida. Indica criterios de aceptación verificables sin prometer una puntuación universal o un aumento de ventas.
En inversión separa honorarios, licencias/apps, producción de material y mantenimiento. El precio S/280 es del producto, nunca el presupuesto de desarrollo. Si no conoces mi tarifa, capacidad semanal, fecha objetivo o condiciones fiscales, hazme UNA ronda corta de preguntas, máximo cuatro. Mientras respondo, prepara el resto. Puedes proponer horas por bloque, contingencia y plazo con supuestos explícitos; no inventes una cotización cerrada ni uses supuestas tarifas de mercado. Deja un borrador pendiente de esos datos y ciérralo con mis respuestas. No presentes tus estimaciones como condiciones ya aprobadas por mí o por Artidoro.

Qué pedir a Artidoro, organizado por momento de entrega:
- Marca/materiales: logos y packaging maestros, fotos definitivas y permisos, material de origen y cafetería, decisión sobre media conceptual y copy final.
- Comercial: productos/variantes, gramajes, precios/stock, reglas de packs y molienda, prioridades de campaña, márgenes si desean compartirlos, envíos/devoluciones/pagos, reseñas autorizadas, responsable de aprobar.
- Accesos: invitación de colaborador con permisos mínimos al tema de trabajo y catálogo; inventario de apps/integraciones; acceso autorizado a analítica si existe. No pedir contraseñas por chat. Trabajar sobre un tema no publicado y acordar respaldo, revisión y autorización de lanzamiento.
Marca qué es necesario para cotizar, para iniciar y para lanzar. El calendario parte de anticipo/accesos/materiales acordados, no de una fecha imaginada.

Separa en una nota interna final para mí los supuestos, riesgos, decisiones comerciales pendientes y datos que no deben afirmarse ante el dueño. Mantén las dos piezas principales listas para conversar con él, con lenguaje natural y sin jerga.

Responde primero en el chat. No modifiques implementación, instrucciones, assets, reference/, tools/apimart/* o el PDF CRO. No generes archivos de presentación ni hagas commits, push o publicación. No contactes al cliente. Detente al entregar la redacción y las preguntas imprescindibles para cerrar presupuesto/plazo.
```
