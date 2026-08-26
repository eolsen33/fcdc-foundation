#!/usr/bin/env python3
"""
OPTIONAL helper — the website itself has NO build step.

Every page in this repo is plain, finished HTML that a browser or a static
host can read directly. This script exists only so that the shared chrome
(header, nav, footer, help-now block, legal disclosure) stays byte-identical
across all six pages when someone edits it.

If you would rather hand-edit the HTML, do that and delete this file. Nothing
in the deploy depends on it.

Usage:  python3 tools/build-pages.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("drug-court.html", "Drug Court"),
    ("narcan.html", "Narcan"),
    ("ways-to-give.html", "Ways to Give"),
    ("contact.html", "Contact"),
]

FOOTER_NAV_LABELS = {
    "index.html": "Home",
    "about.html": "About us",
    "drug-court.html": "How drug court works",
    "narcan.html": "Narcan training",
    "ways-to-give.html": "Ways to give",
    "contact.html": "Contact",
}

ORG_JSONLD = """{
  "@context": "https://schema.org",
  "@type": "NGO",
  "name": "Flagler County Drug Court Foundation",
  "alternateName": "FCDC HOPE Foundation",
  "url": "https://www.fcdcfoundation.org/",
  "logo": "https://www.fcdcfoundation.org/assets/img/hope-logo.png",
  "foundingDate": "2009",
  "taxID": "27-1349987",
  "nonprofitStatus": "Nonprofit501c3",
  "description": "A Florida 501(c)(3) supporting the Flagler County drug court program through community engagement, advocacy, Narcan distribution and training, and education that reduces the stigma around substance use disorder.",
  "areaServed": { "@type": "AdministrativeArea", "name": "Flagler County, Florida" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "55 Black Alder Dr",
    "addressLocality": "Palm Coast",
    "addressRegion": "FL",
    "postalCode": "32137",
    "addressCountry": "US"
  },
  "knowsAbout": ["Substance use disorder recovery", "Drug court", "Narcan", "Naloxone training", "Overdose prevention"]
}"""


def head(page, meta):
    nav_items = "\n".join(
        '        <li><a href="{h}"{c}>{l}</a></li>'.format(
            h=href, l=label,
            c=' aria-current="page"' if href == page else "")
        for href, label in NAV
    )
    extra = meta.get("head_extra", "")
    jsonld = ORG_JSONLD if page == "index.html" else meta.get("jsonld", "")
    jsonld_block = (
        '\n<script type="application/ld+json">\n%s\n</script>\n' % jsonld
    ) if jsonld else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="https://www.fcdcfoundation.org/{'' if page == 'index.html' else page}">

<meta property="og:type" content="website">
<meta property="og:title" content="{meta.get('og_title', meta['title'])}">
<meta property="og:description" content="{meta.get('og_description', meta['description'])}">
<meta property="og:url" content="https://www.fcdcfoundation.org/{'' if page == 'index.html' else page}">
<meta property="og:image" content="https://www.fcdcfoundation.org/assets/img/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Flagler County Drug Court Foundation — treatment costs a fraction of a prison cell">
<meta property="og:site_name" content="Flagler County Drug Court Foundation">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/img/hope-logo.png">
<link rel="preload" href="assets/fonts/Lexend-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
{extra}{jsonld_block}</head>
<body>

<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html">
      <img src="assets/img/hope-logo.webp" alt="Flagler County Drug Court Foundation — HOPE: Helping Our Participants Excel" width="180" height="88">
      <span class="brand__text">Flagler County Drug&nbsp;Court Foundation</span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <svg class="nav-toggle__open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      <svg class="nav-toggle__close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      <span>Menu</span>
    </button>

    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
{nav_items}
      </ul>
    </nav>

    <a class="btn btn--donate header-donate" href="ways-to-give.html" data-donate>Donate</a>
  </div>
</header>

<main id="main">
"""


