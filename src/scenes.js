// L28 scroll scenes: the hero scrubs one video, 03 plays still-frame steps. Both follow a damped
// progress so a fast flick never jumps. The HTML posters are the base experience; without motion
// (system preference, .no-motion, Save-Data or direction B) each scene shows its final state statically.
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const mobile = matchMedia('(max-width:760px)');
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const seg = (p, a, b) => clamp((p - a) / (b - a));
const ease = t => 1 - Math.pow(1 - t, 3);
const still = () => root.dataset.direction !== 'a' || root.classList.contains('no-motion') || reduced.matches;

function progressOf(section) {
  const stage = section.firstElementChild;
  const top = parseFloat(getComputedStyle(stage).top) || 0;
  const range = section.offsetHeight - stage.offsetHeight;
  return clamp((top - section.getBoundingClientRect().top) / Math.max(1, range));
}
// The value eases toward the scroll position (time constant tau) and stops once it arrives.
function damped(read, apply, tau) {
  let value = null, last = 0, running = false;
  function tick(time) {
    const target = read();
    if (value === null) value = target;
    const dt = Math.min(64, last ? time - last : 16);
    last = time;
    value += (target - value) * (1 - Math.exp(-dt / tau));
    if (Math.abs(target - value) < .0005) value = target;
    apply(value);
    if (value !== target) requestAnimationFrame(tick);
    else { running = false; last = 0; }
  }
  return {
    kick() { if (!running) { running = true; requestAnimationFrame(tick); } },
    jump() { value = read(); apply(value); },
  };
}
function loadDeferred(scope) {
  scope.querySelectorAll('[data-srcset]').forEach(source => { source.srcset = source.dataset.srcset; source.removeAttribute('data-srcset'); });
  scope.querySelectorAll('[data-src]').forEach(img => { img.src = img.dataset.src; img.removeAttribute('data-src'); });
}
const set = (el, name, value) => el.style.setProperty(name, value.toFixed(4));

