/* Andiamoo: legge data/events.json, filtra per giorni/categorie/accesso/pubblico/luogo/testo,
   mostra mappa (segnaposti colorati con "+", card sulla mappa) ed elenco con scheda.
   Su telefono l'elenco e' un pannello trascinabile (anteprima / meta' / pieno). */
(() => {
  "use strict";

  const $ = (s) => document.querySelector(s);
  const DOW = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];
  const DAYS = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"];
  const MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
    "settembre", "ottobre", "novembre", "dicembre"];
  const STRIP_DAYS = 45;
  const MOBILE = () => window.matchMedia("(max-width: 760px)").matches;

  const state = {
    from: null, to: null, preset: "all", cats: new Set(), access: "", audience: "", setting: "", q: "",
    selected: null, detail: false, sort: "date", me: null,
  };
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

  // ---------------------------------------------------------------- filtri
  function matches(e, skip = {}) {
    if (!skip.date && !spans(e, state.from, state.to)) return false;
    if (!skip.cat && state.cats.size && !state.cats.has(e.category)) return false;
    if (state.access && e.access !== state.access) return false;
    if (state.audience && !(e.audience || []).includes(state.audience)) return false;
    if (state.setting && e.setting !== state.setting) return false;
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
    strip.innerHTML = "";
    counts.forEach((n, i) => {
      const d = addDays(t, i), key = iso(d), first = d.getDate() === 1 && i > 0;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "day" + (d.getDay() === 0 || d.getDay() === 6 ? " weekend" : "") + (n ? "" : " empty") + (first ? " month-start" : "");
      if (first) b.dataset.month = MONTHS[d.getMonth()].slice(0, 3);
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
      strip.appendChild(b);
    });
    document.querySelectorAll(".presets button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.preset === state.preset)));
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
    const extra = [state.access, state.audience, state.setting].filter(Boolean).length;
    $("#more-filters").innerHTML = extra ? `Filtri <span class="badge">${extra}</span>` : "Filtri";
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
    const who = [...(e.audience || []).map((a) => DATA.audiences[a]), DATA.settings[e.setting]].filter(Boolean).join(", ");
    const accessLabel = e.access !== "sconosciuto" ? DATA.access[e.access] : "";
    const host = e.action_url ? new URL(e.action_url).hostname.replace(/^www\./, "") : "";
    const also = (e.also_on || []).filter((a) => a.url);
    const dist = kmText(km(e));
    el.innerHTML = `
      <button class="text-btn back" type="button">← Tutti gli eventi</button><br>
      <span class="cat" style="--c:${c.color}">${esc(c.label)}${sub ? ` · ${esc(sub)}` : ""}</span>
      <h2>${esc(e.title)}</h2>
      <dl class="facts">
        <dt>Quando</dt><dd>${esc(whenText(e))}</dd>
        ${place ? `<dt>Dove</dt><dd>${esc(place)}${e.geo_precision === "town" ? " <small>(posizione indicativa)</small>" : ""}${dist ? ` · ${dist} da te` : ""}</dd>` : ""}
        ${accessLabel || e.price ? `<dt>Ingresso</dt><dd>${esc([accessLabel, e.price].filter(Boolean).join(" · "))}</dd>` : ""}
        ${who ? `<dt>Per chi</dt><dd>${esc(who)}</dd>` : ""}
      </dl>
      ${e.summary ? `<p class="summary">${esc(e.summary)}</p>` : ""}
      <p class="official-note">${e.ai_summary ? "Dettagli riassunti tramite AI. " : ""}Per il programma ufficiale e le iscrizioni, visita il sito ufficiale${host ? ` (${esc(host)})` : ""}.</p>
      <p class="also">Fonte: <a href="${attr(e.source_url)}" target="_blank" rel="noopener">${esc(e.source_name)}</a>${
        also.length ? `. Anche su: ${also.map((a) => `<a href="${attr(a.url)}" target="_blank" rel="noopener">${esc(a.source)}</a>`).join(", ")}` : ""}</p>
      <p class="small-print">Dati non corretti o evento da rimuovere? ${removalLink(e)}</p>
      <div class="detail-actions">
        <a class="cta" href="${attr(e.action_url)}" target="_blank" rel="noopener"><span>Sito ufficiale</span><i aria-hidden="true">↗</i></a>
        <button class="round" type="button" data-ics aria-label="Aggiungi al calendario" title="Aggiungi al calendario">
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg></button>
        <a class="round" target="_blank" rel="noopener" aria-label="Indicazioni stradali" title="Indicazioni"
           href="https://www.google.com/maps/dir/?api=1&destination=${e.lat},${e.lon}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
        <button class="round" type="button" data-share aria-label="Condividi" title="Condividi">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3M7.5 7.5 12 3l4.5 4.5M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg></button>
      </div>`;
    el.querySelector(".back").addEventListener("click", closeDetail);
    el.querySelector("[data-ics]").addEventListener("click", () => downloadIcs(e));
    el.querySelector("[data-share]").addEventListener("click", () => share(e));
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

  function removalLink(e) {
    const mail = DATA.site.contact_email;
    if (!mail) return "Usa il pulsante Segnala.";
    const subject = encodeURIComponent(`Correzione/rimozione evento ${e.uid}`);
    const body = encodeURIComponent(`Evento: ${e.title}\nLink: ${location.href.split("#")[0]}#e=${e.uid}\n\nRichiesta: `);
    return `<a href="mailto:${attr(mail)}?subject=${subject}&body=${body}">Scrivici</a>.`;
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
    return { top: 170, bottom: 150, left: 470, right: 90 };
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
    map.on("load", () => {
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
        if (uids.length === 1) {
          if (MOBILE()) setSheet("peek");
          select(uids[0], { fly: false, detail: false, reveal: true });
        } else { onlyUids = new Set(uids); closeDetail(); setSheet("half"); }
      });
      map.on("click", (ev) => {
        if (map.queryRenderedFeatures(ev.point, { layers: ["points", "clusters"] }).length) return;
        if (popup) closeCard();
        if (MOBILE() && !state.detail) setSheet("peek");
      });
      // trascinare la mappa su telefono abbassa il pannello
      map.on("dragstart", () => { if (MOBILE() && !state.detail) setSheet("peek"); });
      for (const l of ["clusters", "points"]) {
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
  function showCard(e) {
    const c = CAT[e.category] || { color: "#ddd" };
    const el = document.createElement("div");
    el.className = "card";
    el.style.setProperty("--c", c.color);
    const dist = kmText(km(e));
    el.innerHTML = `<h3>${esc(e.title)}</h3>
      <p>${esc(whenText(e))}</p><p>${esc([e.venue, e.town].filter(Boolean).join(", "))}${dist ? ` · ${dist}` : ""}</p>
      <button class="more" type="button">Dettagli</button>`;
    el.querySelector(".more").addEventListener("click", () => select(e.uid, { fly: false, detail: true }));
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ className: "ev-card", closeButton: false, closeOnClick: false, anchor: "bottom", offset: 22, maxWidth: "none" })
      .setLngLat(COORDS[e.uid] || [e.lon, e.lat]).setDOMContent(el).addTo(map);
    markSelected(e.uid);
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
      if (MOBILE() && opts.detail) { if (popup) { popup.remove(); popup = null; } markSelected(uid); }
      else showCard(e);
      const center = COORDS[uid] || [e.lon, e.lat];
      if (popup && opts.fly) popup.setLngLat(center);
      if (opts.fly) map.flyTo({ center, zoom: Math.max(map.getZoom(), 14.2), speed: 1.4, padding: mapPadding() });
      else if (opts.reveal) map.easeTo({ center, padding: mapPadding(180), duration: 400 });
    }
  }

  function closeDetail(opts = {}) {
    // scheda aperta da noi: il tasto "indietro" del sito equivale a quello del telefono
    if (state.detail && !opts.fromHistory && pushedDetail) { history.back(); return; }
    if (opts.fromHistory) pushedDetail = false;
    const wasDetail = state.detail;
    state.selected = null;
    state.detail = false;
    $("#list").hidden = false;
    $("#detail").hidden = true;
    $("#panel").classList.remove("in-detail");
    closeCard();
    if (!opts.fromHistory && location.hash) history.replaceState(null, "", location.pathname + location.search);
    if (MOBILE() && wasDetail) setSheet("half");
    update();
  }

  window.addEventListener("popstate", (ev) => {
    const uid = ev.state?.uid;
    if (uid) select(uid, { detail: true, fly: true, fromHistory: true });
    else closeDetail({ fromHistory: true });
  });

  // ---------------------------------------------------------------- pannello trascinabile (telefono)
  const SHEETS = ["peek", "half", "full"];
  function setSheet(name) {
    const p = $("#panel");
    if (!MOBILE()) { p.dataset.sheet = "half"; return; }
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
      let target;
      if (velocity > 0.5) target = y > offsetOf("half") ? "peek" : "half";
      else if (velocity < -0.5) target = y < offsetOf("half") ? "full" : "half";
      else target = SHEETS.reduce((a, b) => (Math.abs(offsetOf(b) - y) < Math.abs(offsetOf(a) - y) ? b : a));
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
    const sortBtn = $("#sort-btn");
    sortBtn.setAttribute("aria-pressed", String(state.sort === "distance" && !!state.me));
    sortBtn.textContent = state.sort === "distance" && state.me ? "Più vicini" : state.me ? "Per data" : "Più vicini";
    $("#reset").hidden = !(state.cats.size || state.access || state.audience || state.setting || state.q || onlyUids);
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

  // ---------------------------------------------------------------- segnalazioni
  function setupReport() {
    const s = DATA.site, ul = $("#report-options"), opts = [];
    if (s.telegram_bot) opts.push([`https://t.me/${s.telegram_bot}`, "Con Telegram", "Manda la foto della locandina o il link: ci pensa il bot."]);
    if (s.form_url) opts.push([s.form_url, "Con il modulo", "Per organizzatori: titolo, data, luogo e link."]);
    if (s.contact_email) opts.push([`mailto:${s.contact_email}?subject=Segnalazione%20evento`, "Per email", s.contact_email]);
    ul.innerHTML = opts.length
      ? opts.map(([h, t, d]) => `<li><a href="${attr(h)}" target="_blank" rel="noopener"><strong>${esc(t)}</strong><span>${esc(d)}</span></a></li>`).join("")
      : "<li>Le segnalazioni apriranno a breve.</li>";
    $("#report-btn").addEventListener("click", () => $("#report").showModal());
    $("#removal").innerHTML = s.contact_email
      ? `Organizzi un evento e vuoi correggerlo o toglierlo? <a href="mailto:${attr(s.contact_email)}">Scrivici</a>.` : "";
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
    const fill = (sel, obj) => Object.entries(obj || {}).forEach(([k, v]) => {
      if (k !== "sconosciuto") $(sel).insertAdjacentHTML("beforeend", `<option value="${k}">${esc(v)}</option>`);
    });
    fill("#access", DATA.access);
    fill("#audience", DATA.audiences);
    fill("#setting", DATA.settings);
    const g = new Date(DATA.generated);
    $("#updated").textContent = `Aggiornato il ${g.getDate()} ${MONTHS[g.getMonth()]} alle ${pad(g.getHours())}:${pad(g.getMinutes())}.`;
    setupReport();
    setupSearch();
    setupSheet();
    setSheet(MOBILE() ? "peek" : "half");

    setPreset("all");
    document.querySelectorAll(".presets button").forEach((b) =>
      b.addEventListener("click", () => { setPreset(b.dataset.preset); onlyUids = null; update(); }));
    for (const k of ["access", "audience", "setting"]) {
      $("#" + k).addEventListener("change", (ev) => { state[k] = ev.target.value; onlyUids = null; update(); });
    }
    $("#reset").addEventListener("click", () => {
      state.cats.clear(); state.access = state.audience = state.setting = state.q = ""; onlyUids = null;
      for (const k of ["q", "access", "audience", "setting"]) $("#" + k).value = "";
      setPreset("all"); closeDetail(); update(true);
    });
    $("#more-filters").addEventListener("click", (ev) => {
      const open = $(".filters").classList.toggle("expanded");
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
    initMap();
  }

  start();
})();
