# What we need from the Foundation

Everything below is marked on the site itself with a hatched amber `[PLACEHOLDER]` block.
**Nothing here was invented or estimated.** Where we could not verify a number, we left it
blank rather than guess — a made-up statistic on a nonprofit site is a liability, and a
made-up recovery story is worse.

Grouped by how much it blocks launch.

---

## 1. Blocks launch

| # | What | Where | Why it matters |
|---|------|-------|----------------|
| 1 | **Public phone number** | footer + `contact.html` | Currently `[CLIENT TO SUPPLY]` on every page. |
| 2 | **Email inbox for the contact form** | `contact.html` | Form is wired to Formsubmit but points at a placeholder address. It will not deliver until you set the address and click the activation email. |
| 3 | **Florida charity registration number (`CH#####`)** | footer | Required alongside the state solicitation disclosure, which is already in place. If registration lapsed, renew before soliciting. |
| 4 | **Zeffy account + form slug** | `js/donate-config.js` | The no-fee donation form. Until this is set, giving falls back to your existing PayPal button and the mailing address — both live and working. |
| 5 | **Confirm the mailing address** | footer, `ways-to-give.html` | We carried over *55 Black Alder Dr, Palm Coast, FL 32137* from the old site. Confirm it is still correct. |

---

## 2. Needed for the site to do its job

| # | What | Where |
|---|------|-------|
| 6 | **Real per-item costs** — one two-dose Narcan kit; a month of transportation for one participant; one drug test; per-person graduation cost | home + `ways-to-give.html` giving tiers |
| 7 | **Program outcomes** — graduates since 2009, completion rate, re-arrest rate for graduates vs. comparable non-participants, and the date range each covers | home, "By the numbers" |
| 8 | **Next Narcan class** — date, time, venue, whether registration is required. If classes run on a fixed schedule, tell us the pattern and we will publish that so it never goes stale | home + `narcan.html` |
| 9 | **Facebook page URL** | footer |

Items 6 and 7 are the two that most change how well this site raises money. A tier that
says "$45 puts a Narcan kit in someone's hands" converts; a tier that says "$ —" does not.

**Where to get #7:** the Seventh Judicial Circuit drug court coordinator, or the Office of
the State Courts Administrator.

---

## 3. Worth doing, not urgent

| # | What | Why |
|---|------|-----|
| 10 | **A Flagler County cost-per-participant figure** | The site currently uses Florida's statewide average from a 2014 state report, with the date caveat stated plainly on the page. A current local number would be far more persuasive to county commissioners and local donors. |
| 11 | **Podcast links** — "The Road to Recovery" on Spotify / Apple / YouTube | `about.html` has a spot reserved. |
| 12 | **Drug court eligibility + referral route** | Two FAQ answers on `drug-court.html` are held blank. A wrong answer could stop someone from applying, so we would rather publish nothing until the court confirms. |
| 13 | **Sponsorship levels** | If you have set tiers with prices and benefits, we will publish a proper sponsorship table. |
| 14 | **Vector logo (AI/EPS/SVG)** | The only logo available was a raster image recovered from the old site. If no vector exists, a one-time redraw would sharpen print, signage, banners and the site at once. |
| 15 | **Better event photography** | The current gallery uses what we recovered from the old site. Real, recent, well-lit photos of volunteers and events would lift the whole site. |

---

## 4. Participant stories — read before publishing any

`about.html` has a reserved space marked
**[REQUIRES SIGNED CONSENT — 42 CFR Part 2]**. It is deliberately empty. We did not write
a sample testimonial, because a fictional recovery story on a foundation whose mission
includes destigmatization would be both dishonest and self-defeating.

Before anything goes there:

- Get a **written, signed, specific release** from the person. Records tied to substance
  use treatment are protected under **42 CFR Part 2**, which is stricter than HIPAA:
  consent must name what is disclosed, to whom, and for how long, and it can be revoked.
  A general photo release is **not** sufficient.
- Let the person write or approve their own words.
- No last name and no identifying photo unless they explicitly ask for it.
- Involve the drug court coordinator.
- No before/after framing, no mugshots, no rock-bottom arc.

---

## 5. Things we fixed from the old site

For reference, against the audit:

- **SEO (was F)** — real text instead of text baked into images, unique titles and
  descriptions per page, `robots.txt`, `sitemap.xml`, canonical tags, Open Graph cards
- **AI searchability (was F)** — NGO structured data with EIN, address and service area;
  the site is now plain HTML that renders without JavaScript
- **Accessibility (was F)** — alt text everywhere, real heading structure, keyboard and
  screen-reader support, AA/AAA contrast, 44px tap targets
- **Security (was D)** — header block supplied in `README.md`; the aging PHP mailer is
  replaced with Formsubmit
- **Performance (was D)** — the 1.6 MB homepage graphic is now **20 KB**; fonts are
  self-hosted, images are WebP with fallbacks and explicit dimensions
- **Design & donations (was C)** — persistent donate button, sticky on mobile; a zero-fee
  donation platform; monthly giving built around your existing Club 100

A complete copy of the old site, including all 27 blog posts, is archived in
`../scrape/` alongside this repo.
