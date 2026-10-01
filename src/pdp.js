// PDP gallery and sticky buy bar (L31). Variants, prices and routing stay in catalog.js.

// Gallery: native horizontal scroll with snap (swipe on touch), plus arrows, thumbnails and a counter.
document.querySelectorAll('[data-gallery]').forEach(gallery => {
  const track = gallery.querySelector('.pdp-track');
  const slides = [...track.children];
  const thumbs = [...gallery.querySelectorAll('.pdp-thumbs button')];
  const counter = gallery.querySelector('[data-gallery-index]');
  const prev = gallery.querySelector('[data-gallery-prev]');
  const next = gallery.querySelector('[data-gallery-next]');
  let current = 0;
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.classList.contains('no-motion');
  function go(index) {
    const target = Math.max(0, Math.min(slides.length - 1, index));
    // scrollIntoView keeps the exact (fractional) slide position; scrollLeft would round and show a sliver of the previous slide.
    slides[target].scrollIntoView({block: 'nearest', inline: 'start', behavior: reduced() ? 'instant' : 'smooth'});
  }
  function mark(index) {
    if (index === current && counter.textContent === String(index + 1)) return;
    current = index;
    counter.textContent = String(index + 1);
    thumbs.forEach((thumb, i) => thumb.setAttribute('aria-current', String(i === index)));
    slides.forEach((slide, i) => slide.setAttribute('aria-hidden', String(i !== index)));
    prev.disabled = index === 0;
    next.disabled = index === slides.length - 1;
  }
  let frame = 0;
  track.addEventListener('scroll', () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => mark(Math.round(track.scrollLeft / Math.max(1, track.clientWidth))));
  }, {passive: true});
  prev.addEventListener('click', () => go(current - 1));
  next.addEventListener('click', () => go(current + 1));
  thumbs.forEach((thumb, i) => thumb.addEventListener('click', () => go(i)));
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      go(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  mark(0);
  zoom(gallery, slides, () => current, go);
});

// Zoom: every slide opens full screen; a tap or click zooms in at that point, scrolling pans, arrows browse.
// The slide is cloned, so composed slides (pack, still life with the real bag) zoom as they are shown.
function zoom(gallery, slides, getCurrent, go) {
  const page = gallery.closest('.product-page');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const ZOOM = 2.2;
  const dialog = document.createElement('dialog');
  dialog.className = 'pdp-lightbox';
  dialog.setAttribute('aria-label', 'Foto ampliada');
  dialog.innerHTML = `<div class="pdp-lb-stage"><div class="pdp-lb-canvas"></div></div>
    <p class="pdp-lb-hint" aria-hidden="true">${fine.matches ? 'Haz clic para acercar' : 'Toca para acercar'}</p>
    <p class="pdp-lb-count" aria-hidden="true"></p>
    <button class="pdp-lb-close" type="button" aria-label="Cerrar foto"><span aria-hidden="true">×</span></button>
    <button class="pdp-lb-nav pdp-lb-prev" type="button" aria-label="Foto anterior"><span class="icon icon-arrow" aria-hidden="true"></span></button>
    <button class="pdp-lb-nav pdp-lb-next" type="button" aria-label="Foto siguiente"><span class="icon icon-arrow" aria-hidden="true"></span></button>
    <button class="pdp-lb-zoom" type="button" aria-pressed="false">Acercar</button>`;
  page.append(dialog);
  const stage = dialog.querySelector('.pdp-lb-stage');
  const canvas = dialog.querySelector('.pdp-lb-canvas');
  const zoomButton = dialog.querySelector('.pdp-lb-zoom');
  let index = 0, zoomed = false, fit = 0, ratio = 1;
  function layout() {
    const w = stage.clientWidth, h = stage.clientHeight;
    fit = Math.min(w * .94, h * .9 * ratio);
    const width = zoomed ? fit * ZOOM : fit;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${width / ratio}px`;
  }
  function setZoom(on, x = .5, y = .5) {
    zoomed = on;
    dialog.classList.toggle('is-zoomed', on);
    zoomButton.setAttribute('aria-pressed', String(on));
    zoomButton.textContent = on ? 'Alejar' : 'Acercar';
    layout();
    if (on) {
      stage.scrollLeft = x * canvas.offsetWidth - stage.clientWidth / 2;
      stage.scrollTop = y * canvas.offsetHeight - stage.clientHeight / 2;
    }
  }
  function show(i) {
    index = (i + slides.length) % slides.length;
    const slide = slides[index];
    // A single photo opens in its own proportions; the bag and pack compositions go portrait on a phone.
    const photo = slide.querySelector(':scope > img');
    if (photo && photo.naturalWidth && !slide.matches('.pdp-slide-bag')) ratio = photo.naturalWidth / photo.naturalHeight;
    else if (!fine.matches && slide.matches('.pdp-slide-bag, .pdp-slide-pack')) ratio = .8;
    else ratio = slide.offsetWidth / Math.max(1, slide.offsetHeight) || 1;
    const clone = slide.cloneNode(true);
    clone.removeAttribute('aria-hidden');
    clone.querySelectorAll('.pdp-zoom').forEach(button => button.remove());
    canvas.replaceChildren(clone);
    dialog.querySelector('.pdp-lb-count').textContent = `${index + 1} / ${slides.length}`;
    setZoom(false);
  }
  function open(i) {
    show(i);
    dialog.showModal();
    document.documentElement.classList.add('lb-open');
    layout();
  }
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('lb-open');
    if (index !== getCurrent()) go(index);
  });
  canvas.addEventListener('click', event => {
    const box = canvas.getBoundingClientRect();
    if (zoomed) setZoom(false);
    else setZoom(true, (event.clientX - box.left) / box.width, (event.clientY - box.top) / box.height);
  });
  stage.addEventListener('click', event => { if (event.target === stage) dialog.close(); });
  // With a mouse the zoomed photo follows the pointer; on touch it pans by native scrolling.
  stage.addEventListener('mousemove', event => {
    if (!zoomed || !fine.matches) return;
    stage.scrollLeft = (event.clientX / stage.clientWidth) * (stage.scrollWidth - stage.clientWidth);
    stage.scrollTop = (event.clientY / stage.clientHeight) * (stage.scrollHeight - stage.clientHeight);
  });
  zoomButton.addEventListener('click', () => setZoom(!zoomed));
  dialog.querySelector('.pdp-lb-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.pdp-lb-prev').addEventListener('click', () => show(index - 1));
  dialog.querySelector('.pdp-lb-next').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') show(index - 1);
    else if (event.key === 'ArrowRight') show(index + 1);
  });
  addEventListener('resize', () => { if (dialog.open) layout(); });
  slides.forEach((slide, i) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'pdp-zoom';
    button.setAttribute('aria-label', 'Ampliar foto');
    button.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M10.5 7.5v6M7.5 10.5h6"/></svg>';
    button.addEventListener('click', event => { event.stopPropagation(); open(i); });
    slide.append(button);
    // A tap on the photo (not a swipe: the browser fires no click after scrolling) opens it too.
    slide.addEventListener('click', () => open(i));
  });
}

// Sticky bar: shown whenever the main button is off screen (before reaching it on a phone, and after passing it).
if ('IntersectionObserver' in window) {
  document.querySelectorAll('.product-page').forEach(page => {
    const bar = page.querySelector('[data-pdp-bar]');
    const cta = page.querySelector('.pdp-cta');
    if (!bar || !cta) return;
    new IntersectionObserver(([entry]) => {
      bar.classList.toggle('is-shown', !entry.isIntersecting && !page.hidden);
    }).observe(cta);
  });
}