def foot(page):
    footer_nav = "\n".join(
        '          <li><a href="{h}">{l}</a></li>'.format(h=h, l=FOOTER_NAV_LABELS[h])
        for h, _ in NAV
    )
    return f"""
</main>

<!-- Sticky mobile donate -->
<div class="mobile-donate">
  <a class="btn btn--donate btn--block btn--lg" href="ways-to-give.html" data-donate>Donate</a>
</div>

<footer class="site-footer">
  <div class="container">

    <div class="footer__help">
      <h3>Need help now?</h3>
      <ul>
        <li><strong><a href="tel:988">988</a></strong> — Suicide &amp; Crisis Lifeline. Call or text, 24/7.</li>
        <li><strong><a href="tel:18006624357">1-800-662-4357</a></strong> — SAMHSA National Helpline. Free, confidential treatment referrals, 24/7.</li>
        <li><strong><a href="tel:211">211</a></strong> — Florida 211. Local treatment, housing, and food assistance.</li>
        <li>If someone is overdosing right now, call <strong><a href="tel:911">911</a></strong>. Florida's Good Samaritan law protects people who call for help.</li>
      </ul>
    </div>

    <div class="footer__grid">
      <div class="footer__brand">
        <img src="assets/img/hope-logo.webp" alt="" width="180" height="88">
        <p>
          The Flagler County Drug Court Foundation supports and promotes the Flagler County
          drug court program through community engagement, advocacy, and education.
        </p>
        <p><strong>HOPE</strong> — Helping Our Participants Excel.</p>
      </div>

      <div>
        <h3>Pages</h3>
        <ul>
{footer_nav}
        </ul>
      </div>

      <div>
        <h3>Give</h3>
        <ul>
          <li><a href="ways-to-give.html" data-donate>Donate online</a></li>
          <li><a href="ways-to-give.html#monthly">Monthly giving (Club 100)</a></li>
          <li><a href="ways-to-give.html#business">Business sponsorship</a></li>
          <li><a href="ways-to-give.html#mail">Give by mail</a></li>
          <li><a href="contact.html">Volunteer</a></li>
        </ul>
      </div>

      <div>
        <h3>Contact</h3>
        <ul>
          <li>The Flagler County Drug Court Foundation<br>55 Black Alder Dr<br>Palm Coast, FL 32137</li>
          <li><strong>[PHONE — CLIENT TO SUPPLY]</strong></li>
          <li><strong>[EMAIL — CLIENT TO CONFIRM]</strong></li>
        </ul>
      </div>
    </div>

    <div class="footer__legal">
      <div class="footer__meta">
        <span>EIN 27-1349987</span>
        <span>501(c)(3) nonprofit</span>
        <span>Established 2009</span>
        <span>Florida registration <strong>[CH##### — CLIENT TO SUPPLY]</strong></span>
      </div>

      <p class="footer__disclosure">
        A COPY OF THE OFFICIAL REGISTRATION AND FINANCIAL INFORMATION MAY BE OBTAINED FROM THE
        DIVISION OF CONSUMER SERVICES BY CALLING TOLL-FREE 1-800-HELP-FLA (435-7352) WITHIN THE
        STATE OR AT <a href="https://www.FloridaConsumerHelp.com" rel="noopener">www.FloridaConsumerHelp.com</a>.
        REGISTRATION DOES NOT IMPLY ENDORSEMENT, APPROVAL, OR RECOMMENDATION BY THE STATE.
      </p>

      <p class="footer__disclosure mt-5">
        &copy; <span data-year>2026</span> Flagler County Drug Court Foundation. All contributions
        are tax deductible to the extent allowed by law.
      </p>
    </div>
  </div>
</footer>

<script src="js/donate-config.js"></script>
<script src="js/main.js" defer></script>
</body>
</html>
"""


def build():
    bodies = ROOT / "tools" / "bodies"
    meta_all = {}
    exec((bodies / "_meta.py").read_text(), meta_all)
    META = meta_all["META"]

    for page, meta in META.items():
        body = (bodies / (page.replace(".html", ".part"))).read_text()
        (ROOT / page).write_text(head(page, meta) + body + foot(page))
        print("wrote", page)


if __name__ == "__main__":
    build()
