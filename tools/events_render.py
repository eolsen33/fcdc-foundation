#!/usr/bin/env python3
"""
Event rendering for tools/build-pages.py.

ONE source of truth for events: data/events.json. From it this module generates
every place an event appears — the three cards on the home page, the events page
list, the JSON the calendar script reads, and the schema.org markup. Nothing about
events is hand-written in the .part files; they carry {{TOKENS}} instead.

Past events are marked hidden at BUILD time (against the build date) and hidden
again at VIEW time by js/calendar.js, so a stale deploy still shows the right
thing to a visitor.
"""

import datetime
import html
import json
import re

KIND_LABEL = {
    "fundraiser": "Fundraiser",
    "training":   "Training",
    "community":  "Community",
}

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def _e(s):
    """Escape for an attribute value."""
    return html.escape(str(s), quote=True)


def _t(s):
    """Escape for text content — leaves quotes and apostrophes readable in the source."""
    return html.escape(str(s), quote=False)


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def _parse(d):
    return datetime.date.fromisoformat(d) if d else None


def _expand(ev):
    """One entry per occurrence. ``repeat: "first-friday"`` becomes the first Friday
    of every month from ``start`` through ``until``, minus any dates in ``skip``."""
    if not ev.get("repeat"):
        return [ev]
    assert ev["repeat"] == "first-friday", "unknown repeat: %r" % ev["repeat"]
    start, until = _parse(ev["start"]), _parse(ev["until"])
    skip = set(ev.get("skip") or [])
    out, y, m = [], start.year, start.month
    while datetime.date(y, m, 1) <= until:
        first = datetime.date(y, m, 1)
        day = first + datetime.timedelta(days=(4 - first.weekday()) % 7)
        if start <= day <= until and day.isoformat() not in skip:
            out.append(dict(ev, start=day.isoformat(), _series=slugify(ev["title"])))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def load(root):
    """Read data/events.json and return events sorted: dated ascending, undated last."""
    raw = json.loads((root / "data" / "events.json").read_text())["events"]
    out = []
    for src in raw:
      for ev in _expand(src):
        start = _parse(ev.get("start"))
        end = _parse(ev.get("end")) or start
        out.append({
            "title": ev["title"],
            "summary": ev.get("summary", ""),
            "start": start,
            "end": end,
            "time": ev.get("time"),
            "whenText": ev.get("whenText"),
            "location": ev.get("location"),
            "kind": ev.get("kind", "community"),
            "link": ev.get("link"),
            "linkText": ev.get("linkText"),
            "needsConfirming": bool(ev.get("needsConfirming")),
            "confirmText": ev.get("confirmText"),
            "mapUrl": ev.get("mapUrl"),
            "featured": bool(ev.get("featured")),
            "flyer": ev.get("flyer"),
            "flyerSize": ev.get("flyerSize") or [1120, 1449],
            "popup": bool(ev.get("popup")),
            "popupText": ev.get("popupText"),
            "popupUntil": ev.get("popupUntil"),
            "series": ev.get("_series"),
            "id": "event-" + slugify(ev["title"]) + (("-" + ev["start"]) if ev.get("_series") else ""),
        })
    out.sort(key=lambda e: (e["start"] is None, e["start"] or datetime.date.max))
    return out


def when_text(ev):
    """The printed date. Long form, because half this audience reads it on a phone."""
    if ev["whenText"]:
        return ev["whenText"]
    s, e = ev["start"], ev["end"]
    if not s:
        return "Date to be announced"
    base = f"{WEEKDAYS[(s.weekday() + 1) % 7]}, {MONTHS[s.month - 1]} {s.day}, {s.year}"
    if e and e != s:
        if e.year == s.year and e.month == s.month:
            return f"{MONTHS[s.month - 1]} {s.day}–{e.day}, {s.year}"
        return f"{base} – {MONTHS[e.month - 1]} {e.day}, {e.year}"
    return base


