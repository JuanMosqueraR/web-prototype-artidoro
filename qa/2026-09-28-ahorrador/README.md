# QA — El Ahorrador, 28 de septiembre de 2026

Checkpoint: `87ea725`. Comparación anterior en `../2026-09-28-catalog-pdp/after/`; no se sobrescribe. Windows, Node 22.23.1 aislado, Vite 7.1.3, Python 3.10, Playwright Chromium 148.0.7778.96, DPR 1, preview de producción en `http://127.0.0.1:4175`.

- `verify.py` → `checks.json`: 211/211. Adaptación explícita de la revisión anterior para dos PDP, seis fotos de catálogo y la nueva composición de 05. Su cota observacional de altura aumenta de 1833 a 2020 px; no es un contrato ni una comparación de mejora. La altura real aumenta 161,55 px en 390 × 844.
- `pack-checks.py` → `pack-checks.json`: 316/316; incluye las 125 combinaciones en desktop y mobile, entradas/retornos, independencia del selector, teclado, recarga, imágenes, texto al 200 %, sin JS y fallo de video.
- `verify-external.py` → `external-links.json`: dos variantes seleccionadas en los formularios oficiales, HTTP 200. Lectura sin carrito ni compra.
- `additional.json`: cuatro verificaciones exploratorias mediante Playwright, con condiciones y geometría: build de Pages bajo `/ahorrador-pages/` y posición de compra de 02 en tres viewports móviles.

Reproducir desde la raíz con preview activo:

```powershell
& C:/tmp/node22/node-v22.23.1-win-x64/node.exe node_modules/vite/bin/vite.js build
python qa/2026-09-28-ahorrador/verify.py
python qa/2026-09-28-ahorrador/pack-checks.py
python qa/2026-09-28-ahorrador/verify-external.py
```

Los scripts escriben exclusivamente los resultados/capturas de esta carpeta. Para una iteración posterior, crear otra carpeta de evidencia antes de repetirlos. `verify-external.py` visita la tienda pública y puede reflejar cambios futuros de catálogo. Se corrigió una expectativa del test de teclado: después de Amazonas viene Villa Rica en el orden del formulario; no fue un defecto del control.

Capturas `after/`: A/B, desktop 1440 × 900 y mobile 390 × 844, inicial/expandido, movimiento on/off, fuentes e imágenes decodificadas. B se compara completo y resulta idéntico. En A se excluyen cabecera y zona inferior del acceso nuevo; el área comparada resulta idéntica. Coordenadas de CTA contrastadas con `../measurements.json`; deltas históricos en JSON.

Home completa: movimiento reducido, Tarata/catálogo preparados, FAQ cerradas. 05: imágenes decodificadas, FAQ cerradas. PDP pack: Amazonas/Cajamarca/Puno, precio S/280, imagen de ejemplo fijo; PDP Amazonas: 250 g/grano. Cada captura conserva el ancho del viewport declarado. Exploratorios: 390 × 700, 360 × 740, 768 × 1024, 1024 × 900 y texto ampliado; no redefinen el contrato.

No cubre Safari/iOS físico, red móvil real, performance de campo, checkout, conversión ni publicación de Pages. La confirmación previa de iPhone correspondía al checkpoint anterior.
