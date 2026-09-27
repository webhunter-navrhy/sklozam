// sklozam.cz — menu, galerie, videa po kliknutí, jemná odhalení při scrollu
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* hlavička: linka po odscrollování */
  const top = $('.top');
  const sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;height:8px;width:1px';
  document.body.prepend(sentinel);
  new IntersectionObserver(([e]) => top.classList.toggle('is-scrolled', !e.isIntersecting)).observe(sentinel);

  /* mobilní menu */
  const burger = $('.burger'), nav = $('#nav');
  const setNav = open => {
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  burger.addEventListener('click', () => setNav(!nav.classList.contains('open')));
  $$('a', nav).forEach(a => a.addEventListener('click', () => setNav(false)));

  /* rozbalovací „Další“ */
  const more = $('.more'), moreBtn = $('.more-btn');
  moreBtn?.addEventListener('click', e => {
    e.stopPropagation();
    const open = more.classList.toggle('open');
    moreBtn.setAttribute('aria-expanded', open);
  });
  document.addEventListener('click', e => { if (more && !more.contains(e.target)) { more.classList.remove('open'); moreBtn.setAttribute('aria-expanded', false); } });
  addEventListener('keydown', e => { if (e.key === 'Escape') { setNav(false); more?.classList.remove('open'); } });

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

  /* jemné odhalení */
  if (!reduce && 'IntersectionObserver' in window) {
    const els = $$('.sec .split, .sec .sec-head, .gen-card, .mcard, .film, .school-pics, .school-text, .tcard, .records-docs, .records-text, .prose > .gal, .prose > .fig, .prose > .video, .gen, .pager');
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el, i) => {
      if (el.getBoundingClientRect().top < innerHeight) return; // co je vidět hned, neanimovat
      el.classList.add('rv');
      if (el.matches('.mcard, .gen-card, .tcard')) el.style.transitionDelay = `${(i % 4) * 60}ms`;
      io.observe(el);
    });
  }

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
    const gal = a.closest('.gal, .records-docs');
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
