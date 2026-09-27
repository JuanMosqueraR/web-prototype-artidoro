// One deferred video, one reversible scroll scene. The HTML poster is the base experience.
const scene = document.querySelector('#sensory-scene');
const video = scene.querySelector('video');
const control = scene.querySelector('.sensory-control');
const retry = scene.querySelector('.sensory-retry');
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const mobile = matchMedia('(max-width:760px)');
let near = false, requested = '', ready = false, failed = false, frame = 0, timeout = 0, activationTimer = 0, targetTime = 0, unlocking = false;
const disabled = () => root.dataset.direction !== 'a' || root.classList.contains('no-motion') || reduced.matches || navigator.connection?.saveData;
function seek() {
  if (!ready || unlocking || disabled() || video.seeking || video.readyState < 2) return;
  if (Math.abs(video.currentTime - targetTime) > 0.045) video.currentTime = targetTime;
}
function paint() {
  frame = 0;
  if (!ready || disabled()) return;
  const top = mobile.matches ? 64 : 72;
  const rect = scene.getBoundingClientRect();
  const range = scene.offsetHeight - scene.querySelector('.sensory-stage').offsetHeight;
  const progress = Math.min(1, Math.max(0, (top - rect.top) / Math.max(1, range)));
  scene.style.setProperty('--scene-progress', progress.toFixed(4));
  scene.style.setProperty('--scene-close', Math.min(1, Math.max(0, (progress - .64) / .28)).toFixed(4));
  // Stay clear of the exact duration: some decoders have no frame at that timestamp.
  targetTime = progress * Math.max(0, video.duration - .06);
  if (rect.bottom > top && rect.top < innerHeight) seek();
}
function schedule() { if (!frame) frame = requestAnimationFrame(paint); }
function clearLoadTimers() {
  clearTimeout(timeout);
  clearTimeout(activationTimer);
}
function offerActivation(error = false) {
  retry.textContent = error ? 'Reintentar movimiento' : 'Activar movimiento';
  retry.hidden = disabled();
}
function fallback(stop = false) {
  ready = false;
  clearLoadTimers();
  video.pause();
  unlocking = false;
  // A slow first frame is not a permanent error: keep the request alive.
  // Actual media errors can be retried through an explicit user gesture.
  failed = stop;
  if (stop) {
    requested = '';
    video.removeAttribute('src');
    video.load();
  }
  scene.classList.remove('is-cinematic');
  scene.dataset.media = 'poster';
  scene.style.setProperty('--scene-progress', '0');
  scene.style.setProperty('--scene-close', '1');
  offerActivation(stop);
}
function checkReady() {
  if (!requested || failed || video.readyState < 2 || !Number.isFinite(video.duration) || video.duration <= 0) return;
  clearLoadTimers();
  ready = true;
  retry.hidden = true;
  scene.dataset.media = mobile.matches ? 'mobile-video' : 'desktop-video';
  update();
}
function update() {
  const off = disabled();
  control.hidden = root.dataset.direction !== 'a';
  control.textContent = root.classList.contains('no-motion') || reduced.matches ? 'Movimiento reducido' : 'Sin movimiento';
  if (off) {
    video.pause();
    clearLoadTimers();
    retry.hidden = true;
    scene.classList.remove('is-cinematic');
    scene.style.setProperty('--scene-close', '1');
    // Remove a pending request if accessibility changes before it has loaded.
    if (requested && !ready) { video.removeAttribute('src'); video.load(); requested = ''; }
    return;
  }
  if (failed) { offerActivation(true); return; }
  if (!near) return;
  const source = mobile.matches ? video.dataset.mobile : video.dataset.desktop;
  if (source !== requested) {
    requested = source;
    ready = false;
    scene.classList.remove('is-cinematic');
    retry.hidden = true;
    scene.dataset.media = 'loading';
    video.src = source;
    video.preload = 'auto';
    video.load();
    clearLoadTimers();
    activationTimer = setTimeout(() => offerActivation(), 4500);
    timeout = setTimeout(() => fallback(false), 15000);
  } else if (ready) {
    scene.classList.add('is-cinematic');
    schedule();
  }
}
// Some mobile media loaders don't emit loadeddata reliably. Verify usable
// frame state on multiple lifecycle events; metadata alone is not enough.
for (const event of ['loadeddata', 'canplay', 'progress', 'loadedmetadata']) video.addEventListener(event, checkReady);
video.addEventListener('error', () => { if (requested) fallback(true); });
retry.addEventListener('click', () => {
  if (disabled()) return;
  failed = false;
  near = true;
  update();
  // play() belongs directly to the tap gesture, permitting mobile media startup.
  // Pause immediately once it starts; normal playback never replaces scroll.
  unlocking = true;
  const start = video.play();
  if (start) start.then(() => {
    video.pause();
    unlocking = false;
    checkReady();
    schedule();
  }).catch(() => {
    unlocking = false;
    if (!ready) offerActivation();
  });
});
video.addEventListener('seeked', seek);
new IntersectionObserver(entries => {
  near = entries[0].isIntersecting;
  if (near) update();
}, {rootMargin:'450px 0px'}).observe(scene);
window.addEventListener('scroll', schedule, {passive:true});
window.addEventListener('resize', schedule, {passive:true});
mobile.addEventListener('change', () => { failed = false; update(); });
reduced.addEventListener('change', update);
new MutationObserver(update).observe(root, {attributes:true,attributeFilter:['class','data-direction']});
control.addEventListener('click', () => {
  if (reduced.matches) return;
  root.classList.toggle('no-motion');
  document.querySelector('#reduce-motion').checked = root.classList.contains('no-motion');
});
document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); else { checkReady(); update(); schedule(); } });
update();
