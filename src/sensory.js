// One deferred video, one reversible scroll scene. The HTML poster is the base experience.
const scene = document.querySelector('#sensory-scene');
const video = scene.querySelector('video');
const control = scene.querySelector('.sensory-control');
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const mobile = matchMedia('(max-width:760px)');
let near = false, requested = '', ready = false, failed = false, frame = 0, timeout = 0, targetTime = 0;
const disabled = () => root.dataset.direction !== 'a' || root.classList.contains('no-motion') || reduced.matches || navigator.connection?.saveData;
function seek() {
  if (!ready || disabled() || video.seeking || video.readyState < 2) return;
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
function fallback() {
  ready = false;
  failed = true;
  clearTimeout(timeout);
  video.pause();
  requested = '';
  video.removeAttribute('src');
  video.load();
  scene.classList.remove('is-cinematic');
  scene.dataset.media = 'poster';
  scene.style.setProperty('--scene-progress', '0');
  scene.style.setProperty('--scene-close', '1');
}
function update() {
  const off = disabled();
  control.hidden = root.dataset.direction !== 'a';
  control.textContent = root.classList.contains('no-motion') || reduced.matches ? 'Movimiento reducido' : 'Sin movimiento';
  if (off) {
    video.pause();
    clearTimeout(timeout);
    scene.classList.remove('is-cinematic');
    scene.style.setProperty('--scene-close', '1');
    // Remove a pending request if accessibility changes before it has loaded.
    if (requested && !ready) { video.removeAttribute('src'); video.load(); requested = ''; }
    return;
  }
  if (failed || !near) return;
  const source = mobile.matches ? video.dataset.mobile : video.dataset.desktop;
  if (source !== requested) {
    requested = source;
    ready = false;
    scene.classList.remove('is-cinematic');
    video.src = source;
    video.preload = 'auto';
    video.load();
    clearTimeout(timeout);
    timeout = setTimeout(fallback, 15000);
  } else if (ready) {
    scene.classList.add('is-cinematic');
    schedule();
  }
}
video.addEventListener('loadeddata', () => {
  if (!requested || failed) return;
  clearTimeout(timeout);
  ready = true;
  scene.dataset.media = mobile.matches ? 'mobile-video' : 'desktop-video';
  update();
});
video.addEventListener('error', () => { if (requested) fallback(); });
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
document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); else schedule(); });
update();
