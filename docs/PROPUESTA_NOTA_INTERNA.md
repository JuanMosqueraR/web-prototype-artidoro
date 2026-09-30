# Nota interna — propuesta Etapa 1 (solo para Juan)

29 de septiembre de 2026. Acompaña a [PROPUESTA_ETAPA1.md](PROPUESTA_ETAPA1.md). **No compartir con el cliente.** Son estimaciones del agente con supuestos visibles, no condiciones aprobadas por Juan ni por Artidoro (L23).

## Horas por bloque (una persona)

| Bloque | Horas |
|---|---|
| Revisión de tienda y plan técnico | 6–10 |
| Base del tema, encabezado, menú y pie | 8–12 |
| Home: 01 (6–9), 02 (10–14), 03 (8–12), 04 (3–5), 05 (6–9) | 33–49 |
| Ficha estándar y configuración de 8 productos | 12–18 |
| Ficha de pack | 10–16 |
| Colección y carrito hasta el pago | 6–10 |
| Mejoras de conversión: ahorro visible, molienda con opciones, envíos/cambios/calificación junto al botón, botón fijo en celular, productos y precios en la primera pantalla de colección | 10–16 |
| Rendimiento y medición | 8–12 |
| Pruebas en equipos y correcciones | 10–14 |
| Rondas de revisión | 6–10 |
| Publicación y monitoreo | 3–5 |
| Coordinación y guía | 5–8 |
| **Base** | **117–180** |
| Contingencia 15 % | 18–27 |
| **Total a cotizar** | **~135–207** |

Honorarios = horas × tarifa. Recomendación: presentar el rango y cerrar el precio en H1, después de ver la tienda por dentro.

Plazo, incluida la espera de las rondas:
- a 20 h/semana: unas 8–12 semanas (son las semanas entre corchetes de la propuesta);
- a 30 h/semana: unas 6–9 semanas.

## Datos pendientes de Juan

1. Tarifa por hora, o monto mínimo aceptable por este alcance.
2. Horas semanales reales y fecha posible de inicio.
3. Recibo por honorarios o factura; precios con o sin impuestos.
4. Fecha objetivo o campaña de Artidoro, si la hay; se puede preguntar en la reunión.

También hay que decidir: qué se devuelve si no continúan después de H1, el plazo del último pago si posponen la publicación (propuesto: 10 días hábiles), la duración del soporte (propuesta: 30 días), las horas del mantenimiento y el trato con el dueño («ustedes» o «tú»; la presentación usa «ustedes»).

## Supuestos

- La tienda es Shopify: las imágenes se sirven desde `cdn.shopify.com`. Plan y tema sin confirmar.
- El tema es moderno y editable por secciones, sin apps que interfieran.
- El Ahorrador tiene 125 variantes (3 × 5 orígenes), precio S/280 y precio normal S/330 (snapshot del 29/09). La molienda se escribe en un campo de texto libre, no es una variante: pasarla a opciones exige acordar la regla y cómo llega al pedido.
- Juan trabaja solo.

## Riesgos

- Un tema antiguo o muy modificado aumenta las horas. H1 existe para detectarlo.
- Si los anuncios del pack llevan directo a su ficha, cambiarla afecta al tráfico pagado: publicar fuera de campañas clave.
- La escena de la taza está generada con IA; usarla en la tienda real es una decisión de marca de Artidoro.
- Siguen abiertos la autoría de las fotos de Tarata, la ubicación del cafetal y la foto grupal del pack con etiquetas de 454 g (el 29/09 seguía siendo la misma imagen).
- Retrasos en materiales o respuestas; presión por añadir fichas o páginas.

## No afirmar ante el dueño

- Que El Ahorrador es el más vendido, el de mayor margen o que su campaña rinde. «Está en campaña» es una premisa de Juan, no un dato verificado.
- Cifras de conversión, ventas, ticket medio o velocidad medida con usuarios reales.
- Las cifras del informe CRO del PDF (LCP, puntajes, notas), ni el propio informe. Está en parte desactualizado; solo valen las observaciones propias del 29/09 (`docs/HANDOFF.md`).
- Que la demo ya es un tema Shopify o que se traslada tal cual.
- Que la escena de la taza, el cafetal o las fotos de Tarata son material oficial o verificado.
- Que la foto del pack representa el pedido elegido.
- Que los precios de la demo están vigentes: son snapshots del 28 y 29 de septiembre.

## Antes de la reunión

- La demo en GitHub Pages **no** incluye todavía el ahorro visible (L23): hay que reconstruir y publicar con `scripts/build-pages.py` si se quiere enseñar.
- Comprobar que «Continuar con mi pack» abre una combinación con stock.
- La presentación publicada (Artifact) está compartida con cualquiera que tenga el enlace; las notas del orador (tecla N) son visibles.
