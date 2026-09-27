// Scene 02 owns its selection; no state or events propagate to the rest of the home.
const scene = document.querySelector('#origin-scene');
if (scene) {
  const LOAD_TIMEOUT = 4000, FADE_OUT = 70;
  const buttons = [...scene.querySelectorAll('.origin-row-main')];
  const keys = buttons.map(button => button.dataset.origin);
  const slots = [...scene.querySelectorAll('.origin-slot')];
  const bags = Object.fromEntries([...scene.querySelectorAll('.origin-bag')].map(img => [img.dataset.origin, img]));
  const origins = Object.fromEntries(buttons.map(button => [button.dataset.origin, { name: button.dataset.name, href: button.dataset.href }]));
  const records = [...scene.querySelectorAll('.origin-record')];
  const stage = scene.querySelector('.origin-stage');
  const cta = scene.querySelector('.origin-buy');
  const ctaName = cta.querySelector('[data-cta-name]');
  const status = scene.querySelector('.origin-status');
  const live = scene.querySelector('.origin-sr');
  const count = scene.querySelector('.origin-count');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const preparing = new Map(), failed = new Set();
  let shown = scene.dataset.origin, requested = shown, pending = null, token = 0, timer = 0;
  let gesture = null, suppressClickUntil = 0;
  const instant = () => document.documentElement.classList.contains('no-motion') || reduced.matches;
  const ready = img => img.complete && img.naturalWidth > 0;
  const wrap = index => (index + keys.length) % keys.length;

  function positionSlots() {
    const selected = keys.indexOf(shown);
    slots.forEach((slot, index) => {
      const offset = wrap(index - selected + 2) - 2;
      const decoded = slot.classList.contains('is-ready');
      const neighbor = Math.abs(offset) === 1 && decoded;
      slot.dataset.offset = String(offset);
      slot.disabled = !neighbor;
      slot.tabIndex = neighbor ? 0 : -1;
      slot.setAttribute('aria-hidden', String(Math.abs(offset) > 1 || (!decoded && offset !== 0)));
    });
  }

  // Shared prefetch/selection work. Failed attempts can be explicitly retried;
  // a timed-out decode cannot commit a stale origin later.
  function prepare(key) {
    if (preparing.has(key)) return preparing.get(key);
    const img = bags[key];
    if (!img.getAttribute('src') || failed.has(key)) img.src = img.dataset.src || img.getAttribute('src');
    failed.delete(key);
    const work = new Promise(resolve => {
      let finished = false;
      const finish = ok => {
        if (finished) return;
        finished = true;
        clearTimeout(timeout);
        if (ok) {
          img.closest('.origin-slot').classList.add('is-ready');
          positionSlots();
        } else failed.add(key);
        resolve(ok);
      };
      const timeout = setTimeout(() => finish(false), LOAD_TIMEOUT);
      img.decode().then(() => finish(ready(img)), () => finish(false));
    });
    preparing.set(key, work);
    work.then(() => { if (preparing.get(key) === work) preparing.delete(key); });
    return work;
  }

  function warmNeighbors() {
    const index = keys.indexOf(shown);
    [keys[wrap(index - 1)], keys[wrap(index + 1)]].forEach(key => prepare(key));
  }
  function restore() {
    clearTimeout(timer);
    timer = 0;
    pending = null;
    scene.classList.remove('is-out');
  }
  function commit(key) {
    const focusWasOnBag = document.activeElement?.closest('.origin-slot');
    shown = key;
    requested = key;
    scene.dataset.origin = key;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.origin === key)));
    records.forEach(record => record.setAttribute('aria-hidden', String(record.dataset.origin !== key)));
    cta.href = origins[key].href;
    ctaName.textContent = origins[key].name;
    count.textContent = String(keys.indexOf(key) + 1).padStart(2, '0') + ' / 05';
    live.textContent = 'Origen seleccionado: ' + origins[key].name;
    status.textContent = '';
    scene.removeAttribute('aria-busy');
    positionSlots();
    if (focusWasOnBag) stage.focus({ preventScroll: true });
    warmNeighbors();
  }
  async function select(key) {
    const mine = ++token;
    restore();
    requested = key;
    status.textContent = '';
    scene.removeAttribute('aria-busy');
    if (key === shown) return;
    scene.setAttribute('aria-busy', 'true');
    const ok = await prepare(key);
    if (mine !== token) return;
    if (!ok) {
      requested = shown;
      scene.removeAttribute('aria-busy');
      status.textContent = 'No se pudo cargar este origen. Vuelve a seleccionarlo para reintentar.';
      return;
    }
    if (instant()) { commit(key); return; }
    pending = key;
    scene.classList.add('is-out');
    timer = setTimeout(() => {
      timer = 0;
      pending = null;
      if (mine !== token) return;
      commit(key);
      scene.classList.remove('is-out');
    }, FADE_OUT);
  }
  const move = delta => select(keys[wrap(keys.indexOf(requested) + delta)]);
  function flush() {
    if (!instant()) return;
    stage.style.removeProperty('--o-drag');
    if (!timer) return;
    const key = pending;
    restore();
    commit(key);
  }

  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.origin)));
  slots.forEach(slot => slot.addEventListener('click', () => {
    if (performance.now() >= suppressClickUntil) select(slot.dataset.coffee);
  }));
  scene.querySelector('.origin-prev').addEventListener('click', () => move(-1));
  scene.querySelector('.origin-next').addEventListener('click', () => move(1));
  scene.addEventListener('keydown', event => {
    if (!event.target.closest('.origin-index, .origin-stage') || !['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    const index = event.key === 'Home' ? 0 : event.key === 'End' ? keys.length - 1 : wrap(keys.indexOf(requested) + (event.key === 'ArrowRight' ? 1 : -1));
    select(keys[index]);
    if (event.target.closest('.origin-index')) buttons[index].focus({ preventScroll: true });
  });

  stage.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0 || event.target.closest('.origin-arrow')) return;
    gesture = { id: event.pointerId, x: event.clientX, y: event.clientY, dx: 0, horizontal: false };
  });
  stage.addEventListener('pointermove', event => {
    if (!gesture || gesture.id !== event.pointerId) return;
    const dx = event.clientX - gesture.x, dy = event.clientY - gesture.y;
    if (!gesture.horizontal) {
      if (Math.abs(dy) > 10 && Math.abs(dy) > Math.abs(dx)) { gesture = null; return; }
      if (Math.abs(dx) < 10 || Math.abs(dx) < Math.abs(dy) * 1.2) return;
      gesture.horizontal = true;
      stage.setPointerCapture(event.pointerId);
      stage.classList.add('is-dragging');
    }
    gesture.dx = dx;
    if (!instant()) stage.style.setProperty('--o-drag', Math.max(-48, Math.min(48, dx * .3)) + 'px');
  });
  function endGesture(event) {
    // Touch starts with implicit capture on a child. Its lost-capture event
    // bubbles when the stage takes over; that is not the end of the gesture.
    if (event.type === 'lostpointercapture' && event.target !== stage) return;
    if (!gesture || gesture.id !== event.pointerId) return;
    const finished = gesture;
    gesture = null;
    stage.classList.remove('is-dragging');
    stage.style.removeProperty('--o-drag');
    if (finished.horizontal) {
      suppressClickUntil = performance.now() + 350;
      if (event.type === 'pointerup' && Math.abs(finished.dx) >= 40) move(finished.dx < 0 ? 1 : -1);
    }
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
  }
  stage.addEventListener('pointerup', endGesture);
  stage.addEventListener('pointercancel', endGesture);
  stage.addEventListener('lostpointercapture', endGesture);

  buttons.forEach(button => { button.disabled = false; });
  scene.querySelectorAll('.origin-arrow').forEach(button => { button.disabled = false; });
  stage.tabIndex = 0;
  positionSlots();
  scene.classList.add('is-enhanced');
  prepare(shown);
  const observer = new IntersectionObserver(entries => {
    if (!entries.some(entry => entry.isIntersecting) || document.documentElement.dataset.direction === 'b') return;
    warmNeighbors();
    observer.disconnect();
  }, { rootMargin: '200px' });
  observer.observe(scene);
  new MutationObserver(flush).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  reduced.addEventListener('change', flush);
}
