// Laboratory only: two independent scenes, one shared product and no app framework.
const root = document.documentElement;
const scenes = { a: document.querySelector('#direction-a'), b: document.querySelector('#direction-b') };
const indicator = document.querySelector('.frame-indicator');
const labels = { a: ['Acercar origen', 'Alejar origen'], b: ['Desplegar origen', 'Plegar origen'] };
const queries = new URLSearchParams(location.search);
let current = 'a';
function updateIndicator() { indicator.textContent = scenes[current].dataset.expanded === 'true' ? 'FRAME B' : 'FRAME A'; }
function setDirection() {
  const requested = location.hash.replace('#', '').toLowerCase() || queries.get('direction') || (location.pathname.match(/\/b\/?$/) ? 'b' : root.dataset.direction);
  current = requested === 'b' ? 'b' : 'a';
  root.dataset.direction = current;
  Object.entries(scenes).forEach(([key, scene]) => { scene.hidden = key !== current; });
  document.querySelectorAll('[data-direction-link]').forEach(link => {
    if (link.dataset.directionLink === current) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  document.querySelector('meta[name="theme-color"]').content = current === 'a' ? '#102e25' : '#30bc4e';
  updateIndicator();
}
function setExpanded(key, expanded) {
  const scene = scenes[key];
  const button = scene.querySelector('[data-reveal]');
  scene.dataset.expanded = String(expanded);
  button.setAttribute('aria-expanded', String(expanded));
  button.querySelector('.origin-button-label').textContent = labels[key][Number(expanded)];
  scene.querySelector('#' + button.getAttribute('aria-controls')).setAttribute('aria-hidden', String(!expanded));
  updateIndicator();
}
document.querySelectorAll('[data-reveal]').forEach(button => {
  button.addEventListener('click', () => {
    const key = button.dataset.reveal;
    setExpanded(key, scenes[key].dataset.expanded !== 'true');
  });
});
const motionToggle = document.querySelector('#reduce-motion');
motionToggle.checked = queries.get('motion') === 'off' || matchMedia('(prefers-reduced-motion: reduce)').matches;
root.classList.toggle('no-motion', motionToggle.checked);
motionToggle.addEventListener('change', () => root.classList.toggle('no-motion', motionToggle.checked));
window.addEventListener('hashchange', setDirection);
setDirection();
if (queries.get('frame') === 'b') setExpanded(current, true);
