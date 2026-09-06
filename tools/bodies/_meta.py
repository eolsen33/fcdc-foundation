# Per-page <head> metadata. Used only by tools/build-pages.py.

META = {
    "index.html": {
        "title": "Flagler County Drug Court Foundation | Recovery, Hope, Second Chances",
        "description": "The Flagler County Drug Court Foundation helps people in the Flagler County drug court program recover — transportation, housing deposits, GEDs, specialized treatment, free Narcan and training. A local 501(c)(3) since 2009.",
        "og_description": "We help Flagler County neighbors in the drug court program get through recovery — rides, deposits, GEDs, free Narcan — and we provide hope. Every dollar stays in this county.",
    },
    "about.html": {
        "title": "About Us | Flagler County Drug Court Foundation",
        "description": "A Flagler County 501(c)(3) founded in 2009 by residents who believe in the drug court program. Our mission, vision, education work, and the volunteers behind it.",
    },
    "drug-court.html": {
        "title": "How Drug Court Works | Flagler County Drug Court Foundation",
        "description": "Drug court offers supervised treatment instead of incarceration for people with a substance use disorder. How the Flagler County program works, who is eligible, and what it costs taxpayers.",
        # FAQPage schema from the 2026-09-05 SEO pass. Lives here, not in the HTML,
        # so the generator does not silently drop it. Keep in step with the FAQ on the page.
        "head_extra": """<!-- seo-kit:faq -->
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Who is eligible for drug court in Flagler County?", "acceptedAnswer": {"@type": "Answer", "text": "[CLIENT / COURT TO CONFIRM] Eligibility is set by the Seventh Judicial Circuit, not by the Foundation. We need the current criteria — charge types, prior record limits, residency, and the referral route — before publishing anything here, because a wrong answer could keep someone from applying."}}, {"@type": "Question", "name": "How does someone get referred?", "acceptedAnswer": {"@type": "Answer", "text": "[CLIENT / COURT TO CONFIRM] Who initiates a referral — defense counsel, the State Attorney, the judge, or self-referral — and the contact for the drug court coordinator."}}, {"@type": "Question", "name": "How long does the program take?", "acceptedAnswer": {"@type": "Answer", "text": "A minimum of one year. The actual length depends on the person's progress through the program's phases."}}, {"@type": "Question", "name": "What does the Foundation pay for?", "acceptedAnswer": {"@type": "Answer", "text": "We fund the things the court budget does not cover: transportation to treatment and court, car repairs, driver’s license reinstatement, GEDs, housing deposits, specialized treatment, life skills programming, graduations, free Narcan, and community training. We do not pay for drug testing — that is part of the court program — and we do not pay anyone’s fines. See Ways to Give ."}}, {"@type": "Question", "name": "Is the Foundation part of the court?", "acceptedAnswer": {"@type": "Answer", "text": "No. We are an independent 501(c)(3) nonprofit (EIN 27-1349987) that supports the program. Having a nonprofit backing a public agency is unusual — it is what lets the program act quickly without waiting on a budget cycle."}}]}
</script>
<!-- /seo-kit:faq -->
""",
    },
    "narcan.html": {
        "title": "Free Narcan & Overdose Response Training | Flagler County",
        "description": "Free naloxone (Narcan) kits and overdose response training in Flagler County. The first local nonprofit to secure a Florida DCF grant to distribute Narcan at no cost, since 2019.",
    },
    "podcast.html": {
        "title": "The Road to Recovery Podcast | Flagler County Drug Court Foundation",
        "description": "The Road to Recovery is the podcast of the Flagler County Drug Court Foundation \u2014 honest conversations with drug court graduates, families, counselors, and the local businesses that hire people in recovery.",
        "og_title": "The Road to Recovery \u2014 our podcast",
        "og_description": "Honest conversations with people who have lived it: graduates of the Flagler County drug court program, their families, and the people who work alongside them.",
    },
    "events.html": {
        "title": "Events Calendar | Flagler County Drug Court Foundation",
        "description": "Upcoming Flagler County Drug Court Foundation events — the Ride for Recovery, the spring golf tournament, Dine to Donate nights, and free Narcan training classes.",
        "og_description": "Ride for Recovery, the spring golf tournament, restaurant fundraiser nights, and free Narcan training. Come out with us in Flagler County.",
    },
    "ways-to-give.html": {
        "title": "Ways to Give | Flagler County Drug Court Foundation",
        "description": "Give monthly through Club 100, make a one-time gift, sponsor as a local business, or give by mail. Every dollar stays in Flagler County. EIN 27-1349987.",
    },
    "contact.html": {
        "title": "Contact & Volunteer | Flagler County Drug Court Foundation",
        "description": "Reach the Flagler County Drug Court Foundation, request a Narcan training, volunteer, or ask about business sponsorship. Palm Coast, Florida.",
    },
}
