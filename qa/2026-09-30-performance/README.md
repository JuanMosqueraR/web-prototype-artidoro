# Rendimiento de laboratorio de la home publicada — 30 de septiembre de 2026

Medición de solo lectura sobre https://juanmosquerar.github.io/web-prototype-artidoro/ (GitHub Pages; `master` en `3873cc8` al medir, sin verificar que el build publicado coincida exactamente con ese commit). No modifica el repositorio ni la web.

**Método.** `perf.py`: Python Playwright con Chromium 148 y CDP, caché desactivada, 3 corridas por perfil, se reporta la mediana. Perfil mobile: 390 × 844, red emulada ~Slow 4G (1,6 Mbps de bajada, 150 ms de latencia) y CPU 4× más lenta. Perfil desktop: 1440 × 900 sin throttling. LCP y CLS vía `PerformanceObserver`; TBT aproximado como la suma de `duration − 50 ms` de las tareas largas posteriores a FCP; peso = bytes transferidos; peticiones = respuestas HTTP. Reproducir: `python qa/2026-09-30-performance/perf.py [URL]`.

## Resultado (mediana; `perf.json` guarda cada corrida)

| Perfil | FCP | LCP | CLS | TBT (aprox.) | Peso | Peticiones |
|---|---|---|---|---|---|---|
| Mobile, Slow 4G + CPU 4× | 1,30 s | **1,67 s** | 0 | 9 ms | 513 KB | 13 |
| Desktop, sin throttling | 0,19 s | **0,21 s** | 0 | 0 ms | 556 KB | 13 |

- Sin peticiones con estado ≥ 400. El elemento LCP es siempre la foto del cafetal del hero (`cafetal-home-*`), con `fetchpriority=high`.
- **La primera corrida mobile de cada sesión fue en frío** (DNS/TLS/CDN): FCP ≈ 3,6 s y LCP ≈ 4,0 s en las dos mediciones hechas hoy (TBT 21 y 86 ms); las otras dos corridas dieron LCP 1,55–1,67 s. La mediana oculta ese arranque; un visitante nuevo puede experimentar algo intermedio.
- El video de 03 y las imágenes de 04 y 05 no se solicitan al entrar (carga diferida); los ~513 KB iniciales son hero, bolsa, fuentes y recursos de 02.

## Límites — qué NO demuestra

- Es laboratorio, no de campo: sin CrUX ni usuarios reales, sin variedad de dispositivos o redes.
- No es Lighthouse: su emulación de dispositivo y su TBT difieren; los valores no son comparables 1:1.
- El **LCP de 12,1 s del diagnóstico CRO** corresponde a la tienda actual en Shopify, medido con otra herramienta y condiciones. La comparación con la demo es indicativa: la demo no incluye apps de terceros, checkout ni catálogo dinámico, así que el número no anticipa el rendimiento de una migración real.
- Solo la home. No cubre PDPs, la interacción de scroll de 03 ni la carga completa del video.
- El throttling es aproximado.

Pendiente para una conclusión de campo: PageSpeed Insights/CrUX con tráfico real, o repetir esta medición tras cada deploy y otras horas del día.
