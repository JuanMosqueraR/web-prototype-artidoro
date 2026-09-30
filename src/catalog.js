import snapshot from './amazonas-variants.json';
import packSnapshot from './ahorrador-variants.json';

// Two representative PDPs. Existing official links remain useful without JavaScript.
const root = document.documentElement;
const home = document.querySelector('#home-main');
const product = document.querySelector('#producto-amazonas');
const menu = document.querySelector('.store-menu');
const form = product.querySelector('form');
const cta = product.querySelector('.product-continue');
const route = '#producto-amazonas';
const official = 'https://www.artidororodriguez.com/products/cafe-amazonas';
const packOfficial = 'https://www.artidororodriguez.com/products/pack-3kg-origenes-1';
const pack = document.querySelector('#producto-ahorrador');
const packForm = pack.querySelector('form');
const pages = { [route]: product, '#producto-ahorrador': pack };
const homeTitle = document.title;
// Native lazy loading can fetch 05 while the visitor is still at the hero.
// Prepare catalog photos only as their section approaches the viewport.
const catalog = document.querySelector('#shop');
function loadCatalog() {
  catalog.querySelectorAll('[data-catalog-src]').forEach(img => { img.src = img.dataset.catalogSrc; });
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting || root.dataset.direction !== 'a') return;
    loadCatalog();
    observer.disconnect();
  }, {rootMargin: '600px 0px'});
  observer.observe(catalog);
} else loadCatalog();
const sizeLabels = { '250g': '250 g', '454gr': '454 g', '1kg': '1 kg' };
let opener = null;
let wasProduct = false;
let viewToken = 0;
history.scrollRestoration = 'manual';

function updateVariant() {
  const values = new FormData(form);
  const variant = snapshot.variants.find(v => v.option1 === values.get('size') && v.option2 === values.get('grind'));
  const available = Boolean(variant?.available);
  const price = variant ? `S/ ${(variant.price / 100).toFixed(2)}` : 'No disponible';
  product.querySelector('.product-price').textContent = price;
  product.querySelector('.product-selection').textContent = variant
    ? `${sizeLabels[variant.option1]} · ${variant.option2 === 'Grano' ? 'En grano' : variant.option2} · ${price}${available ? '' : ' · Agotado'}`
    : 'Esta combinación no está disponible.';
  cta.setAttribute('aria-disabled', String(!available));
  if (available) cta.href = `${official}?variant=${variant.id}`;
  else cta.removeAttribute('href');
}
form.addEventListener('change', updateVariant);
form.addEventListener('submit', event => event.preventDefault());

function updatePack() {
  const chosen = [...packForm.querySelectorAll('select')].map(select => select.value);
  const variant = packSnapshot.variants.find(v => v.options.every((origin, index) => origin === chosen[index]));
  const available = Boolean(variant?.available);
  const price = variant ? `S/ ${(variant.price / 100).toFixed(2)}` : 'No disponible';
  pack.querySelector('.product-price').textContent = price;
  pack.querySelector('.pack-total strong').textContent = price;
  const compareAt = Number(pack.dataset.compareAt);
  const saving = variant && compareAt > variant.price ? compareAt - variant.price : 0;
  pack.querySelector('[data-pack-saving]').hidden = !saving;
  pack.querySelector('[data-pack-total-saving]').hidden = !saving;
  if (saving) {
    const amount = `S/ ${Number.isInteger(saving / 100) ? saving / 100 : (saving / 100).toFixed(2)}`;
    pack.querySelector('[data-pack-saving]').lastChild.textContent = ` · Ahorras ${amount}`;
    pack.querySelector('[data-pack-total-saving]').textContent = ` · Ahorras ${amount}`;
  }
  pack.querySelector('.pack-selection').textContent = variant
    ? chosen.join(' · ') + (available ? '' : ' · Agotado')
    : 'Esta combinación no está disponible.';
  const link = pack.querySelector('.pack-continue');
  link.setAttribute('aria-disabled', String(!available));
  if (available) link.href = `${packOfficial}?variant=${variant.id}`;
  else link.removeAttribute('href');
}
packForm.addEventListener('change', updatePack);
packForm.addEventListener('submit', event => event.preventDefault());

function closeMenu(focus = false) {
  menu.open = false;
  if (focus) menu.querySelector('summary').focus();
}
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.open) closeMenu(true);
});
document.addEventListener('pointerdown', event => {
  if (menu.open && !menu.contains(event.target)) closeMenu();
});
document.addEventListener('focusin', event => {
  if (menu.open && !menu.contains(event.target)) closeMenu();
});
menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });

function render() {
  const token = ++viewToken;
  const active = pages[location.hash];
  const show = Boolean(active);
  home.hidden = show;
  Object.values(pages).forEach(page => { page.hidden = page !== active; });
  document.title = show ? `${active === pack ? 'Pack El Ahorrador' : 'Café Amazonas'} — Artidoro Rodríguez` : homeTitle;
  if (show) {
    root.dataset.direction = 'a';
    if (active === pack) pack.querySelectorAll('[data-pack-src]').forEach(img => {
      if (!img.getAttribute('src')) img.src = img.dataset.packSrc;
    });
    // Hidden home retains 02 state. Its media never intersects on a direct PDP visit.
    requestAnimationFrame(() => {
      if (token !== viewToken) return;
      scrollTo({top: 0, behavior: 'instant'});
      if (opener) active.querySelector('h1').focus({preventScroll: true});
    });
  } else if (wasProduct) {
    requestAnimationFrame(() => {
      if (token !== viewToken) return;
      if (Number.isFinite(history.state?.catalogHomeY)) {
        scrollTo({top: history.state.catalogHomeY, behavior: 'instant'});
        if (opener?.isConnected) opener.focus({preventScroll: true});
      } else {
        const target = document.getElementById(location.hash.slice(1));
        if (target) {
          target.scrollIntoView({behavior: 'instant', block: 'start'});
          target.setAttribute('tabindex', '-1');
          target.focus({preventScroll: true});
        } else scrollTo({top: 0, behavior: 'instant'});
      }
    });
  }
  wasProduct = show;
  closeMenu();
}

document.addEventListener('click', event => {
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const link = event.target.closest('a');
  if (!link) return;
  const href = link.getAttribute('href');
  const coffeeEntry = link.matches('.hero-peru .buy-button, .origin-buy, [data-pdp]') && href === official;
  const packEntry = link.hasAttribute('data-pack-pdp') && href === packOfficial;
  const inProduct = Boolean(pages[location.hash]);
  if (coffeeEntry || packEntry) {
    event.preventDefault();
    event.stopImmediatePropagation();
    opener = link;
    if (!inProduct) history.replaceState({...history.state, catalogHomeY: scrollY}, '', location.href);
    history.pushState({catalogProduct: true, catalogReturn: true}, '', packEntry ? '#producto-ahorrador' : route);
    render();
  } else if (inProduct && link.hasAttribute('data-product-back')) {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (history.state?.catalogReturn) history.back();
    else { history.replaceState(null, '', href); render(); }
  } else if (inProduct && href?.startsWith('#') && href !== location.hash) {
    // Return before the existing home anchor handler measures the hidden section.
    event.preventDefault();
    event.stopImmediatePropagation();
    history.pushState(null, '', href);
    render();
  }
}, true);
window.addEventListener('hashchange', render);
updateVariant();
updatePack();
render();
