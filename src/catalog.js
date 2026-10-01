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
// Prepare catalog photos only as their section approaches the viewport. The closing bands are watched too:
// an anchor jump (header «Cafeterías») can land past the shop without the shop ever intersecting.
function loadCatalog() {
  document.querySelectorAll('#shop [data-catalog-src], .close-bands [data-catalog-src]').forEach(img => { img.src = img.dataset.catalogSrc; });
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    if (!entries.some(entry => entry.isIntersecting) || root.dataset.direction !== 'a') return;
    loadCatalog();
    observer.disconnect();
  }, {rootMargin: '600px 0px'});
  document.querySelectorAll('#shop, .close-bands').forEach(section => observer.observe(section));
} else loadCatalog();
const sizeLabels = { '250g': '250 g', '454gr': '454 g', '1kg': '1 kg' };
const soles = cents => `S/ ${(cents / 100).toFixed(2)}`;
// Sticky buy bar (mobile): mirrors the selection, price and link of the main button.
function syncBar(page, selection, price, href, name, internal = false) {
  const bar = page.querySelector('[data-pdp-bar]');
  if (!bar) return;
  bar.querySelector('[data-bar-selection]').textContent = selection;
  bar.querySelector('[data-bar-price]').textContent = price;
  if (name) bar.querySelector('.pdp-bar-info b').textContent = name;
  const link = bar.querySelector('a');
  if (href) link.href = href; else link.removeAttribute('href');
  setRoute(link, internal);
}
// A product link either leaves for the official store (new tab, external icon) or opens the pack PDP of the demo.
function setRoute(link, internal) {
  link.toggleAttribute('data-pack-pdp', internal);
  if (internal) link.removeAttribute('target'); else link.target = '_blank';
  const icon = link.querySelector('.icon');
  if (icon) { icon.classList.toggle('icon-arrow', internal); icon.classList.toggle('icon-ext', !internal); }
}
// El Ahorrador as the fourth size of the Amazonas PDP (L31): figures from the pack snapshot and its regular price.
const packCents = Math.min(...packSnapshot.variants.map(v => v.price));
const packCompare = Number(document.querySelector('#producto-ahorrador').dataset.compareAt);
const wholeSoles = cents => `S/ ${Number.isInteger(cents / 100) ? cents / 100 : (cents / 100).toFixed(2)}`;
product.querySelector('[data-pack-price]').textContent = wholeSoles(packCents);
product.querySelector('[data-pack-compare]').textContent = wholeSoles(packCompare);
product.querySelector('[data-pack-kilo]').textContent = `${soles(Math.round(packCents / 3))} el kilo`;
product.querySelector('[data-pack-saving-amount]').textContent = wholeSoles(packCompare - packCents);
// The badge holds only while the pack's kilo is cheaper than the 1 kg bag's.
const kiloCents = Math.min(...snapshot.variants.filter(v => v.option1 === '1kg').map(v => v.price));
product.querySelector('[data-pack-badge]').hidden = !(packCents / 3 < kiloCents);
const ctaLabel = cta.firstChild;
const handoff = product.querySelector('.product-handoff');
const handoffText = handoff.textContent;
// Each size button shows its official price (lowest variant of that size in the snapshot).
form.querySelectorAll('input[name=size]').forEach(input => {
  const prices = snapshot.variants.filter(v => v.option1 === input.value).map(v => v.price);
  if (prices.length) input.closest('label').querySelector('[data-size-price]').textContent = soles(Math.min(...prices));
});
let opener = null;
let wasProduct = false;
let viewToken = 0;
history.scrollRestoration = 'manual';

