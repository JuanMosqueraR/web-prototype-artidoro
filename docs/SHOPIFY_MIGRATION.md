# Mapa de migración a Shopify — 1 de octubre de 2026

Para quien vaya a construir el tema y para el equipo de Artidoro que lo mantendrá. Describe cómo llevar la dirección A de esta demo (home y las dos PDP) a la tienda Shopify **sin perder la capacidad de gestionar el contenido**. No es una aprobación de la fase de Shopify: esa decisión es del usuario (ver `DECISIONS.md`, O06 y L30).

## 1. Punto de partida

- **Tienda actual:** tema **Prestige 10.4.0** (theme store 855), observado en el HTML de la tienda el 1 de octubre de 2026.
- **Apps y servicios detectados en la página:**
  - Judge.me (reseñas);
  - Klaviyo (formularios y correo);
  - enlace de WhatsApp;
  - Microsoft Clarity;
  - píxeles de Meta, TikTok, Pinterest, X y Reddit;
  - servicios de Google.

  No se auditó su configuración.
- **Demo:**
  - HTML/CSS/JS sin dependencias (Vite);
  - unos 37 KB de JS propio;
  - precios y variantes copiados en snapshots fechados;
  - la compra termina en la tienda oficial.

## 2. Enfoque recomendado

Construir la experiencia como **secciones y bloques Online Store 2.0 dentro de una copia del tema actual**, no como un tema nuevo desde cero:

- **Se conserva lo que ya funciona:** checkout, apps instaladas, ajustes, políticas, idioma y menús.
- **Las secciones nuevas** (hero por scroll, carrusel de orígenes, «De la bolsa a tu taza», PDP renovada, selector del pack) llevan el CSS y JS de la demo a archivos de sección, con su `schema` para que el editor de temas permita cambiar textos, imágenes y orden.
- **Coste:** una copia personalizada de Prestige deja de recibir sus actualizaciones automáticas. Hay que decidir quién las aplica, o limitar los cambios a secciones nuevas que no toquen los archivos base.

## 3. Modelo de datos (lo que el equipo edita en el admin)

**Metafields de producto** (uno por café de origen; el mismo esquema sirve para los cinco):

| Campo | Tipo | Hoy en la demo |
|---|---|---|
| `origen.lugar` | texto | «Rodríguez de Mendoza, Amazonas» |
| `origen.altitud` | texto | «1.700–1.900 m s. n. m.» |
| `origen.variedades` | texto | «Caturra, Típica y Catimor» |
| `origen.tueste` | texto | «Medio» |
| `origen.notas` | texto | «Naranja y melaza» |
| `origen.frase` | texto | «Una taza cítrica, envolvente y con carácter» |
| `origen.mapa` | archivo (imagen) | mapa de origen |
| `origen.foto_bolsa_1kg` | archivo (imagen) | imagen que usa el selector del pack |

**Metafield de variante:** `rendimiento.tazas` (número) para «unas 16 / 30 / 65 tazas», o calcularlo en Liquid a partir del peso con 15 g por taza (FAQ oficial).

**Metaobjects** (contenido reutilizable que el equipo crea y ordena):

| Metaobject | Campos | Dónde se usa |
|---|---|---|
| Paso del proceso | número, título, texto, imagen | «Del cafetal a tu taza» (home y PDP) |
| Pregunta frecuente | pregunta, respuesta (texto enriquecido), etiquetas (general, envío, pack…) | FAQ de la home y de cada PDP |
| Cafetería | nombre, dirección, horarios, enlace a Maps, fotos | 04 «Nos vemos en Miraflores» |
| Mensaje de confianza | icono, título, texto, enlace | líneas junto al botón y franja de la home |

**Nativo de Shopify, ya no a mano:**
- precios, precio tachado y disponibilidad (`variant.price`, `compare_at_price`);
- iconos de pago (`shop.enabled_payment_types`);
- políticas de envío y devolución;
- botón «Añadir al carrito» real, en lugar del paso a la tienda oficial.

Desaparecen los snapshots y los scripts de precios de la demo.

## 4. Home (dirección A)

| Sección de la demo | En Shopify | Qué edita el equipo | Desarrollo |
|---|---|---|---|
| Hero «Del cafetal a tu bolsa» (video por scroll) | Sección propia; video en Archivos de Shopify; textos y CTA en ajustes | Textos, CTA, producto destacado, póster | Alto (JS del scroll, versión mobile, sin movimiento) |
| 02 «Encuentra tu origen» (carrusel) | Sección que lee una colección; notas y lugar desde los metafields | Qué cafés entran y en qué orden (colección) | Medio |
| 03 «De la bolsa a tu taza» | Sección con 4 bloques de imagen y texto | Imágenes y textos de cada paso | Medio (cruces ligados al scroll) |
| Moliendas | Sección con bloques (icono, nombre, métodos) | Todo | Bajo |
| Tienda, confianza, reseñas | Secciones con bloques de producto y app block de Judge.me | Productos destacados, mensajes, reseñas destacadas | Bajo/medio |
| Cafeterías | Sección que lista metaobjects «Cafetería» | Direcciones, horarios, fotos | Bajo |
| FAQ y «Sigue explorando» | Metaobjects «Pregunta frecuente» y bloques de colección | Todo | Bajo |

