# Verificación del diagnóstico para la presentación — 1 de octubre de 2026

Revisión de solo lectura de artidororodriguez.com, para que la presentación (`deliverables/presentacion-artidoro.html`) muestre solo los hallazgos que siguen vigentes. Las puntuaciones son del análisis de conversión del 22.09.2026 (`docs/blueprint_convertmate_co_report_*.pdf`, archivo del usuario, no versionado). Por indicación del usuario, la presentación no nombra ese documento ni la herramienta: las presenta como «puntuación orientativa» que mide cuánto de las buenas prácticas de venta online ya está cubierto, con referencias públicas verificadas (web.dev/articles/lcp, baymard.com/blog/show-shipping-costs-on-product-pages, nngroup.com/articles/ecommerce-product-pages). Si preguntan cómo se calculó, la respuesta veraz está en las notas de la diapositiva 2: puntuación orientativa de una revisión automatizada, sin datos de visitas ni de ventas.

**Condiciones.** Chromium 148 (Python Playwright), celular 390 × 844 con agente de iPhone y computadora 1440 × 900, sin iniciar sesión ni llegar al carrito. Scripts: `capture_store.py` (capturas y datos de la primera pantalla; resultado en `store-evidence.json`) y `verify_findings.py` (comprobaciones por hallazgo; resultado en `findings-check.json`).

| Área | Hallazgo del 22.09 | 01.10 |
|---|---|---|
| Home | Sin señales de confianza en la primera pantalla | Sigue |
| Home | Titular = nombre de la marca | Sigue |
| Home | CTA «Explorar los orígenes» sin forma de botón | Sigue (enlace de 22 px de alto, sin fondo) |
| Home | Imagen del hero sin producto | Sigue (ahora un video de campo, sin producto) |
| Home | Prueba social fuera de la primera pantalla | Sigue (reseñas a ~3 250 px) |
| Home | FAQ con títulos de navegación | **Ya no aplica hoy**: 5 preguntas reales (no se sabe si cambió o si el análisis no lo vio) |
| Home | Sin sección «cómo funciona» | Sigue |
| Colecciones | Sin productos en la primera pantalla | Sigue (primera tarjeta a 832 px en 844) |
| Colecciones | Tarjetas sin precio | **Ya no aplica hoy**: las tarjetas muestran precio, precio normal tachado y etiquetas «PACK x % OFF» (verificado con captura el 01.10.2026) |
| Colecciones | Sin precios claros | **Ya no aplica hoy** |
| Colecciones | Sin badges | En parte: hay etiquetas de descuento en los packs, no estrellas ni «más vendido» (sigue vigente) |
| Ficha | Sin envío/devolución junto al botón | Sigue |
| Ficha | Galería sin primer plano ni escala | Sigue |
| Ficha | Botón fuera de pantalla y sin botón fijo | Sigue (botón a 1 522 px en celular) |
| Ficha | Rating lejos del precio | **Ya no aplica hoy**: estrellas junto al precio en Amazonas |
| Ficha | Sin precio tachado ni cuotas (Amazonas) | Sigue |
| Ficha | Sin sellos junto al precio | Sigue |
| Ficha | Venta cruzada sin incentivo | Sigue |
| Ficha | Sin video | Sigue |
| Ficha | Sin «cómo funciona» | Sigue |
| Velocidad | LCP 12,06 s · FCP 2,27 s · puntaje móvil 50/100 | No se volvió a medir (L30); cifras del 22.09 |

Resultado: **19 de 23 siguen vigentes y 4 ya no aplican hoy** (preguntas frecuentes, precio visible en las tarjetas, claridad de precios y estrellas junto al precio). No se atribuye el cambio al equipo de la tienda: no hay forma de saber si cambió desde el 22.09 o si el análisis automatizado no lo vio. Las etiquetas «PACK x % OFF» cuentan como cambio parcial y el punto sigue vigente (faltan estrellas y «más vendido»). La ficha oficial del pack también usa selectores de botón; no era uno de los 23 hallazgos. Corrección de la versión anterior de este documento y de la presentación, que decían «18» y «5 corregidos por su equipo» y «23 criterios».

Otros datos usados en la presentación: «Delivery gratis para compras arriba de S/. 280» (barra superior de la tienda, 01.10.2026), tomado como solo para Lima por indicación del usuario; precios del snapshot `audit/source/prices-2026-10-01.json`.

**Nota sobre Tienda.** Por indicación del usuario, la presentación muestra la puntuación 15 del 22.09 en el área Tienda. No se recalculó: no hay base para una cifra nueva sin repetir el análisis. El texto aclara que las tarjetas ya muestran precio y descuento y que el margen está en abrir con los productos y diferenciarlos.

## Referencias de mercado para la inversión (no se muestran en las diapositivas)
Consultadas el 02.10.2026 para ajustar los montos; solo aparecen en las notas del orador. Cifras tomadas de las páginas, sin verificar de forma independiente; el tipo de cambio (~S/ 3,7 por US$) es aproximado y no se verificó.

| Dato | Cifra | Fuente |
|---|---|---|
| Implementación de tienda Shopify o Tiendanube (plantilla) | S/ 1 500 a S/ 4 000 | ldxsoftware.com.pe, 13.06.2026 |
| Desarrollo 100 % a medida | S/ 12 000 a S/ 35 000 | ldxsoftware.com.pe, 13.06.2026 |
| Tienda básica / e-commerce avanzado | S/ 2 000 a S/ 4 500 / S/ 4 500 a S/ 10 000 | leveluperu.com, 2026 |
| Tienda con pasarela y catálogo cargado (agencia) | US$ 1 500 | flamacreators.com |
| Tarifa media de un desarrollador freelance en Perú | US$ 20 por hora (rango US$ 11 a 40) | freelancermap.com, 15.04.2025 |
| Sueldo medio de un programador front end en Lima | S/ 3 074 al mes (35 sueldos) | pe.indeed.com, actualizado 16.09.2026 |

Las diapositivas de inversión (opciones A y B, temporales hasta que el usuario elija) usan los montos que fijó el usuario: valor S/ 11 000, ya desarrollado S/ 5 000 e inversión S/ 6 000 en tres sprints (S/ 2 700, S/ 2 200 y S/ 1 100), sin IGV. La base de cálculo del precio no se registra aquí: el repositorio es público.
