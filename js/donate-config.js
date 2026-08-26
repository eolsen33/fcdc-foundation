/* ==========================================================================
   DONATION CONFIG — the only file you edit to switch/point the donation form.
   ==========================================================================

   PLATFORM CHOICE: Zeffy.
   Why: Zeffy charges the nonprofit $0 in platform fees and $0 in card fees
   (it runs on optional tips from donors). At FCDC's revenue level that is
   the difference between keeping ~97% and ~100% of every gift. Givebutter
   (~1-3% + card) and Donorbox (~1.75% + card) both skim more.

   ---------------------------------------------------------------------------
   SETUP — 3 steps, ~15 minutes, done once by the Foundation:
   ---------------------------------------------------------------------------
   1. Create the org account at https://www.zeffy.com  (needs EIN 27-1349987).
   2. Build ONE donation form. Turn ON the recurring/monthly option.
   3. Open the form's "Share" tab, copy the URL, and paste the slug below.

   ---------------------------------------------------------------------------
   !! VERIFY BEFORE LAUNCH — amount pre-fill !!
   ---------------------------------------------------------------------------
   Zeffy does not publicly document its query-string parameters for
   pre-selecting a gift amount or frequency, so the names below are NOT
   confirmed. Do not assume they work.

   To confirm: open your live Zeffy form, click a suggested amount and the
   monthly toggle, and watch the address bar / "Share" link for the parameter
   names Zeffy actually uses. Then correct AMOUNT_PARAM and FREQUENCY_PARAM
   here — every tier button on the site routes through this one file, so
   nothing else needs to change.

   If Zeffy turns out not to support pre-fill at all, set
   PREFILL_SUPPORTED = false. Tier buttons then deep-link to the form and the
   amount is shown as guidance text instead — no broken or ignored URLs.
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

  /* ---- Fallback while Zeffy is being set up ----
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
