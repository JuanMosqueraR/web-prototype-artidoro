# Tarata editorial — 26 de septiembre de 2026

[Abrir demo](http://127.0.0.1:4174/#seat-scene) · [Galería](../deliverables/tarata-review.html) · [Desktop](../qa/2026-09-26-tarata/captures/desktop-04-motion-rest.png) · [Mobile](../qa/2026-09-26-tarata/captures/mobile-04-motion-rest.png)

Implementada la opción 1 aprobada: interior y fachada con moto en una sola composición editorial. El interior con personas y cascos domina desktop; en mobile domina la fachada, con un inserto interior colocado por encima de la moto para dejarla visible. Titular grande «TOMA ASIENTO.», una frase breve, dirección y Cómo llegar. No hay selector ni otra secuencia de video.

## Movimiento y entrega de imágenes

Entrada única de fotografías y título: 850–1100 ms, con desfase de hasta 140 ms. Desplazamiento máximo 28 px desktop y 14 px mobile para las fotos; después quedan en reposo. Sin fijar el scroll ni reproducir la entrada al volver hacia arriba. Movimiento reducido del sistema y del sitio desactivan la animación. La composición también funciona sin JavaScript.

Las fotos se solicitan al acercarse a 800 px de 04; no forman parte de la carga inicial comprobada. Se entrega una versión menor del interior en mobile. Peso de las dos imágenes usadas: aproximadamente 330 KB desktop / 235 KB mobile. No hay dependencias nuevas. No se generaron imágenes ni videos: **coste adicional US$0**.

## Fuentes

`reference/tarata/05-counter-staff-2.jpg` y `02-facade-motorcycle.jpg`, expresamente elegidas en la propuesta aprobada. Copias exactas preservadas en `audit/source/`; preparación mediante Pillow limitada a orientación, tamaño y WebP. Sin retoque, IA, reconstrucción de logos ni cambios en personas, motos o cascos. Las referencias originales permanecen intactas.

Autoría/licencia y fecha de captura sin confirmar: continúa el aviso provisional/de referencia. No se presentan como fotografía oficial definitiva. Las imágenes conceptuales previas de Tarata quedan archivadas; no se renderizan en esta versión. Fuentes, hashes y preparación en `audit/assets.json`.

## Validación

Build Vite 7.1.3 correcto con Node aislado 22.23.1. **147 comprobaciones pasan: 30 específicas de Tarata y 117 del recorrido 01–05 y heroes A/B.** Chromium 148.0.7778.96, DPR 1, desktop 1440×900 y mobile 390×844, viewport real de la captura verificado. Se revisaron visualmente composición, visibilidad de la moto/cascos, copy y continuidad hacia 05.

Cobertura específica: entrada activa y reposo, ausencia de repetición, motion reducido del sistema/sitio, fotos responsive decodificadas, carga diferida, scroll libre, mapa conservado, ausencia de errores JS/desbordamiento y fallback sin JS. El QA del recorrido repite estados/keyframes y comprueba que 03 y los cinco enlaces comerciales siguen funcionando. Exploración adicional a 320, 360, 768, 1024 y 1920 px.

Los CTA de ambos heroes no cambian de geometría respecto al checkpoint anterior. Quince de dieciséis capturas de hero coinciden píxel a píxel con el 25 de septiembre; una captura B desktop expandida/reduced tiene 409 píxeles distintos en el titular (máxima diferencia 14/255), sin cambio de geometría ni modificación del código de B. Diferencia visual menor registrada, no corregida dentro de esta tarea. No se formula una nueva comparación creativa A/B. Las diferencias de A frente al Hero Lab original continúan siendo las ya documentadas el25; esta revisión añade delta cero.

[QA y JSON](../qa/2026-09-26-tarata/README.md). Las capturas del 25 permanecen como snapshot anterior. Las nuevas capturas completas usan movimiento reducido y todos los assets decodificados, incluido el poster de 03.

No se cubren Safari/iOS físico, lectores de pantalla ni conversión real. No se ejecutó compra ni se navegó al mapa externo durante el QA. No hay un bloqueo conocido para revisar la demo local.

## Git y archivos

Checkpoint recuperable previo: **`3830028`** (`checkpoint: home 01-05 before Tarata editorial revision`). Excluye `reference/`, el PDF CRO y los cambios ajenos de `tools/apimart/*`. **No hay commit final de esta revisión.**

Modificados: `index.html`, `src/home.css`, `src/home.js`, `audit/assets.json`; descripciones actuales en `README.md`, `docs/DECISIONS.md`, `docs/CREATIVE_DIRECTIONS.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ASSET_AUDIT.md`; avisos de snapshot anterior en `docs/HOME_REVIEW.md` y `deliverables/home-review.html`.

Nuevos: dos originales `audit/source/tarata-{facade-motorcycle,counter-staff}-original.jpg`, tres WebP `public/assets/tarata-{facade,interior,interior-mobile}.webp`, `scripts/prepare-tarata-editorial.py`, `qa/2026-09-26-tarata/`, `deliverables/tarata-review.html` y este informe.

L19 registra la aprobación actual, incluida la presencia de moto/cascos, sin reclasificar el registro histórico LOCKED/OPEN. 01,02,03,05 y B conservan su implementación; el texto de procedencia del footer se actualiza para describir las fotografías actuales de 04.
