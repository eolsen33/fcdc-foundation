/* ==========================================================================
   DONATION CONFIG — the only file you edit to switch/point the donation form.
   ==========================================================================

   PLATFORM CHOICE: PayPal (decided 2026-09-30).
   Every [data-donate] link keeps its authored href (ways-to-give.html, or
   #donate on that page), where the Foundation's hosted PayPal button lives.
   That button has "Make this a monthly donation" enabled, so the Club 100
   tiers work through it, and it accepts cards without a PayPal account.

   The Zeffy code path below is dormant: ZEFFY_SLUG is empty, so
   fcdcDonateUrl() returns '' and nothing is rewritten. Leave it empty
   unless the Foundation ever moves to Zeffy.
   ========================================================================== */

window.FCDC_DONATE = {
  /* ---- Zeffy ---- */
  // Paste the slug from your form URL, e.g.
  // https://www.zeffy.com/donation-form/THIS-PART  →  'THIS-PART'
  ZEFFY_SLUG: '',

  ZEFFY_FORM_BASE:  'https://www.zeffy.com/donation-form/',
  ZEFFY_EMBED_BASE: 'https://www.zeffy.com/embed/donation-form/',

  // See the VERIFY block above before trusting these.
  PREFILL_SUPPORTED: true,
  AMOUNT_PARAM:    'amount',
  FREQUENCY_PARAM: 'frequency',
  MONTHLY_VALUE:   'monthly',

  /* ---- The live donation route ----
     This is the Foundation's REAL existing PayPal hosted button, carried over
     from the old site. It keeps the site able to take money from day one. */
  PAYPAL_BUTTON_ID: 'Z4S96Q5ZEGJE4',
  PAYPAL_URL: 'https://www.paypal.com/donate?hosted_button_id=Z4S96Q5ZEGJE4',

  /* ---- Mail-in giving (real, from the Foundation) ---- */
  MAIL_TO: 'The Flagler County Drug Court Foundation',
  MAIL_ADDRESS: '55 Black Alder Dr, Palm Coast, FL 32137'
};

/**
 * Build a donation URL.
 * @param {Object}  opts
 * @param {number} [opts.amount]   dollars, e.g. 35
 * @param {boolean}[opts.monthly]  true for recurring
 * @param {boolean}[opts.embed]    true for the iframe src
 * @returns {string} URL, or '' when Zeffy is not configured yet
 */
window.fcdcDonateUrl = function (opts) {
  opts = opts || {};
  var C = window.FCDC_DONATE;
  if (!C.ZEFFY_SLUG) return '';

  var base = (opts.embed ? C.ZEFFY_EMBED_BASE : C.ZEFFY_FORM_BASE) + C.ZEFFY_SLUG;
  if (!C.PREFILL_SUPPORTED) return base;

  var qs = [];
  if (opts.amount)  qs.push(encodeURIComponent(C.AMOUNT_PARAM) + '=' + encodeURIComponent(opts.amount));
  if (opts.monthly) qs.push(encodeURIComponent(C.FREQUENCY_PARAM) + '=' + encodeURIComponent(C.MONTHLY_VALUE));
  return qs.length ? base + '?' + qs.join('&') : base;
};

/** True once the Foundation has pasted a Zeffy slug. */
window.fcdcDonateReady = function () {
  return !!window.FCDC_DONATE.ZEFFY_SLUG;
};
