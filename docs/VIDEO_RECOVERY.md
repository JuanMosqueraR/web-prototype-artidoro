# Recuperación de video 03 — 26 de septiembre de 2026

**Versionado autorizado por el usuario («commitea»):** corrección funcional en `891bbc4`; evidencia QA en `94fa987`. No se hizo push ni despliegue desde esta sesión. La adaptación `fetch → Blob` descrita por Claude no está en el repo y no forma parte de estos commits.

**Actualización del Artifact, según el informe compartido por el usuario:** Claude publicó una v4 que intercepta la asignación de `src` y descarga el MP4 mediante `fetch → Blob`, solo en el build del Artifact, con fallback a la URL original. El usuario confirma que en Chrome iPhone funciona tras tocar «Activar movimiento». No se confirmó arranque automático ni la causa exacta. Una respuesta403 a una petición anónima no demuestra fallo de la petición contextual del reproductor; el mismo informe indica que la sonda con `src` normal sí reproducía. Estos datos son reportados por el usuario/Claude, no una prueba independiente realizada aquí.

El usuario informa que el Artifact publicado a veces muestra solo el poster en su celular. La causa exacta en el host real no está confirmada: no se obtuvo acceso verificable al contenido del Artifact desde la herramienta web. La validación de esta corrección es local en Chromium, no en Safari/iOS físico ni en Claude Artifacts.

## Fragilidad encontrada y corrección local

`src/sensory.js` dependía exclusivamente de `loadeddata`; tras 15 segundos sin primer frame retiraba la fuente, marcaba fallo permanente y no ofrecía reintento. Ese comportamiento impedía recuperarse de una carga lenta durante la misma visita. No prueba por sí solo qué provoca el retraso en Artifacts.

Ahora una espera de 15 segundos mantiene el poster y la descarga pendiente; un primer frame tardío puede activar la escena. Se comprueba disponibilidad real de frame, duración finita y estado del medio en `loadeddata`, `canplay`, `progress` y `loadedmetadata`; metadata por sí sola no habilita el video. Tras 4.5 segundos sin arranque se ofrece «Activar movimiento». Un error de red ofrece «Reintentar movimiento». El clic inicia `play()` dentro del gesto del usuario y pausa inmediatamente al iniciar, devolviendo el control al scroll. No hay reproducción continua nueva. Preferencia reduced motion y ahorro de datos siguen prevaleciendo.

Contexto técnico, no diagnóstico del teléfono: [MDN — loadeddata](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/loadeddata_event) documenta que ese evento puede no emitirse con ahorro de datos móvil; [WebKit — políticas de video iOS](https://webkit.org/blog/6784/new-video-policies-for-ios/) explica las condiciones de arranque y el papel de los gestos. Estas fuentes no verifican la política, CSP, entrega de archivos ni rangos HTTP del Artifact concreto.

## Pruebas

`qa/2026-09-26-video-recovery/verify-recovery.py`: 20 comprobaciones, desktop 1440×900 y mobile 390×844, Chromium148, DPR1. Retraso real de17s en la primera solicitud MP4, aborto de red seguido de clic, cambio de reduced motion y supresión deliberada del listener loadeddata. Comprueba recuperación tardía, poster, botón, pausa tras activación y control por scroll. `recovery.json` guarda el resultado y `*-waiting.png` la composición durante la espera.

`verify-journey.py` repite las 117 comprobaciones del recorrido y heroes A/B en una carpeta nueva, sin sobrescribir evidencia anterior. Resultados del código local: **20/20 recuperación y117/117 recorrido**. La copia móvil de Chromium no equivale a una prueba en iPhone. Las primeras pruebas detectaron una aserción prematura tras cambiar la preferencia de movimiento; se corrigió la espera del test y se añadió protección CSS inmediata para ocultar el botón en reduced motion.

## Qué necesita actualizar Claude

Para una nueva exportación, compilar/exportar **el working tree actual**, incluyendo los cambios en `index.html`, `src/sensory.js` y `src/sensory.css`; conservar ambos MP4, posters y el resto de assets. Adaptar las rutas de `data-desktop`/`data-mobile` y comprobar en el host real que apuntan a archivos accesibles. No basta con volver a subir los videos o sustituir una captura. La v4 reportada incorpora además el adaptador Blob externo descrito arriba; no se puede regenerar ese adaptador desde este repositorio.

Verificar desde el celular tanto el arranque normal como «Activar movimiento» y «Reintentar movimiento». Si también falla tras un toque, revisar la respuesta de los MP4, restricciones del iframe/CSP y entrega de rangos del host; no atribuirlo automáticamente a autoplay. La recuperación local no puede arreglar una URL inaccesible o un recurso bloqueado por el host.

No se publicó ni modificó el Artifact desde esta sesión, ni se generó media. Coste adicional US$0. Checkpoint previo `8d24ed9`, excluyendo reference/, PDF CRO y cambios ajenos APIMart. La corrección quedó inicialmente sin commit y se versionó posteriormente por instrucción explícita del usuario; referencias de commits al inicio.

## Posible prueba en GitHub Pages — todavía no implementada

Pages serviría el build estático como sitio independiente y permitiría evaluar la implementación del repo sin las transformaciones, iframe y adaptación Blob de Artifacts. Eso cambia el contexto de entrega, pero no elimina las restricciones de reproducción del navegador/iOS ni garantiza arranque automático. Es una prueba útil para separar ambas causas.

Antes de publicar bajo `/<repo>/`, se necesita configurar la base de Vite y revisar rutas absolutas, especialmente URLs guardadas en atributos `data-*` y enlaces `/b/`/`/?motion=off`. Estas rutas no deben darse por corregidas solo por configurar `base`. El deploy debe publicar `dist`, no todo el repositorio. No se añadió remoto ni workflow ni se modificó la configuración de despliegue.

Fuentes: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Vite — despliegue en Pages](https://vite.dev/guide/static-deploy#github-pages), [MDN — permisos de play()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play).

Archivos funcionales modificados: `index.html`, `src/sensory.js`, `src/sensory.css`. Documentación actualizada: este informe, README, CREATIVE_DIRECTIONS e IMPLEMENTATION_STATUS. Nueva evidencia en `qa/2026-09-26-video-recovery/`. No se alteran 01/02/04/05, packaging, textos comerciales ni la coreografía del clip.
