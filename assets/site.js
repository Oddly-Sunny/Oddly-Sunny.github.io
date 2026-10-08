/* oddly sunny: shared behaviour */
(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // header: solid on scroll, mobile menu
  var hdr = $('.hdr');
  function onScroll() { if (!hdr) return; hdr.classList.toggle('scrolled', window.scrollY > 12); if (hdr.hasAttribute('data-away')) hdr.classList.toggle('away', window.scrollY < 90); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = $('.burger');
  if (burger) burger.addEventListener('click', function () {
    var open = document.body.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('menu-open'); }); });

  // hero logo entrance (same pop + nudge as before)
  var hm = $('#heroMark');
  if (hm) {
    setTimeout(function () { hm.classList.add('animate'); }, 250);
    setTimeout(function () { hm.classList.add('ready'); }, 2300);
  }

  // home: show the header logo only while the animated hero logo is out of view
  if (hm && hdr && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      hdr.classList.toggle('brand-hidden', es[0].isIntersecting);
    }, { threshold: 0.2 }).observe(hm);
  }

  // reveal on scroll
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal,.frame').forEach(function (el) { io.observe(el); });

  // lit words on scroll
  var hls = $$('[data-highlight]');
  function lit() {
    hls.forEach(function (b) {
      var words = $$('.word', b), r = b.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (window.innerHeight - r.top) / (window.innerHeight + r.height * 0.4)));
      words.forEach(function (w, i) { w.classList.toggle('lit', p >= (i / words.length) * 0.62 + 0.12); });
    });
  }
  if (hls.length) { window.addEventListener('scroll', lit, { passive: true }); lit(); }

  // header takes the scheme of the section beneath it (green / purple / ember / cream / tan)
  var secs = $$('[data-scheme]').filter(function (e) { return e !== hdr && e.tagName === 'SECTION'; });
  function hdrScheme() {
    if (!hdr) return;
    var cur = 'green';
    secs.forEach(function (s) { var r = s.getBoundingClientRect(); if (r.top <= 40 && r.bottom > 40) cur = s.getAttribute('data-scheme'); });
    if (hdr.getAttribute('data-scheme') !== cur) hdr.setAttribute('data-scheme', cur);
  }
  window.addEventListener('scroll', hdrScheme, { passive: true }); hdrScheme();

  // work filters
  var fb = $$('.filters button');
  fb.forEach(function (b) {
    b.addEventListener('click', function () {
      fb.forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var f = b.getAttribute('data-f');
      $$('.item[data-cat]').forEach(function (c) {
        c.classList.toggle('hide', f !== 'all' && c.getAttribute('data-cat').split(' ').indexOf(f) < 0);
      });
    });
  });
})();

