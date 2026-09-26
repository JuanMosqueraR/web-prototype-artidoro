# Assets de la home — revisión del 26 de septiembre de 2026

Actualización descriptiva de la fase L18. `audit/assets.json` sigue siendo el registro canónico de fuentes, dimensiones, preparación, clasificación y hashes. La tabla histórica que sigue conserva los usos anteriores; esta sección registra los usos actuales sin convertir material provisional en oficial.

- **Producto real:** Amazonas y Cajamarca conservados; Villa Rica, Cusco y Puno descargados de las fotos oficiales del catálogo, con snapshot fuente en `audit/source/home-catalog-2026-09-25.json`. Los cinco recortes de bolsa son derivados preparados, sin redibujo ni alteración de las etiquetas. Cajamarca ya no se limita a 02: también aparece en 03/05. Precios/variantes y enlaces verificados el 25 de septiembre; notas con fuentes en `verified_copy`. La nota «dulce» de Villa Rica procede de la web, mientras la etiqueta visible enumera frutos rojos y pasas; se registra la diferencia.
- **03 conceptual:** cuatro stills Nano Banana Pro y dos clips Kling V3 mediante APIMart, autorizados para esta demo. Packaging, logotipo, copy y UI quedan fuera del video generado. No es evidencia de origen, proceso, local o menaje oficial. Prompts, parámetros, tareas, costes y originales: `audit/source/scene03-generation.json`. La generación es no determinista; la compresión y extracción de frames sí son reproducibles desde los archivos retenidos.
- **Tarata (L19):** `tarata-facade.webp` y `tarata-interior{,-mobile}.webp` son derivados de las referencias aprobadas `02-facade-motorcycle.jpg` y `05-counter-staff-2.jpg`. Sus originales se copiaron byte a byte a `audit/source/`; preparación reproducible con `scripts/prepare-tarata-editorial.py` (Pillow: orientación, resize y WebP). Sin IA, retoque, sustitución de branding ni cambios en personas/moto/cascos. Clasificación `USABLE_WITH_PREPARATION`, condición provisional por autoría/licencia y fecha de captura sin confirmar; no se presentan como material oficial autorizado. Las anteriores imágenes conceptuales de Tarata se conservan archivadas, fuera de la home. `reference/` permanece intacto. Dimensiones, bytes y hashes solo en el registro canónico.
- **Paisaje:** dos WebP responsive desde el fotograma ya auditado. Misma localización sin confirmar y aviso `PROVISIONAL_ASSET`; no son nuevas fotografías ni prueba geográfica.
- **Tipografía:** Barlow Condensed se convierte de TTF a WOFF2 con fontTools, conservando los glifos y métricas. Chivo y logos existentes se reutilizan sin reconstrucción.

Derivados preparados mediante `scripts/prepare-home-assets.py` y `scripts/prepare-scene03-video.py`; rutas y funciones en [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md). Costes de producción y límites: [HOME_REVIEW.md](HOME_REVIEW.md). Ningún material conceptual se reclasifica como `REAL_ASSET`.

---

## Snapshot histórico del inventario — 23/24 de septiembre de 2026

# Asset audit — consolidación para el handoff

Inventario del proyecto entregado, revisado el 23 de septiembre de 2026. Las rutas de las tablas son relativas a la raíz del proyecto, no a `/docs`.

[Audit original](../audit/ASSETS.md) conserva el resumen inicial. [Manifest de fuentes](../audit/assets.json) es la referencia para URLs exactas de CDN, tamaños originales, timecode y preparación; no se duplica íntegramente aquí. Este documento añade el mapa de archivos actualmente presentes y su condición de uso.

**REAL_ASSET indica procedencia real, no aprobación definitiva para producción.** USABLE_WITH_PREPARATION identifica un material derivado/preparado para el lab. MISSING_ASSET significa que el archivo necesario no está disponible en este proyecto; no afirma que la marca no lo posea.

## REAL_ASSET