// --- Hero: «Del cafetal a tu bolsa» -------------------------------------------------
// Desktop scrubs the video. Mobile (and any browser whose video is not ready in time) draws the same
// encode as a 6 fps image sequence on a canvas: iOS Safari does not reliably prepare a video that is
// never played, and an image sequence always paints. hero.dataset.media reports the active path.
const hero = document.querySelector('#direction-a');
const video = hero.querySelector('.hs-video');
const canvas = hero.querySelector('.hs-seq');
let ready = false, requested = '', wanted = 0, lastP = 0;
function seek() {
  if (!ready || video.seeking) return;
  if (Math.abs(video.currentTime - wanted) > .03) video.currentTime = wanted;
}
const sequence = {frames: [], count: 0, active: false, shown: false, base: '', ext: '', bitmaps: new Map(), pending: new Set(), failed: 0, disposed: false};
// 2×2 AVIF used to learn whether this browser decodes AVIF (iOS < 16 does not): it then gets the 6 fps WebP set.
const AVIF_PROBE = 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADrbWV0YQAAAAAAAAAhaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAAAAAAAOcGl0bQAAAAAAAQAAAB5pbG9jAAAAAEQAAAEAAQAAAAEAAAETAAAAGAAAAChpaW5mAAAAAAABAAAAGmluZmUCAAAAAAEAAGF2MDFDb2xvcgAAAABqaXBycAAAAEtpcGNvAAAAFGlzcGUAAAAAAAAAAgAAAAIAAAAQcGl4aQAAAAADCAgIAAAADGF2MUOBAAwAAAAAE2NvbHJuY2x4AAEADQAGgAAAABdpcG1hAAAAAAAAAAEAAQQBAoMEAAAAIG1kYXQSAAoFGAA2BCAyDRmAEEEEBAAAsBNdtUA=';
const avifSupported = () => new Promise(resolve => {
  const probe = new Image();
  probe.onload = () => resolve(probe.width === 2);
  probe.onerror = () => resolve(false);
  probe.src = AVIF_PROBE;
});
function sizeCanvas() {
  const ratio = Math.min(devicePixelRatio || 1, 2);
  const w = Math.round(canvas.clientWidth * ratio), h = Math.round(canvas.clientHeight * ratio);
  if (w && h && (canvas.width !== w || canvas.height !== h)) { canvas.width = w; canvas.height = h; }
}
const frameReady = i => { const img = sequence.frames[i]; return Boolean(img && img.complete && img.naturalWidth > 0); };
// Decoded bitmaps are kept only around the current frame: ~120 full-size frames decoded at once would cost
// hundreds of MB on a phone. Outside the window a frame is decoded from the image on demand.
function keepBitmaps(center) {
  for (let i = Math.max(0, center - 3); i <= Math.min(sequence.count - 1, center + 8); i++) {
    if (sequence.bitmaps.has(i) || sequence.pending.has(i) || !frameReady(i) || !window.createImageBitmap) continue;
    sequence.pending.add(i);
    createImageBitmap(sequence.frames[i]).then(bitmap => {
      sequence.pending.delete(i);
      if (sequence.active) sequence.bitmaps.set(i, bitmap); else bitmap.close();
    }).catch(() => sequence.pending.delete(i));
  }
  for (const [i, bitmap] of sequence.bitmaps) if (i < center - 8 || i > center + 14) { bitmap.close(); sequence.bitmaps.delete(i); }
}
function drawFrame(ctx, i, alpha) {
  const src = sequence.bitmaps.get(i) || sequence.frames[i];
  const sw = src.naturalWidth || src.width, sh = src.naturalHeight || src.height;
  const scale = Math.max(canvas.width / sw, canvas.height / sh);
  ctx.globalAlpha = alpha;
  ctx.drawImage(src, (canvas.width - sw * scale) / 2, (canvas.height - sh * scale) / 2, sw * scale, sh * scale);
}
function drawSequence(p) {
  if (!sequence.active || !sequence.count) return;
  const at = p * (sequence.count - 1);
  let a = Math.floor(at), b = Math.min(sequence.count - 1, a + 1);
  while (a > 0 && !frameReady(a)) a--;
  while (b < sequence.count - 1 && !frameReady(b)) b++;
  if (!frameReady(a)) return;
  sizeCanvas();
  const ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  drawFrame(ctx, a, 1);
  // Blend toward the next loaded frame so the frame rate reads as continuous motion.
  if (b > a && frameReady(b)) drawFrame(ctx, b, clamp((at - a) / (b - a)));
  keepBitmaps(Math.round(at));
  if (!sequence.shown) { sequence.shown = true; hero.classList.add('has-seq'); }
}
function loadSequence(format) {
  const device = mobile.matches ? 'mobile' : 'desktop';
  sequence.ext = format;
  sequence.count = Number(video.dataset[`seq${format === 'avif' ? 'Avif' : 'Webp'}`]) || 0;
  sequence.base = `${video.dataset.seq}${device}-${format}/`;
  sequence.frames = [];
  sequence.failed = 0;
  hero.dataset.media = 'sequence';
  // Coarse to fine, so the whole scroll range is covered early and then fills in.
  const order = [];
  for (const step of [8, 4, 2, 1]) for (let i = 0; i < sequence.count; i += step) if (!order.includes(i)) order.push(i);
  order.forEach(i => {
    const img = new Image();
    img.decoding = 'async';
    img.onload = () => { if (!sequence.shown || Math.abs(i - lastP * (sequence.count - 1)) < 9) drawSequence(lastP); };
    // A format the browser cannot decode: start again with WebP, once.
    img.onerror = () => { if (format === 'avif' && ++sequence.failed === 3 && sequence.ext === 'avif') { sequence.active = true; sequence.shown = false; loadSequence('webp'); } };
    img.src = `${sequence.base}f${String(i).padStart(3, '0')}.${format}`;
    sequence.frames[i] = img;
  });
}
function startSequence() {
  if (sequence.active || still() || ready) return;
  sequence.active = true;
  clearTimeout(primeTimer);
  video.removeAttribute('src');
  video.load();
  avifSupported().then(ok => { if (sequence.active) loadSequence(ok ? 'avif' : 'webp'); });
}
function stopSequence() {
  if (!sequence.active) return;
  sequence.active = false;
  for (const bitmap of sequence.bitmaps.values()) bitmap.close();
  sequence.bitmaps.clear();
  sequence.frames = [];
  hero.classList.remove('has-seq');
}
// Once the hero is far above the viewport the decoded frames are released (a phone cannot hold ~120 of them
// comfortably); the canvas keeps its last picture and the frames come back from the HTTP cache when the visitor returns.
function sequenceMemory() {
  const bottom = hero.getBoundingClientRect().bottom;
  if (sequence.active && sequence.count) {
    if (!sequence.disposed && bottom < -innerHeight * 2) {
      sequence.disposed = true;
      for (const bitmap of sequence.bitmaps.values()) bitmap.close();
      sequence.bitmaps.clear();
      sequence.frames = [];
    } else if (sequence.disposed && bottom > -innerHeight) {
      sequence.disposed = false;
      loadSequence(sequence.ext);
    }
  }
  // The same for the video: its decoder and buffers are released far from the hero and prepared again on return.
  if (ready && bottom < -innerHeight * 2) {
    ready = false;
    requested = '';
    hero.classList.remove('has-video');
    video.removeAttribute('src');
    video.load();
  } else if (!ready && !requested && !sequence.active && bottom > -innerHeight) requestVideo();
}
function paintHero(p) {
  lastP = p;
  set(hero, '--p', p);
  set(hero, '--s1', 1 - seg(p, .28, .34));
  set(hero, '--s2', Math.min(seg(p, .36, .42), 1 - seg(p, .66, .72)));
  set(hero, '--s3', seg(p, .8, .88));
  set(hero, '--bag', ease(seg(p, .8, .96)));
  set(hero, '--bagv', seg(p, .8, .86));
  set(hero, '--end', seg(p, .62, .8));
  hero.dataset.step = p < .35 ? '1' : p < .78 ? '2' : '3';
  if (ready) { wanted = p * Math.max(0, video.duration - .06); seek(); } else drawSequence(p);
}
const heroMotion = damped(() => progressOf(hero), paintHero, 170);
let primeTimer = 0, videoTimer = 0;
function markReady() {
  if (ready || !requested || video.readyState < 2 || !Number.isFinite(video.duration)) return;
  clearTimeout(primeTimer);
  clearTimeout(videoTimer);
  ready = true;
  stopSequence();
  hero.dataset.media = 'video';
  hero.classList.add('has-video');
  heroMotion.jump();
}
// Video first, on every device: it is the sharpest and smoothest path. If it is not usable in time the same shot
// is drawn from an image sequence instead (iOS in Low Power Mode, or any browser that will not prepare the video).
function requestVideo() {
  if (still() || navigator.connection?.saveData || ready || requested) return;
  requested = mobile.matches ? video.dataset.mobile : video.dataset.desktop;
  hero.dataset.media = 'loading';
  video.src = requested;
  video.preload = 'auto';
  video.load();
  // The previous 03 needed no play(). If nothing is usable after 1.5 s, try a muted play/pause (some iOS states allow it).
  primeTimer = setTimeout(() => {
    if (ready) return;
    const start = video.play();
    if (start) start.then(() => { video.pause(); markReady(); }).catch(() => {});
  }, 1500);
  videoTimer = setTimeout(() => { if (!ready) startSequence(); }, 3500);
}
// Some mobile media loaders never emit loadeddata, so readiness is checked on every lifecycle event
// (a usable frame, not just metadata, is still required by markReady).
for (const event of ['loadeddata', 'canplay', 'progress', 'loadedmetadata', 'seeked']) video.addEventListener(event, () => { markReady(); seek(); });
video.addEventListener('error', () => { if (video.getAttribute('src') && !ready) startSequence(); });
addEventListener('resize', () => { if (sequence.active) drawSequence(lastP); }, {passive: true});

