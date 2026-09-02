/* ==========================================================================
   Events calendar — events.html
   ==========================================================================

   Progressive enhancement, on purpose. The full list of events is already in
   the HTML (generated from data/events.json by tools/build-pages.py). This
   file adds the month grid on top of it, re-hides events that have gone past
   since the page was last built, and wires the "Add to my calendar" buttons.

   With JavaScript off, everything below the grid still works.

   Nothing here needs a server. To change events, edit data/events.json and
   re-run tools/build-pages.py.
   ========================================================================== */
(function () {
  'use strict';

  var node = document.getElementById('fcdc-events-data');
  var mount = document.querySelector('[data-calendar]');
  if (!node) return;

  var events;
  try {
    events = JSON.parse(node.textContent) || [];
  } catch (err) {
    return; // Malformed data must never take the static list down with it.
  }

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  /* Parse 'YYYY-MM-DD' as a LOCAL date. new Date('2026-10-24') is parsed as UTC
     and lands on the 23rd for anyone west of Greenwich — which is all of Florida. */
  function ymd(s) {
    if (!s) return null;
    var p = s.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function midnight(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function key(d) { return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }

  var today = midnight(new Date());

  events.forEach(function (ev) {
    ev._start = ymd(ev.start);
    ev._end = ymd(ev.end) || ev._start;
    ev._past = !!(ev._end && ev._end < today);
  });

  var dated = events.filter(function (ev) { return ev._start; });

  /* ---- Re-hide anything that has gone past since the last build ---------- */
  dated.forEach(function (ev) {
    var li = document.getElementById(ev.id);
    if (li && li.classList.contains('evt')) li.hidden = ev._past;
  });

  var list = document.getElementById('event-list');
  if (list && !list.querySelector('.evt:not([hidden])')) {
    var empty = document.createElement('li');
    empty.className = 'evt evt--empty';
    empty.innerHTML = '<p class="mb-0">No dates are on the calendar right now. ' +
      '<a href="contact.html?subject=general">Ask us what is coming</a> — ' +
      'events go up here as soon as they are set.</p>';
    list.appendChild(empty);
  }

  /* ---- Day → events index ------------------------------------------------ */
  var byDay = {};
  dated.forEach(function (ev) {
    var d = new Date(ev._start.getTime());
    while (d <= ev._end) {
      (byDay[key(d)] = byDay[key(d)] || []).push(ev);
      d.setDate(d.getDate() + 1);
    }
  });

  /* ---- Month grid -------------------------------------------------------- */
  if (!mount) return;

  var upcoming = dated.filter(function (ev) { return !ev._past; })
                      .sort(function (a, b) { return a._start - b._start; });
  var view = upcoming.length
    ? new Date(upcoming[0]._start.getFullYear(), upcoming[0]._start.getMonth(), 1)
    : new Date(today.getFullYear(), today.getMonth(), 1);

  var bar = document.createElement('div');
  bar.className = 'cal__bar';
  var label = document.createElement('p');
  label.className = 'cal__month';
  label.setAttribute('aria-live', 'polite');
  var nav = document.createElement('div');
  nav.className = 'cal__nav';

  function navButton(dir, title, path) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', title);
    b.title = title;
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="' + path + '"/></svg>';
    b.addEventListener('click', function () {
      view = new Date(view.getFullYear(), view.getMonth() + dir, 1);
      render();
    });
    return b;
  }
  nav.appendChild(navButton(-1, 'Previous month', 'M15 18l-6-6 6-6'));
  nav.appendChild(navButton(1, 'Next month', 'M9 18l6-6-6-6'));
  bar.appendChild(label);
  bar.appendChild(nav);

  var grid = document.createElement('table');
  grid.className = 'cal__grid';

  mount.insertBefore(bar, mount.firstChild);
  mount.insertBefore(grid, bar.nextSibling);

  function render() {
    var year = view.getFullYear(), month = view.getMonth();
    var title = MONTHS[month] + ' ' + year;
    label.textContent = title;

    var first = new Date(year, month, 1);
    var days = new Date(year, month + 1, 0).getDate();
    var lead = first.getDay();

    var html = '<caption class="visually-hidden">Foundation events in ' + title +
               '. Days with an event link to the full details below.</caption><thead><tr>';
    DAYS.forEach(function (d) {
      html += '<th scope="col"><abbr title="' + d + '">' + d.slice(0, 3) + '</abbr></th>';
    });
    html += '</tr></thead><tbody>';

    var cell = 0;
    var total = lead + days;
    var rows = Math.ceil(total / 7);

    for (var r = 0; r < rows; r++) {
      html += '<tr>';
      for (var c = 0; c < 7; c++, cell++) {
        var day = cell - lead + 1;
        if (day < 1 || day > days) { html += '<td class="is-blank"></td>'; continue; }

        var date = new Date(year, month, day);
        var todays = byDay[key(date)] || [];
        var attrs = todays.length ? ' class="has-events"' : '';
        if (date.getTime() === today.getTime()) attrs += ' aria-current="date"';

        html += '<td' + attrs + '><span class="cal__num">' + day + '</span>';
        todays.forEach(function (ev) {
          html += '<a class="cal__evt cal__evt--' + esc(ev.kind) + '" href="#' + esc(ev.id) +
                  '" title="' + esc(ev.title) + '"><span class="visually-hidden">' +
                  esc(ev.title) + '</span></a>';
        });
        html += '</td>';
      }
      html += '</tr>';
    }
    grid.innerHTML = html + '</tbody>';
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }

  render();

  /* ---- "Add to my calendar" — a .ics file built in the browser ----------- */
  function icsDate(d) {
    return d.getFullYear() +
      String(d.getMonth() + 1).padStart(2, '0') +
      String(d.getDate()).padStart(2, '0');
  }
  function icsText(s) {
    return String(s || '').replace(/\\/g, '\\\\').replace(/;/g, '\\;')
                          .replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
  }
  function fold(line) {
    // RFC 5545 caps a content line at 75 octets; continuations start with a space.
    var out = [], i = 0;
    while (line.length - i > 74) { out.push((i ? ' ' : '') + line.substr(i, 74)); i += 74; }
    out.push((i ? ' ' : '') + line.substr(i));
    return out.join('\r\n');
  }

  document.querySelectorAll('[data-ics]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var ev = events.filter(function (e) { return e.id === btn.getAttribute('data-ics'); })[0];
      if (!ev || !ev._start) return;

      var end = new Date(ev._end.getTime());
      end.setDate(end.getDate() + 1); // DTEND is exclusive for all-day events

      var desc = ev.summary || '';
      if (ev.time) desc = ev.time + '. ' + desc;
      if (ev.needsConfirming) desc = 'DATE TO BE CONFIRMED. ' + desc;

      var lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Flagler County Drug Court Foundation//Events//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'BEGIN:VEVENT',
        'UID:' + ev.id + '@fcdcfoundation.org',
        'DTSTAMP:' + icsDate(new Date()) + 'T000000Z',
        'DTSTART;VALUE=DATE:' + icsDate(ev._start),
        'DTEND;VALUE=DATE:' + icsDate(end),
        fold('SUMMARY:' + icsText(ev.title)),
        fold('DESCRIPTION:' + icsText(desc)),
        fold('LOCATION:' + icsText(ev.location || 'Flagler County, Florida')),
        fold('URL:' + location.origin + location.pathname + '#' + ev.id),
        'END:VEVENT',
        'END:VCALENDAR'
      ];

      var blob = new Blob([lines.join('\r\n') + '\r\n'], { type: 'text/calendar;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = ev.id.replace(/^event-/, '') + '.ics';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });
  });
})();
