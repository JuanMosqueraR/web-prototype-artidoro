// Home navigation and motion preference. Origin selection remains local to 02.
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const motionButton = document.querySelector('[data-home-motion]');
const labToggle = document.querySelector('#reduce-motion');
function syncMotionButton() {
  const off = root.classList.contains('no-motion') || reduced.matches;
  motionButton.setAttribute('aria-pressed', String(off));
  motionButton.textContent = off ? 'Movimiento reducido' : 'Reducir movimiento';
}
motionButton?.addEventListener('click', () => {
  // A system accessibility preference always wins over the site's switch.
  if (reduced.matches) return;
  root.classList.toggle('no-motion');
  labToggle.checked = root.classList.contains('no-motion');
  syncMotionButton();
});
new MutationObserver(syncMotionButton).observe(root, {attributes:true,attributeFilter:['class']});
reduced.addEventListener('change', syncMotionButton);
syncMotionButton();

// Let native anchors work without JS; improve focus and avoid smooth-scrolling through 03.
document.querySelectorAll('.home-only a[href^="#"], .hero-peru a[href^="#"]').forEach(link => {
  link.addEventListener('click', event => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    history.replaceState(null, '', link.getAttribute('href'));
    target.scrollIntoView({behavior:'instant',block:'start'});
    target.setAttribute('tabindex','-1');
    target.focus({preventScroll:true});
  });
});

// Tarata: a single entrance, then still photographs. Visible without JS; no scroll pinning.
const seat = document.querySelector('#seat-scene');
function loadSeatPhotos() {
  seat.querySelectorAll('[data-seat-srcset]').forEach(source => { source.srcset = source.dataset.seatSrcset; });
  seat.querySelectorAll('[data-seat-src]').forEach(img => { img.src = img.dataset.seatSrc; });
}
if (seat && 'IntersectionObserver' in window) {
  const photoObserver = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting || root.dataset.direction !== 'a') return;
    loadSeatPhotos();
    photoObserver.disconnect();
  }, {rootMargin:'800px 0px'});
  photoObserver.observe(seat);
  const seatObserver = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting || root.dataset.direction !== 'a') return;
    if (!reduced.matches && !root.classList.contains('no-motion')) seat.classList.add('seat-entered');
    seatObserver.disconnect();
  }, {rootMargin:'0px 0px -32px 0px', threshold:0});
  seatObserver.observe(seat);
} else if (seat) loadSeatPhotos();
