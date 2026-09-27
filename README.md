# Artidoro — demo de la home 01–05

**Publicación de revisión:** GitHub Pages ([cómo publicar](#publicar-en-github-pages)). El Artifact que se había publicado se retiró el 26 de septiembre de 2026; ver [recuperación de video y resultado](docs/VIDEO_RECOVERY.md).

**Actualización del 26 de septiembre:** [Tarata editorial — entrega y QA](docs/TARATA_REVIEW.md) · [Galería actual](deliverables/tarata-review.html). Checkpoint previo `3830028`; revisión sin commit final. La home sigue en `http://127.0.0.1:4174/`.

Estado actual, 25 de septiembre de 2026: dirección A «Perú, en profundidad», con cinco orígenes, momento cinematográfico 03, pausa breve en Tarata y cierre comercial. Checkpoint recuperable `0a1da04`; esta fase queda sin commit final para revisión.

- [Galería visual, videos y capturas](deliverables/home-review.html)
- [Entrega y límites](docs/HOME_REVIEW.md)
- [Implementación actual](docs/IMPLEMENTATION_STATUS.md)
- [QA y condiciones](qa/2026-09-25-home/README.md)

## Ejecutar la demo actual

Vite 7.1.3 requiere Node 20.19+ o 22.12+. En esta máquina se usó Node 22.23.1 aislado, sin actualizar el Node global:

```powershell
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js build
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js preview --host 127.0.0.1 --port 4174
```

Home: `http://127.0.0.1:4174/`. Hero B conservado: `/b/`. Con un Node compatible, también funcionan `npm run build` y `npm run preview -- --host 127.0.0.1 --port 4174`. Las dependencias ya estaban instaladas en el entorno revisado.

03 tiene video horizontal/vertical diferido, poster y reduced motion. Compra y catálogo enlazan a la tienda oficial; no hay checkout propio ni integración Shopify. La página `deliverables/home-review.html` se puede abrir como archivo local para revisar capturas y clips; la home interactiva requiere el servidor Vite.

## Publicar en GitHub Pages

`scripts/build-pages.py` compila con Vite, hace relativas las rutas `/assets/…` (incluidos los atributos `data-*` que lee el JS), cambia los enlaces `/b/` y `/?motion=off` del pie por `#b` y `?motion=off`, y añade `.nojekyll`. Escribe en `dist/pages/` (ignorado por git) y, con `--branch-dir`, prepara un commit `gh-pages` en un repositorio local **fuera** de este. No añade remotos ni hace push: publicar es una acción manual. Se niega a compilar si `index.html`, `src/`, `public/` o los archivos de paquete tienen cambios sin commit (`--allow-dirty` lo permite; el commit registra el hash de origen).

```powershell
python scripts/build-pages.py --node 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' --branch-dir 'C:/ruta/fuera/del/repo/gh-pages'
cd 'C:/ruta/fuera/del/repo/gh-pages'
git remote add origin https://github.com/JuanMosqueraR/web-prototype-artidoro.git   # solo la primera vez
git push -u origin gh-pages
```

En GitHub: Settings → Pages → Deploy from a branch → `gh-pages` / `(root)`. La URL es `https://juanmosquerar.github.io/web-prototype-artidoro/`, con la barra final. Con el Node 18 global el script se detiene con un aviso; usa `--node` con Node 20.19+ o 22.12+. En Pages funcionan `#a`, `#b` y `?motion=off`; no existen rutas `/a/` ni `/b/`. El build publica también los assets de `public/` que la home no usa (KI-62).

**Las instrucciones, HTML autónomos y capturas del Hero Lab de abajo son históricos.** No representan esta home y su exportador no se ejecutó ni actualizó para incluir el video. No regenerar los baselines anteriores para revisar esta fase.

---

## Snapshot histórico del Hero Lab

# Artidoro — Hero Lab

Checkpoint de comparación. Solo dos heroes, con el mismo café Amazonas 250 g (Rodríguez de Mendoza; naranja y melaza). Sin home, Shopify, video, WebGL ni imágenes generadas mediante IA.

## Abrir sin instalar

Descargar y abrir cualquiera de estos archivos en el navegador:

- `deliverables/A-peru-en-profundidad.html`
- `deliverables/B-fuera-de-la-lata.html`

Ambos incluyen todos los assets y el selector A/B. No necesitan conexión para visualizarse. El CTA abre la ficha real de café Amazonas en una pestaña nueva; no simula un checkout.

## Ejecutar el proyecto

Node 20.19+ o 22.12+ y npm. Desde esta carpeta:

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4173
```

- A: `http://localhost:4173/a/`
- B: `http://localhost:4173/b/`

El selector de laboratorio queda fuera de la composición. Cada dirección conserva su estado al alternar. La casilla **Sin motion** elimina las transiciones; también se respeta la preferencia del sistema. Las interacciones son reversibles y no requieren scroll ni espera.

## Archivos

- `src/peru.css`: composición A y acercamiento del cafetal.
- `src/lata.css`: composición B y despliegue del otorongo.
- `src/common.css`: tipografía, producto, CTA y controles compartidos.
- `src/main.js`: selector, revelado y preferencia de movimiento.
- `src/origin.css` y `src/origin.js`: escena 02 “Encontrar tu origen” (solo con A).
- `audit/ASSETS.md` y `audit/assets.json`: clasificación, fuentes y gaps.
- `qa/QA.md` y `qa/measurements.json`: comprobaciones del checkpoint.
- `deliverables/*.jpg`: capturas finales.

La foto de cafetal y el otorongo se marcan **PROVISIONAL_ASSET**. La primera procede de la marca pero carece de atribución geográfica verificada. El segundo es un trazado determinista de una extracción pequeña del packaging; no es el arte maestro original.

## Construir / regenerar entregables

```sh
npm run build
python3 scripts/export-standalone.py
```

Las exportaciones HTML son archivos de revisión con recursos embebidos. El proyecto Vite sirve los recursos por separado y comparte la misma foto de producto entre variantes. No hay arquitectura de tienda ni integración de compra.

Las fuentes originales de fotografía usadas para la preparación están en `audit/source/`. Los scripts de preparación son utilidades opcionales de auditoría (Pillow y NumPy), no dependencias de ejecución del lab.