def short_when(ev):
    if ev["whenText"]:
        return ev["whenText"]
    s = ev["start"]
    return f"{MONTHS[s.month - 1]} {s.day}" if s else "Date to be announced"


def is_past(ev, today):
    return bool(ev["end"]) and ev["end"] < today


# ── Renderers ───────────────────────────────────────────────────────────────

def _kind_tag(ev):
    label = KIND_LABEL.get(ev["kind"], "Event")
    return f'<span class="evt-kind evt-kind--{_e(ev["kind"])}">{_t(label)}</span>'


def _confirm_note(ev):
    if not ev["needsConfirming"]:
        return ""
    if ev["confirmText"]:
        return f'<p class="evt-confirm">{_t(ev["confirmText"])}</p>'
    return ('<p class="evt-confirm"><strong>Date to be confirmed</strong> — '
            'check with us before you make plans around it.</p>')


def _map_link(ev, cls="btn btn--outline"):
    """A Google Maps link for the venue. Opens in a new tab so the page is not lost."""
    if not ev["mapUrl"]:
        return ""
    return (f'<a class="{cls}" href="{_e(ev["mapUrl"])}" target="_blank" rel="noopener">'
            'Map &amp; directions</a>')


def home_cards(events, today, limit=3):
    """The three next events, as tier cards, for the home page.

    An event marked ``featured: true`` keeps a slot even when more than
    ``limit`` events come before it — the latest non-featured pick is dropped
    to make room. Cards stay in date order either way."""
    upcoming, seen = [], set()
    for e in events:
        if is_past(e, today) or (e["series"] and e["series"] in seen):
            continue          # a repeating event gets one card: its next date
        seen.add(e["series"])
        upcoming.append(e)
    live = upcoming[:limit]
    for ev in upcoming[limit:]:
        if not ev["featured"]:
            continue
        drop = [i for i, e in enumerate(live) if not e["featured"]]
        if not drop:
            break
        live.pop(drop[-1])
        live.append(ev)
    live.sort(key=upcoming.index)
    if not live:
        return ('      <p class="lede">Nothing on the calendar just now. '
                '<a href="events.html">Check the calendar</a> — we add events as they are set.</p>')
    out = ['      <div class="grid grid--3">']
    for ev in live:
        out.append('        <div class="tier">')
        out.append(f'          <p class="tier__buys">{_t(ev["title"])}</p>')
        out.append(f'          <p class="tier__amount" style="font-size:1.5rem">{_t(short_when(ev))}</p>')
        if ev["summary"]:
            out.append(f'          <p>{_t(ev["summary"])}</p>')
        href = ev["link"] or f'events.html#{ev["id"]}'
        text = ev["linkText"] or "Details"
        out.append(f'          <a class="btn btn--outline" href="{_e(href)}">{_t(text)}</a>')
        if ev["mapUrl"]:
            out.append("          " + _map_link(ev))
        out.append('        </div>')
    out.append('      </div>')
    return "\n".join(out)


