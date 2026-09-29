# Handoff — demo Artidoro, 28 de septiembre de 2026

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
