/* ANDIAMO?: legge data/events.json, filtra per giorni/categorie/accesso/pubblico/luogo/testo,
   mostra mappa (segnaposti colorati con "+", card sulla mappa) ed elenco con scheda.
   Su telefono l'elenco e' un pannello trascinabile (anteprima / meta' / pieno). */
(() => {
  "use strict";

  const $ = (s) => document.querySelector(s);
  const DOW = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];
  const DAYS = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"];
  const MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
    "settembre", "ottobre", "novembre", "dicembre"];
  let STRIP_DAYS = 120;                    // giorni nella striscia (= orizzonte della pipeline)
  const MOBILE = () => window.matchMedia("(max-width: 760px)").matches;

  const state = {
    from: null, to: null, preset: "all", cats: new Set(), access: new Set(), aud: new Set(), q: "",
    selected: null, detail: false, sort: "date", me: null,
    sidebarHidden: false, hiddenBeforeDetail: false,
  };
  let API = "", apiOk = false, aiOk = false;
  let DATA = null, EVENTS = [], CAT = {}, map = null, mapReady = false, popup = null, meMarker = null, onlyUids = null;
  let pushedDetail = false;                // la scheda aperta ha una voce nostra nella cronologia?
  const COORDS = {};                       // uid -> [lon, lat] mostrati (con il piccolo scarto anti-sovrapposizione)

  // ---------------------------------------------------------------- date e distanze
  const pad = (n) => String(n).padStart(2, "0");
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseDay = (s) => { const [y, m, d] = s.slice(0, 10).split("-").map(Number); return new Date(y, m - 1, d); };
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const today = () => { const t = new Date(); t.setHours(0, 0, 0, 0); return t; };
  const timeOf = (e) => (e.start && e.start.length > 10 ? e.start.slice(11, 16) : "");
  const dayLabel = (d) => {
    const diff = Math.round((d - today()) / 86400000);
    const base = `${DAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`;
    return diff === 0 ? `Oggi, ${base}` : diff === 1 ? `Domani, ${base}` : base[0].toUpperCase() + base.slice(1);
  };
  const shortDay = (s) => { const d = parseDay(s); const diff = Math.round((d - today()) / 86400000);
    return diff <= 0 ? "oggi" : diff === 1 ? "domani" : `${DOW[d.getDay()]} ${d.getDate()}`; };
  const shortDate = (s) => { const d = parseDay(s); return `${d.getDate()} ${MONTHS[d.getMonth()].slice(0, 3)}`; };
  const spans = (e, from, to) => {
    const s = e.start.slice(0, 10), en = (e.end || e.start).slice(0, 10);
    return (!to || s <= to) && (!from || en >= from);
  };
  const whenText = (e) => {
    let w = dayLabel(parseDay(e.start));
    if (timeOf(e)) w += `, ore ${timeOf(e)}`;
    if (e.end && e.end.slice(0, 10) !== e.start.slice(0, 10)) w += ` – fino a ${dayLabel(parseDay(e.end)).toLowerCase()}`;
    return w;
  };
  function km(e) {
    if (!state.me) return null;
    const R = 6371, r = Math.PI / 180;
    const dLat = (e.lat - state.me.lat) * r, dLon = (e.lon - state.me.lon) * r;
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(state.me.lat * r) * Math.cos(e.lat * r) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  const kmText = (d) => (d == null ? "" : d < 1 ? `${Math.round(d * 1000 / 50) * 50} m` : `${d.toFixed(d < 10 ? 1 : 0).replace(".", ",")} km`);

  // ---------------------------------------------------------------- accesso: tre gruppi riconoscibili a colpo d'occhio
  const ACCESS_ICON = {
    libero: '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16.5 9"/>',
    offerta: '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    biglietto: '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M14 7v10" stroke-dasharray="2 2"/>',
    iscrizione: '<rect x="5.5" y="4" width="13" height="17" rx="2"/><path d="M9 3.5h6v3H9zM9 12h6M9 16h4"/>',
    invito: '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="m3.5 7.5 8.5 6 8.5-6"/>',
  };
  function accessGroup(e) {
    for (const [g, v] of Object.entries(DATA.access_groups || {})) if ((v.includes || []).includes(e.access)) return g;
    return "";
  }
  // badge con icona e stile del gruppo; il testo e' il tipo preciso (es. "Offerta libera", "Su invito")
  // Un solo stile per gruppo, uguale su filtri, card e scheda: stessa icona, stessa forma.
  //   libero = bordo pieno, a pagamento = pieno scuro, iscrizione = bordo tratteggiato
  const GROUP_ICON = { libero: "libero", pagamento: "biglietto", iscrizione: "iscrizione" };
  const accIcon = (g) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ACCESS_ICON[GROUP_ICON[g]] || ""}</svg>`;
  function accessBadge(e) {
    const g = accessGroup(e);
    if (!g) return "";
    const label = (DATA.access[e.access] || DATA.access_groups[g].label).replace(/\s*\(.*\)$/, "");
    return `<span class="acc acc-${g}" title="${esc(DATA.access_groups[g].label)}">${accIcon(g)}${esc(label)}</span>`;
  }

  // ---------------------------------------------------------------- filtri
  function matches(e, skip = {}) {
    if (!skip.date && !spans(e, state.from, state.to)) return false;
    if (!skip.cat && state.cats.size && !state.cats.has(e.category)) return false;
    if (state.access.size && !state.access.has(accessGroup(e))) return false;   // piu' scelte = uno qualsiasi
    for (const a of state.aud) if (!(e.audience || []).includes(a)) return false;   // scelte attivabili insieme
    if (state.q) {
      const hay = `${e.title} ${e.venue} ${e.town} ${e.summary} ${(CAT[e.category] || {}).label || ""}`.toLowerCase();
      if (!state.q.split(/\s+/).every((w) => hay.includes(w))) return false;
    }
    return true;
  }

  function setPreset(p) {
    state.preset = p;
    const t = today();
    if (p === "today") { state.from = state.to = iso(t); }
    else if (p === "week") { state.from = iso(t); state.to = iso(addDays(t, 6)); }
    else if (p === "weekend") {
      const dow = t.getDay();
      const fri = dow === 0 ? addDays(t, -2) : addDays(t, (5 - dow + 7) % 7);
      const start = dow === 6 || dow === 0 ? t : fri;
      state.from = iso(start); state.to = iso(dow === 0 ? t : addDays(fri, 2));
    } else { state.from = iso(t); state.to = null; }
  }

  // ---------------------------------------------------------------- striscia giorni
  function renderStrip() {
    const strip = $("#strip");
    const t = today();
    const base = EVENTS.filter((e) => matches(e, { date: true }));
    const counts = [];
    for (let i = 0; i < STRIP_DAYS; i++) { const d = iso(addDays(t, i)); counts.push(base.filter((e) => spans(e, d, d)).length); }
    const max = Math.max(1, ...counts);
    const keep = strip.scrollLeft;
    strip.innerHTML = "";
    let days = null;                       // giorni raggruppati per mese: l'etichetta del mese resta ferma mentre si scorre
    counts.forEach((n, i) => {
      const d = addDays(t, i), key = iso(d);
      if (i === 0 || d.getDate() === 1) {
        const m = document.createElement("div");
        m.className = "month";
        m.innerHTML = `<span class="mlabel">${MONTHS[d.getMonth()].slice(0, 3)}${d.getMonth() === 0 && i > 0 ? ` ${d.getFullYear()}` : ""}</span><div class="mdays"></div>`;
        strip.appendChild(m);
        days = m.querySelector(".mdays");
      }
      const b = document.createElement("button");
      b.type = "button";
      b.className = "day" + (d.getDay() === 0 || d.getDay() === 6 ? " weekend" : "") + (n ? "" : " empty");
      const on = state.preset !== "all" && state.from && key >= state.from && (!state.to || key <= state.to);
      b.setAttribute("aria-pressed", String(!!on));
      b.setAttribute("aria-label", `${dayLabel(d)}: ${n} eventi`);
      b.innerHTML = `<span class="bar-wrap"><span class="bar" style="height:${Math.round((n / max) * 28) + 2}px"></span></span>
        <span class="dow">${i === 0 ? "oggi" : DOW[d.getDay()]}</span><span class="num">${d.getDate()}</span>`;
      b.addEventListener("click", () => {
        if (state.preset === "day" && state.from === key) setPreset("all");
        else { state.preset = "day"; state.from = state.to = key; }
        onlyUids = null; update();
      });
      days.appendChild(b);
    });
    strip.scrollLeft = keep;
    document.querySelectorAll(".presets button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.preset === state.preset)));
    updateStripNav();
  }

  // frecce avanti/indietro (desktop) per le righe che scorrono: giorni e categorie
  function updateScrollNav(sel) {
    const s = $(sel), id = sel.slice(1);
    const atStart = s.scrollLeft <= 2, atEnd = s.scrollLeft + s.clientWidth >= s.scrollWidth - 2;
    $(`#${id}-prev`).disabled = atStart;
    $(`#${id}-next`).disabled = atEnd;
    s.classList.toggle("at-end", atEnd);
  }
  const updateStripNav = () => updateScrollNav("#strip");

  function setupScrollNav(sel) {
    const s = $(sel), id = sel.slice(1);
    const step = () => Math.max(120, Math.floor(s.clientWidth * 0.8));
    $(`#${id}-prev`).addEventListener("click", () => s.scrollBy({ left: -step() }));
    $(`#${id}-next`).addEventListener("click", () => s.scrollBy({ left: step() }));
    s.addEventListener("scroll", () => requestAnimationFrame(() => updateScrollNav(sel)), { passive: true });
    window.addEventListener("resize", () => updateScrollNav(sel));
  }

  // ---------------------------------------------------------------- categorie
  function renderChips() {
    const box = $("#chips");
    const base = EVENTS.filter((e) => matches(e, { cat: true }));
    box.innerHTML = "";
    DATA.categories.forEach((c) => {
      const n = base.filter((e) => e.category === c.id).length;
      if (n === 0 && !state.cats.has(c.id)) return;          // categorie vuote: nascoste
      const b = document.createElement("button");
      b.type = "button"; b.className = "chip";
      b.style.setProperty("--c", c.color);
      b.setAttribute("aria-pressed", String(state.cats.has(c.id)));
      b.innerHTML = `<span class="dot"></span>${esc(c.label)} <span class="n">${n}</span>`;
      b.addEventListener("click", () => { state.cats.has(c.id) ? state.cats.delete(c.id) : state.cats.add(c.id); onlyUids = null; update(); });
      box.appendChild(b);
    });
    const extra = (state.access.size ? 1 : 0) + state.aud.size;
    $("#more-filters").innerHTML = extra ? `Filtri <span class="badge">${extra}</span>` : "Filtri";
    // nessuna scelta = tutti attivi (e tutti mostrati come attivi)
    document.querySelectorAll("#access button").forEach((b) =>
      b.setAttribute("aria-pressed", String(!state.access.size || state.access.has(b.dataset.v))));
    document.querySelectorAll("#audience button").forEach((b) => b.setAttribute("aria-pressed", String(state.aud.has(b.dataset.v))));
    requestAnimationFrame(() => updateScrollNav("#chips"));
  }

  // Filtri "Accesso": all'inizio tutti attivi; il primo clic tiene solo quel gruppo, i successivi
  // aggiungono o tolgono gruppi (vale uno qualsiasi); togliendo l'ultimo si torna a tutti.
  // "Per chi": attivabili insieme, l'evento deve averli tutti; nessuno = tutti.
  function setupFilters() {
    const acc = $("#access");
    Object.entries(DATA.access_groups || {}).forEach(([k, v]) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = `acc acc-${k} acc-btn`; b.dataset.v = k;
      b.innerHTML = accIcon(k) + esc(v.label);
      b.addEventListener("click", () => {
        if (state.access.has(k)) state.access.delete(k); else state.access.add(k);
        if (state.access.size === Object.keys(DATA.access_groups).length) state.access.clear();   // tutti = nessun filtro
        onlyUids = null; update();
      });
      acc.appendChild(b);
    });
    const aud = $("#audience");
    Object.entries(DATA.audience_filters || {}).forEach(([k, label]) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "seg-btn toggle"; b.dataset.v = k;
      b.innerHTML = `<span class="tick" aria-hidden="true"></span>${esc(label)}`;
      b.addEventListener("click", () => { state.aud.has(k) ? state.aud.delete(k) : state.aud.add(k); onlyUids = null; update(); });
      aud.appendChild(b);
    });
  }

  // ---------------------------------------------------------------- elenco
  function renderList(items) {
    const list = $("#list");
    list.innerHTML = "";
    if (!items.length) {
      list.innerHTML = `<li class="empty-state"><strong>Nessun evento con questi filtri.</strong>Prova un altro giorno o togli qualche categoria.</li>`;
      return;
    }
    let lastGroup = "";
    const from = state.from || iso(today());
    const byDistance = state.sort === "distance" && state.me;
    items.forEach((e) => {
      if (!byDistance) {
        const groupDay = e.start.slice(0, 10) < from ? from : e.start.slice(0, 10);
        if (groupDay !== lastGroup) {
          lastGroup = groupDay;
          const g = document.createElement("li");
          g.className = "group"; g.textContent = dayLabel(parseDay(groupDay));
          list.appendChild(g);
        }
      }
      const c = CAT[e.category] || {};
      const longRun = e.end && e.end.slice(0, 10) !== e.start.slice(0, 10);
      let when = byDistance ? shortDay(e.start < from ? from : e.start) + (timeOf(e) ? ` ${timeOf(e)}` : "")
        : timeOf(e) || (longRun ? `fino al ${shortDate(e.end)}` : "");
      const dist = kmText(km(e));
      const li = document.createElement("li");
      li.className = "item";
      li.innerHTML = `<button type="button" data-uid="${e.uid}" style="--c:${c.color}">
          <span class="dot" aria-hidden="true"></span>
          <span><h3>${esc(e.title)}</h3><span class="meta">${esc([e.venue, e.town].filter(Boolean).join(", "))}</span></span>
          <span class="when">${esc(when)}${dist ? `<small>${dist}</small>` : ""}</span></button>`;
      const btn = li.querySelector("button");
      btn.addEventListener("click", () => select(e.uid, { fly: true, detail: true }));
      btn.addEventListener("mouseenter", () => hover(e.uid));
      btn.addEventListener("mouseleave", () => hover(null));
      list.appendChild(li);
    });
  }

  // ---------------------------------------------------------------- scheda
  function renderDetail(e) {
    const el = $("#detail");
    const c = CAT[e.category] || { label: "Evento", color: "#ddd" };
    const sub = (c.sub || {})[e.subcategory];
    const place = [e.venue, e.address, e.town].filter(Boolean).join(", ");
    const who = (e.audience || []).map((a) => DATA.audiences[a]).filter(Boolean).join(", ");
    const where = DATA.settings[e.setting] || "";
    const g = accessGroup(e);
    const private_ = (DATA.access[e.access] || "").match(/\((.*)\)$/);       // es. "Su invito (evento privato)"
    const accessText = g ? [private_ ? private_[1][0].toUpperCase() + private_[1].slice(1) : "", e.price].filter(Boolean).join(" · ")
      : ["Da verificare sul sito ufficiale", e.price].filter(Boolean).join(" · ");
    const host = e.action_url ? new URL(e.action_url).hostname.replace(/^www\./, "") : "";
    const also = (e.also_on || []).filter((a) => a.url);
    const dist = kmText(km(e));
    el.innerHTML = `
      <button class="text-btn back" type="button">← Tutti gli eventi</button><br>
      <span class="cat" style="--c:${c.color}">${esc(c.label)}${sub ? ` · ${esc(sub)}` : ""}</span>
      <h2>${esc(e.title)}</h2>
      <dl class="facts">
        <dt>Quando</dt><dd>${esc(whenText(e))}</dd>
        ${place ? `<dt>Dove</dt><dd>${esc(place)}${where ? ` · ${esc(where.toLowerCase())}` : ""}${dist ? ` · ${dist} da te` : ""}</dd>` : ""}
        <dt>Accesso</dt><dd class="acc-dd">${accessBadge(e)}${accessText ? `<span>${esc(accessText)}</span>` : ""}</dd>
        ${who ? `<dt>Per chi</dt><dd>${esc(who)}</dd>` : ""}
      </dl>
      ${e.summary ? `<p class="summary">${esc(e.summary)}</p>` : ""}
      <p class="official-note">${e.ai_summary ? "Dettagli riassunti tramite AI. " : ""}Per il programma ufficiale e le iscrizioni, visita il sito ufficiale${host ? ` (${esc(host)})` : ""}.</p>
      <p class="also">Fonte: <a href="${attr(e.source_url)}" target="_blank" rel="noopener">${esc(e.source_name)}</a>${
        also.length ? `. Anche su: ${also.map((a) => `<a href="${attr(a.url)}" target="_blank" rel="noopener">${esc(a.source)}</a>`).join(", ")}` : ""}</p>
      <button class="report-link" type="button" data-report>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4h11l-1.5 4L16 12H5"/></svg>Segnala una modifica o la rimozione</button>
      <div class="detail-actions">
        <a class="cta" href="${attr(e.action_url)}" target="_blank" rel="noopener"><span>Sito ufficiale</span><i aria-hidden="true">↗</i></a>
        <button class="round" type="button" data-ics aria-label="Aggiungi al calendario" title="Aggiungi al calendario">
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg></button>
        <a class="round" target="_blank" rel="noopener" aria-label="Indicazioni stradali" title="Indicazioni"
           href="https://www.google.com/maps/dir/?api=1&destination=${e.geo_precision === "town" ? encodeURIComponent([e.venue, e.address, e.town].filter(Boolean).join(", ")) : `${e.lat},${e.lon}`}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
        <button class="round" type="button" data-share aria-label="Condividi" title="Condividi">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3M7.5 7.5 12 3l4.5 4.5M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg></button>
      </div>`;
    el.querySelector(".back").addEventListener("click", closeDetail);
    el.querySelector("[data-ics]").addEventListener("click", () => downloadIcs(e));
    el.querySelector("[data-share]").addEventListener("click", () => share(e));
    el.querySelector("[data-report]").addEventListener("click", () => openReport(e));
  }

  async function share(e) {
    const url = `${location.origin}${location.pathname}#e=${e.uid}`;
    const text = `${e.title} · ${whenText(e)}${e.town ? " · " + e.town : ""}`;
    try {
      if (navigator.share) { await navigator.share({ title: e.title, text, url }); return; }
      await navigator.clipboard.writeText(url);
      toast("Link copiato");
    } catch (_) { /* condivisione annullata */ }
  }

  // ---------------------------------------------------------------- calendario (.ics)
  function downloadIcs(e) {
    const dt = (s, end) => (s.length === 10
      ? `;VALUE=DATE:${(end ? iso(addDays(parseDay(s), 1)) : s).replace(/-/g, "")}`
      : `;TZID=Europe/Rome:${s.replace(/[-:]/g, "")}00`);
    const endVal = e.end || (e.start.length > 10 ? e.start.slice(0, 11) + pad(Math.min(23, +e.start.slice(11, 13) + 2)) + e.start.slice(13) : e.start);
    const lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Andiamoo//IT", "BEGIN:VEVENT",
      `UID:${e.uid}@andiamoo`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").slice(0, 15)}Z`,
      `DTSTART${dt(e.start)}`, `DTEND${dt(endVal, endVal.length === 10)}`,
      `SUMMARY:${ics(e.title)}`, `LOCATION:${ics([e.venue, e.address, e.town].filter(Boolean).join(", "))}`,
      `DESCRIPTION:${ics((e.summary ? e.summary + "\\n\\n" : "") + "Sito ufficiale: " + e.action_url)}`,
      `URL:${e.action_url}`, "END:VEVENT", "END:VCALENDAR"];
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([lines.join("\r\n")], { type: "text/calendar" }));
    a.download = `${e.title.slice(0, 40).replace(/[^\w]+/g, "-")}.ics`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  // ---------------------------------------------------------------- mappa
  function warmStyle() {
    const set = (id, prop, val) => { try { map.setPaintProperty(id, prop, val); } catch (_) { /* proprieta' assente */ } };
    for (const l of map.getStyle().layers) {
      const id = l.id;
      if (l.type === "background") set(id, "background-color", "#d9d5cb");
      else if (l.type === "fill" && /water/.test(id)) set(id, "fill-color", "#f5f3ee");
      else if (l.type === "fill" && /landcover|landuse|park|wood|grass/.test(id)) { set(id, "fill-color", "#d2cec3"); set(id, "fill-opacity", 0.6); }
      else if (l.type === "fill" && /building/.test(id)) set(id, "fill-color", "#cdc8bd");
      else if (l.type === "line" && /water|river|waterway/.test(id)) set(id, "line-color", "#f5f3ee");
      else if (l.type === "line" && /boundary|admin/.test(id)) set(id, "line-color", "#ffffff");
      else if (l.type === "line" && /road|highway|street|path|bridge|tunnel|rail/.test(id)) set(id, "line-color", "#e7e3da");
      else if (l.type === "symbol") { set(id, "text-color", "#5f5b54"); set(id, "text-halo-color", "#e3dfd6"); }
    }
  }

  function pinImage(color, minus) {
    const s = 2, r = 13, size = (r + 3) * 2;
    const cv = document.createElement("canvas");
    cv.width = cv.height = size * s;
    const g = cv.getContext("2d");
    g.scale(s, s);
    g.beginPath(); g.arc(size / 2, size / 2, r, 0, Math.PI * 2);
    g.fillStyle = color; g.fill();
    g.lineWidth = 1.5; g.strokeStyle = "#111"; g.stroke();
    g.strokeStyle = "#111"; g.lineWidth = 2; g.lineCap = "round";
    g.beginPath(); g.moveTo(size / 2 - 5, size / 2); g.lineTo(size / 2 + 5, size / 2);
    if (!minus) { g.moveTo(size / 2, size / 2 - 5); g.lineTo(size / 2, size / 2 + 5); }
    g.stroke();
    return { width: cv.width, height: cv.height, data: g.getImageData(0, 0, cv.width, cv.height).data };
  }

  // Spazio occupato dai pannelli sopra la mappa: serve a centrare i punti nella parte visibile.
  function mapPadding(extraBottom = 0) {
    if (MOBILE()) {
      const top = $(".filters").getBoundingClientRect().bottom + 40;
      const panelTop = $("#panel").getBoundingClientRect().top;
      return { top, bottom: Math.max(60, window.innerHeight - panelTop + 20 + extraBottom), left: 30, right: 30 };
    }
    return { top: 190, bottom: 150, left: state.sidebarHidden ? 100 : 470, right: 90 };
  }

  // Zona della mappa davvero visibile (fuori da testata, giorni, filtri, elenco).
  function visibleArea() {
    const r = $("#map").getBoundingClientRect();
    const v = { left: r.left + 12, right: r.right - 12, top: r.top + 12, bottom: r.bottom - 12 };
    if (MOBILE()) {
      v.top = $(".filters").getBoundingClientRect().bottom + 10;
      v.bottom = Math.min(v.bottom, $("#panel").getBoundingClientRect().top - 10);
    } else {
      v.top = $(".days").getBoundingClientRect().bottom + 12;
      v.bottom = $(".filters").getBoundingClientRect().top - 12;
      v.left = (state.sidebarHidden ? $("#list-toggle") : $("#panel")).getBoundingClientRect().right + 12;
      v.right = $(".map-ctrl").getBoundingClientRect().left - 12;
    }
    return v;
  }

  // Sposta la mappa quanto basta perche' card aperta e segnaposto siano interi nella zona visibile.
  function ensureCardVisible(animate = true) {
    if (!popup || !mapReady) return;
    const el = popup.getElement();
    if (!el) return;
    const c = el.getBoundingClientRect(), v = visibleArea();
    const box = { left: c.left, right: c.right, top: c.top, bottom: c.bottom + 38 };   // + segnaposto sotto la card
    let dx = 0, dy = 0;
    if (box.right - box.left > v.right - v.left || box.left < v.left) dx = v.left - box.left;
    else if (box.right > v.right) dx = v.right - box.right;
    if (box.bottom - box.top > v.bottom - v.top || box.top < v.top) dy = v.top - box.top;
    else if (box.bottom > v.bottom) dy = v.bottom - box.bottom;
    if (Math.abs(dx) > 1 || Math.abs(dy) > 1) map.panBy([-dx, -dy], { duration: animate ? 380 : 0 });
  }

  function initMap() {
    const s = DATA.site;
    map = new maplibregl.Map({
      container: "map",
      style: "https://tiles.openfreemap.org/styles/positron",
      center: [s.center[1], s.center[0]],
      zoom: s.zoom - (MOBILE() ? 1 : 0),
      attributionControl: { compact: true },
      dragRotate: false, pitchWithRotate: false, touchPitch: false,
    });
    map.touchZoomRotate.disableRotation();
    $("#zoom-in").addEventListener("click", () => map.zoomIn());
    $("#zoom-out").addEventListener("click", () => map.zoomOut());
    map.once("style.load", () => {        // subito, senza aspettare tutte le tessere
      warmStyle();
      DATA.categories.forEach((c) => {
        map.addImage(`pin-${c.id}`, pinImage(c.color, false), { pixelRatio: 2 });
        map.addImage(`pin-sel-${c.id}`, pinImage(c.color, true), { pixelRatio: 2 });
      });
      map.addSource("ev", { type: "geojson", data: geojson([]), cluster: true, clusterRadius: 40, clusterMaxZoom: 13 });
      map.addLayer({ id: "clusters", type: "circle", source: "ev", filter: ["has", "point_count"],
        paint: { "circle-color": "#111", "circle-radius": ["step", ["get", "point_count"], 15, 10, 19, 40, 24],
          "circle-stroke-width": 2, "circle-stroke-color": "#f5f3ee" } });
      map.addLayer({ id: "cluster-count", type: "symbol", source: "ev", filter: ["has", "point_count"],
        layout: { "text-field": ["get", "point_count_abbreviated"], "text-size": 12, "text-font": ["Noto Sans Bold"] },
        paint: { "text-color": "#fff" } });
      const icon = (prefix) => ["concat", prefix, ["get", "category"]];
      map.addLayer({ id: "points", type: "symbol", source: "ev", filter: pointsFilter(""),
        layout: { "icon-image": icon("pin-"), "icon-allow-overlap": true, "icon-ignore-placement": true } });
      // evidenziato e selezionato vivono in sorgenti separate, non raggruppate: restano visibili sopra i gruppi
      map.addSource("hov", { type: "geojson", data: geojson([], true) });
      map.addSource("sel", { type: "geojson", data: geojson([], true) });
      map.addLayer({ id: "points-hover", type: "symbol", source: "hov",
        layout: { "icon-image": icon("pin-"), "icon-size": 1.25, "icon-allow-overlap": true, "icon-ignore-placement": true } });
      map.addLayer({ id: "points-selected", type: "symbol", source: "sel",
        layout: { "icon-image": icon("pin-sel-"), "icon-size": 1.15, "icon-allow-overlap": true, "icon-ignore-placement": true } });

      map.on("click", "clusters", (ev) => {
        const f = ev.features[0];
        map.getSource("ev").getClusterExpansionZoom(f.properties.cluster_id).then((z) =>
          map.easeTo({ center: f.geometry.coordinates, zoom: z + 0.3, padding: mapPadding() }));
      });
      map.on("click", "points", (ev) => {
        const uids = [...new Set(ev.features.map((f) => f.properties.uid))];
        if (state.detail) closeDetail({ keepHistory: true });          // altro evento: la scheda torna elenco
        if (uids.length === 1) {
          if (MOBILE()) setSheet("peek");
          select(uids[0], { fly: false, detail: false });
        } else { onlyUids = new Set(uids); closeCard(); update(); setSheet("half"); }
      });
      // "−" sul segnaposto aperto, o clic fuori: chiude la card e la sidebar torna all'elenco
      map.on("click", "points-selected", () => closeAll());
      map.on("click", (ev) => {
        if (map.queryRenderedFeatures(ev.point, { layers: ["points", "clusters", "points-selected"] }).length) return;
        if (popup || state.detail) closeAll();
        else if (MOBILE()) setSheet("peek");
      });
      // trascinare la mappa su telefono abbassa il pannello
      map.on("dragstart", () => { if (MOBILE() && !state.detail) setSheet("peek"); });
      for (const l of ["clusters", "points", "points-selected"]) {
        map.on("mouseenter", l, () => (map.getCanvas().style.cursor = "pointer"));
        map.on("mouseleave", l, () => (map.getCanvas().style.cursor = ""));
      }
      mapReady = true;
      update(true);
      if (state.selected) select(state.selected, { fly: true, detail: true, fromHistory: true });
    });
  }

  function pointsFilter(selUid) {
    return ["all", ["!", ["has", "point_count"]], ["!=", ["get", "uid"], selUid]];
  }

  function geojson(items, keepCoords) {
    if (keepCoords) {      // usa le coordinate gia' mostrate (con lo scarto anti-sovrapposizione)
      return { type: "FeatureCollection", features: items.map((e) => ({ type: "Feature",
        properties: { uid: e.uid, category: e.category }, geometry: { type: "Point", coordinates: COORDS[e.uid] || [e.lon, e.lat] } })) };
    }
    const seen = {};
    return { type: "FeatureCollection", features: items.map((e) => {
      const k = `${e.lat.toFixed(4)},${e.lon.toFixed(4)}`;
      const i = (seen[k] = (seen[k] || 0) + 1) - 1;
      const ang = i * 2.4, r = i ? 0.0007 * Math.sqrt(i) : 0;
      const coords = [e.lon + r * Math.cos(ang), e.lat + r * Math.sin(ang)];
      COORDS[e.uid] = coords;
      return { type: "Feature", properties: { uid: e.uid, category: e.category }, geometry: { type: "Point", coordinates: coords } };
    }) };
  }

  const byUid = (uid) => (uid ? EVENTS.filter((e) => e.uid === uid) : []);
  function hover(uid) {
    if (mapReady) map.getSource("hov").setData(geojson(byUid(uid), true));
  }

  // ---------------------------------------------------------------- card sulla mappa
  function showCard(e, opts = {}) {
    const c = CAT[e.category] || { color: "#ddd" };
    const el = document.createElement("div");
    el.className = "card" + (e.title.length > 60 ? " long" : "");
    el.style.setProperty("--c", c.color);
    const dist = kmText(km(e));
    el.innerHTML = `${accessBadge(e)}<h3>${esc(e.title)}</h3>
      <p>${esc(whenText(e))}</p><p>${esc([e.venue, e.town].filter(Boolean).join(", "))}${dist ? ` · ${dist}` : ""}</p>
      <button class="more" type="button">Dettagli</button>`;
    el.querySelector(".more").addEventListener("click", () => select(e.uid, { fly: false, detail: true }));
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ className: "ev-card", closeButton: false, closeOnClick: false, anchor: "bottom", offset: 22, maxWidth: "none" })
      .setLngLat(COORDS[e.uid] || [e.lon, e.lat]).setDOMContent(el).addTo(map);
    fitTitle(el.querySelector("h3"));
    markSelected(e.uid);
    if (!opts.noReveal) requestAnimationFrame(() => ensureCardVisible());
  }

  // Titoli: si va a capo tra parole intere. Solo una parola piu' larga della card viene spezzata,
  // con il trattino nel punto in cui serve (trattini morbidi, senza dizionario).
  function fitTitle(h) {
    const max = h && h.clientWidth;
    if (!max) return;
    const probe = document.createElement("span");
    probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap";
    h.appendChild(probe);
    let changed = false;
    const parts = h.textContent.replace(probe.textContent, "").split(/(\s+)/).map((w) => {
      if (!w.trim()) return w;
      probe.textContent = w;
      if (probe.getBoundingClientRect().width <= max) return w;
      changed = true;
      return [...w].join("\u00AD");
    });
    probe.remove();
    if (changed) h.textContent = parts.join("");
  }

  function markSelected(uid) {
    if (!mapReady) return;
    map.getSource("sel").setData(geojson(byUid(uid), true));
    map.setFilter("points", pointsFilter(uid || ""));
  }

  function closeCard() {
    if (popup) { popup.remove(); popup = null; }
    markSelected("");
  }

  // ---------------------------------------------------------------- selezione e cronologia
  // opts: fly (centra la mappa), detail (apre la scheda), reveal (porta il punto nella zona visibile),
  //       fromHistory (chiamata dal tasto indietro/avanti: non tocca la cronologia)
  function select(uid, opts = {}) {
    const e = uid && EVENTS.find((x) => x.uid === uid);
    if (!e) { closeDetail(); return; }
    state.selected = uid;
    if (opts.detail) {
      if (state.sidebarHidden && !MOBILE()) { state.hiddenBeforeDetail = true; setSidebar(true, { remember: false }); }
      state.detail = true;
      $("#list").hidden = true;
      $("#detail").hidden = false;
      $("#panel").classList.add("in-detail");
      renderDetail(e);
      $("#panel-body").scrollTop = 0;
      setSheet(MOBILE() ? "full" : "half");
      if (!opts.fromHistory && history.state?.uid !== uid) {
        if (pushedDetail) history.replaceState({ uid }, "", `#e=${uid}`);
        else { history.pushState({ uid }, "", `#e=${uid}`); pushedDetail = true; }
      }
    }
    if (mapReady) {
      // su telefono la scheda copre la mappa: basta il segnaposto evidenziato, senza card
      const center = COORDS[uid] || [e.lon, e.lat];
      if (MOBILE() && opts.detail) { if (popup) { popup.remove(); popup = null; } markSelected(uid); }
      else showCard(e, { noReveal: !!opts.fly || !!opts.detail });
      if (opts.fly) {
        map.flyTo({ center, zoom: Math.max(map.getZoom(), 14.2), speed: 1.4, padding: mapPadding() });
        map.once("moveend", () => ensureCardVisible());
      } else if (opts.detail && !MOBILE()) {
        requestAnimationFrame(() => ensureCardVisible());   // la sidebar puo' essere ricomparsa
      }
    }
  }

  function closeDetail(opts = {}) {
    // scheda aperta da noi: il tasto "indietro" del sito equivale a quello del telefono
    if (state.detail && !opts.fromHistory && !opts.keepHistory && pushedDetail) { history.back(); return; }
    if (opts.fromHistory || opts.keepHistory) pushedDetail = false;
    const wasDetail = state.detail;
    state.selected = null;
    state.detail = false;
    $("#list").hidden = false;
    $("#detail").hidden = true;
    $("#panel").classList.remove("in-detail");
    if (!opts.keepCard) closeCard();
    if (!opts.fromHistory && location.hash) history.replaceState(null, "", location.pathname + location.search);
    if (MOBILE() && wasDetail) setSheet("half");
    if (wasDetail && state.hiddenBeforeDetail && !MOBILE()) { state.hiddenBeforeDetail = false; setSidebar(false, { remember: false }); }
    update();
  }

  // Chiude card e scheda: la sidebar torna all'elenco degli eventi visibili.
  function closeAll() {
    if (state.detail) closeDetail();
    else { closeCard(); state.selected = null; if (location.hash) history.replaceState(null, "", location.pathname + location.search); }
  }

  // ---------------------------------------------------------------- sidebar (desktop): nascondi / mostra
  function setSidebar(visible, opts = { remember: true }) {
    state.sidebarHidden = !visible;
    document.body.classList.toggle("sidebar-hidden", !visible);
    if (opts.remember) { try { localStorage.setItem("andiamo-sidebar", visible ? "1" : "0"); } catch (_) { /* privato */ } }
    if (mapReady) setTimeout(() => { map.resize(); ensureCardVisible(); }, 30);
  }

  window.addEventListener("popstate", (ev) => {
    const uid = ev.state?.uid;
    if (uid) select(uid, { detail: true, fly: true, fromHistory: true });
    else closeDetail({ fromHistory: true });
  });

  // ---------------------------------------------------------------- pannello trascinabile (telefono)
  function setSheet(name) {
    const p = $("#panel");
    if (!MOBILE()) { p.dataset.sheet = "half"; return; }
    if (name === "half") name = "full";      // su telefono solo due posizioni: chiuso in basso o aperto del tutto
    p.dataset.sheet = name;
    p.style.removeProperty("--sheet-y");
    $("#sheet-toggle").setAttribute("aria-expanded", String(name !== "peek"));
    $("#sheet-toggle").setAttribute("aria-label", name === "peek" ? "Apri l'elenco" : "Riduci l'elenco");
  }

  function setupSheet() {
    const p = $("#panel"), head = $("#sheet-head");
    let startY = 0, startOffset = 0, lastY = 0, lastT = 0, velocity = 0, dragging = false, moved = false, fromBody = false;
    const height = () => p.getBoundingClientRect().height;
    const offsetOf = (name) => {
      const h = height(), peek = parseFloat(getComputedStyle(p).getPropertyValue("--peek")) || 76;
      return name === "full" ? 0 : name === "half" ? h * 0.45 : h - peek;
    };
    const currentOffset = () => new DOMMatrixReadOnly(getComputedStyle(p).transform).m42;

    function down(ev) {
      if (!MOBILE() || (ev.target.closest && ev.target.closest(".sort"))) return;
      fromBody = !head.contains(ev.target);
      if (fromBody && p.dataset.sheet !== "peek") return;      // a pannello aperto il contenuto scorre normalmente
      dragging = true; moved = false;
      startY = lastY = ev.clientY; lastT = performance.now(); velocity = 0;
      startOffset = currentOffset();
    }
    function move(ev) {
      if (!dragging) return;
      const dy = ev.clientY - startY;
      if (!moved && Math.abs(dy) < 6) return;
      if (!moved) { moved = true; p.classList.add("dragging"); p.setPointerCapture?.(ev.pointerId); }
      const now = performance.now();
      velocity = (ev.clientY - lastY) / Math.max(1, now - lastT);
      lastY = ev.clientY; lastT = now;
      const y = Math.min(Math.max(0, startOffset + dy), offsetOf("peek"));
      p.style.setProperty("--sheet-y", `${y}px`);
      ev.preventDefault();
    }
    function up() {
      if (!dragging) return;
      dragging = false;
      p.classList.remove("dragging");
      if (!moved) return;
      const y = currentOffset();
      // due sole posizioni: un gesto verso l'alto apre del tutto, verso il basso chiude fino in fondo
      // basta un breve trascinamento (o un colpo veloce) nella direzione voluta
      const dy = y - startOffset;
      let target;
      if (velocity > 0.25 || dy > 50) target = "peek";
      else if (velocity < -0.25 || dy < -50) target = "full";
      else target = p.dataset.sheet === "peek" ? "peek" : "full";
      setSheet(target);
    }
    p.addEventListener("pointerdown", down);
    window.addEventListener("pointermove", move, { passive: false });
    window.addEventListener("pointerup", up);
    window.addEventListener("pointercancel", up);
    $("#sheet-toggle").addEventListener("click", () => setSheet(p.dataset.sheet === "peek" ? "half" : "peek"));
    head.addEventListener("click", (ev) => {
      if (!MOBILE() || ev.target.closest(".sort, .grab") || moved) return;
      if (p.dataset.sheet === "peek") setSheet("half");
    });
    window.matchMedia("(max-width: 760px)").addEventListener("change", () => setSheet(MOBILE() ? "peek" : "half"));
  }

  // ---------------------------------------------------------------- vicino a me
  function locate() {
    const btn = $("#locate");
    if (!navigator.geolocation) { toast("Posizione non disponibile su questo dispositivo"); return; }
    btn.classList.add("busy");
    navigator.geolocation.getCurrentPosition((pos) => {
      btn.classList.remove("busy");
      btn.setAttribute("aria-pressed", "true");
      state.me = { lat: pos.coords.latitude, lon: pos.coords.longitude };
      state.sort = "distance";
      if (mapReady) {
        if (!meMarker) { const d = document.createElement("div"); d.className = "me-dot"; meMarker = new maplibregl.Marker({ element: d }); }
        meMarker.setLngLat([state.me.lon, state.me.lat]).addTo(map);
        map.flyTo({ center: [state.me.lon, state.me.lat], zoom: 11, padding: mapPadding(), speed: 1.4 });
      }
      update();
      if (MOBILE() && !state.detail) setSheet("half");
      const b = DATA.site.center, far = Math.abs(state.me.lat - b[0]) > 0.6 || Math.abs(state.me.lon - b[1]) > 0.8;
      if (far) toast("Sei fuori dalla provincia di Treviso: ordino comunque per distanza");
    }, (err) => {
      btn.classList.remove("busy");
      toast(err.code === 1 ? "Per vedere gli eventi vicini consenti l'accesso alla posizione" : "Posizione non trovata, riprova");
    }, { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 });
  }

  function toggleSort() {
    if (!state.me) { locate(); return; }
    state.sort = state.sort === "distance" ? "date" : "distance";
    update();
  }

  let toastTimer;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (t.hidden = true), 3500);
  }

  // ---------------------------------------------------------------- aggiornamento
  function update(fit) {
    let items = EVENTS.filter((e) => matches(e));
    if (onlyUids) items = items.filter((e) => onlyUids.has(e.uid));
    const from = state.from || "";
    if (state.sort === "distance" && state.me) items.sort((a, b) => km(a) - km(b));
    else {
      const key = (e) => (e.start.slice(0, 10) < from ? from : e.start.slice(0, 10)) + (timeOf(e) || "99");
      items.sort((a, b) => key(a).localeCompare(key(b)));
    }
    renderStrip();
    renderChips();
    if (!state.detail) renderList(items);
    const n = items.length;
    $("#count-label").textContent = onlyUids ? `${n} in questo punto` : `${n} ${n === 1 ? "evento" : "eventi"}`;
    $("#list-toggle-count").textContent = n;
    $("#list-toggle").setAttribute("aria-label", `Mostra l'elenco: ${n} ${n === 1 ? "evento" : "eventi"}`);
    const sortBtn = $("#sort-btn");
    sortBtn.setAttribute("aria-pressed", String(state.sort === "distance" && !!state.me));
    sortBtn.textContent = state.sort === "distance" && state.me ? "Più vicini" : state.me ? "Per data" : "Più vicini";
    $("#reset").hidden = !(state.cats.size || state.access.size || state.aud.size || state.q || onlyUids);
    if (mapReady) {
      map.getSource("ev").setData(geojson(items));
      if (fit && items.length && !state.selected) {
        const b = new maplibregl.LngLatBounds();
        items.forEach((e) => b.extend([e.lon, e.lat]));
        map.fitBounds(b, { padding: mapPadding(), maxZoom: 12, duration: 0 });
      }
    }
  }

  // ---------------------------------------------------------------- testata telefono: ricerca a scomparsa
  function setupSearch() {
    const wrap = $("#top-right"), input = $("#q"), toggle = $("#search-toggle");
    const open = (on) => {
      wrap.classList.toggle("searching", on);
      toggle.setAttribute("aria-expanded", String(on));
      toggle.setAttribute("aria-label", on ? "Chiudi la ricerca" : "Cerca");
      toggle.innerHTML = on
        ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
        : '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>';
      if (on) input.focus();
    };
    toggle.addEventListener("click", () => {
      const on = !wrap.classList.contains("searching");
      if (!on && input.value) { input.value = ""; state.q = ""; update(); }
      open(on);
    });
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") { input.blur(); if (MOBILE()) setSheet("half"); }
      if (ev.key === "Escape") { input.value = ""; state.q = ""; update(); open(false); }
    });
    let t;
    input.addEventListener("input", () => {
      clearTimeout(t);
      t = setTimeout(() => {
        state.q = input.value.trim().toLowerCase(); onlyUids = null;
        if (state.detail) closeDetail(); else update();
      }, 180);
    });
  }

  // ---------------------------------------------------------------- API sul PC (Cloudflare Tunnel)
  async function apiCall(path, body, timeoutMs = 15000) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), timeoutMs);
    try {
      const r = await fetch(API + path, body
        ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), signal: ctl.signal }
        : { signal: ctl.signal });
      const data = await r.json().catch(() => ({}));
      if (!r.ok || data.ok === false) throw Object.assign(new Error(data.messaggio || "Errore"), { code: data.errore || r.status });
      return data;
    } catch (err) {
      if (err.name === "AbortError") throw Object.assign(new Error("Il servizio non risponde: riprova tra poco."), { code: "timeout" });
      if (err.code) throw err;
      throw Object.assign(new Error("Servizio non raggiungibile in questo momento."), { code: "offline" });
    } finally { clearTimeout(t); }
  }

  async function checkApi() {
    if (!API) { apiOk = aiOk = false; return; }
    try { const r = await apiCall("/api/salute", null, 6000); apiOk = true; aiOk = !!r.ai; }
    catch (_) { apiOk = aiOk = false; }
  }

  function altLinks() {
    const s = DATA.site, out = [];
    if (s.telegram_bot) out.push(`<a class="btn-light" href="https://t.me/${attr(s.telegram_bot)}" target="_blank" rel="noopener">Telegram</a>`);
    if (s.contact_email) out.push(`<a class="btn-light" href="mailto:${attr(s.contact_email)}?subject=Nuovo%20evento">Email</a>`);
    return out.length ? `<div class="alt-links">${out.join("")}</div>` : "";
  }

  // ---------------------------------------------------------------- AGGIUNGI EVENTO
  const FIELD_NAMES = { title: "titolo", date: "data", town: "comune", time: "ora", venue: "luogo", category: "categoria" };
  const REQUIRED = ["title", "date", "town"];

  function setupAdd() {
    const dlg = $("#add-dlg"), form = $("#event-form"), submit = $("#add-submit");
    DATA.categories.forEach((c) => $("#f-category").insertAdjacentHTML("beforeend", `<option value="${c.id}">${esc(c.label)}</option>`));
    Object.entries(DATA.access).forEach(([k, v]) => { if (k !== "sconosciuto") $("#f-access").insertAdjacentHTML("beforeend", `<option value="${k}">${esc(v)}</option>`); });
    dlg.querySelectorAll("[data-close]").forEach((b) => b.addEventListener("click", () => dlg.close()));

    $("#add-btn").addEventListener("click", async () => {
      resetAdd();
      dlg.showModal();
      await checkApi();
      if (!API || !apiOk) {
        addStatus("warn", `<div><strong>La lettura automatica non è attiva in questo momento.</strong> Puoi compilare a mano${
          DATA.site.contact_email ? " e inviarci i dati per email" : ""}${altLinks() ? ", oppure scriverci:" : "."}${altLinks()}</div>`);
        setSourceEnabled(false);
      } else if (!aiOk) {
        addStatus("warn", "La lettura automatica è momentaneamente spenta: compila i campi a mano.");
        setSourceEnabled(false);
      }
    });

    $("#url-form").addEventListener("submit", (ev) => {
      ev.preventDefault();
      const url = $("#ev-link").value.trim();
      if (!/^https?:\/\//i.test(url)) { addStatus("err", "Incolla un link completo, che inizi con https://"); return; }
      extract({ url }, "Sto leggendo la pagina dell'evento…");
    });

    const drop = $("#drop"), input = $("#ev-image");
    input.addEventListener("change", () => input.files[0] && useImage(input.files[0]));
    drop.addEventListener("dragover", (ev) => { ev.preventDefault(); drop.classList.add("over"); });
    drop.addEventListener("dragleave", () => drop.classList.remove("over"));
    drop.addEventListener("drop", (ev) => {
      ev.preventDefault(); drop.classList.remove("over");
      const f = ev.dataTransfer.files[0];
      if (f && f.type.startsWith("image/")) useImage(f);
    });
    // incolla uno screenshot direttamente (Cmd/Ctrl+V)
    dlg.addEventListener("paste", (ev) => {
      const item = [...(ev.clipboardData?.items || [])].find((i) => i.type.startsWith("image/"));
      if (item && !$("#drop").classList.contains("disabled")) { ev.preventDefault(); useImage(item.getAsFile()); }
    });

    $("#manual-btn").addEventListener("click", () => { showForm({}, null); $("#f-title").focus(); });
    form.addEventListener("input", (ev) => {
      const field = ev.target.closest(".field");
      if (field) {
        field.classList.remove("ai");
        if (ev.target.value.trim()) field.classList.remove("missing", "todo");
      }
      validate();
    });
    submit.addEventListener("click", sendEvent);
    $("#add-again").addEventListener("click", () => { resetAdd(); if (API && apiOk && aiOk) setSourceEnabled(true); });
  }

  function setSourceEnabled(on) {
    $("#ev-link").disabled = !on; $("#url-go").disabled = !on; $("#ev-image").disabled = !on;
    $("#drop").classList.toggle("disabled", !on);
    $("#drop").style.opacity = on ? "" : ".45";
  }

  function addStatus(kind, html) {
    const s = $("#add-status");
    s.className = "status " + (kind || "");
    s.innerHTML = kind === "busy" ? `<span class="spinner" aria-hidden="true"></span><div>${html}</div>` : html;
    s.hidden = false;
  }

  function resetAdd() {
    $("#add-step-source").hidden = false;
    $("#event-form").hidden = true; $("#event-form").reset();
    $("#add-done").hidden = true; $("#add-status").hidden = true;
    $("#add-submit").hidden = false; $("#add-submit").disabled = true; $("#add-submit").textContent = "Invia evento";
    $("#add-again").hidden = true; $("#add-hint").hidden = false;
    $("#ev-link").value = "";
    $("#drop-title").textContent = "Carica screenshot o locandina";
    $("#drop-sub").textContent = "Anche lo screenshot di un post Instagram o Facebook";
    $("#drop-ico").innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/></svg>';
    document.querySelectorAll("#event-form .field").forEach((f) => f.classList.remove("ai", "missing", "todo"));
    setSourceEnabled(true);
  }

  // Riduce l'immagine (max 1600 px) prima dell'invio: piu' veloce anche da rete mobile.
  function shrinkImage(file) {
    return new Promise((resolve, reject) => {
      const img = new Image(), url = URL.createObjectURL(file);
      img.onload = () => {
        const k = Math.min(1, 1600 / Math.max(img.width, img.height));
        const cv = document.createElement("canvas");
        cv.width = Math.round(img.width * k); cv.height = Math.round(img.height * k);
        cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
        URL.revokeObjectURL(url);
        resolve(cv.toDataURL("image/jpeg", 0.85));
      };
      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("Immagine non leggibile")); };
      img.src = url;
    });
  }

  async function useImage(file) {
    let data;
    try { data = await shrinkImage(file); } catch (_) { addStatus("err", "Non riesco ad aprire questa immagine. Prova con un JPG o PNG."); return; }
    $("#drop-ico").innerHTML = `<img src="${data}" alt="">`;
    $("#drop-title").textContent = file.name || "Immagine incollata";
    $("#drop-sub").textContent = "Tocca per cambiare immagine";
    extract({ immagine: data }, "Sto leggendo la locandina… può volerci qualche secondo.");
  }

  async function extract(payload, busyText) {
    setSourceEnabled(false);
    addStatus("busy", busyText);
    try {
      const r = await apiCall("/api/estrai", payload, 120000);
      const ev = r.eventi[0];
      showForm(ev, r.mancanti);
      const filled = Object.values(ev).filter((v) => v).length;
      const req = r.mancanti.required.map((f) => FIELD_NAMES[f] || f);
      let msg = `<div><strong>Ho compilato ${filled} campi.</strong> Controlla i dati evidenziati`;
      msg += req.length ? ` e completa quelli che mancano: <strong>${esc(req.join(", "))}</strong>.` : " e invia.";
      if (r.eventi.length > 1) msg += ` Ho trovato ${r.eventi.length} eventi: ho compilato il primo.`;
      addStatus(req.length ? "warn" : "ok", msg + "</div>");
    } catch (err) {
      addStatus("err", `<div><strong>${esc(err.message)}</strong></div>`);
      showForm(payload.url && err.code !== "social" ? { official_url: payload.url } : {}, null);
    } finally {
      setSourceEnabled(true);
    }
  }

  // Riempie il modulo; i campi arrivati dall'AI si colorano, i mancanti si segnalano.
  function showForm(values, mancanti) {
    const form = $("#event-form");
    form.hidden = false;
    form.querySelectorAll(".field[data-f]").forEach((field) => {
      const name = field.dataset.f, input = field.querySelector("input, select, textarea");
      const v = values[name] || "";
      if (v || !mancanti) input.value = v;
      field.classList.toggle("ai", !!(v && mancanti));
      field.classList.remove("missing", "todo");
      const badge = field.querySelector(".field-badge");
      if (mancanti && mancanti.required.includes(name)) { field.classList.add("missing"); if (badge) badge.textContent = "Mancante"; }
      else if (mancanti && mancanti.recommended.includes(name)) { field.classList.add("todo"); if (badge) badge.textContent = "Da completare"; }
    });
    $("#form-legend").hidden = !mancanti;
    validate();
    const firstMissing = form.querySelector(".field.missing input");
    (firstMissing || form).scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function formData() {
    const out = {};
    new FormData($("#event-form")).forEach((v, k) => (out[k] = String(v).trim()));
    return out;
  }

  function validate() {
    const d = formData();
    const ok = !$("#event-form").hidden && REQUIRED.every((k) => d[k]);
    $("#add-submit").disabled = !ok;
    $("#add-submit").textContent = (!API || !apiOk) && DATA.site.contact_email ? "Invia per email" : "Invia evento";
    return ok;
  }

  async function sendEvent() {
    const d = formData();
    const missingReq = REQUIRED.filter((k) => !d[k]);
    if (missingReq.length) {
      missingReq.forEach((k) => { const f = document.querySelector(`.field[data-f="${k}"]`); f.classList.add("missing"); f.querySelector(".field-badge").textContent = "Mancante"; });
      return;
    }
    if (!API || !apiOk) {              // servizio spento: email precompilata
      if (!DATA.site.contact_email) { addStatus("err", "L'invio non è disponibile in questo momento. Riprova più tardi."); return; }
      const body = Object.entries(d).filter(([k, v]) => v && k !== "website").map(([k, v]) => `${k}: ${v}`).join("\n");
      location.href = `mailto:${DATA.site.contact_email}?subject=${encodeURIComponent("Nuovo evento: " + d.title)}&body=${encodeURIComponent(body)}`;
      return;
    }
    const btn = $("#add-submit");
    btn.disabled = true; btn.textContent = "Invio…";
    try {
      await apiCall("/api/invia", d, 60000);
      $("#add-step-source").hidden = true; $("#event-form").hidden = true; $("#add-done").hidden = false;
      btn.hidden = true; $("#add-again").hidden = false; $("#add-hint").hidden = true;
      $("#add-body").scrollTop = 0;
    } catch (err) {
      addStatus("err", `<div><strong>Invio non riuscito.</strong> ${esc(err.message)}</div>`);
      $("#add-step-source").hidden = false;
      $("#add-status").scrollIntoView({ behavior: "smooth", block: "nearest" });
      validate();
    }
  }

  // ---------------------------------------------------------------- SEGNALA MODIFICA / RIMOZIONE
  let reportEvent = null;
  function setupReport() {
    const dlg = $("#report-dlg");
    dlg.querySelectorAll("[data-close]").forEach((b) => b.addEventListener("click", () => dlg.close()));
    $("#report-submit").addEventListener("click", sendReport);
  }

  function openReport(e) {
    reportEvent = e;
    $("#report-form").reset();
    $("#report-status").hidden = true;
    $("#report-submit").disabled = false;
    $("#report-event").textContent = e.title;
    $("#report-dlg").showModal();
    checkApi();
  }

  async function sendReport() {
    const st = $("#report-status");
    const show = (kind, html) => { st.className = "status " + kind; st.innerHTML = html; st.hidden = false; };
    const fd = new FormData($("#report-form"));
    const data = { uid: reportEvent.uid, tipo: fd.get("tipo"), messaggio: String(fd.get("messaggio") || "").trim(),
      contatto: String(fd.get("contatto") || "").trim(), website: String(fd.get("website") || "") };
    if (data.messaggio.length < 5) { show("err", "Scrivi in breve cosa va corretto o perché rimuoverlo."); $("#r-msg").focus(); return; }
    if (!API || !apiOk) {
      if (DATA.site.contact_email) {
        const subj = `${data.tipo === "rimozione" ? "Rimozione" : "Correzione"} evento ${reportEvent.uid}`;
        location.href = `mailto:${DATA.site.contact_email}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(`Evento: ${reportEvent.title}\n\n${data.messaggio}`)}`;
      } else show("err", "Il servizio di segnalazione non è attivo in questo momento. Riprova più tardi.");
      return;
    }
    $("#report-submit").disabled = true;
    try {
      await apiCall("/api/segnala", data);
      show("ok", "<strong>Grazie, la controlliamo al più presto.</strong>");
      setTimeout(() => $("#report-dlg").close(), 1600);
    } catch (err) {
      show("err", esc(err.message));
      $("#report-submit").disabled = false;
    }
  }

  // ---------------------------------------------------------------- utilità
  function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function attr(s) { const v = String(s || "#"); return /^(https?:|mailto:)/.test(v) ? esc(v) : "#"; }
  function ics(s) { return String(s || "").replace(/[\\;,]/g, (c) => "\\" + c).replace(/\n/g, "\\n"); }

  // ---------------------------------------------------------------- avvio
  async function start() {
    try {
      DATA = await (await fetch("data/events.json", { cache: "no-cache" })).json();
    } catch (err) {
      $("#count-label").textContent = "non disponibili";
      $("#list").innerHTML = `<li class="empty-state"><strong>Non riesco a caricare gli eventi.</strong>Ricarica la pagina tra qualche minuto.</li>`;
      return;
    }
    EVENTS = DATA.events.filter((e) => e.start && e.lat != null);
    DATA.categories.forEach((c) => (CAT[c.id] = c));
    if (DATA.site.title) { $("#site-title").textContent = DATA.site.title; document.title = DATA.site.title; }
    const g = new Date(DATA.generated);
    $("#updated").textContent = `Aggiornato il ${g.getDate()} ${MONTHS[g.getMonth()]} alle ${pad(g.getHours())}:${pad(g.getMinutes())}.`;
    API = (DATA.site.api_url || "").replace(/\/$/, "");
    if (DATA.site.days_ahead) STRIP_DAYS = DATA.site.days_ahead;
    setupAdd();
    setupReport();
    setupSearch();
    setupScrollNav("#strip");
    setupScrollNav("#chips");
    setupFilters();
    // barre dei giorni e dei filtri a tutta larghezza: l'elenco (desktop) sta nello spazio tra le due;
    // su telefono i filtri partono sotto la barra dei giorni
    const placePanels = () => {
      const root = document.documentElement.style, gap = MOBILE() ? 8 : 12;
      root.setProperty("--below-days", `${Math.round($(".days").getBoundingClientRect().bottom + gap)}px`);
      if (!MOBILE()) root.setProperty("--above-filters", `${Math.round(window.innerHeight - $(".filters").getBoundingClientRect().top + gap)}px`);
    };
    placePanels();
    window.addEventListener("resize", placePanels);
    if (window.ResizeObserver) { const ro = new ResizeObserver(placePanels); ro.observe($(".days")); ro.observe($(".filters")); }
    if (document.fonts) document.fonts.ready.then(placePanels);
    $("#panel-hide").addEventListener("click", () => setSidebar(false));
    $("#list-toggle").addEventListener("click", () => setSidebar(true));
    try { if (localStorage.getItem("andiamo-sidebar") === "0" && !MOBILE()) setSidebar(false, { remember: false }); } catch (_) { /* privato */ }
    setupSheet();
    setSheet(MOBILE() ? "peek" : "half");

    setPreset("all");
    document.querySelectorAll(".presets button").forEach((b) =>
      b.addEventListener("click", () => { setPreset(b.dataset.preset); onlyUids = null; update(); }));
    $("#reset").addEventListener("click", () => {
      state.cats.clear(); state.aud.clear(); state.access.clear(); state.q = ""; onlyUids = null;
      $("#q").value = "";
      setPreset("all"); closeDetail(); update(true);
    });
    $("#more-filters").addEventListener("click", (ev) => {
      const open = $(".filters").classList.toggle("expanded");
      if (open && MOBILE()) setSheet("peek");          // il pannello eventi non deve coprire i filtri
      ev.currentTarget.setAttribute("aria-expanded", String(open));
    });
    $("#locate").addEventListener("click", locate);
    $("#sort-btn").addEventListener("click", toggleSort);
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && state.detail) closeDetail(); });

    const m = location.hash.match(/e=([0-9a-f]+)/);
    if (m && EVENTS.some((e) => e.uid === m[1])) {
      state.selected = m[1];
      history.replaceState({ uid: m[1] }, "", `#e=${m[1]}`);
    }
    update();
    if (state.selected) select(state.selected, { detail: true, fromHistory: true });   // scheda subito, mappa dopo
    initMap();
  }

  // accesso di sola lettura per test e debug dalla console
  window.andiamo = { map: () => map, coords: (uid) => COORDS[uid], events: () => EVENTS };

  start();
})();