## 5. PDP (plantilla única para los cafés de origen)

Una plantilla `product.origen` con bloques. Sirve para los cinco orígenes sin trabajo extra por producto: cada café solo necesita sus metafields y sus fotos.

| Bloque | Implementación | Gestión |
|---|---|---|
| Galería con swipe, miniaturas y zoom | Lee `product.media` (fotos y video); JS de la demo | Fotos y video del producto en el admin, con su texto alternativo |
| Título, lugar, rating junto al precio | Metafields + app block de Judge.me (estrellas y recuento reales) | Automático |
| Tamaño con precio y tazas | Opciones de variante + `rendimiento.tazas` | Automático |
| El Ahorrador como cuarta opción | Bloque que referencia el producto pack (metafield `upsell.pack`, producto), con precio por kilo calculado en Liquid | Elegir el pack en el admin |
| Molienda con iconos y «Para empezar» | Variante `Tipo de molido` + iconos en el bloque | Etiqueta recomendada en ajustes del bloque |
| Botón, botón fijo, iconos de pago | Formulario de producto del tema + barra fija propia | Automático |
| Envío, tostado, pedidos dañados | Metaobjects «Mensaje de confianza» | Textos y enlaces |
| «Del cafetal a tu taza» | Metaobjects «Paso del proceso» | Imágenes y textos |
| Origen con mapa | Metafields `origen.*` y `origen.mapa` | Por producto |
| Reseñas | App block de Judge.me (lista completa, no una copia) | En Judge.me |
| Descubrir (Explorador, otros orígenes) | App Search & Discovery (productos complementarios) o metafield de lista de productos | En el admin |
| FAQ | Metaobjects «Pregunta frecuente» filtrados por etiqueta | Todo |

**Pack El Ahorrador.** Plantilla `product.pack`:
- **Variantes:** las 125 combinaciones ya existen en la tienda.
- **Selectores por bolsa:** una sección propia que muestra la imagen de 1 kg de cada origen, desde `origen.foto_bolsa_1kg`, y arma la variante.
- **Molienda:** sigue como nota del pedido, como hoy.
- **Atajo y precio:** «Las tres bolsas de…» y el ahorro calculado desde el precio tachado vienen con la sección.

## 6. Activos

- **Imágenes generadas con IA** (hero, 03, granos, moliendas): en la demo llevan el aviso de escena conceptual. Para producción conviene sustituirlas por fotografía real, o decidir explícitamente usarlas con su aviso.
- **Fotos oficiales** (bolsas, mapa, foto en la montaña): ya están en la tienda; se reutilizan como medios del producto.
- **Video del hero:** se sube a Archivos de Shopify. La secuencia de imágenes de respaldo de la demo es opcional: complica la gestión y solo sirve cuando el video no carga.

## 7. Rendimiento (L30)

En la demo no se vuelve a medir. En Shopify se mide en el tema con las apps instaladas, antes de lanzar. Presupuesto propio que conviene mantener:
- **Video del hero:** ~3,3 MB por formato, pedido después de la carga.
- **Imágenes de 03 y de las PDP:** diferidas hasta que hacen falta.
- **JS propio:** ~40 KB, sin librerías de animación.

Los píxeles y las apps detectados (sección 1) suelen pesar más que todo eso; conviene revisarlos en la misma medición.

## 8. Qué necesita desarrollo y qué no

- **El equipo, sin programar:** textos, imágenes, videos, orden de secciones, productos destacados, preguntas frecuentes, cafeterías, mensajes de confianza, datos de origen por producto y reseñas (Judge.me).
- **Desarrollo:**
  - crear las secciones y el modelo de datos al inicio;
  - cambios de estructura o comportamiento (scroll del hero, cruces de 03, selector del pack);
  - actualizaciones del tema base.

## 9. Riesgos y decisiones abiertas

- **Judge.me:** su widget solo se puede restilizar hasta cierto punto; para igualar el diseño de la demo puede hacer falta su API o un plan de pago.
- **Actualizaciones de Prestige** en una copia personalizada (sección 2).
- **Imágenes generadas** en producción (sección 6).
- **Alcance:** solo la dirección A está desarrollada; B no se migra salvo decisión contraria. No hay pruebas con usuarios (O07).
- **Medición:** eventos de analítica para comparar con la tienda actual (vistas de PDP, uso del selector del pack, añadir al carrito); no existen en la demo.
- **Avisos de la demo:** al pasar a producción hay que retirar «Demo», los avisos de laboratorio y los snapshots fechados.