def event_list(events, today):
    """The full, static, no-JavaScript-required list on the events page."""
    dated = [e for e in events if e["start"]]
    undated = [e for e in events if not e["start"]]
    out = []

    # The list is a horizontal slideshow: CSS scroll-snap does the sliding, so it
    # works with JavaScript off (a plain sideways scroll); calendar.js adds the
    # arrows, dots and "1 of 4" count.
    out.append('      <div class="evt-slider" data-evt-slider>')
    out.append('      <ul class="evt-list" id="event-list" aria-label="Upcoming events">')
    if not dated:
        out.append('        <li class="evt evt--empty"><p class="mb-0">No dates are on the '
                   'calendar right now.</p></li>')
    for ev in dated:
        past = is_past(ev, today)
        hid = " hidden" if past else ""
        out.append(f'        <li class="evt" id="{_e(ev["id"])}" data-start="{ev["start"].isoformat()}" '
                   f'data-end="{(ev["end"] or ev["start"]).isoformat()}"{hid}>')
        out.append('          <div class="evt__date" aria-hidden="true">')
        out.append(f'            <span class="evt__mon">{_t(MONTHS[ev["start"].month - 1][:3])}</span>')
        out.append(f'            <span class="evt__day">{ev["start"].day}</span>')
        out.append('          </div>')
        out.append('          <div class="evt__body">')
        out.append(f'            {_kind_tag(ev)}')
        out.append(f'            <h3>{_t(ev["title"])}</h3>')
        out.append(f'            <p class="evt__when">{_t(when_text(ev))}'
                   + (f' &middot; {_t(ev["time"])}' if ev["time"] else '') + '</p>')
        if ev["location"]:
            out.append(f'            <p class="evt__where">{_t(ev["location"])}</p>')
        note = _confirm_note(ev)
        if note:
            out.append("            " + note)
        if ev["summary"]:
            out.append(f'            <p>{_t(ev["summary"])}</p>')
        out.append('            <p class="evt__actions">')
        if ev["link"]:
            out.append(f'              <a class="btn btn--outline" href="{_e(ev["link"])}">'
                       f'{_t(ev["linkText"] or "Details")}</a>')
        if ev["mapUrl"]:
            out.append("              " + _map_link(ev))
        if ev["flyer"]:
            out.append(f'              <a class="btn btn--outline" href="assets/img/{_e(ev["flyer"])}-1120.webp" '
                       'target="_blank" rel="noopener">See the flyer</a>')
        out.append(f'              <button class="btn btn--outline" type="button" data-ics="{_e(ev["id"])}">'
                   'Add to my calendar</button>')
        out.append('            </p>')
        out.append('          </div>')
        out.append('        </li>')
    out.append('      </ul>')
    out.append('      </div>')
    return "\n".join(out)


def undated_cards(events):
    """The 'Dates still to come' cards — events with start: null. Empty string if none."""
    undated = [e for e in events if not e["start"]]
    out = []
    if undated:
        out.append('      <h2 id="undated-heading">Dates still to come</h2>')
        out.append('      <div class="grid grid--2">')
        for ev in undated:
            out.append(f'        <div class="card" id="{_e(ev["id"])}">')
            out.append(f'          {_kind_tag(ev)}')
            out.append(f'          <h3>{_t(ev["title"])}</h3>')
            out.append(f'          <p class="evt__when">{_t(when_text(ev))}</p>')
            if ev["summary"]:
                out.append(f'          <p>{_t(ev["summary"])}</p>')
            if ev["link"]:
                out.append(f'          <a class="btn btn--outline" href="{_e(ev["link"])}">'
                           f'{_t(ev["linkText"] or "Details")}</a>')
            out.append('        </div>')
        out.append('      </div>')

    return "\n".join(out)


