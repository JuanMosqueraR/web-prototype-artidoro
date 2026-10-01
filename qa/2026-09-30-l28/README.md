# QA L28 — hero «Del cafetal a tu bolsa», 03 «De la bolsa a tu taza», moliendas y mejoras generales — 30 de septiembre de 2026

**Condiciones.** Python Playwright con Chromium (versión en `checks.json`), DPR 1, build de producción de la Vite 7.1.3 del repo con Node 22.23.1 aislado, servido por HTTP con soporte de Range en `http://127.0.0.1:4192`. Reproducir: `ARTIDORO_REVIEW_URL=<url> python qa/2026-09-30-l28/verify.py` (escribe solo en esta carpeta).

**Resultado: 107/107** (`checks.json`), tras las correcciones posteriores a la prueba en iPhone (sin barra de compra, secuencia AVIF a 12 fps en mobile con respaldo WebP, viewport alto sin franja inferior, espera mínima por paso en 03, swipe del carrusel como control de regresión).

| Bloque | Viewports / estados | Qué se comprueba |
|---|---|---|
| Hero y 03 con movimiento | 1440 × 900, 390 × 844, 390 × 664, 768 × 1024 | CTA, confianza y pack dentro del primer viewport; header transparente sobre el hero y sólido después; todos los viewports: solo su video (`hero-desktop.mp4` o `hero-mobile.mp4`), que sigue al scroll (~5 s a mitad, ~9,9 s al final), sin secuencia; con el video bloqueado en mobile, la secuencia AVIF (121) toma el relevo y se repinta con el scroll, y sin AVIF cae a WebP (61); final con paso 3 y bolsa; 03 pasa por los pasos 1 → 2 → 2 → 3; en mobile el título final queda debajo de la bolsa y sin kicker; final con fotogramas decodificados, bolsa y título en pantalla; desplazamiento continuo por la 03 a 0,95 y 1,18 pantallas por segundo: cada texto queda totalmente legible con la sección en pantalla ≥ 1,5 / 0,8 / 0,9 s (primero, medio y final) y ≥ 1,2 / 0,6 / 0,6 s respectivamente; con las barras del navegador ocultas (`--bars`) el escenario crece y el contenido sigue en el viewport pequeño; en 02 el swipe táctil cambia el origen, también un flick corto y rápido (34 px / 50 ms) y un gesto cancelado por el sistema al soltar; sin desbordamiento horizontal; sin texto < 11 px en las secciones nuevas; objetivos ≥ 44 px; sin errores de página |
| Bandas | mismos | Franja de moliendas con 4 elementos y título revelado; franja de confianza de 05 con 4 puntos, el último «Precio justo al caficultor» |
| Barra de compra | todos | Ya no existe (retirada a petición del usuario) |
| Sin movimiento | 1440 × 900 y 390 × 844, con `?motion=off` y con `prefers-reduced-motion` | Ambas escenas estáticas (sin fijación), fotograma final cargado y visible, bolsa visible, 03 en el paso 3, **ni MP4 ni secuencia solicitados**, títulos visibles, CTA y pack en el primer viewport |
| Inercia | 1440 × 900 | La rueda se desliza hasta su destino; el teclado llega al final; con movimiento reducido la rueda es nativa |
| Etiquetas para compartir | 1440 × 900 | `og:title` marcado «Demo», `og:image` absoluta que termina en `/assets/og-share.jpg` y existe como JPEG de 1200 × 630, `twitter:card` de imagen grande |
| PDPs | 1440 × 900 | CTA del hero → PDP Amazonas; pack del hero → PDP El Ahorrador; sin errores |
| B | 1440 × 900 y 390 × 844, movimiento y sin movimiento, fotogramas inicial y expandido | Diferencia de píxeles frente a `qa/2026-09-29-ahorro/after/` dentro de la tolerancia del ruido de codificación |

Capturas en `after/` (hero en tres puntos, 03 en cuatro, bandas, estados sin movimiento, B).

## Rendimiento de laboratorio (build local, mediana de 3)

Mismo método y perfiles que [`qa/2026-09-30-performance`](../2026-09-30-performance/README.md) (copia del script ejecutada fuera del repo para no sobrescribir su `perf.json`). Build anterior (`HEAD` = `6a73635`) y build L28 servidos en local con el mismo servidor, por lo que **no es comparable con la medición de Pages** (sin CDN ni latencia real).

| Perfil | Build | FCP | LCP | CLS | TBT | Peso | Peticiones |
|---|---|---|---|---|---|---|---|
| Mobile, Slow 4G + CPU 4× | anterior | 2,09 s | 2,09 s | 0 | 0 ms | 622 KB | 13 |
| Mobile, Slow 4G + CPU 4× | L28 | 2,02 s | 2,02 s | 0 | 0 ms | 406 KB | 11 |
| Desktop, sin throttling | anterior | 0,12 s | 0,12 s | 0 | 0 ms | 665 KB | 13 |
| Desktop, sin throttling | L28 | 0,12 s | 0,12 s | 0 | 0 ms | 3 816 KB | 11 |

- Medido con la tercera ronda de iPhone. El peso desktop incluye el video (3,49 MB); en mobile con Slow 4G el video (3,22 MB) no había llegado dentro de la ventana de 4 s, así que no está sumado. Ambos se piden después de la carga: FCP/LCP dependen solo del póster (45 KB) y del texto.
- En L28 el elemento LCP es el titular, no el póster del hero.

## Límites

Solo Chromium: sin Safari/iOS instrumental ni Firefox. El video no se preparaba en Chrome de iPhone (motor WebKit) en la prueba física del usuario; la secuencia de mobile debe confirmarse allí. Laboratorio, no campo. No cubre lectores de pantalla más allá de la estructura (pasos en `ol`, `h1`/`h2`).
