// L28: inertial wheel scrolling on desktop only. Never on touch, never with reduced motion or .no-motion.
// It eases the native window scroll toward the wheel target; keyboard, scrollbar, anchors and any
// scroll it did not cause take over immediately. Nested scroll areas keep their native wheel.
const root = document.documentElement;
const pointer = matchMedia('(hover: hover) and (pointer: fine)');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
let target = 0, current = 0, running = false, last = 0;
// .lb-open: a PDP photo is open full screen; the wheel then belongs to the zoomed photo, not to the page.
const enabled = () => pointer.matches && !reduced.matches && !root.classList.contains('no-motion') && !root.classList.contains('lb-open') && root.dataset.direction === 'a';

function nestedScroll(element, dy) {
  for (let el = element; el && el !== document.body && el !== root; el = el.parentElement) {
    const style = getComputedStyle(el);
    if (!/(auto|scroll)/.test(style.overflowY) || el.scrollHeight <= el.clientHeight + 1) continue;
    if (dy < 0 ? el.scrollTop > 0 : el.scrollTop + el.clientHeight < el.scrollHeight - 1) return true;
  }
  return false;
}
function tick(time) {
  const dt = Math.min(64, last ? time - last : 16);
  last = time;
  current += (target - current) * (1 - Math.exp(-dt / 110));
  if (Math.abs(target - current) < .5) current = target;
  scrollTo(0, current);
  if (running && current !== target) requestAnimationFrame(tick);
  else { running = false; last = 0; }
}
// Registered only where a fine pointer with hover exists: phones and tablets never carry a non-passive wheel listener.
if (pointer.matches) addEventListener('wheel', event => {
  if (!enabled() || event.ctrlKey || event.defaultPrevented || Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
  if (nestedScroll(event.target, event.deltaY)) return;
  event.preventDefault();
  if (!running) target = current = scrollY;
  const unit = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? innerHeight : 1;
  target = Math.max(0, Math.min(root.scrollHeight - innerHeight, target + event.deltaY * unit));
  if (!running) { running = true; last = 0; requestAnimationFrame(tick); }
}, {passive: false});
// Anything that moves the page away from our own position (keys, scrollbar, anchors) ends the glide.
addEventListener('scroll', () => {
  if (running && Math.abs(scrollY - Math.round(current)) > 3) { running = false; target = current = scrollY; }
}, {passive: true});
