# Flagler County Drug Court Foundation — website

Static site for the Flagler County Drug Court Foundation (dba **FCDC HOPE Foundation**),
a Florida 501(c)(3), EIN **27-1349987**, established 2009.

Built by [EricOlsen.Studio](https://ericolsen.studio). Build fee donated.

---

## Stack

Vanilla HTML, CSS and JS. **No framework, no build step, no dependencies.**
Upload the files and it runs.

```
index.html  about.html  drug-court.html  narcan.html  ways-to-give.html  contact.html
404.html  robots.txt  sitemap.xml
css/style.css              one stylesheet, palette as CSS custom properties
js/donate-config.js        ← the only file you edit to connect the donation form
js/main.js                 nav, form validation, donate links (progressive enhancement)
assets/fonts/              self-hosted Lexend + Source Sans 3 (88 KB, no Google request)
assets/img/                WebP with JPEG/PNG fallbacks
brand/                     brand kit — colours, type, voice rules (noindex)
tools/                     OPTIONAL page generator; delete it and nothing breaks
```

Everything works with JavaScript disabled. Nothing loads from a third-party host
except the donation form iframe once it is connected.

---

## Deploy (static, VPS)

Serve the repo root as the document root. Nothing to compile.

```bash
rsync -avz --delete \
  --exclude '.git' --exclude 'tools' --exclude 'README.md' --exclude 'HANDOFF.md' \
  ./ user@vps:/var/www/fcdcfoundation/
```

Caddy is already the reverse proxy on the studio VPS:

```caddy
fcdc.ericolsen.studio {
    root * /var/www/fcdcfoundation
    file_server
    encode gzip zstd
    handle_errors {
        @404 expression {http.error.status_code} == 404
        rewrite @404 /404.html
        file_server
    }
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
    }
    @static path *.woff2 *.webp *.jpg *.png *.css *.js
    header @static Cache-Control "public, max-age=31536000, immutable"
    @html path *.html /
    header @html Cache-Control "public, max-age=0, must-revalidate"
}
```

The old site's audit failed on security headers — the block above is what fixes it.
Keep the `@html` no-cache rule: it prevents the stale-HTML problem seen on Hostinger.

### When it moves to the real domain

The old site was served at both `www.fcdcfoundation.org` and `fcdcfoundation.org`,
which split its search ranking. Pick **one** canonical host and 301 the other to it.
The `<link rel="canonical">` tags currently point at `https://fcdc.ericolsen.studio/`
— if the apex is chosen instead, update the canonical and `og:url` tags in
`tools/bodies/_meta.py` and re-run the generator, plus `sitemap.xml` and `robots.txt`.

---

## Editing

Two options — pick one and stick with it.

**Hand-edit the HTML.** Every page is complete, readable HTML. Header and footer are
duplicated in each file, so a nav change means editing six files.

**Use the generator.** `tools/bodies/*.part` holds each page's content,
`tools/build-pages.py` wraps it in the shared header/footer:

```bash
python3 tools/build-pages.py
```

The generator is a convenience, not a dependency. The committed `.html` files are the
real site.

---

## Connecting the donation form

Open `js/donate-config.js`. It is heavily commented and it is the only file to touch.

**Platform: Zeffy** — chosen because it charges nonprofits **$0** in platform and card
fees (it runs on an optional donor tip). At this revenue level that is the difference
between keeping ~97% and 100% of every gift. Givebutter and Donorbox both take a cut.

1. Create the org account at [zeffy.com](https://www.zeffy.com) using EIN 27-1349987.
2. Build one donation form; enable the recurring/monthly option.
3. Copy the slug from the form's share URL into `ZEFFY_SLUG`.

The form then embeds itself on `ways-to-give.html` automatically, and every
`Donate` button across the site starts pointing at it.

### ⚠️ Verify amount pre-fill before launch

Zeffy does not publicly document its query-string parameters, so `AMOUNT_PARAM` and
`FREQUENCY_PARAM` in the config are **unverified guesses and must be checked**. Open the
live form, click a suggested amount and the monthly toggle, and read the parameter names
out of the address bar. Correct them in that one file.

If Zeffy turns out not to support pre-fill, set `PREFILL_SUPPORTED = false`. Tier buttons
then deep-link to the form without a bogus query string.

Until Zeffy is connected, the Foundation's **real existing PayPal button**
(`Z4S96Q5ZEGJE4`, carried over from the old site) and the mail-in address are both live,
so the site can take money from day one.

---

## Connecting the contact form

`contact.html` posts to [Formsubmit.co](https://formsubmit.co) — free, no server code.

1. Replace `YOUR-EMAIL@EXAMPLE.COM` in the form `action` with the Foundation's inbox.
2. Submit the form once. Formsubmit emails a one-time activation link; **the form does
   not deliver until it is clicked.**
3. Swap the address for the hashed endpoint Formsubmit provides, so the address is not
   exposed in page source.

---

## What still needs the client

See `HANDOFF.md` for the full list. Nothing in it was invented or guessed — every gap is
marked in the page with a hatched amber `[PLACEHOLDER]` block that is impossible to miss.

---

## Language rules — non-negotiable

Destigmatization is in the Foundation's mission statement, so stigmatizing copy would
contradict the client's own mission. This is a correctness constraint, not a style
preference. Full rules in `brand/`:

- **person with a substance use disorder** — never "addict", "abuser", "junkie"
- **substance use disorder** — never "drug problem"
- **returned to use** — never "relapsed"
- **positive / negative** test results — never "clean" / "dirty"
- No before/after framing, mugshots, or rock-bottom narratives
- Any participant story requires a signed release — **42 CFR Part 2** is stricter than
  HIPAA. Never write a fictional testimonial, even as a sample.

---

## Accessibility

The old site scored **F** on accessibility. This one targets WCAG 2.2 AA, AAA on text:

- Body text 17px (audience skews older), contrast 17.4:1; headings 9.4:1
- Visible 3px focus ring on every interactive element
- 44×44px minimum tap targets
- Real alt text on every meaningful image, `alt=""` on decorative ones
- Skip link, landmarks, one `<h1>` per page, no heading-level skips
- Cost bars carry text labels — never colour alone
- `prefers-reduced-motion` respected

Verified: no horizontal overflow at 375px on any page; all internal links resolve.

## Performance

The old site shipped a 1.6 MB homepage graphic. The equivalent here is **20 KB**.
Whole site is ~2.5 MB including every image and font. Fonts are self-hosted (88 KB) so
there are zero third-party requests on load.
