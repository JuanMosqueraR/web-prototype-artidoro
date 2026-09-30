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
const sequence = {frames: [], count: 0, active: false, shown: false, base: ''};
function sizeCanvas() {
  const ratio = Math.min(devicePixelRatio || 1, 2);
  const w = Math.round(canvas.clientWidth * ratio), h = Math.round(canvas.clientHeight * ratio);
  if (w && h && (canvas.width !== w || canvas.height !== h)) { canvas.width = w; canvas.height = h; }
}
function drawFrame(ctx, img, alpha) {
  const scale = Math.max(canvas.width / img.naturalWidth, canvas.height / img.naturalHeight);
  const w = img.naturalWidth * scale, h = img.naturalHeight * scale;
  ctx.globalAlpha = alpha;
  ctx.drawImage(img, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
}
function drawSequence(p) {
  if (!sequence.active) return;
  const loaded = i => sequence.frames[i]?.complete && sequence.frames[i].naturalWidth > 0;
  const at = p * (sequence.count - 1);
  let a = Math.floor(at), b = Math.min(sequence.count - 1, a + 1);
  while (a > 0 && !loaded(a)) a--;
  while (b < sequence.count - 1 && !loaded(b)) b++;
  if (!loaded(a)) return;
  sizeCanvas();
  const ctx = canvas.getContext('2d');
  drawFrame(ctx, sequence.frames[a], 1);
  // Blend toward the next loaded frame so 6 fps reads as continuous motion.
  if (b > a && loaded(b)) drawFrame(ctx, sequence.frames[b], clamp((at - a) / (b - a)));
  if (!sequence.shown) { sequence.shown = true; hero.classList.add('has-seq'); }
}
function startSequence() {
  if (sequence.active || still() || ready) return;
  sequence.active = true;
  sequence.count = Number(video.dataset.seqCount) || 0;
  sequence.base = mobile.matches ? video.dataset.seqMobile : video.dataset.seqDesktop;
  video.removeAttribute('src');
  video.load();
  hero.dataset.media = 'sequence';
  // Coarse to fine, so the whole scroll range is covered early and then fills in.
  const order = [];
  for (const step of [6, 3, 1]) for (let i = 0; i < sequence.count; i += step) if (!order.includes(i)) order.push(i);
  order.forEach(i => {
    const img = new Image();
    img.decoding = 'async';
    img.onload = () => { if (Math.abs(i - lastP * (sequence.count - 1)) < 7 || !sequence.shown) drawSequence(lastP); };
    img.src = `${sequence.base}f${String(i).padStart(3, '0')}.webp`;
    sequence.frames[i] = img;
  });
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
function markReady() {
  if (ready || sequence.active || video.readyState < 2 || !Number.isFinite(video.duration)) return;
  ready = true;
  hero.dataset.media = 'video';
  hero.classList.add('has-video');
  heroMotion.jump();
}
function requestVideo() {
  if (still() || navigator.connection?.saveData || sequence.active) return;
  if (mobile.matches) { startSequence(); return; }
  const source = mobile.matches ? video.dataset.mobile : video.dataset.desktop;
  if (source === requested) return;
  requested = source;
  ready = false;
  hero.classList.remove('has-video');
  video.src = source;
  video.preload = 'auto';
  video.load();
  // A muted inline play/pause lets iOS paint seeked frames; normal playback never replaces the scroll.
  const start = video.play();
  if (start) start.then(() => { video.pause(); markReady(); }).catch(() => {});
  // A video that is not usable in time gives way to the image sequence.
  setTimeout(() => { if (!ready) startSequence(); }, 4000);
}
// As in the previous 03: some mobile media loaders never emit loadeddata, so readiness is checked on every
// lifecycle event (a usable frame, not just metadata, is still required by markReady).
for (const event of ['loadeddata', 'canplay', 'progress', 'loadedmetadata', 'seeked']) video.addEventListener(event, () => { markReady(); seek(); });
video.addEventListener('error', () => { if (!requested || sequence.active) return; ready = false; hero.classList.remove('has-video'); startSequence(); });
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
function paintCup(p) {
  set(cup, '--p', p);
  // Small hysteresis so a resting scroll position never flickers between two steps.
  const edges = [.2, .4, .6], margin = .015;
  let n = shownFrame || 1;
  while (n < 4 && p > edges[n - 1] + margin) n++;
  while (n > 1 && p < edges[n - 2] - margin) n--;
  showFrame(n);
}
const cupMotion = damped(() => progressOf(cup), paintCup, 200);

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
}
addEventListener('scroll', onScroll, {passive: true});
addEventListener('resize', onScroll, {passive: true});
mobile.addEventListener('change', () => { requested = ''; if (ready || video.src) requestVideo(); });
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
