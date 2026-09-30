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

// Let native anchors work without JS. Smooth scrolling only where the path does not cross a pinned
// scroll scene (hero or 03), which would otherwise play through; a crossing jump is instant with a short arrival fade.
const scenes = [document.querySelector('#direction-a'), document.querySelector('#sensory-scene')];
const motionOff = () => reduced.matches || root.classList.contains('no-motion');
function crossesSensory(targetY) {
  const from = scrollY, to = targetY;
  return scenes.some(scene => {
    if (scene.classList.contains('is-static')) return false;
    const box = scene.getBoundingClientRect();
    return Math.min(from, to) < box.bottom + scrollY - 1 && Math.max(from, to) > box.top + scrollY + 1 + innerHeight * .5;
  });
}
document.querySelectorAll('.home-only a[href^="#"], .hero-peru a[href^="#"]').forEach(link => {
  link.addEventListener('click', event => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    history.replaceState(null, '', link.getAttribute('href'));
    const targetY = target.getBoundingClientRect().top + scrollY;
    const smooth = !motionOff() && !crossesSensory(targetY);
    target.scrollIntoView({behavior: smooth ? 'smooth' : 'instant', block: 'start'});
    if (!smooth && !motionOff() && target.id !== 'sensory-scene') {
      target.classList.remove('anchor-arrive');
      void target.offsetWidth;
      target.classList.add('anchor-arrive');
      target.addEventListener('animationend', () => target.classList.remove('anchor-arrive'), {once: true});
    }
    target.setAttribute('tabindex','-1');
    target.focus({preventScroll:true});
  });
});

// Header marker for the Tarata section while it is on screen.
const seatLink = document.querySelector('.nav-cafe');
if (seatLink && 'IntersectionObserver' in window) {
  new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) seatLink.setAttribute('aria-current', 'location');
    else seatLink.removeAttribute('aria-current');
  }, {rootMargin:'-40% 0px -40% 0px'}).observe(document.querySelector('#seat-scene'));
}

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

// L28: the header is transparent while the hero stage is under it, solid everywhere else (and on PDPs).
const heroScene = document.querySelector('#direction-a');
const homeMain = document.querySelector('#home-main');
function syncHeader() {
  const box = heroScene.getBoundingClientRect();
  root.classList.toggle('nav-over-hero', root.dataset.direction === 'a' && !homeMain.hidden && box.height > 0 && box.bottom > innerHeight * .5);
}
addEventListener('scroll', syncHeader, {passive: true});
addEventListener('resize', syncHeader, {passive: true});
new MutationObserver(syncHeader).observe(homeMain, {attributes: true, attributeFilter: ['hidden']});
syncHeader();

// L28: section titles rise line by line once. Split only on plain <br>; decorative breaks keep their class.
const revealTitles = document.querySelectorAll('[data-reveal-lines]');
if (revealTitles.length && 'IntersectionObserver' in window && !motionOff()) {
  revealTitles.forEach(title => {
    title.innerHTML = title.innerHTML.split(/<br\s*\/?>/i).map(line => `<span class="rl"><span>${line.trim()}</span></span>`).join('');
  });
  root.classList.add('reveal-on');
  const titleObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      titleObserver.unobserve(entry.target);
    });
  }, {rootMargin: '0px 0px -8% 0px'});
  revealTitles.forEach(title => titleObserver.observe(title));
}