## 10. Fases sugeridas

1. **Base:** copia del tema, modelo de datos (metafields y metaobjects) y carga de contenido de un origen.
2. **PDP:** plantilla `product.origen` y `product.pack`, Judge.me, iconos de pago y botón fijo. Es la parte con más peso de conversión según el informe CRO.
3. **Home:** secciones en el orden de la demo, empezando por las de menor complejidad (moliendas, tienda, cafeterías, FAQ) y dejando para el final el hero y 03.
4. **Cierre:** carga de los cinco orígenes, medición de rendimiento con apps, QA en iPhone y Android, y retiro de los avisos de demo.

## 11. Cobertura del catálogo y de la web actual (revisión del 2 de octubre de 2026)

Fuente: `products.json`, `collections.json` y el mapa del sitio públicos de la tienda, y una visita de solo lectura a la home (computadora). Es una foto de esa fecha.

**Catálogo: 32 productos publicados. La propuesta diseña la ficha de 6 (19 %).**

| Grupo | Productos | Ficha propia en la propuesta |
|---|---|---|
| Cafés de origen | 5 (Amazonas, Cajamarca, Villa Rica, Cusco, Puno) | Sí, una plantilla para los cinco |
| Packs de café | 8 (El Ahorrador, El Explorador, El Curioso, La Dupla, La Despensa, El Dulce Trato, El Cafetalero, Pack Regalo con taza) | Solo El Ahorrador |
| Packs de miel | 2 (El MelOSO, La GenerOSA) | No |
| Packs de microlotes | 2 (La Selección, Rupa Rupa) | No |
| Microlotes | 4 (Yanesha, Mazamari, Longar, Quilmaná) | No |
| Nanolotes | 3 | No |
| Travel Line y tote bags | 4 | No (Travel Line aparece como tarjeta en la home) |
| Infusiones | 2 | No |
| Mieles | 2 | No (la miel Perfil Frutal aparece como tarjeta en la home) |

Los 26 productos restantes conservarían la ficha actual del tema. Una plantilla de pack con número variable de bolsas (2 o 3) podría cubrir La Dupla, El Curioso, El Dulce Trato y La Despensa; es una decisión de alcance pendiente.

**Colecciones: 15** (`cafe`, `cafes-de-origen`, `packs-de-cafe`, `microlotes`, `nanolotes`, `mieles`, `infusiones`, `merch`, `cafeteras`, `los-mas-buscados`, `nuevos-ingresos`, `mes-del-cafe-peruano`, `para-el-papa-que-lo-merece`, `presentacion-250gr`, `cafe-peruano-artidoro-rodriguez`). La propuesta diseña una página Tienda; una plantilla de colección puede servir a las demás.

**Páginas: 14 y un blog con 3 historias**, sin diseño en la propuesta: contacto, cafetería, maquila, sobre nosotros, tostaduría, tueste, contacto empresas, locales, nuestra historia, socios e inversionistas, libro de reclamaciones, términos de servicio, HORECA y preguntas frecuentes; blogs `news`, `blog` e `historia`.

**Home actual frente a la home de la demo**

| Home actual | En la demo |
|---|---|
| Barra de anuncio «Delivery gratis para compras arriba de S/. 280» | No |
| Hero con video del campo | Sí, rediseñado |
| Franja «+83 pts SCA · Tostado cada semana · Envío gratis en Lima» | En parte (falta «+83 pts SCA», dato propio de la tienda) |
| Texto «Café fresco de verdad» y «Café fresco garantizado» | En parte (franja de confianza) |
| «Los más buscados» (colección con 45 productos) | En parte: selección fija de 5 en la sección Tienda |
| Preguntas frecuentes | Sí |
| «Nuestros clientes dicen…» (carrusel de reseñas) | En parte: 2 reseñas |
| «Trabajamos en pro de los caficultores peruanos…» | En parte: «Precio justo al caficultor» |
| Newsletter (Klaviyo) | No |
| Pie: quiénes somos, blog, preguntas frecuentes, política de envíos, términos y privacidad, **libro de reclamaciones**, café de origen, nuevos ingresos, más vendidos, encuéntranos, menú, eventos, venta al por mayor, capacitaciones | No: el pie de la demo es mínimo |
| Menú: Tienda, Tostaduría, Cafeterías, Explora con nosotros, Diario de viaje; cuenta, búsqueda y cesta | No: la demo solo tiene Tienda, Cafeterías y comprar |
| Enlaces a WhatsApp (3) | No |
| Ventana «Ganaste un café 250 g gratis» | No (a decidir) |

Para producción hay que conservar lo que ya existe en el pie y el menú actuales (libro de reclamaciones, términos y privacidad, búsqueda, cuenta y cesta) y el newsletter; hoy la demo no los muestra.
