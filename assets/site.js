/* oddly sunny: shared behaviour */
(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // header: solid on scroll, mobile menu
  var hdr = $('.hdr');
  var lastY = window.scrollY;
  function onScroll() {
    if (!hdr) return; var y = window.scrollY;
    if (!document.body.classList.contains('menu-open')) hdr.classList.toggle('tuck', y > 320 && y > lastY + 4 ? true : (y < lastY - 4 || y <= 320) ? false : hdr.classList.contains('tuck'));
    lastY = y;
    hdr.classList.toggle('scrolled', y > 12); if (hdr.hasAttribute('data-away')) hdr.classList.toggle('away', y < 90); }
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
  // stagger siblings that reveal together (cards, features, rows) unless a delay is already set
  $$('.reveal').forEach(function (el) {
    if (el.style.getPropertyValue('--d')) return;
    var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.classList.contains('reveal'); });
    if (sibs.length > 1) el.style.setProperty('--d', (sibs.indexOf(el) % 4) * 90 + 'ms');
  });
  $$('.reveal,.frame,.vs-table').forEach(function (el) { io.observe(el); });

  // hidden play: the three icons in "Personal by design" are tiny games
  var plays = $$('[data-play]');
  if (plays.length) {
    var found = {}, daily = 0, ready = 64, combo = 0, lastXp = 0, unlocked = false;
    var COLORS = ['#40916C', '#6AB58E', '#2D6A4F', '#D4A63C'];
    var burst = function (el, txt) {
      var f = document.createElement('span'); f.className = 'pf'; f.textContent = txt; f.setAttribute('aria-hidden', 'true');
      el.appendChild(f); setTimeout(function () { f.remove(); }, 1000);
      for (var i = 0; i < 9; i++) {
        var c = document.createElement('i'), a = Math.random() * Math.PI * 2, d = 28 + Math.random() * 30;
        c.className = 'pc';
        c.style.cssText = '--x:' + Math.cos(a) * d + 'px;--y:' + Math.sin(a) * d + 'px;--r:' + (Math.random() * 360 - 180) + 'deg;--c:' + COLORS[i % 4];
        el.appendChild(c); setTimeout(function (n) { return function () { n.remove(); }; }(c), 850);
      }
      el.classList.remove('hit'); void el.offsetWidth; el.classList.add('hit');
    };
    plays.forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-play'), txt;
        if (k === 'daily') { daily++; txt = daily <= 2 ? 'Challenge ' + daily + ' of 2' : 'Day ' + (daily - 1) + ' done'; }
        if (k === 'ready') { ready = Math.min(100, ready + 6); txt = ready >= 100 ? 'Ready to pass!' : 'Ready ' + ready + '%'; }
        if (k === 'xp') { var now = Date.now(); combo = now - lastXp < 900 ? combo + 1 : 1; lastXp = now; txt = combo > 1 ? 'Combo x' + combo : '+10 XP'; }
        burst(b, txt);
        found[k] = 1;
        if (!unlocked && Object.keys(found).length === plays.length) {
          unlocked = true;
          // the reward: the heading itself changes its mind
          var w = $('h2.h2 i', b.closest('section'));
          if (w) {
            w.style.transitionDelay = '0s';
            w.classList.add('swap-out');
            setTimeout(function () { w.textContent = 'feels like winning'; w.classList.remove('swap-out'); }, 450);
          }
        }
      });
    });
  }

  // playable mini games on the homepage: memory match, scratch cards, swipe true/false
  var pg = $('[data-pg]'), pgData = $('#pg-data');
  if (pg && pgData) (function () {
    var D = JSON.parse(pgData.textContent), stage = $('.pg-stage', pg), tabs = $$('.pg-tabs button', pg);
    var hearts = $$('.pg-hearts svg', pg), prog = $('.pg-prog i', pg), streakEl = $('.pg-streak', pg), xpEl = $('.pg-xp b', pg);
    var COLORS = ['#40916C', '#6AB58E', '#2D6A4F', '#D4A63C'];
    var game, total, done, lives, streak, xp = 0, gained, busy;
    function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }
    function best(g, v) { try { var k = 'os-pg-' + g, b = +localStorage.getItem(k) || 0; if (v != null && v > b) { localStorage.setItem(k, v); return v; } return b; } catch (e) { return 0; } }
    function confetti(el) {
      for (var i = 0; i < 12; i++) {
        var c = document.createElement('i'), a = Math.random() * Math.PI * 2, d = 40 + Math.random() * 50;
        c.className = 'pc';
        c.style.cssText = '--x:' + Math.cos(a) * d + 'px;--y:' + Math.sin(a) * d + 'px;--r:' + (Math.random() * 360 - 180) + 'deg;--c:' + COLORS[i % 4];
        el.appendChild(c); setTimeout(function (n) { return function () { n.remove(); }; }(c), 900);
      }
    }
    function float(el, txt) { var f = document.createElement('span'); f.className = 'pf'; f.textContent = txt; el.appendChild(f); setTimeout(function () { f.remove(); }, 1000); }
    function hud() {
      hearts.forEach(function (h, i) { h.classList.toggle('lost', i >= lives); });
      prog.style.transform = 'scaleX(' + (total ? done / total : 0) + ')';
      streakEl.textContent = streak >= 2 ? 'Streak ' + streak : '';
      streakEl.classList.toggle('on', streak >= 2);
    }
    function win(el, n) {
      streak++; var pts = n + (streak >= 3 ? 5 : 0); xp += pts; gained += pts; xpEl.textContent = xp;
      xpEl.parentNode.classList.remove('bump'); void xpEl.offsetWidth; xpEl.parentNode.classList.add('bump');
      if (el) { confetti(el); float(el, '+' + pts); }
      hud();
    }
    function miss(el) {
      streak = 0; lives--; var h = hearts[lives]; if (h) { h.classList.remove('pop'); void h.getBoundingClientRect(); h.classList.add('pop'); }
      if (el) { el.classList.remove('shake'); void el.offsetWidth; el.classList.add('shake'); }
      hud();
    }
    function start(g) {
      game = g; done = 0; lives = 3; streak = 0; gained = 0; busy = false;
      tabs.forEach(function (t) { var on = t.getAttribute('data-game') === g; t.classList.toggle('on', on); t.setAttribute('aria-selected', on); });
      ({ match: match, flash: flash, fact: fact })[g]();
      hud();
    }
    function end(score) {
      var stars = lives === 3 ? 3 : lives === 2 ? 2 : 1; if (score === 0) stars = 0;
      var b = best(game, score), st = '';
      for (var i = 0; i < 3; i++) st += '<i class="' + (i < stars ? 'on' : '') + '" style="--i:' + i + '"></i>';
      stage.innerHTML = '<div class="pg-card pg-end"><div class="pg-stars">' + st + '</div><span class="pg-score"><b>' + score + '</b>/' + total + '</span>' +
        '<p class="pg-meta">+' + gained + ' XP this round · Best ' + b + '/' + total + '</p>' +
        '<div class="pg-opts two"><button type="button" class="pg-again">Play again</button><button type="button" class="pg-next">Next game</button></div></div>';
      if (stars === 3) confetti($('.pg-stars', stage));
      $('.pg-again', stage).addEventListener('click', function () { start(game); });
      $('.pg-next', stage).addEventListener('click', function () { var g = ['match', 'flash', 'fact']; start(g[(g.indexOf(game) + 1) % 3]); });
    }
    function out() { return lives <= 0; }

    // 1. Sign Match: flip cards, find the pairs
    function match() {
      var names = {}; D.match.forEach(function (m) { names[m[0]] = m[1]; });
      var keys = D.match.map(function (m) { return m[0]; }), deck = shuffle(keys.concat(keys)), seen = {}, open = [], pairs = 0;
      total = keys.length;
      var h = '<div class="pg-card pg-mem"><p class="pg-hint">Find the matching signs</p><div class="pg-grid">';
      deck.forEach(function (k, i) { h += '<button type="button" class="pg-flip" data-k="' + k + '" data-i="' + i + '" aria-label="Hidden card"><span class="pg-back"></span><span class="pg-front"><img src="/assets/img/signs/' + k + '.svg" alt="" draggable="false"></span></button>'; });
      stage.innerHTML = h + '</div></div>';
      $$('.pg-flip', stage).forEach(function (c) {
        c.addEventListener('click', function () {
          if (busy || c.classList.contains('up') || out()) return;
          c.classList.add('up'); c.setAttribute('aria-label', names[c.getAttribute('data-k')]); open.push(c);
          if (open.length < 2) return;
          busy = true; var a = open[0], b = open[1]; open = [];
          if (a.getAttribute('data-k') === b.getAttribute('data-k')) {
            setTimeout(function () { a.classList.add('got'); b.classList.add('got'); pairs++; done = pairs; win(b, 10); busy = false; if (pairs === total) setTimeout(function () { end(pairs); }, 700); }, 350);
          } else {
            var mistake = seen[a.getAttribute('data-i')] && seen[b.getAttribute('data-i')];
            mistake = mistake || (seen[b.getAttribute('data-k') + '@'] && !seen[b.getAttribute('data-i')] && false);
            setTimeout(function () {
              if (seen[a.getAttribute('data-i')] || seen[b.getAttribute('data-i')]) miss($('.pg-mem', stage)); else { streak = 0; hud(); }
              seen[a.getAttribute('data-i')] = seen[b.getAttribute('data-i')] = 1;
              a.classList.remove('up'); b.classList.remove('up'); a.setAttribute('aria-label', 'Hidden card'); b.setAttribute('aria-label', 'Hidden card');
              busy = false; if (out()) setTimeout(function () { end(pairs); }, 500);
            }, 800);
          }
        });
      });
    }

    // 2. Flash Cards: scratch to reveal, then say honestly if you knew it
    function flash() {
      var cards = shuffle(D.flash).slice(0, 5), i = 0, knew = 0; total = cards.length;
      function show() {
        var c = cards[i];
        stage.innerHTML = '<div class="pg-card"><span class="pg-tag">' + esc(c.tag) + '</span><p class="pg-q big">' + esc(c.q) + '</p>' +
          '<div class="pg-scratch"><span class="pg-ans">' + esc(c.a) + '</span><canvas aria-hidden="true"></canvas><i class="pg-shine" aria-hidden="true"></i></div>' +
          '<div class="pg-opts two pg-self" hidden><button type="button" data-v="0">Didn’t know</button><button type="button" data-v="1">Knew it</button></div>' +
          '<button type="button" class="pg-reveal">Reveal</button></div>';
        var box = $('.pg-scratch', stage), cv = $('canvas', box), ctx = cv.getContext('2d'), r = box.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
        cv.width = r.width * dpr; cv.height = r.height * dpr; ctx.scale(dpr, dpr);
        // brand gold foil: soft bands, a faint sheen, a little grain and a stamped label
        var g = ctx.createLinearGradient(0, 0, r.width, r.height);
        [[0, '#C9982F'], [.3, '#DDB65A'], [.55, '#D4A63C'], [.8, '#E2BE66'], [1, '#C5932C']].forEach(function (st) { g.addColorStop(st[0], st[1]); });
        ctx.fillStyle = g; ctx.fillRect(0, 0, r.width, r.height);
        var sh = ctx.createLinearGradient(0, r.height, r.width, 0);
        sh.addColorStop(.38, 'rgba(255,248,225,0)'); sh.addColorStop(.5, 'rgba(255,248,225,.22)'); sh.addColorStop(.62, 'rgba(255,248,225,0)');
        ctx.fillStyle = sh; ctx.fillRect(0, 0, r.width, r.height);
        for (var s2 = 0; s2 < 140; s2++) { ctx.fillStyle = Math.random() < .5 ? 'rgba(255,245,215,.35)' : 'rgba(90,62,12,.12)'; ctx.fillRect(Math.random() * r.width, Math.random() * r.height, 1.2, 1.2); }
        ctx.font = '600 13px Sora, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '2px';
        ctx.fillStyle = 'rgba(255,240,205,.5)'; ctx.fillText('SCRATCH HERE', r.width / 2 + .8, r.height / 2 + .8);
        ctx.fillStyle = 'rgba(74,52,16,.6)'; ctx.fillText('SCRATCH HERE', r.width / 2, r.height / 2);
        ctx.globalCompositeOperation = 'destination-out';
        ctx.strokeStyle = '#000'; ctx.fillStyle = '#000'; ctx.lineWidth = 42; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        var down = false, n = 0, revealed = false, last = null;
        function dab(x, y) {
          var R = 24, rg = ctx.createRadialGradient(x, y, 0, x, y, R);
          rg.addColorStop(0, 'rgba(0,0,0,1)'); rg.addColorStop(.55, 'rgba(0,0,0,.85)'); rg.addColorStop(1, 'rgba(0,0,0,0)');
          ctx.fillStyle = rg; ctx.fillRect(x - R, y - R, R * 2, R * 2);
        }
        function reveal() {
          if (revealed) return; revealed = true; box.classList.add('clear'); $('.pg-self', stage).hidden = false; $('.pg-reveal', stage).hidden = true;
        }
        function scratch(e) {
          if (!down) return; var b = cv.getBoundingClientRect(), x = e.clientX - b.left, y = e.clientY - b.top;
          // soft-edged dabs along the stroke, so the foil wears away with a feathered edge
          var from = last || [x, y], dist = Math.hypot(x - from[0], y - from[1]), steps = Math.max(1, Math.ceil(dist / 5));
          for (var q = 1; q <= steps; q++) dab(from[0] + (x - from[0]) * q / steps, from[1] + (y - from[1]) * q / steps);
          last = [x, y];
          box.classList.add('started');
          if (++n % 8 === 0) {
            var px = ctx.getImageData(0, 0, cv.width, cv.height).data, clear = 0;
            for (var k = 3; k < px.length; k += 64) if (px[k] < 60) clear++;
            if (clear / (px.length / 64) > 0.45) reveal();
          }
        }
        cv.addEventListener('pointerdown', function (e) { e.preventDefault(); down = true; cv.setPointerCapture(e.pointerId); scratch(e); });
        cv.addEventListener('pointermove', scratch);
        cv.addEventListener('pointerup', function () { down = false; last = null; });
        cv.addEventListener('pointerleave', function () { last = null; });
        $('.pg-reveal', stage).addEventListener('click', reveal);
        $$('.pg-self button', stage).forEach(function (b) {
          b.addEventListener('click', function () {
            if (b.getAttribute('data-v') === '1') { knew++; win(b, 10); } else { streak = 0; hud(); }
            done = ++i; hud();
            setTimeout(function () { i < cards.length ? show() : end(knew); }, 650);
          });
        });
      }
      show();
    }

    // 3. Fact Check: a swipe deck, right for true, left for false
    function fact() {
      var cards = shuffle(D.fact), i = 0, right = 0; total = cards.length;
      var h = '<div class="pg-deck" tabindex="0" aria-label="Fact Check cards. Use the left and right arrow keys.">';
      for (var k = cards.length - 1; k >= 0; k--) h += '<div class="pg-sc" data-k="' + k + '"><span class="pg-stamp t">True</span><span class="pg-stamp f">False</span><p class="pg-q big">' + esc(cards[k].q) + '</p><p class="pg-hint">Swipe right if true, left if false</p></div>';
      stage.innerHTML = h + '</div><p class="pg-why"></p><div class="pg-round"><button type="button" class="no" data-v="false" aria-label="False"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button><button type="button" class="yes" data-v="true" aria-label="True"><svg viewBox="0 0 24 24"><path d="m5 12.500 4.500 4.500L19 7"/></svg></button></div>';
      var deck = $('.pg-deck', stage), why = $('.pg-why', stage), W = deck.offsetWidth;
      var EASE = 'cubic-bezier(.2,.8,.2,1)', SPRING = 'cubic-bezier(.34,1.4,.5,1)';
      function rest(c, pos) {
        var p = Math.min(pos, 2);
        c.style.transform = 'translate3d(0,' + p * 12 + 'px,0) scale(' + (1 - p * .05) + ')';
        c.style.opacity = pos > 2 ? 0 : 1; c.style.zIndex = 10 - pos;
      }
      function stack() {
        $$('.pg-sc', deck).forEach(function (c) {
          var pos = +c.getAttribute('data-k') - i; if (pos < 0) return;
          c.style.transition = 'transform .55s ' + SPRING + ', opacity .3s ease';
          rest(c, pos); if (pos === 0) bind(c);
        });
      }
      function tint(card, p) { card.style.setProperty('--t', Math.max(0, p)); card.style.setProperty('--f', Math.max(0, -p)); }
      function bind(card) {
        if (card._b) return; card._b = 1;
        var x0, y0, dx = 0, dy = 0, grabTop = false, samples = [], drag = false, raf = 0, next = null;
        function paint() {
          raf = 0;
          var rot = dx / W * 16 * (grabTop ? 1 : -1);
          card.style.transform = 'translate3d(' + dx + 'px,' + dy * .25 + 'px,0) rotate(' + rot + 'deg)';
          tint(card, Math.max(-1, Math.min(1, dx / (W * .3))));
          next = next || $('.pg-sc[data-k="' + (i + 1) + '"]', deck);
          if (next) { var a = Math.min(1, Math.abs(dx) / (W * .45)); next.style.transition = 'none'; next.style.transform = 'translate3d(0,' + 12 * (1 - a) + 'px,0) scale(' + (.95 + .05 * a) + ')'; }
        }
        card.addEventListener('pointerdown', function (e) {
          if (card._gone || e.button > 0) return; drag = true; x0 = e.clientX; y0 = e.clientY; dx = dy = 0; samples = [[e.clientX, performance.now()]];
          var r = card.getBoundingClientRect(); grabTop = e.clientY < r.top + r.height / 2;
          card.setPointerCapture(e.pointerId); card.style.transition = 'none'; card.classList.add('drag');
        });
        card.addEventListener('pointermove', function (e) {
          if (!drag) return; dx = e.clientX - x0; dy = e.clientY - y0;
          samples.push([e.clientX, performance.now()]); if (samples.length > 6) samples.shift();
          if (!raf) raf = requestAnimationFrame(paint);
        });
        function velocity() { var a = samples[0], b = samples[samples.length - 1]; return b && a && b[1] > a[1] ? (b[0] - a[0]) / (b[1] - a[1]) : 0; }
        function release() {
          if (!drag) return; drag = false; card.classList.remove('drag'); if (raf) { cancelAnimationFrame(raf); raf = 0; paint(); }
          var v = velocity();
          if (Math.abs(dx) > W * .28 || (Math.abs(v) > .45 && Math.abs(dx) > 24)) throwCard(card, (Math.abs(v) > .45 ? v : dx) > 0 ? 'true' : 'false', v, dx, dy, grabTop);
          else {
            card.style.transition = 'transform .6s ' + SPRING; card.style.transform = 'translate3d(0,0,0)'; tint(card, 0);
            if (next) { next.style.transition = 'transform .6s ' + EASE; rest(next, 1); }
          }
        }
        card.addEventListener('pointerup', release); card.addEventListener('pointercancel', release);
        card._throw = function (v) {
          // buttons and keys: a short lean, then the throw
          var dir = v === 'true' ? 1 : -1;
          card.style.transition = 'transform .16s ease-out'; card.style.transform = 'translate3d(' + dir * 26 + 'px,0,0) rotate(' + dir * 4 + 'deg)'; tint(card, dir * .5);
          setTimeout(function () { throwCard(card, v, dir * 1.1, dir * 26, 0, true); }, 150);
        };
      }
      function throwCard(card, v, vel, dx, dy, grabTop) {
        if (card._gone) return; card._gone = true;
        var c = cards[i], ok = String(c.a) === v, dir = v === 'true' ? 1 : -1;
        var speed = Math.max(.9, Math.min(2.4, Math.abs(vel || 0)));
        var dist = W * 1.5, dur = Math.max(.32, Math.min(.6, dist / (speed * 1000) * 1.6));
        var endY = (dy || 0) * .25 + (dy || 0) * .6, rot = dir * 24 * (grabTop === false ? -1 : 1);
        card.style.transition = 'transform ' + dur.toFixed(2) + 's cubic-bezier(.25,.6,.35,1), opacity ' + dur.toFixed(2) + 's ease-in';
        tint(card, dir);
        card.style.transform = 'translate3d(' + dir * dist + 'px,' + endY + 'px,0) rotate(' + rot + 'deg)';
        card.style.opacity = 0;
        var btn = $('.pg-round .' + (dir > 0 ? 'yes' : 'no'), stage); btn.classList.remove('hit'); void btn.offsetWidth; btn.classList.add('hit');
        if (ok) { right++; why.textContent = ''; win(btn, 10); }
        else { streak = 0; lives--; var hh = hearts[lives]; if (hh) { hh.classList.remove('pop'); void hh.getBoundingClientRect(); hh.classList.add('pop'); } why.textContent = c.why || ('That one is ' + (c.a ? 'true.' : 'false.')); }
        done = ++i; hud();
        setTimeout(function () { card.remove(); }, dur * 1000 + 50);
        if (i < cards.length && !out()) setTimeout(stack, 60);
        else setTimeout(function () { end(right); }, ok ? 650 : 1500);
      }
      function topCard() { return $('.pg-sc[data-k="' + i + '"]', deck); }
      $$('.pg-round button', stage).forEach(function (b) {
        b.addEventListener('click', function () { var t = topCard(); if (t && t._throw && !t._gone) t._throw(b.getAttribute('data-v')); });
      });
      deck.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return; e.preventDefault();
        var t = topCard(); if (t && t._throw && !t._gone) t._throw(e.key === 'ArrowRight' ? 'true' : 'false');
      });
      stack();
    }

    tabs.forEach(function (t) { t.addEventListener('click', function () { start(t.getAttribute('data-game')); }); });
    start('match');
  })();


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
