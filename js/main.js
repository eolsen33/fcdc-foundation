/* FCDC HOPE Foundation — site behaviour.
   Progressive enhancement only: every page works with JS disabled. */
(function () {
  'use strict';

  // Form delivery — Formsubmit today, Web3Forms once the client's key arrives.
  const FORM = { endpoint: "https://formsubmit.co/ajax/fcdcfoundation01@gmail.com", web3formsKey: "" }; // when the Web3Forms key arrives: set web3formsKey and the endpoint switches automatically

  // POSTs a form as JSON. Resolves only on a confirmed delivery — Formsubmit
  // answers 200 even when it drops a message, so the body is what counts.
  function sendForm(form) {
    var data = {};
    new FormData(form).forEach(function (value, key) {
      data[key] = key in data ? data[key] + ', ' + value : value;
    });
    if (data._subject) data.subject = data._subject;
    var url = FORM.endpoint;
    if (FORM.web3formsKey) {
      url = 'https://api.web3forms.com/submit';
      data.access_key = FORM.web3formsKey;
      Object.keys(data).forEach(function (key) { if (key.charAt(0) === '_') delete data[key]; });
    }
    var httpOk = false;
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        httpOk = res.ok;
        return res.json().catch(function () { return {}; });
      })
      .then(function (out) {
        if (!httpOk || !(out.success === true || out.success === 'true')) {
          throw new Error(out.message || 'Form submission failed');
        }
        return out;
      });
  }

  document.documentElement.classList.add('js');

  /* ---------------------------------------------------------------- nav */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });

    // Close on Escape, return focus to the toggle.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });

    // Close when the viewport grows past the desktop breakpoint.
    var mq = window.matchMedia('(min-width: 900px)');
    var sync = function () {
      if (mq.matches) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    };
    mq.addEventListener ? mq.addEventListener('change', sync) : mq.addListener(sync);
  }

  /* ------------------------------------------------------- donate links */
  // Any element with [data-donate] gets its href built from donate-config.js.
  // data-amount="35"  data-monthly="true"
  if (window.fcdcDonateUrl) {
    var ready = window.fcdcDonateReady();

    document.querySelectorAll('[data-donate]').forEach(function (el) {
      var amount = el.getAttribute('data-amount');
      var monthly = el.getAttribute('data-monthly') === 'true';
      var url = window.fcdcDonateUrl({
        amount: amount ? Number(amount) : undefined,
        monthly: monthly
      });

      if (url) {
        el.setAttribute('href', url);
        el.setAttribute('rel', 'noopener');
      }
      // Not configured yet: leave the authored href (ways-to-give.html), which
      // always shows a working way to give. Never leave a dead link.
    });

    // Surface setup state to whoever is reviewing the site.
    document.querySelectorAll('[data-donate-setup]').forEach(function (el) {
      el.hidden = ready;
    });
    document.querySelectorAll('[data-donate-live]').forEach(function (el) {
      el.hidden = !ready;
    });

    // Build the embedded form only when configured.
    var mount = document.getElementById('donate-embed');
    if (mount && ready) {
      var iframe = document.createElement('iframe');
      iframe.src = window.fcdcDonateUrl({ embed: true });
      iframe.title = 'Donation form for the Flagler County Drug Court Foundation';
      iframe.loading = 'lazy';
      iframe.allow = 'payment';
      mount.innerHTML = '';
      mount.appendChild(iframe);
    }
  }

  /* -------------------------------------------------------- sticky bar */
  if (document.querySelector('.mobile-donate')) {
    document.body.classList.add('has-mobile-donate');
  }

  /* ------------------------------------------------------------ reveal */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var reveals = document.querySelectorAll('.reveal');

  if (reveals.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* ----------------------------------------------------- contact form */
  var form = document.getElementById('contact-form');
  if (form) {
    var status = form.querySelector('.form__status');

    var setError = function (field, message) {
      var wrap = field.closest('.field');
      wrap.classList.add('has-error');
      wrap.querySelector('.field__error').textContent = message;
      field.setAttribute('aria-invalid', 'true');
    };
    var clearError = function (field) {
      var wrap = field.closest('.field');
      wrap.classList.remove('has-error');
      field.removeAttribute('aria-invalid');
    };

    // Validate on blur, not on every keystroke.
    form.querySelectorAll('input[required], textarea[required]').forEach(function (field) {
      field.addEventListener('blur', function () {
        if (!field.value.trim()) {
          setError(field, 'This field is required.');
        } else if (field.type === 'email' && !field.checkValidity()) {
          setError(field, 'Please enter a valid email address, like name@example.com.');
        } else {
          clearError(field);
        }
      });
    });

    form.addEventListener('submit', function (e) {
      var firstBad = null;

      form.querySelectorAll('input[required], textarea[required]').forEach(function (field) {
        if (!field.value.trim()) {
          setError(field, 'This field is required.');
          firstBad = firstBad || field;
        } else if (field.type === 'email' && !field.checkValidity()) {
          setError(field, 'Please enter a valid email address, like name@example.com.');
          firstBad = firstBad || field;
        } else {
          clearError(field);
        }
      });

      if (firstBad) {
        e.preventDefault();
        firstBad.focus();
        if (status) status.textContent = 'Please fix the highlighted fields and try again.';
        return;
      }

      // Send it ourselves so delivery is confirmed — the plain POST redirects
      // even when Formsubmit drops the message. With JS off it still posts.
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sending…';
      }
      if (status) status.textContent = 'Sending your message…';

      sendForm(form)
        .then(function () {
          form.reset();
          if (status) status.textContent = 'Thank you — your message is on its way. We will reply within a couple of days.';
        })
        .catch(function () {
          if (status) status.textContent = 'Something went wrong. Please email fcdcfoundation01@gmail.com or call (401) 864-6997.';
        })
        .then(function () {
          if (btn) {
            btn.disabled = false;
            btn.textContent = 'Send message';
          }
        });
    });
  }

  /* ---------------------------------------------------- Facebook feed */
  // Facebook's Page Plugin, as a plain iframe (no SDK). Nothing is requested
  // from Facebook until the section is close to the viewport. The plugin is a
  // fixed width (180–500px) chosen at load, so it is re-requested if the
  // column changes width. The link inside the box stays as the fallback.
  var fbBox = document.querySelector('[data-fb-page]');
  if (fbBox) {
    var FB_HEIGHT = 640;
    var fbFrame = null;
    var fbWidth = 0;
    fbBox.classList.add('fb-feed--live');

    var fbRender = function () {
      var width = Math.max(180, Math.min(500, Math.floor(fbBox.clientWidth)));
      if (width === fbWidth) return;
      fbWidth = width;
      if (!fbFrame) {
        fbFrame = document.createElement('iframe');
        fbFrame.title = 'Latest posts from the Flagler County Drug Court Foundation Facebook page';
        fbFrame.setAttribute('scrolling', 'no');
        fbFrame.setAttribute('allow', 'encrypted-media; picture-in-picture; web-share');
        fbBox.textContent = '';
        fbBox.appendChild(fbFrame);
      }
      fbFrame.width = String(width);
      fbFrame.height = String(FB_HEIGHT);
      fbFrame.src = 'https://www.facebook.com/plugins/page.php?href=' +
        encodeURIComponent(fbBox.getAttribute('data-fb-page')) +
        '&tabs=timeline&width=' + width + '&height=' + FB_HEIGHT +
        '&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false';
    };

    var fbStart = function () {
      fbRender();
      var timer;
      window.addEventListener('resize', function () {
        clearTimeout(timer);
        timer = setTimeout(fbRender, 300);
      });
    };

    if ('IntersectionObserver' in window) {
      var fbObserver = new IntersectionObserver(function (entries) {
        if (entries.some(function (e) { return e.isIntersecting; })) {
          fbObserver.disconnect();
          fbStart();
        }
      }, { rootMargin: '400px 0px' });
      fbObserver.observe(fbBox);
    } else {
      fbStart();
    }
  }

  /* ------------------------------------------------------ event pop-up */
  // Home page only. Shown once per visit (browser session) and never after the
  // moment in data-until, so it retires itself. ?popup=1 always shows it.
  var pop = document.querySelector('dialog[data-popup]');
  if (pop && pop.showModal) {
    var popKey = 'fcdc_pop_' + pop.getAttribute('data-popup');
    var popSeen = false;
    try { popSeen = sessionStorage.getItem(popKey) === '1'; } catch (e) {}
    var popForce = /[?&]popup=1/.test(location.search);
    // "2026-12-16T20:00" with no zone reads as the visitor's local time.
    var popUntil = new Date(pop.getAttribute('data-until')).getTime();
    if (popForce || (!popSeen && Date.now() < popUntil)) {
      setTimeout(function () {
        if (nav && nav.classList.contains('is-open')) return;
        pop.showModal();
        try { sessionStorage.setItem(popKey, '1'); } catch (e) {}
      }, 700);
    }
    pop.querySelector('.pop__x').addEventListener('click', function () { pop.close(); });
    // A click on the dimmed page behind it closes it too.
    pop.addEventListener('click', function (e) { if (e.target === pop) pop.close(); });
  }

  /* ------------------------------------------------------ current year */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