// --- 03: «De la bolsa a tu taza» ---------------------------------------------------------
const cup = document.querySelector('#sensory-scene');
const frames = [...cup.querySelectorAll('.cs-frame')];
let shownFrame = 0;
function showFrame(n) {
  if (n === shownFrame) return;
  shownFrame = n;
  frames.forEach((frame, i) => frame.classList.toggle('is-shown', i < n));
  cup.dataset.step = n === 1 ? '1' : n < 4 ? '2' : '3';
}
// Frames follow the scroll position and overlap in time; STEP_DWELL (ms) is only a short guard against flicker. A longer
// hold cannot coexist with fast scrolling: the pinned range lasts ~2 s at 1000 px/s, so a queue of holds would show the
// final frame only after the scene had already left the screen.
const STEP_DWELL = [450, 450, 450];
let stepAt = 0, stepTimer = 0, wantFrame = 1;
function advanceFrame() {
  stepTimer = 0;
  if (wantFrame === shownFrame) return;
  const wait = STEP_DWELL[Math.max(0, shownFrame - 1)] - (performance.now() - stepAt);
  if (shownFrame && wait > 0) { stepTimer = setTimeout(advanceFrame, wait); return; }
  stepAt = performance.now();
  showFrame(shownFrame + Math.sign(wantFrame - shownFrame));
  if (wantFrame !== shownFrame) stepTimer = setTimeout(advanceFrame, STEP_DWELL[Math.max(0, shownFrame - 1)]);
}
function paintCup(p) {
  set(cup, '--p', p);
  // Small hysteresis so a resting scroll position never flickers between two steps.
  const edges = [.12, .3, .46], margin = .01;
  let n = wantFrame;
  while (n < 4 && p > edges[n - 1] + margin) n++;
  while (n > 1 && p < edges[n - 2] - margin) n--;
  wantFrame = n;
  if (!stepTimer) advanceFrame();
}
const cupMotion = damped(() => progressOf(cup), paintCup, 130);