/* analytics + cookie consent (Consent Mode v2, same storage key as before) */
(function () {
  var KEY = 'oddly-sunny:consent';
  var GDPR = {AT:1,BE:1,BG:1,HR:1,CY:1,CZ:1,DK:1,EE:1,FI:1,FR:1,DE:1,GR:1,HU:1,IE:1,IT:1,LV:1,LT:1,LU:1,MT:1,NL:1,PL:1,PT:1,RO:1,SK:1,SI:1,ES:1,SE:1,IS:1,LI:1,NO:1,GB:1,CH:1};
  var local = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { dataLayer.push(arguments); };
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
  gtag('js', new Date());
  gtag('config', 'G-Q5VRS4WZ09');
  if (!local) {
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-Q5VRS4WZ09';
    document.head.appendChild(s);
  }

  var css = document.createElement('style');
  css.textContent = '#cookieBanner{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;margin:0 auto;max-width:600px;background:#0d2119;color:#eef3ef;border:1px solid rgba(238,243,239,.16);border-radius:16px;padding:16px 18px;box-shadow:0 24px 50px -28px rgba(0,0,0,.7);display:flex;gap:14px;align-items:center;flex-wrap:wrap;font-family:Sora,system-ui,sans-serif}#cookieBanner[hidden]{display:none}#cookieMsg{margin:0;flex:1 1 260px;font-size:13.5px;line-height:1.5;opacity:.9}#cookieBanner .cc-btns{display:flex;gap:8px;flex-wrap:wrap}#cookieBanner button{font:inherit;font-size:13px;font-weight:500;padding:8px 16px;border-radius:999px;cursor:pointer;border:1px solid transparent;transition:opacity .15s}#cookieBanner button:hover{opacity:.85}#cookieBanner.cc-optin .cc-primary,#cookieBanner.cc-optin .cc-secondary,#cookieBanner.cc-optout .cc-primary{background:#eef3ef;color:#0d2119;border-color:#eef3ef}#cookieBanner.cc-optout .cc-secondary{background:transparent;color:#eef3ef;border-color:rgba(238,243,239,.5)}#cookieBanner .cc-learn{color:inherit;opacity:.75;font-size:12px;text-decoration:underline;white-space:nowrap}';
  document.head.appendChild(css);
  var banner = document.createElement('div');
  banner.id = 'cookieBanner'; banner.setAttribute('role', 'dialog'); banner.setAttribute('aria-label', 'Cookie choices'); banner.hidden = true;
  banner.innerHTML = '<p id="cookieMsg"></p><div class="cc-btns"><button type="button" class="cc-secondary" id="cookieDecline"></button><button type="button" class="cc-primary" id="cookieAccept"></button></div>';
  document.body.appendChild(banner);
  var msg = banner.querySelector('#cookieMsg'), acceptBtn = banner.querySelector('#cookieAccept'), declineBtn = banner.querySelector('#cookieDecline');

  function read() { try { var v = localStorage.getItem(KEY); return (v === 'granted' || v === 'denied') ? v : null; } catch (e) { return null; } }
  function apply(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
    gtag('consent', 'update', { analytics_storage: v, ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
  }
  function hasGpc() { try { return navigator.globalPrivacyControl === true; } catch (e) { return false; } }
  function show(mode) {
    var optIn = mode === 'optin';
    banner.className = optIn ? 'cc-optin' : 'cc-optout';
    msg.innerHTML = (optIn
      ? 'We would like to use a little analytics to see how the site is used. We will not set any cookies until you agree.'
      : 'We use a little analytics to see how the site is used. Nothing personal, and you can opt out any time.') + ' <a href="/privacy/" class="cc-learn">Learn more</a>';
    declineBtn.textContent = optIn ? 'Decline' : 'Opt out';
    acceptBtn.textContent = optIn ? 'Accept' : 'Got it';
    banner.hidden = false;
  }
  function choose(v) { apply(v); banner.hidden = true; }
  acceptBtn.addEventListener('click', function () { choose('granted'); });
  declineBtn.addEventListener('click', function () { choose('denied'); });

  var existing = read(), gpc = hasGpc();
  if (existing) apply(existing); else if (gpc) apply('denied');
  fetch('/cdn-cgi/trace').then(function (r) { return r.text(); }).then(function (t) {
    var m = /(?:^|\n)loc=([A-Z]{2})/.exec(t), cc = m ? m[1] : '';
    var optIn = !cc || !!GDPR[cc];
    if (existing || gpc) return;
    if (optIn) show('optin'); else { apply('granted'); show('optout'); }
  }).catch(function () { if (!existing && !gpc) show('optin'); });
})();

/* hero: floating photos. One slot changes at a time, slowly, and nothing repeats on screen. */
(function () {
  var hero = document.querySelector('.hero[data-imgs]');
  if (!hero) return;
  var pools = {}; try { pools = JSON.parse(hero.getAttribute('data-imgs')); } catch (e) {}
  var slots = Array.prototype.slice.call(hero.querySelectorAll('.float'));
  if (!slots.length) return;
  var ptr = { p: 0, l: 0 }, shown = {};
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function pick(slot) {
    var k = slot.getAttribute('data-pool'), list = pools[k] || [];
    for (var n = 0; n < list.length; n++) {
      var it = list[ptr[k]++ % list.length];
      if (!shown[it.src]) return it;
    }
    return list[0];
  }
  function load(slot, done) {
    var it = pick(slot); if (!it) return;
    shown[it.src] = 1;
    var img = slot.querySelector('img'), pre = new Image();
    pre.onload = function () {
      var old = slot.getAttribute('data-src'); if (old) delete shown[old];
      shown[it.src] = 1; slot.setAttribute('data-src', it.src);
      img.src = it.src; img.style.objectPosition = it.pos + ' 50%'; done();
    };
    pre.src = it.src;
  }
  function show(slot) { requestAnimationFrame(function () { slot.classList.add('in'); }); }
  /* fetch every first photo at once, reveal them in pairs as soon as they are ready */
  slots.forEach(function (slot, i) {
    var at = 120 + Math.floor(i / 2) * 300, t0 = Date.now();
    load(slot, function () {
      setTimeout(function () { show(slot); }, Math.max(0, at - (Date.now() - t0)));
    });
  });
  if (still) return;
  var last = -1;
  setInterval(function () {
    var i; do { i = Math.floor(Math.random() * slots.length); } while (i === last && slots.length > 1);
    last = i; var slot = slots[i];
    slot.classList.remove('in');
    setTimeout(function () { load(slot, function () { show(slot); }); }, 1200);
  }, 6500);
})();

/* method panel: a dotted, warped coordinate mesh (Joukowski map) that drifts slowly; dots flow along the lines.
   Ported from the Airwaves IQ hero. Hover joins nearby dots into faint traces. */
(function () {
  var canvas = document.querySelector('canvas.mesh');
  if (!canvas) return;
  var ctx = canvas.getContext('2d'); if (!ctx) return;
  var DOT = 'rgba(24,18,8,', SPACING = 5.2;
  var v = { k: 1, rot: 0.75, cx: 0.5, cy: 0.6, scale: 0.5, rings: 26, rays: 40, rmax: 6.2, mirror: false };
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = 0, H = 0, dpr = 1, raf = 0, visible = true, last = 0;
  var hov = { x: 0, y: 0, tx: 0, ty: 0, a: 0, ta: 0 };

  function resize() {
    var r = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    draw(performance.now());
  }

  function draw(now) {
    var t = now / 1000;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    hov.x += (hov.tx - hov.x) * 0.07; hov.y += (hov.ty - hov.y) * 0.07; hov.a += (hov.ta - hov.a) * 0.06;
    var k = v.k + (reduced ? 0 : 0.17 * Math.sin(t * 0.38) + 0.07 * Math.sin(t * 0.21 + 1.3));
    var spin = reduced ? 0 : t * 0.045;
    var f = reduced ? 0 : (((t * 2.2) % 1) + 1) % 1;
    var S = Math.max(W / 9, H / 2.6) * v.scale, cx = W * v.cx, cy = H * v.cy, flip = v.mirror ? -1 : 1;
    var cosR = Math.cos(v.rot), sinR = Math.sin(v.rot);
    ctx.clearRect(0, 0, W, H);
    var TR = Math.max(120, Math.min(W, H) * 0.42), px = 0, py = 0, pw = 0, has = false;
    function put(re, im, a) {
      var x = cx + flip * S * (re * cosR - im * sinR), y = cy - S * (re * sinR + im * cosR);
      var inside = !(x < -2 || x > W + 2 || y < -2 || y > H + 2), w = 0;
      if (hov.a > 0.01) { var d = Math.hypot(x - hov.x, y - hov.y); if (d < TR) w = Math.pow(1 - d / TR, 1.5) * hov.a; }
      if (inside) { ctx.fillStyle = DOT + a.toFixed(2) + ')'; ctx.fillRect(x - 0.6, y - 0.6, 1.2, 1.2); }
      if (has && (w > 0.02 || pw > 0.02)) {
        ctx.strokeStyle = DOT + (0.34 * Math.max(w, pw)).toFixed(3) + ')'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(x, y); ctx.stroke();
      }
      px = x; py = y; pw = w; has = true;
    }
    var step = SPACING / S, g = Math.pow(v.rmax, 1 / v.rings), i, guard;
    for (i = 0; i <= v.rings; i++) {
      var r = Math.pow(g, i), a = 0.72 - 0.22 * (i / v.rings), sx = r + k / r, sy = r - k / r, th = 0, first = true;
      has = false;
      for (guard = 0; th < Math.PI * 2 && guard < 4000; guard++) {
        var sp = Math.max(Math.hypot(sx * Math.sin(th), sy * Math.cos(th)), 0.02), d = step / sp;
        if (first) { th += f * d; first = false; }
        put(sx * Math.cos(th), sy * Math.sin(th), a); th += d;
      }
    }
    for (var j = 0; j < v.rays; j++) {
      var th2 = (j / v.rays) * Math.PI * 2 + spin, c = Math.cos(th2), s = Math.sin(th2), rr = 1.0, first2 = true;
      has = false;
      for (guard = 0; rr < v.rmax && guard < 4000; guard++) {
        var sp2 = Math.max(Math.hypot((1 - k / (rr * rr)) * c, (1 + k / (rr * rr)) * s), 0.05), d2 = Math.min(step / sp2, 0.25);
        if (first2) { rr += f * d2; first2 = false; }
        put((rr + k / rr) * c, (rr - k / rr) * s, 0.66 - 0.2 * (rr / v.rmax)); rr += d2;
      }
    }
  }
  function loop(now) {
    raf = requestAnimationFrame(loop);
    if (!visible || now - last < (hov.a > 0.01 || hov.ta > 0 ? 16 : 33)) return;
    last = now; draw(now);
  }
  if (!reduced && window.matchMedia && window.matchMedia('(pointer: fine)').matches) {
    canvas.addEventListener('pointermove', function (e) {
      var r = canvas.getBoundingClientRect(); hov.tx = e.clientX - r.left; hov.ty = e.clientY - r.top;
      if (hov.ta === 0 && hov.a < 0.01) { hov.x = hov.tx; hov.y = hov.ty; } hov.ta = 1;
    });
    canvas.addEventListener('pointerleave', function () { hov.ta = 0; });
  }
  resize();
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(canvas);
  if (!reduced) raf = requestAnimationFrame(loop);
})();

/* header logo "life": random short routines (wink, blink, glance, gold cell morphs) every few seconds */
(function () {
  var svg = document.querySelector('.hdr .live-mark');
  if (!svg || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var c1 = svg.querySelector('.c1'), c2 = svg.querySelector('.c2'), c4 = svg.querySelector('.c4');
  var shapes = {}; Array.prototype.forEach.call(svg.querySelectorAll('.sh'), function (g) { shapes[g.getAttribute('data-s')] = g; });
  var cur = 'diamond', busy = false;
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function shape(n) { if (n === cur) return; shapes[cur].classList.remove('on'); shapes[n].classList.add('on'); cur = n; }
  function lids(cells, v) { cells.forEach(function (c) { c.style.transform = v ? 'scaleY(' + v + ')' : ''; }); }
  function shift(cells, x, y) { cells.forEach(function (c) { c.style.transform = (x || y) ? 'translate(' + x + 'px,' + y + 'px)' : ''; }); }
  var routines = [
    async function () { lids([c2], 0.1); await sleep(170); lids([c2]); },                       // wink
    async function () { lids([c1], 0.1); await sleep(170); lids([c1]); },                       // wink, other side
    async function () { lids([c1, c2], 0.1); await sleep(110); lids([c1, c2]); await sleep(130); lids([c1, c2], 0.1); await sleep(110); lids([c1, c2]); }, // double blink
    async function () { shift([c1, c2], -5, 0); await sleep(550); shift([c1, c2], 5, -2); await sleep(550); shift([c1, c2]); },  // look around
    async function () { shape('triangle'); await sleep(1500); shape('diamond'); },
    async function () { shape('arrow'); await sleep(650); shape('circle'); await sleep(650); shape('check'); await sleep(900); shape('diamond'); },
    async function () { shape('heart'); shift([c1, c2], 0, -3); await sleep(1500); shift([c1, c2]); shape('diamond'); },
    async function () { shape('plus'); await sleep(1300); shape('diamond'); },
    async function () { shape('check'); shift([c1, c2], 0, -3); await sleep(1300); shift([c1, c2]); shape('diamond'); }
  ];
  var last = -1;
  async function tick() {
    if (!busy && !document.hidden) {
      busy = true;
      var i; do { i = Math.floor(Math.random() * routines.length); } while (i === last);
      last = i;
      try { await routines[i](); } catch (e) {}
      busy = false;
    }
    setTimeout(tick, 3200 + Math.random() * 3800);
  }
  setTimeout(tick, 2200);
})();

/* looping videos: respect reduced motion, and only play while on screen */
(function () {
  var vids = Array.prototype.slice.call(document.querySelectorAll('.pic video'));
  if (!vids.length) return;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  vids.forEach(function (v) { if (still) { v.removeAttribute('autoplay'); v.pause(); } });
  if (still || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { var p = e.target.play(); if (p && p.catch) p.catch(function () {}); } else e.target.pause(); });
  }, { threshold: 0.2 });
  vids.forEach(function (v) { io.observe(v); });
})();

