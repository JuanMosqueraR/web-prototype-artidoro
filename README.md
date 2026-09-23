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