| Asset | Dónde se encontró | Archivo en el proyecto | Uso | Condición |
|---|---|---|---|---|
| Foto oficial de bolsa Amazonas 250 g | [Ficha de café Amazonas](https://www.artidororodriguez.com/products/cafe-amazonas), archivo CDN `250GAMAZONAS.jpg` | `audit/source/amazonas-original.jpg` | A y B, mediante recorte preparado | Fuente real del producto común. Seleccionada para el experimento; no implica aprobación de producción. |
| Foto oficial de bolsa Cajamarca 250 g | [Ficha de café Cajamarca](https://www.artidororodriguez.com/products/cafe-cajamarca), archivo CDN `250GCAJAMARCA.jpg` | `audit/source/cajamarca-original.jpg` | Escena 02 (24 sept. 2026), mediante recorte preparado | Fuente real. Solo se usa en 02; no sustituye a Amazonas en los heroes. Detalles en `audit/assets.json` (id `cajamarca-bag`). |
| Logotipos blanco y negro | Web oficial; URLs individuales en el manifest, id `logos` | `public/assets/logo-white.png`, `public/assets/logo-black.png` | Blanco en A; negro en B | Assets reales, sin marcador provisional; márgenes transparentes recortados. |
| Ilustración botánica de la bolsa habitual | Integrada en la foto oficial del packaging | Dentro de `audit/source/amazonas-original.jpg` y `public/assets/amazonas-250g.webp` | A y B | Real y conservada en la foto. No existe un archivo independiente del dibujo en el proyecto. |
| Chivo regular y bold | Fuentes servidas por la web oficial; id `body-type` | `public/assets/chivo-regular.woff2`, `public/assets/chivo-bold.woff2` | A y B | Tipografía real reutilizada localmente, sin marcador provisional. |

## USABLE_WITH_PREPARATION

| Asset preparado | Origen y preparación | Archivo en el proyecto | Uso | Condición |
|---|---|---|---|---|
| Bolsa recortada con transparencia | Foto oficial; máscara de silueta y WebP, sin cambiar etiqueta ni contenido fotografiado | `public/assets/amazonas-250g.webp` | A y B | Recorte final de este lab. Fuente limitada: la bolsa ocupa aproximadamente 310 × 747 px en la foto original. No es una nueva fotografía de alta resolución. |
| Bolsa Cajamarca recortada con transparencia | Foto oficial; mismo polígono de silueta y recorte que Amazonas, validado contra la foto de Cajamarca; sin cambiar etiqueta ni contenido fotografiado | `public/assets/cajamarca-250g.webp`; script `scripts/prepare-cajamarca.py` | Escena 02 | Misma limitación de resolución que Amazonas (326 × 761). Registro estructurado en `audit/assets.json`. |
| Cafetal, plano lejano | Fotograma 00:02.500 de video de la [home oficial](https://www.artidororodriguez.com/), 1280 × 720 | `audit/source/artidoro-landscape-still.jpg`; `public/assets/cafetal-provisional.webp` | A | **PROVISIONAL_ASSET. Ubicación geográfica sin confirmar.** |
| Cafetal, plano cercano | Recorte con transparencia gradual de la misma foto, no una segunda toma ni vegetación inventada | `public/assets/cafetal-foreground.webp` | A | **Provisional**, con la misma incertidumbre geográfica. El video original no forma parte del proyecto distribuido. |
| Otorongo extraído y trazado | Foto pública `LATASCONJUNTO…png` de [Travel Line](https://www.artidororodriguez.com/products/la-expedicion-coleccion-travel-line-preventa). Recorte de 164 × 195 px sobre una lata curva, extracción de tinta y trazado determinista | `audit/source/otorongo-curved-tin-detail.png`; intermedio `audit/source/otorongo-extract.webp`; utilizado `public/assets/otorongo-traced.svg` | B | **PROVISIONAL_ASSET.** El SVG deriva de una imagen pequeña e incompleta; no es el arte maestro. No se reconstruyó anatomía faltante. La foto conjunta completa no se incluyó en el paquete final; su URL sí consta en el manifest. |
| Verde Amazonas y tinta | Aproximación a partir del packaging Travel Line | Variables `--green: #30bc4e` y `--ink: #0f1d12` en `src/common.css` | B como lenguaje gráfico | **Provisional como especificación cromática.** No es un brandbook oficial ni color homologado. No tiene archivo raster independiente. |

## CONCEPTUAL_ASSET (solo CP04, L15–L17)

Imágenes intervenidas con IA a partir de fotos de referencia del local de Tarata. **No son evidencia documental del local** y deben seguir identificadas como conceptuales/provisionales. Las fotos base proceden de Google Maps, con **autoría sin confirmar**, y se usan solo para esta demo; están en `reference/tarata/` (sin versionar), no en `audit/source/`. Modelo, task_id, prompts y regiones de branding restauradas: `audit/assets.json` (ids `cp04-entrada`, `cp04-mesa`).

| Asset | Base | Archivo en el proyecto | Uso | Condición |
|---|---|---|---|---|
| CP04 estado 1 “Desde la entrada” | `reference/tarata/02-facade.webp` (vista desde la puerta) | `public/assets/cp04-entrada.jpg` | CP04 (escena 04) | Luz de tarde y limpieza con IA. Rótulos de los sacos, hexágono del fondo y placa hexagonal de la estantería restaurados con píxeles de la foto base. Quedan textos pequeños deformados en bolsas del fondo. Sin guiño visible a los cascos (L17). |
| CP04 estado 2 “Desde la mesa”, versión A | `reference/tarata/03-counter-perspective-3.webp` | `public/assets/cp04-mesa.jpg` | CP04 (escena 04) | Luz de tarde y limpieza con IA. Hexágono de la barra restaurado con píxeles de la foto base. Sin cascos (L17). |

Preparación manual y no reproducible: los pasos generativos no son deterministas y la restauración se hizo con un script local ad hoc que no está en `scripts/`.

## MISSING_ASSET

| Material faltante | Situación / fuente necesaria | Archivo local | Dirección | Estado |
|---|---|---|---|---|
| Paisaje atribuido a Rodríguez de Mendoza / Amazonas | Falta evidencia de localización y material adecuado con profundidad/separación de planos | No disponible; se usa el fotograma señalado arriba | A | Pendiente. El nombre del origen del producto no prueba dónde se filmó el video. |
| Arte maestro completo del otorongo | No se obtuvo vector original ni imagen completa de alta resolución | No disponible; `otorongo-traced.svg` no cubre este gap | B | Pendiente. Requiere original para juzgar acabado definitivo. |
| Arte botánico independiente del packaging | Solo se dispone de la ilustración dentro de la fotografía de la bolsa | No disponible como archivo independiente | Referencia potencial para ambas; no se utiliza separado | Pendiente, no necesario para ejecutar este lab. |
| Mapas o texturas propios en archivos independientes | No se obtuvieron materiales verificables de esta clase en el paquete | No disponibles | Ninguno incorporado | Gap del inventario; no implica aprobar su producción o uso posterior. |

## Elecciones del lab que no son assets oficiales de Artidoro

- **Barlow Condensed ExtraBold:** `public/assets/barlow-condensed-800.ttf`, procedente de Google Fonts; URL en el manifest, id `display-type`. Se utiliza en ambas direcciones. Es una elección tipográfica nueva del experimento, no una fuente preexistente de marca que hayamos verificado.
- Verde oscuro de A (`#102e25`), crema (`#f4f0e5`), degradados, sombras, líneas de anotación y pequeño icono SVG de confianza: recursos de interfaz del laboratorio. No se presentan como texturas, ilustraciones o sellos oficiales. El icono no representa una certificación externa.

## Acceso, atribución y límites

Instagram tuvo acceso parcial/login. No se afirma una auditoría completa de publicaciones, reels o stories; no se utilizaron assets exclusivos del feed.

Fuera de CP04 no se generaron imágenes mediante IA; las dos excepciones de CP04 (L15) se listan arriba como CONCEPTUAL_ASSET. Extraer un fotograma, recortar la bolsa o trazar determinísticamente tinta existente no constituye una generación de arte nuevo. La eventual utilización de IA sigue abierta y no está autorizada como siguiente acción automática.

No presentar el paisaje como una fotografía confirmada de Rodríguez de Mendoza, ni el trazado como vector oficial definitivo. Mantener los avisos `PROVISIONAL_ASSET` mientras persistan esos gaps. Que un asset provenga de una publicación oficial no convierte su derivado preparado en arte maestro aprobado.

Los scripts [prepare-assets.py](../scripts/prepare-assets.py) y [trace-otorongo.py](../scripts/trace-otorongo.py) documentan las transformaciones realizadas. No es necesario ejecutarlos para abrir el Hero Lab.
