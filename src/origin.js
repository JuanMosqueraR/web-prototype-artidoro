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
  const ctaIcon = cta.querySelector('.icon');
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
    // Only Amazonas opens the demo PDP (catalog.js); the other origins go straight to the official store.
    ctaIcon.classList.toggle('icon-arrow', key === 'amazonas');
    ctaIcon.classList.toggle('icon-ext', key !== 'amazonas');
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

  // Swipe, built like a Framer-style drag: listeners on the window, no pointer capture, the strip follows the finger,
  // and release decides by distance or by speed. The previous version captured the pointer on the stage, dropped the
  // gesture at the first sign of vertical drift and moved the strip at most 48 px, which on iOS felt unresponsive.
  const COMMIT = 40, FLICK_MIN = 18, FLICK_SPEED = .35, FOLLOW = .55, FOLLOW_MAX = 110;
  const clampTo = (value, limit) => Math.max(-limit, Math.min(limit, value));
  function endGesture(event) {
    if (!gesture || (event && gesture.id !== event.pointerId)) return;
    const finished = gesture;
    gesture = null;
    window.removeEventListener('pointermove', dragMove);
    window.removeEventListener('pointerup', endGesture);
    window.removeEventListener('pointercancel', endGesture);
    stage.classList.remove('is-dragging');
    stage.style.removeProperty('--o-drag');
    if (!finished.horizontal) return;
    suppressClickUntil = performance.now() + 350;
    const far = Math.abs(finished.dx) >= COMMIT;
    const flick = Math.abs(finished.dx) >= FLICK_MIN && Math.abs(finished.speed) >= FLICK_SPEED && Math.sign(finished.speed) === Math.sign(finished.dx);
    // Also on pointercancel: iOS can cancel a fast flick as the finger lifts, after the horizontal move was already clear.
    if (far || flick) move(finished.dx < 0 ? 1 : -1);
  }
  function dragMove(event) {
    if (!gesture || gesture.id !== event.pointerId) return;
    const dx = event.clientX - gesture.x, dy = event.clientY - gesture.y;
    if (!gesture.horizontal) {
      // Clearly vertical: leave it to the page scroll.
      if (Math.abs(dy) > 12 && Math.abs(dy) > Math.abs(dx) * 1.6) { endGesture(event); return; }
      if (Math.abs(dx) < 4 || Math.abs(dx) < Math.abs(dy) * .8) return;
      gesture.horizontal = true;
      stage.classList.add('is-dragging');
    }
    const dt = event.timeStamp - gesture.lastT;
    if (dt > 0) gesture.speed = ((event.clientX - gesture.lastX) / dt) * .6 + gesture.speed * .4;   // smoothed px/ms
    gesture.lastX = event.clientX;
    gesture.lastT = event.timeStamp;
    gesture.dx = dx;
    if (!instant()) stage.style.setProperty('--o-drag', clampTo(dx * FOLLOW, FOLLOW_MAX) + 'px');
  }
  stage.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0 || event.target.closest('.origin-arrow')) return;
    gesture = { id: event.pointerId, x: event.clientX, y: event.clientY, dx: 0, horizontal: false, lastX: event.clientX, lastT: event.timeStamp, speed: 0 };
    window.addEventListener('pointermove', dragMove);
    window.addEventListener('pointerup', endGesture);
    window.addEventListener('pointercancel', endGesture);
  });

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