function updateVariant() {
  const values = new FormData(form);
  const packMode = values.get('size') === 'pack';
  form.querySelector('.pdp-grind-field').hidden = packMode;
  form.querySelector('[data-pack-note]').hidden = !packMode;
  form.querySelector('[data-pack-nudge]').hidden = values.get('size') !== '1kg' || packCompare <= packCents;
  if (packMode) {
    const price = soles(packCents);
    product.querySelector('.product-price').textContent = price;
    product.querySelector('[data-yield]').textContent = '3 bolsas de 1 kg · unas 195 tazas';
    product.querySelector('.product-selection').textContent = `Pack El Ahorrador · 3 kg · ${price}`;
    ctaLabel.textContent = `Armar mi pack · ${wholeSoles(packCents)} `;
    cta.href = packOfficial;
    cta.setAttribute('aria-disabled', 'false');
    setRoute(cta, true);
    syncBar(product, '3 bolsas de 1 kg', price, packOfficial, 'El Ahorrador · 3 kg', true);
    handoff.textContent = 'Te llevamos a armar tu pack; desde allí continúas en la tienda oficial.';
    return;
  }
  handoff.textContent = handoffText;
  ctaLabel.textContent = 'Continuar en la tienda ';
  setRoute(cta, false);
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
  // Cups per bag: official FAQ (about 15 g per cup), carried on each size input.
  const size = form.querySelector('input[name=size]:checked');
  product.querySelector('[data-yield]').textContent = `Bolsa de ${size.dataset.label} · unas ${size.dataset.cups} tazas`;
  syncBar(product, variant ? `${sizeLabels[variant.option1]} · ${variant.option2 === 'Grano' ? 'En grano' : variant.option2}` : 'No disponible', price, available ? cta.href : '', 'Amazonas');
}
form.addEventListener('change', updateVariant);
form.querySelector('[data-pick-pack]').addEventListener('click', () => {
  const tier = form.querySelector('input[name=size][value=pack]');
  tier.checked = true;
  updateVariant();
  tier.focus();
});
form.addEventListener('submit', event => event.preventDefault());

// Origin chips for each bag, in the official option order; the pack picture follows the choice.
const packOrigins = packSnapshot.options[0].values;
const slug = origin => origin.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, '-');
const packDefaults = ['Amazonas', 'Cajamarca', 'Puno'];
packForm.querySelectorAll('[data-bag]').forEach(group => {
  const n = Number(group.dataset.bag);
  group.innerHTML = packOrigins.map(origin => `<label class="pdp-chip"><input type="radio" name="bag${n}" value="${origin}"${origin === packDefaults[n - 1] ? ' checked' : ''} /><span><img data-pack-src="/assets/ahorrador-${slug(origin)}-1kg.webp" alt="" width="410" height="840" /><b>${origin}</b></span></label>`).join('');
});
function updatePack() {
  const values = new FormData(packForm);
  const chosen = [1, 2, 3].map(n => values.get(`bag${n}`));
  pack.querySelectorAll('[data-pack-visual] img').forEach((img, index) => {
    const next = `/assets/ahorrador-${slug(chosen[index])}-1kg.webp`;
    if (img.getAttribute('src')) img.src = next; else img.dataset.packSrc = next;
    img.alt = `Bolsa ${index + 1}: café ${chosen[index]} de 1 kg`;
  });
  repeatButton.querySelector('[data-repeat-origin]').textContent = chosen[0];
  repeatButton.hidden = chosen.every(origin => origin === chosen[0]);
  const caption = pack.querySelector('[data-pack-caption]');
  if (caption) caption.textContent = `Tu combinación: ${chosen[0]}, ${chosen[1]} y ${chosen[2]}.`;
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
  syncBar(pack, variant ? chosen.join(' · ') : 'No disponible', price, available ? link.href : '');
}
packForm.addEventListener('change', updatePack);
// Shortcut: the origin of bag 1 in all three bags.
const repeatButton = packForm.querySelector('[data-repeat-bag]');
repeatButton.addEventListener('click', () => {
  const origin = new FormData(packForm).get('bag1');
  [2, 3].forEach(n => { packForm.querySelector(`input[name=bag${n}][value="${origin}"]`).checked = true; });
  updatePack();
});
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
  root.classList.toggle('on-pdp', show);
  Object.values(pages).forEach(page => { page.hidden = page !== active; });
  document.title = show ? `${active === pack ? 'Pack El Ahorrador' : 'Café Amazonas'} — Artidoro Rodríguez` : homeTitle;
  if (show) {
    root.dataset.direction = 'a';
    // PDP pictures are requested only when their page opens (the pages are hidden on the home).
    active.querySelectorAll('[data-pack-src], [data-pdp-src]').forEach(img => {
      if (!img.getAttribute('src')) img.src = img.dataset.packSrc || img.dataset.pdpSrc;
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
    if (packEntry && link.closest('#producto-amazonas')) {
      const first = packForm.querySelector('input[name=bag1][value="Amazonas"]');
      if (first && !first.checked) { first.checked = true; updatePack(); }
    }
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
