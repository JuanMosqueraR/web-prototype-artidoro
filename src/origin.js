// Scene 02 only: its own origin state, independent of the hero's Acercar/Alejar state.
// Flow per request: prepare (async, image ready) -> animate (~180 ms) -> commit (one synchronous update of the whole set).
const scene = document.querySelector('#origin-scene');
if (scene) {
  const LOAD_TIMEOUT = 4000, HALF = 90;
  const buttons = [...scene.querySelectorAll('button[data-origin]')];
  const bags = Object.fromEntries([...scene.querySelectorAll('.origin-bag')].map(img => [img.dataset.origin, img]));
  const origins = Object.fromEntries(buttons.map(b => [b.dataset.origin, { name: b.dataset.name, href: b.dataset.href }]));
  const cta = scene.querySelector('.origin-buy');
  const ctaName = cta.querySelector('[data-cta-name]');
  const status = scene.querySelector('.origin-status');
  const live = scene.querySelector('.origin-sr');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let shown = scene.dataset.origin, pending = null, token = 0, timer = 0;
  const instant = () => document.documentElement.classList.contains('no-motion') || reduced.matches;
  const ready = img => img.complete && img.naturalWidth > 0;
  // Resolves true once the incoming bag is decodable; false on error or timeout. Never rejects.
  function prepare(key) {
    const img = bags[key];
    if (img.loading === 'lazy' && !ready(img)) img.loading = 'eager';
    return new Promise(resolve => {
      let done = false;
      const finish = ok => {
        if (done) return;
        done = true;
        clearTimeout(t);
        if (!ok) img.src = img.getAttribute('src');
        resolve(ok);
      };
      const t = setTimeout(() => finish(false), LOAD_TIMEOUT);
      img.decode().then(() => finish(ready(img)), () => finish(false));
    });
  }
  function restore() {
    clearTimeout(timer);
    timer = 0;
    pending = null;
    scene.classList.remove('is-out');
  }
  function commit(key) {
    const data = origins[key];
    shown = key;
    scene.dataset.origin = key;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.origin === key)));
    cta.href = data.href;
    ctaName.textContent = data.name;
    live.textContent = 'Origen seleccionado: ' + data.name;
    status.textContent = '';
  }
  async function select(key) {
    const mine = ++token;
    restore();
    status.textContent = '';
    if (key === shown) return;
    const ok = await prepare(key);
    if (mine !== token) return;
    if (!ok) { status.textContent = 'No se pudo cargar este origen. Inténtalo de nuevo.'; return; }
    if (instant()) { commit(key); return; }
    pending = key;
    scene.classList.add('is-out');
    timer = setTimeout(() => { timer = 0; pending = null; if (mine !== token) return; commit(key); scene.classList.remove('is-out'); }, HALF);
  }
  // "Sin motion" / reduced motion switched on mid-animation: the image is already ready, so finish now.
  function flush() {
    if (!timer || !instant()) return;
    const key = pending;
    restore();
    commit(key);
  }
  buttons.forEach(b => b.addEventListener('click', () => select(b.dataset.origin).catch(restore)));
  new MutationObserver(flush).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  reduced.addEventListener('change', flush);
}
