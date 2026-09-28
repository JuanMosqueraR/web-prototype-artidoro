# QA catálogo/PDP — 28 de septiembre de 2026

Checkpoint `38a209f`, rama `feat/catalogo-pdp`. Python Playwright + Pillow, Chromium 148.0.7778.96, DPR 1, preview de producción `http://127.0.0.1:4175/`. No se efectuaron compras ni publicación.

- `before/`: contrato A/B en 1440 × 900 y 390 × 844, ambos keyframes, movimiento on/off, imágenes del hero decodificadas. Capturado antes de modificar la implementación, mediante Python Playwright; fotos de 05 anterior incluidas. No sobrescribir.
- `after/`: mismo contrato y capturas de 05/PDP/home completa. Home completa con preferencia de movimiento reducido y fotografías cargadas; PDP inicial 250 g/grano.
- `verify.py`, `checks.json`: 211 comprobaciones, geometría y comparaciones. La cabecera de A cambia intencionadamente de Los orígenes a Tienda; comparación de píxeles del hero excluye sus 72/64 px. B se compara completo. Tolerancia de antialias: ≤0,05 % de píxeles y delta máximo de canal 16; se conserva el delta observado.
- `extra-checks.py`, `extra-checks.json`: carga inicial móvil sin fotos adicionales ni MP4; texto de 05 al 200 %; compra con video bloqueado y poster; combinación de variante inexistente bloqueada. La ampliación es una sonda CSS, no ajuste nativo de iOS.
- `verify-external.py`, `external-links.json`: lectura de las fichas oficiales con variantes 1 kg/grueso y miel/300 g; sus formularios mantienen los IDs solicitados. Nunca se envían formularios.

Ejecutar sobre un build actual servido por Vite preview:

```powershell
& 'C:/tmp/node22/node-v22.23.1-win-x64/node.exe' node_modules/vite/bin/vite.js build
python qa/2026-09-28-catalog-pdp/verify.py
python qa/2026-09-28-catalog-pdp/extra-checks.py
```

Estos scripts escriben exclusivamente evidencia en esta carpeta. `verify.py` acepta `ARTIDORO_REVIEW_URL`; los checks adicionales usan el puerto local 4175. Nuevas revisiones deben conservar esta evidencia en una carpeta fechada distinta. No cubre dispositivo físico, red celular real, estado publicado de Pages ni métricas de conversión. Informe de alcance/resultados: `docs/CATALOG_PDP_REVIEW.md`.
