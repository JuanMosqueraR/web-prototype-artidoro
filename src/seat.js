// Scene 04 only: its own view state (entrada / mesa), independent of the hero and of scene 02.
// Same robust flow as scene 02: prepare (async, image decoded) -> fade out (~90 ms) -> commit (one synchronous update) -> fade in.
const scene = document.querySelector('#seat-scene');
if (scene) {
  const LOAD_TIMEOUT = 4000, HALF = 90;
  const buttons = [...scene.querySelectorAll('button[data-view]')];
  const images = Object.fromEntries([...scene.querySelectorAll('.seat-img')].map(img => [img.dataset.view, img]));
  const labels = Object.fromEntries(buttons.map(b => [b.dataset.view, b.dataset.label]));
  const error = scene.querySelector('.seat-error');
  const live = scene.querySelector('.seat-sr');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let shown = scene.dataset.view, pending = null, token = 0, timer = 0;
  const instant = () => document.documentElement.classList.contains('no-motion') || reduced.matches;
  const ready = img => img.complete && img.naturalWidth > 0;
  // Resolves true once the incoming image is decodable; false on error or timeout. Never rejects.
  function prepare(key) {
    const img = images[key];
    if (img.loading === 'lazy' && !ready(img)) img.loading = 'eager';
    if (img.complete && img.naturalWidth === 0) img.src = img.getAttribute('src'); // a previous attempt failed: request it again
    return new Promise(resolve => {
      let done = false;
      const finish = ok => {
        if (done) return;
        done = true;
        clearTimeout(t);
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
    shown = key;
    scene.dataset.view = key;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === key)));
    live.textContent = 'Vista: ' + labels[key];
    error.textContent = '';
  }
  async function select(key) {
    const mine = ++token;
    restore();
    error.textContent = '';
    if (key === shown) return;
    const ok = await prepare(key);
    if (mine !== token) return;
    if (!ok) { error.textContent = 'No se pudo cargar esta vista. Inténtalo de nuevo.'; return; }
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
  buttons.forEach(b => b.addEventListener('click', () => select(b.dataset.view).catch(restore)));
  new MutationObserver(flush).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  reduced.addEventListener('change', flush);
}