def popup(events, today):
    """The home-page pop-up: the flyer of the first upcoming event marked ``popup``,
    a short blurb and two buttons. js/main.js opens it once per visit and stops on
    its own when the event is over, so a stale deploy never advertises a past date."""
    ev = next((e for e in events if e["popup"] and e["flyer"] and e["start"]
               and not is_past(e, today)), None)
    if not ev:
        return ""
    w, h = ev["flyerSize"]
    until = ev["popupUntil"] or (ev["end"] or ev["start"]).isoformat() + "T23:59"
    img = "assets/img/" + ev["flyer"]
    when = when_text(ev) + (f' &middot; {_t(ev["time"])}' if ev["time"] else "")
    alt = f'Flyer: {ev["title"]}, {when_text(ev)}' + (f', {ev["time"]}' if ev["time"] else "") \
        + (f', {ev["location"]}' if ev["location"] else "") + "."
    out = [
        "",
        "  <!-- Event pop-up: generated from data/events.json (popup: true) -->",
        f'  <dialog class="pop" data-popup="{_e(ev["id"])}-{ev["start"].isoformat()}" data-until="{_e(until)}" aria-labelledby="pop-heading">',
        '    <button class="pop__x" type="button" aria-label="Close">',
        '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
        '    </button>',
        '    <div class="pop__in">',
        '      <figure class="pop__flyer">',
        f'        <img src="{_e(img)}-560.webp" srcset="{_e(img)}-560.webp 560w, {_e(img)}-1120.webp 1120w"',
        f'          sizes="(min-width: 760px) 440px, 70vw" width="{w}" height="{h}" alt="{_e(alt)}">',
        '      </figure>',
        '      <div class="pop__copy">',
        f'        {_kind_tag(ev)}',
        f'        <h2 id="pop-heading">{_t(ev["title"])}</h2>',
        f'        <p class="pop__when">{when}</p>',
    ]
    if ev["location"]:
        out.append(f'        <p class="pop__where">{_t(ev["location"])}</p>')
    out.append(f'        <p>{_t(ev["popupText"] or ev["summary"])}</p>')
    out.append('        <p class="pop__act">')
    out.append(f'          <a class="btn btn--primary" href="events.html#{_e(ev["id"])}">Event details</a>')
    if ev["mapUrl"]:
        out.append("          " + _map_link(ev))
    out.append('        </p>')
    out.append('      </div>')
    out.append('    </div>')
    out.append('  </dialog>')
    return "\n".join(out)


def data_script(events):
    """The events, inlined as JSON so the calendar needs no fetch and works on file://."""
    payload = [{
        "id": e["id"], "title": e["title"], "summary": e["summary"],
        "start": e["start"].isoformat() if e["start"] else None,
        "end": (e["end"] or e["start"]).isoformat() if e["start"] else None,
        "time": e["time"], "when": when_text(e), "location": e["location"],
        "kind": e["kind"], "needsConfirming": e["needsConfirming"],
        "mapUrl": e["mapUrl"],
    } for e in events]
    body = json.dumps(payload, indent=2).replace("</", "<\\/")
    return ('  <script type="application/json" id="fcdc-events-data">\n'
            + body + "\n  </script>")


def jsonld(events, today, site):
    """schema.org Event markup — this is how a nonprofit's events surface in search."""
    items = []
    for ev in events:
        if not ev["start"] or is_past(ev, today):
            continue
        item = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": ev["title"],
            "startDate": ev["start"].isoformat(),
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "eventStatus": "https://schema.org/EventScheduled",
            "organizer": {
                "@type": "NGO",
                "name": "Flagler County Drug Court Foundation",
                "url": site + "/",
            },
            "url": f"{site}/events.html#{ev['id']}",
            "isAccessibleForFree": True,
        }
        if ev["end"] and ev["end"] != ev["start"]:
            item["endDate"] = ev["end"].isoformat()
        if ev["summary"]:
            item["description"] = ev["summary"]
        item["location"] = {
            "@type": "Place",
            "name": ev["location"] or "Flagler County, Florida",
            "address": {"@type": "PostalAddress", "addressLocality": "Palm Coast",
                        "addressRegion": "FL", "addressCountry": "US"},
        }
        if ev["mapUrl"]:
            item["location"]["hasMap"] = ev["mapUrl"]
        items.append(item)
    if not items:
        return ""
    return ('  <script type="application/ld+json">\n'
            + json.dumps(items, indent=2).replace("</", "<\\/") + "\n  </script>")


def tokens(root, site, today=None):
    today = today or datetime.date.today()
    events = load(root)
    return {
        "EVENTS_HOME_CARDS": home_cards(events, today),
        "EVENTS_LIST":       event_list(events, today),
        "EVENTS_UNDATED":    undated_cards(events),
        "EVENTS_DATA":       data_script(events),
        "EVENTS_JSONLD":     jsonld(events, today, site),
        "EVENTS_POPUP":      popup(events, today),
    }
