// sklozam.cz — menu na mobilu, mapa, galerie (lightbox), videa z YouTube po kliknutí
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* menu na mobilu */
  const btn = $('.menu-btn'), menu = $('.menu');
  btn?.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });

  /* mapa se načte až po rozbalení */
  $$('details.map').forEach(d => d.addEventListener('toggle', () => {
    const f = $('iframe', d);
    if (d.open && !f.src) f.src = f.dataset.src;
  }));

  /* tisk */
  $$('[data-print]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); print(); }));

  /* video: náhled → přehrávač youtube-nocookie */
  $$('.yt').forEach(b => b.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${b.dataset.id}?autoplay=1&rel=0`;
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    f.title = b.getAttribute('aria-label');
    b.replaceChildren(f);
    b.style.cursor = 'default';
  }, { once: true }));

  /* lightbox — listuje v rámci jedné galerie */
  const box = $('#lb');
  if (!box) return;
  const bImg = $('img', box), bCap = $('figcaption', box);
  let group = [], idx = 0;
  const show = i => {
    idx = (i + group.length) % group.length;
    const a = group[idx];
    bImg.src = a.href;
    bImg.alt = a.dataset.cap || '';
    bCap.textContent = a.dataset.cap || '';
  };
  $$('a.lb').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const gal = a.closest('.gal');
    group = gal ? $$('a.lb', gal) : [a];
    box.classList.toggle('single', group.length < 2);
    show(group.indexOf(a));
    box.showModal();
  }));
  $('.lb-prev', box).addEventListener('click', () => show(idx - 1));
  $('.lb-next', box).addEventListener('click', () => show(idx + 1));
  $('[data-close]', box).addEventListener('click', () => box.close());
  box.addEventListener('click', e => { if (e.target === box) box.close(); });
  box.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
})();
