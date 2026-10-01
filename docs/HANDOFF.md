# Handoff — demo Artidoro

## Actualización del 1 de octubre de 2026 (L29)

**Estado recuperable:** `master` va 7 commits por delante de `origin/master` (`f27473b`, L28 publicada en Pages); L29 (`dbd0e59`…) aún no está publicada. Árbol limpio salvo los cambios ajenos de siempre (`tools/apimart/*`, `reference/`, el PDF CRO, `.mcp.json`).

| Commit | Contenido |
|---|---|
| `dbd0e59` | Home: correcciones de la revisión, limpieza de textos, 04 «Nos vemos en Miraflores» con Tarata y La Mar |
| `ac1ab1d` | Registro de direcciones y horarios oficiales de las dos cafeterías |
| `6de9b6e` | QA de P1–P3 (143/143) |
| `f6a2b17` | Docs de L29 (rehecho sin el PDF CRO, que se había incluido por error en un commit local nunca publicado) |
| `cf13a83` | Nuevo orden de secciones (P4) y carga de fotos de los bloques de cierre |
| `496a097` | QA de P4 (154/154) |
| (siguiente) | Docs de P4 y estado de publicación |

**Qué hay y cómo se verificó:** detalle en [HOME_AUDIT_2026_09_30.md](HOME_AUDIT_2026_09_30.md#l29). El usuario probó P1–P3 y P4 en su iPhone («todo ok»); QA en Chromium en `qa/2026-10-01-revision/` y `qa/2026-10-01-orden/`. Sin Safari/iOS instrumental ni Firefox.

**Pendiente / decisiones del usuario:** `git push` a `master` para publicar L29; tras publicar quedan desactualizados la medición de rendimiento de la web publicada, `deliverables/presentacion-artidoro.html` y las capturas de A de QA anteriores. No implementados (no se nombraron): más reseñas publicadas, foto de La Mar, «Abierto ahora», enlace a cafeterías en el menú mobile. Lo demás pendiente de L28 (abajo) sigue igual.

## Actualización del 1 de octubre de 2026 (L28)

**Estado al cerrar L28:** `master` en `f5bb542`, entonces 7 commits por delante de `origin/master` (`4beaf0d`); L28 se publicó después con `f27473b`.

| Commit | Contenido |
|---|---|
| `fd19e35` | Assets del hero: videos de 24 fps constantes con limpieza de ruido, secuencias AVIF/WebP de respaldo, imagen de previsualización |
| `045e4c9` | Home: hero con video primero, swipe de 02, etiquetas para compartir, escenarios con viewport alto |
| `ed1fe7a` | QA de L28 tras las rondas de iPhone |
| `145fc5d` | Docs: complementos 1–7 de L28 y revisión de Forno |
| `73b0292` | 03 vuelve a su primera configuración ligada al scroll |
| `75a08db` | QA: ritmo legible por paso en 03 |
| `f5bb542` | Docs: octavo complemento |

**Qué hay y cómo se verificó:** hero, 03, franja de moliendas, swipe de 02 y etiquetas para compartir; el usuario los probó en un iPhone físico (Chrome iOS) y confirmó hero, 03 y swipe. QA automático de 107 controles en Chromium: [qa/2026-09-30-l28](../qa/2026-09-30-l28/README.md). Nada se probó en Safari/iOS instrumental ni en Firefox. Detalle: [HOME_AUDIT_2026_09_30.md](HOME_AUDIT_2026_09_30.md#l28).

**Pendiente / decisiones del usuario:**
- `git push` a `master` (dispara el despliegue en Pages); tras publicar, la medición de rendimiento de la web publicada y `deliverables/presentacion-artidoro.html` quedan desactualizados y no se regeneraron.
- Mejorar la nitidez de fondo exige regenerar los cuatro clips en 1080p (≈ US$ 1,80 por pasada; presupuesto APIMart restante ≈ US$ 4,6 de un tope de US$ 8). Sin aprobar.
- Hallazgos sin acción: KI-92 (horizontal), KI-93 (peso de Pages), KI-94 (respaldos sin probar en iPhone) en [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- La fase de PDP no se ha iniciado («aún no empecemos con PDP»).

---

# Handoff — 28 de septiembre de 2026 (histórico)

## Estado recuperable

El usuario pidió actualizar docs, commitear, integrar en `master` y preparar el paso a presentación/propuesta comercial. Se integró `feat/catalogo-pdp` en `master` por fast-forward desde `7b122b9` hasta `a5512e2`, sin conflictos. Incluye también el selector de 02 y el catálogo/PDP de Amazonas que aún no estaban en `master`. Las ramas de trabajo se conservan. Este handoff se añade después de esa integración mediante un commit documental; consultar `git log -1` para su hash.

Commits de esta entrega:

| Commit | Contenido |
|---|---|
| `f6f5337` | Alcance de El Ahorrador y autorización de cierre/merge (L21/L22) |
| `ab437b9` | Fotografías reales de 1 kg, fuentes, preparación y variantes |
| `8d770a6` | Accesos al pack, nueva jerarquía de 05 y PDP configurable |
| `adea9b3` | Evidencia de QA y capturas |
| `a5512e2` | Informe de entrega y documentación descriptiva |

Checkpoint anterior al pack: `87ea725`. No hubo push ni publicación de esta revisión; actualizar `master` local no actualiza GitHub Pages. No asumir que el enlace público muestra este código. No se tocó `AGENTS.md` ni `CLAUDE.md`.

Quedan fuera de los commits, intactos, los cambios preexistentes de `tools/apimart/README.md`, `cli.cjs`, `client.cjs`, `pricing.cjs`; `reference/` y el PDF `docs/blueprint_convertmate_co_report_dc24a3cb_4d38_4376_bf4a_4112fa4a5dc0.pdf` siguen sin seguimiento. No usar `git add .` ni limpiar/stashear esos archivos para la siguiente tarea. El árbol no está limpio únicamente por esas exclusiones.

## Qué está construido

Dirección A «Perú, en profundidad», home navegable 01→05 y dos PDP de demostración. Es una demo comercial independiente, no un tema Shopify instalado ni una tienda lista para producción.

- 01: presencia visual de marca, café Amazonas con precio/CTA, acceso secundario a El Ahorrador.
- 02: cinco orígenes, carrusel horizontal y ficha compacta; selección local, no gobierna el resto de la home. Acceso adicional al pack.
- 03: momento sensorial central, video controlado por scroll, poster, carga diferida y movimiento reducido. El usuario pidió no seguir iterándolo.
- 04: pausa breve de Tarata con fotos de interior y fachada/moto; guiño al dueño aportado por el usuario, sin convertir la marca en un concepto de motos.
- 05: El Ahorrador protagonista, Travel Line segundo, Explorador/miel complementarios, categorías, dos reseñas atribuidas y FAQ.
- `#producto-amazonas`: doce variantes reales; tamaño/molienda y continuación a la tienda oficial.
- `#producto-ahorrador`: tres bolsas de 1 kg, cinco opciones por bolsa, repetición permitida, 125 variantes reales. Molienda en la tienda oficial. Foto de combinación representativa, no imagen dinámica del pedido.

B queda conservada como hero del laboratorio, no como una segunda home ni como resultado de una prueba de conversión.

## Qué significa para el negocio

Intención: unir deseo de marca, facilidad para elegir y acceso a compra. El diagnóstico CRO aportado por el usuario señalaba impulso de compra bajo, propuesta/CTA débiles en hero, producto/precio enterrados, pocas señales para decidir y problemas de rendimiento. La demo responde con compra temprana, selector mobile compacto, pack accesible antes del tramo cinematográfico y una resolución comercial explícita. Estas son decisiones e hipótesis de diseño; no resultados demostrados en ventas.

El Ahorrador se priorizó porque el usuario lo señaló como pack con ads activas. No se auditó rendimiento ni se confirmó que sea el más vendido o de mayor margen. Precio S/280 y variantes: snapshot oficial del 28 de septiembre. Travel Line conserva presencia. No confundir el ticket mayor de un pack con un aumento demostrado de ticket medio o rentabilidad.

El siguiente encargo recomendado debe convertir esta dirección en una experiencia operativa sobre la tienda real, sujeto a revisar tema, apps, estructura de productos/packs y accesos. Eso es una propuesta pendiente, no alcance ya contratado ni permiso para tocar producción. No prometer trasladar el HTML de Vite directamente a Shopify sin adaptación.

## Evidencia y límites que sobreviven a la sesión

Entrega: [AHORRADOR_REVIEW.md](AHORRADOR_REVIEW.md). Capturas actuales en `qa/2026-09-28-ahorrador/after/`: home completa, 05 y ambas PDP, desktop/mobile. No usar las galerías antiguas como si representaran el último cierre comercial. Fuentes: `audit/assets.json`; precios/variantes son estáticos.

QA ya completado sobre este código: 211/211 regresión, 316/316 pack, dos destinos oficiales, cuatro comprobaciones adicionales. Chromium 148.0.7778.96, DPR 1, contrato 1440×900 y 390×844, ambos keyframes/movimientos; medidas adicionales y límites en el informe. El build se volvió a ejecutar correctamente al cerrar los commits. Al integrar por fast-forward no se alteró código ni fue necesario sobrescribir capturas o repetir toda la suite.

El usuario confirmó iPhone para selector/catálogo anteriores. Esta última iteración del pack sigue pendiente en Safari/Chrome físicos. No hay resultados de conversión, medición de campo de Core Web Vitals ni checkout completo verificado.

Gaps para producción: ubicación del paisaje no confirmada; autoría/licencias de fotos de Tarata sin cerrar; 03 conceptual generado, no evidencia del origen/proceso/local; arte maestro de B pendiente; materiales/copy definitivos por aprobar. La foto grupal oficial del pack tiene etiquetas de 454 g: por eso la demo compone fotos individuales auténticas de 1 kg. Los avisos provisionales permanecen. Ninguno de estos gaps autoriza otra ronda de diseño por sí solo.

## Retomar sin gastar contexto innecesario

Leer primero `AGENTS.md`, `docs/DECISIONS.md` y este handoff. Para presentación/propuesta bastan luego `docs/AHORRADOR_REVIEW.md`, `docs/CREATIVE_DIRECTIONS.md` (actualización superior), `docs/ASSET_AUDIT.md` (actualización superior) y las capturas actuales relevantes. Consultar código, inventario y PDF solo para resolver una afirmación concreta. `PROJECT_BRIEF.md` conserva debajo su brief histórico; no usarlo para negar el alcance posterior autorizado en L18–L22.

No repetir QA, generar media, construir otra galería, rediseñar 03, editar la web, publicar ni hacer más commits para redactar la presentación. El usuario pidió un argumento breve y una propuesta concreta, con poca planificación adicional.

Prompt combinado para Claude: [CLAUDE_PRESENTACION_PROMPT.md](CLAUDE_PRESENTACION_PROMPT.md). Produce dos piezas coherentes: guion de demo y propuesta del siguiente trabajo. No fija tarifa/plazo sin supuestos visibles y confirmación de Juan.

## Entorno local

Windows PowerShell, Python 3.10, Vite 7.1.3. Se verificó Node aislado `C:/tmp/node22/node-v22.23.1-win-x64/node.exe` v22.23.1; Node global 18 no cumple. No actualizar tooling como parte de una tarea comercial. Antes de ejecutar comandos en otra sesión comprobar versiones y puertos.

Preview usado: `http://127.0.0.1:4175/`, rutas `#producto-amazonas` y `#producto-ahorrador`; requiere servidor activo. En caso de necesitar arrancarlo, después de verificar entorno:

```powershell
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js build
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js preview --host 0.0.0.0 --port 4175 --strictPort
```

El build escribe `dist/`, ignorado por Git. Para Pages existe `scripts/build-pages.py`; leer antes de ejecutar y publicar solo con autorización explícita. No incluir el build local anterior como evidencia de un despliegue nuevo.

## Actualización, 29 de septiembre de 2026

El usuario confirma que probó esta iteración del pack en un iPhone físico sin problemas y que la versión actual está publicada en GitHub Pages. Es confirmación del usuario: el agente no hizo la prueba en iPhone. Sobre Pages, el agente solo comprobó que `https://juanmosquerar.github.io/web-prototype-artidoro/` responde y que su HTML incluye `#producto-ahorrador`, `#producto-amazonas` y las secciones 02–05; no verificó su render ni su comportamiento. Las menciones anteriores a la prueba de iPhone pendiente y al enlace público desactualizado quedan superadas por esta actualización.

Presentación para la reunión con el dueño: [`deliverables/presentacion-artidoro.html`](../deliverables/presentacion-artidoro.html), escrita manualmente, con notas del orador (tecla N) y enlaces a la demo publicada. Usa fuentes y fotos de `public/assets/` y capturas de `qa/2026-09-28-ahorrador/after/` por ruta relativa: abrir desde el repositorio. La propuesta comercial y su nota interna se entregaron en el chat y no están en el repo; la forma de pago que indicó el usuario es 20 % al aceptar, 40 % con la vista previa completa y 40 % al publicar. Tarifa, capacidad, condiciones fiscales y fecha objetivo siguen pendientes. Nada de esto es un alcance contratado ni autoriza trabajar en la tienda.

## Revisión de la tienda actual y presentación de 12 diapositivas, 29 de septiembre de 2026

A petición del usuario, la presentación incorpora hallazgos de conversión sin citar el informe CRO del PDF. Sus cifras (LCP, puntajes, notas) no se usan: no tienen fuente verificable y el informe está en parte desactualizado. Solo se presentan observaciones propias.

- **Condiciones.** Revisión de la tienda pública del 29.09.2026 (home, `/collections/cafe`, `/products/pack-3kg-origenes-1`) con Playwright y Chromium 148, DPR 1, a 1440×900 y 390×844. Se bloquearon analítica, píxeles y Klaviyo, y no se llegó al carrito. Capturas y `captures.json` en `qa/draft-2026-09-29-tienda-actual/`, carpeta ignorada por Git. El filtro también bloqueó recursos del pago acelerado de Shopify, así que esos botones pueden faltar en las capturas.
- **Ya presente en la tienda.**
  - Envío gratis desde S/110, en la barra superior.
  - Precios con ahorro en colecciones y en la ficha del pack (precio normal S/330, oferta S/280).
  - Mensajes de tostado semanal y de envíos a todo el Perú.
  - Reseñas y preguntas frecuentes en la home.
  - Bloque «¿Cómo funciona?» en la ficha del pack.
- **Oportunidades confirmadas.**
  - La primera pantalla de la home muestra la marca, sin producto ni precio, y con un enlace de texto como llamada a la acción.
  - La colección de cafés abre con imagen y texto antes de los productos, en computadora y celular.
  - En la ficha del pack en celular, el botón de compra llega tras quince selectores, sin plazo de envío, cambios ni calificación a su lado.
- **Contradicen el informe.** Las tarjetas de colección sí muestran precio, y la home sí tiene señales de confianza y preguntas frecuentes, aunque fuera de la primera pantalla.
- **Para la implementación futura.** La molienda del pack se indica en un campo de texto libre, no mediante variantes. No se presenta como defecto.
- **Velocidad.** La API de PageSpeed Insights sin clave devolvió 429 (cuota diaria agotada) en los dos intentos. En la presentación la velocidad figura sin cifra, como medición pendiente al empezar.

Cambios en la presentación:
- dos diapositivas nuevas: «Buena base. Espacio para crecer.» (revisión) y «Del antojo al carrito.» (oportunidad → lo que hace la demo → lo que se sumaría en la tienda);
- una palanca de conversión en cada parada;
- la Etapa 1 ampliada con envíos, cambios y calificación junto al botón, colecciones con precios a la vista y medición con punto de partida;
- el cierre «La comanda» en lugar de «Gracias».

Las mejoras sugeridas forman parte de la propuesta, no son cambios en la demo. La estimación de horas de la propuesta, entregada en el chat, se amplía en consecuencia.

## Presentación publicada como Artifact, 29 de septiembre de 2026

A petición explícita del usuario, la presentación se publicó como Artifact privado de claude.ai: https://claude.ai/artifact/NxqnsgrjQ4cvEoFVAaiTKJ (versión 1, título «Propuesta Artidoro Rodríguez»). Solo pueden abrirla el propietario y quienes él invite desde el menú Compartir de la página.

- **Cómo se generó la copia.** Se parte de `deliverables/presentacion-artidoro.html` y se hacen tres transformaciones: se quita el esqueleto `html/head/body` (lo aporta el visor), se incrustan las tres fuentes como data URI y se aplanan las rutas a `assets/` (logos y bolsa Amazonas) y `capturas/` (siete capturas de `qa/2026-09-28-ahorrador/after/`), publicadas junto a la página. El script de transformación quedó en el scratchpad de la sesión, fuera del repo. Para actualizar el Artifact desde otra sesión, hay que repetir esas transformaciones y publicar con la URL anterior.
- **Cambios que también quedan en el archivo del repo.**
  - Título «Propuesta Artidoro Rodríguez».
  - Fuente explícita en `body`, porque el visor fija `system-ui`.
  - Márgenes de área segura en controles y notas.
  - Aviso para girar el teléfono en vertical estrecho, con un margen lateral de 16 px.
  - Tolerancia a fallos de pantalla completa y de `history.replaceState`.
- **Qué se verificó.** Una sola vista previa local de la copia (Chromium 148, DPR 1, 1600×900 y 390×844, sin errores ni imágenes rotas), antes de corregir la fuente de `body`. No se revisó el render en el visor de claude.ai. Las notas del orador están dentro de la página (tecla N): cualquiera con acceso puede verlas.

## Ahorro visible, propuesta en el repo y script de publicación, 29 de septiembre de 2026 (L23)

- **Demo.** La tarjeta del pack en 05 y la PDP de El Ahorrador muestran el precio normal tachado S/ 330.00 y «Ahorras S/ 50». El dato procede de `audit/source/ahorrador-2026-09-29.json`, verificado hoy en JSON y HTML. 01 y 02 no cambian. QA en `qa/2026-09-29-ahorro/`: regresión 211/211, pack 316/316 y ahorro 20/20; hero A/B idéntico. **GitHub Pages no incluye este cambio**: para enseñarlo desde el enlace público hay que reconstruir con `scripts/build-pages.py` y publicar, algo que hace el usuario.
- **Propuesta.** Borrador en `docs/PROPUESTA_ETAPA1.md`, con pagos 20/40/40 y las mejoras de conversión dentro del alcance. La nota interna con horas (unas 135–207 con contingencia), supuestos, riesgos y lo que no debe afirmarse está en `docs/PROPUESTA_NOTA_INTERNA.md`. Tarifa, capacidad, impuestos y fecha siguen pendientes.
- **Presentación y Artifact.** La presentación usa ahora las capturas del 29/09 y menciona el ahorro. La copia publicable se genera con `python scripts/build-presentation-artifact.py`, que escribe en `dist/presentation-artifact/` e imprime el mapa de archivos. Se republicó en la misma URL como versión 2. El Artifact figura ahora compartido con «cualquiera con el enlace», un cambio de ajustes hecho fuera de esta sesión. Esto sustituye la nota anterior de que el script de transformación quedaba en el scratchpad.
- **Notas anteriores resueltas.** La foto grupal oficial del pack sigue siendo `packelahorrador.jpg?v=1789062040`, con etiquetas de 454 g: la discrepancia sigue vigente. Las menciones a la prueba de iPhone pendiente en README, IMPLEMENTATION_STATUS y AHORRADOR_REVIEW llevan ahora un aviso de actualización.
