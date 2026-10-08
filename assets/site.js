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

/* hero: floating photos fade and blur in and out */
(function () {
  var hero = document.querySelector('.hero[data-imgs]');
  if (!hero) return;
  var list = []; try { list = JSON.parse(hero.getAttribute('data-imgs')); } catch (e) {}
  var slots = Array.prototype.slice.call(hero.querySelectorAll('.float'));
  if (!list.length || !slots.length) return;
  var idx = 0, still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function take() { return list[idx++ % list.length]; }
  function load(slot, done) {
    var it = take(), img = slot.querySelector('img'), pre = new Image();
    pre.onload = function () { img.src = pre.src; img.style.objectPosition = it.p + ' 50%'; done(); };
    pre.src = '/assets/img/wall/' + it.n + '.jpg';
  }
  function cycle(slot) {
    slot.classList.remove('in');
    setTimeout(function () {
      load(slot, function () {
        requestAnimationFrame(function () { slot.classList.add('in'); });
        if (!still) setTimeout(function () { cycle(slot); }, 3800 + Math.random() * 2200);
      });
    }, 1100);
  }
  slots.forEach(function (slot, i) {
    setTimeout(function () {
      load(slot, function () {
        slot.classList.add('in');
        if (!still) setTimeout(function () { cycle(slot); }, 3600 + i * 700 + Math.random() * 2000);
      });
    }, 500 + i * 450);
  });
})();