// --- Shared lifecycle ---------------------------------------------------------------------
function update() {
  const off = still();
  hero.classList.toggle('is-static', off);
  cup.classList.toggle('is-static', off);
  if (off) {
    loadDeferred(hero);
    loadDeferred(cup);
    video.pause();
    paintHero(1);
    clearTimeout(stepTimer); stepTimer = 0; wantFrame = 4;
    showFrame(4);
    set(cup, '--p', 1);
    return;
  }
  heroMotion.jump();
  cupMotion.jump();
}
function onScroll() {
  if (still()) return;
  heroMotion.kick();
  cupMotion.kick();
  sequenceMemory();
}
addEventListener('scroll', onScroll, {passive: true});
addEventListener('resize', onScroll, {passive: true});
mobile.addEventListener('change', () => { stopSequence(); ready = false; requested = ''; hero.classList.remove('has-video'); requestVideo(); });
reduced.addEventListener('change', update);
new MutationObserver(update).observe(root, {attributes: true, attributeFilter: ['class', 'data-direction']});
document.addEventListener('visibilitychange', () => { if (!document.hidden) { markReady(); seek(); } });

// The first frame is the LCP poster: the video, the end frame and 03 wait until after load.
function afterLoad() {
  loadDeferred(hero);
  const idle = window.requestIdleCallback || (fn => setTimeout(fn, 600));
  idle(requestVideo, {timeout: 1500});
}
if (document.readyState === 'complete') afterLoad(); else addEventListener('load', afterLoad, {once: true});
addEventListener('scroll', requestVideo, {passive: true, once: true});
if ('IntersectionObserver' in window) {
  const near = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting || root.dataset.direction !== 'a') return;
    loadDeferred(cup);
    near.disconnect();
  }, {rootMargin: '900px 0px'});
  near.observe(cup);
} else loadDeferred(cup);
update();