/* product story pages: the hero image grows as it scrolls into view, and drifts inside its frame (parallax) */
(function () {
  var fig = document.querySelector('.s-fig');
  if (!fig || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var frame = fig.querySelector('.s-frame'), ticking = false;
  function ease(t) { return t * t * (3 - 2 * t); }
  function update() {
    ticking = false;
    var r = fig.getBoundingClientRect(), vh = window.innerHeight;
    var grow = Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.85)));          // 0 as it enters, 1 once well inside
    var pass = Math.max(0, Math.min(1, (vh - r.top) / (vh + r.height)));      // 0 to 1 across the whole traversal
    var shrink = Math.max(0, Math.min(1, (vh * 0.15 - r.bottom + r.height * 0.25) / (vh * 0.5))); // eases back a little as it leaves the top
    var sc = 0.84 + 0.16 * ease(grow) - 0.05 * ease(shrink);
    frame.style.transform = 'scale(' + sc.toFixed(4) + ')';
    frame.style.borderRadius = (28 - 14 * ease(grow)) + 'px';
    frame.style.setProperty('--sp', pass.toFixed(3));
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();

/* contact form: posts to the configured endpoint, otherwise opens a pre-filled email */
(function () {
  var f = document.getElementById('contactForm'); if (!f) return;
  var note = document.getElementById('contactNote');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(f), name = (d.get('name') || '').trim(), email = (d.get('email') || '').trim(), msg = (d.get('message') || '').trim();
    if (d.get('website')) return;
    if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || !msg) { note.className = 'c-note err'; note.textContent = 'Please add your name, a valid email and a message.'; return; }
    var ep = f.getAttribute('data-endpoint');
    if (ep) {
      fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ name: name, email: email, message: msg }) })
        .then(function (r) { if (!r.ok) throw 0; f.reset(); note.className = 'c-note'; note.textContent = 'Thank you. We will be in touch soon.'; })
        .catch(function () { note.className = 'c-note err'; note.textContent = 'Something went wrong. Please email us directly.'; });
    } else {
      location.href = 'mailto:' + f.getAttribute('data-mail') + '?subject=' + encodeURIComponent('Message from ' + name) + '&body=' + encodeURIComponent(msg + '\n\n' + name + '\n' + email);
      note.className = 'c-note'; note.textContent = 'Your email app should open with the message ready to send.';
    }
  });
})();

/* product stage: play the screen scroll once when at least half of it is on screen */
(function () {
  var st = document.querySelector('.stage'); if (!st || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) {
    if (es[0].isIntersecting) { st.classList.add('play'); io.disconnect(); }
  }, { threshold: 0.55 });
  io.observe(st);
})();
