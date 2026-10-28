/* Mappa eventi: legge data/events.json, filtra per giorni/categorie/accesso/testo, mostra mappa ed elenco. */
(() => {
  "use strict";

  const $ = (s) => document.querySelector(s);
  const DOW = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];
  const MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
    "settembre", "ottobre", "novembre", "dicembre"];
  const STRIP_DAYS = 45;

  const state = { from: null, to: null, preset: "all", cats: new Set(), access: "", audience: "", setting: "", q: "", selected: null };
  let DATA = null, EVENTS = [], CAT = {}, map = null, mapReady = false;

  // ---------------------------------------------------------------- date
  const pad = (n) => String(n).padStart(2, "0");
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseDay = (s) => { const [y, m, d] = s.slice(0, 10).split("-").map(Number); return new Date(y, m - 1, d); };
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const today = () => { const t = new Date(); t.setHours(0, 0, 0, 0); return t; };
  const timeOf = (e) => (e.start && e.start.length > 10 ? e.start.slice(11, 16) : "");
  const dayLabel = (d) => {
    const diff = Math.round((d - today()) / 86400000);
    const base = `${["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"][d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`;
    return diff === 0 ? `Oggi, ${base}` : diff === 1 ? `Domani, ${base}` : base[0].toUpperCase() + base.slice(1);
  };
  const shortDate = (s) => { const d = parseDay(s); return `${d.getDate()} ${MONTHS[d.getMonth()].slice(0, 3)}`; };

  // Un evento e' "attivo" in un giorno se il giorno cade tra inizio e fine.
  const spans = (e, from, to) => {
    const s = e.start.slice(0, 10), en = (e.end || e.start).slice(0, 10);
    return (!to || s <= to) && (!from || en >= from);
  };

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
      const dow = t.getDay();                          // 0 dom ... 6 sab
      const fri = dow === 0 ? addDays(t, -2) : addDays(t, (5 - dow + 7) % 7);
      const start = dow === 6 || dow === 0 ? t : fri;
      state.from = iso(start); state.to = iso(dow === 0 ? t : addDays(fri, 2));
    } else { state.from = iso(t); state.to = null; }
  }

  // ---------------------------------------------------------------- render: striscia giorni
  function renderStrip() {
    const strip = $("#strip");
    const t = today();
    const base = EVENTS.filter((e) => matches(e, { date: true }));
    const counts = [];
    for (let i = 0; i < STRIP_DAYS; i++) {
      const d = iso(addDays(t, i));
      counts.push(base.filter((e) => spans(e, d, d)).length);
    }
    const max = Math.max(1, ...counts);
    strip.innerHTML = "";
    counts.forEach((n, i) => {
      const d = addDays(t, i), key = iso(d);
      const b = document.createElement("button");
      b.type = "button";
      b.className = "day" + (d.getDay() === 0 || d.getDay() === 6 ? " weekend" : "") + (n ? "" : " empty")
        + (d.getDate() === 1 && i > 0 ? " month-start" : "");
      if (d.getDate() === 1 && i > 0) b.dataset.month = MONTHS[d.getMonth()].slice(0, 3);
      const selected = state.from && key >= state.from && (state.to ? key <= state.to : state.preset !== "all");
      b.setAttribute("aria-pressed", String(!!selected && state.preset !== "all"));
      b.setAttribute("aria-label", `${dayLabel(d)}: ${n} eventi`);
      b.innerHTML = `<span class="bar-wrap"><span class="bar" style="height:${Math.round((n / max) * 40) + 2}px"></span></span>
        <span class="dow">${i === 0 ? "oggi" : DOW[d.getDay()]}</span><span class="num">${d.getDate()}</span>`;
      b.addEventListener("click", () => {
        if (state.preset === "day" && state.from === key) { setPreset("all"); }
        else { state.preset = "day"; state.from = state.to = key; }
        update();
      });
      strip.appendChild(b);
    });
    document.querySelectorAll(".presets button").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.preset === state.preset)));
  }

  // ---------------------------------------------------------------- render: categorie
  function renderChips() {
    const box = $("#chips");
    const base = EVENTS.filter((e) => matches(e, { cat: true }));
    box.innerHTML = "";
    DATA.categories.forEach((c) => {
      const n = base.filter((e) => e.category === c.id).length;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      b.style.setProperty("--c", c.color);
      b.setAttribute("aria-pressed", String(state.cats.has(c.id)));
      b.disabled = n === 0 && !state.cats.has(c.id);
      b.innerHTML = `<span class="dot"></span>${c.label} <span class="n">${n}</span>`;
      b.addEventListener("click", () => {
        state.cats.has(c.id) ? state.cats.delete(c.id) : state.cats.add(c.id);
        update();
      });
      box.appendChild(b);
    });
  }

  // ---------------------------------------------------------------- render: elenco
  function renderList(items) {
    const list = $("#list");
    list.innerHTML = "";
    if (!items.length) {
      list.innerHTML = `<li class="empty-state"><strong>Nessun evento con questi filtri.</strong>
        Prova un altro giorno o togli qualche categoria.</li>`;
      return;
    }
    let lastGroup = "";
    const from = state.from || iso(today());
    items.forEach((e) => {
      // eventi lunghi iniziati prima del periodo scelto: raggruppati nel primo giorno del periodo
      const groupDay = e.start.slice(0, 10) < from ? from : e.start.slice(0, 10);
      if (groupDay !== lastGroup) {
        lastGroup = groupDay;
        const g = document.createElement("li");
        g.className = "group";
        g.textContent = dayLabel(parseDay(groupDay));
        list.appendChild(g);
      }
      const c = CAT[e.category] || {};
      const li = document.createElement("li");
      li.className = "item";
      const longRun = e.end && e.end.slice(0, 10) !== e.start.slice(0, 10);
      const when = timeOf(e) || (longRun ? "fino al" : "tutto il giorno");
      li.innerHTML = `<button type="button" data-uid="${e.uid}">
          <span class="when">${esc(when)}${longRun ? `<small>${shortDate(e.end)}</small>` : ""}</span>
          <span><h3>${esc(e.title)}</h3>
          <span class="meta" style="--c:${c.color}"><span class="dot"></span>${esc([e.venue, e.town].filter(Boolean).join(", "))}</span></span>
        </button>`;
      li.querySelector("button").addEventListener("click", () => select(e.uid, true));
      li.querySelector("button").addEventListener("mouseenter", () => highlight(e.uid));
      list.appendChild(li);
    });
  }

  // ---------------------------------------------------------------- render: scheda
  function renderDetail(e) {
    const el = $("#detail");
    const c = CAT[e.category] || { label: "Evento", color: "#000" };
    const sub = (c.sub || {})[e.subcategory];
    const d = parseDay(e.start);
    let when = dayLabel(d);
    if (timeOf(e)) when += `, ore ${timeOf(e)}`;
    if (e.end && e.end.slice(0, 10) !== e.start.slice(0, 10)) when += ` fino a ${dayLabel(parseDay(e.end)).toLowerCase()}`;
    const place = [e.venue, e.address, e.town].filter(Boolean).join(", ");
    const accessLabel = DATA.access[e.access] || "";
    const aiNote = e.ai_summary ? "Dettagli riassunti tramite AI. " : "";
    const official = e.action_url;
    const host = official ? new URL(official).hostname.replace(/^www\./, "") : "";
    const also = (e.also_on || []).filter((a) => a.url);
    const geoNote = e.geo_precision === "town" ? " (posizione indicativa: centro del comune)" : "";
    el.innerHTML = `
      <button class="link back" type="button">Torna all'elenco</button>
      <div class="cat" style="--c:${c.color}"><span class="dot"></span>${esc(c.label)}${sub ? ` / ${esc(sub)}` : ""}</div>
      <h2>${esc(e.title)}</h2>
      <dl class="facts">
        <dt aria-label="Quando">📅</dt><dd>${esc(when)}</dd>
        ${place ? `<dt aria-label="Dove">📍</dt><dd>${esc(place)}${geoNote}</dd>` : ""}
        ${(e.audience || []).length || e.setting ? `<dt aria-label="Per chi">👥</dt><dd>${esc([...(e.audience || []).map((a) => DATA.audiences[a]), DATA.settings[e.setting]].filter(Boolean).join(", "))}</dd>` : ""}
        ${accessLabel ? `<dt aria-label="Accesso">🎟️</dt><dd><span class="badge ${e.access}">${esc(accessLabel)}</span>${e.price ? ` ${esc(e.price)}` : ""}</dd>` : ""}
      </dl>
      ${e.summary ? `<p class="summary">${esc(e.summary)}</p>` : ""}
      <div class="official">
        <p>${aiNote}Per il programma ufficiale e le iscrizioni, visita il sito ufficiale${host ? ` (${esc(host)})` : ""}.</p>
        <a class="btn" href="${attr(official)}" target="_blank" rel="noopener">Apri il sito ufficiale</a>
      </div>
      <div class="actions">
        <button class="btn btn-ghost" type="button" data-ics>Aggiungi al calendario</button>
        <a class="btn btn-ghost" target="_blank" rel="noopener"
           href="https://www.google.com/maps/dir/?api=1&destination=${e.lat},${e.lon}">Indicazioni</a>
      </div>
      <p class="also">Fonte: <a href="${attr(e.source_url)}" target="_blank" rel="noopener">${esc(e.source_name)}</a>${
        also.length ? `. Anche su: ${also.map((a) => `<a href="${attr(a.url)}" target="_blank" rel="noopener">${esc(a.source)}</a>`).join(", ")}` : ""}</p>
      <p class="small-print">Dati non corretti o evento da rimuovere? ${removalLink(e)}</p>`;
    el.querySelector(".back").addEventListener("click", () => select(null));
    el.querySelector("[data-ics]").addEventListener("click", () => downloadIcs(e));
  }

  function removalLink(e) {
    const mail = DATA.site.contact_email;
    if (!mail) return "Scrivici dalla pagina di segnalazione.";
    const subject = encodeURIComponent(`Correzione/rimozione evento ${e.uid}`);
    const body = encodeURIComponent(`Evento: ${e.title}\nLink: ${location.href.split("#")[0]}#e=${e.uid}\n\nRichiesta: `);
    return `<a href="mailto:${attr(mail)}?subject=${subject}&body=${body}">Scrivici</a>.`;
  }

  // ---------------------------------------------------------------- calendario (.ics)
  function downloadIcs(e) {
    const dt = (s, end) => {
      if (s.length === 10) return `;VALUE=DATE:${(end ? iso(addDays(parseDay(s), 1)) : s).replace(/-/g, "")}`;
      return `;TZID=Europe/Rome:${s.replace(/[-:]/g, "")}00`;
    };
    const endVal = e.end || (e.start.length > 10 ? e.start.slice(0, 11) + pad(Math.min(23, +e.start.slice(11, 13) + 2)) + e.start.slice(13) : e.start);
    const lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Andiamoo//IT", "BEGIN:VEVENT",
      `UID:${e.uid}@andiamoo`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").slice(0, 15)}Z`,
      `DTSTART${dt(e.start)}`, `DTEND${dt(endVal, endVal.length === 10)}`,
      `SUMMARY:${ics(e.title)}`, `LOCATION:${ics([e.venue, e.address, e.town].filter(Boolean).join(", "))}`,
      `DESCRIPTION:${ics((e.summary ? e.summary + "\\n\\n" : "") + "Sito ufficiale: " + e.action_url)}`,
      `URL:${e.action_url}`, "END:VEVENT", "END:VCALENDAR"];
    const blob = new Blob([lines.join("\r\n")], { type: "text/calendar" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${e.title.slice(0, 40).replace(/[^\w]+/g, "-")}.ics`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  // ---------------------------------------------------------------- mappa
  function initMap() {
    const s = DATA.site;
    map = new maplibregl.Map({
      container: "map",
      style: "https://tiles.openfreemap.org/styles/positron",
      center: [s.center[1], s.center[0]],
      zoom: s.zoom - (window.innerWidth < 760 ? 1 : 0),
      attributionControl: { compact: true },
      cooperativeGestures: false,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.addControl(new maplibregl.GeolocateControl({ positionOptions: { enableHighAccuracy: false } }), "top-right");
    map.on("load", () => {
      const colorExpr = ["match", ["get", "category"]];
      DATA.categories.forEach((c) => colorExpr.push(c.id, c.color));
      colorExpr.push("#000000");
      map.addSource("ev", { type: "geojson", data: geojson([]), cluster: true, clusterRadius: 38, clusterMaxZoom: 13 });
      map.addLayer({ id: "clusters", type: "circle", source: "ev", filter: ["has", "point_count"],
        paint: { "circle-color": "#000", "circle-radius": ["step", ["get", "point_count"], 14, 10, 18, 40, 23],
          "circle-stroke-width": 2, "circle-stroke-color": "#fff" } });
      map.addLayer({ id: "cluster-count", type: "symbol", source: "ev", filter: ["has", "point_count"],
        layout: { "text-field": ["get", "point_count_abbreviated"], "text-size": 12,
          "text-font": ["Noto Sans Bold"] }, paint: { "text-color": "#fff" } });
      map.addLayer({ id: "points", type: "circle", source: "ev", filter: ["!", ["has", "point_count"]],
        paint: { "circle-color": colorExpr, "circle-radius": ["case", ["boolean", ["feature-state", "hl"], false], 10, 7],
          "circle-stroke-width": 2, "circle-stroke-color": "#fff" } });

      map.on("click", "clusters", (ev) => {
        const f = ev.features[0];
        map.getSource("ev").getClusterExpansionZoom(f.properties.cluster_id).then((z) =>
          map.easeTo({ center: f.geometry.coordinates, zoom: z + 0.3 }));
      });
      map.on("click", "points", (ev) => {
        const uids = [...new Set(ev.features.map((f) => f.properties.uid))];
        if (uids.length === 1) select(uids[0], false);
        else { state.q = ""; showOnly(uids); }
      });
      for (const l of ["clusters", "points"]) {
        map.on("mouseenter", l, () => (map.getCanvas().style.cursor = "pointer"));
        map.on("mouseleave", l, () => (map.getCanvas().style.cursor = ""));
      }
      mapReady = true;
      update(true);
    });
  }

  function geojson(items) {
    // Eventi nello stesso punto (es. centro del comune): piccolo spostamento a spirale per non sovrapporli.
    const seen = {};
    return { type: "FeatureCollection", features: items.map((e) => {
      const k = `${e.lat.toFixed(4)},${e.lon.toFixed(4)}`;
      const i = (seen[k] = (seen[k] || 0) + 1) - 1;
      const ang = i * 2.4, r = i ? 0.0006 * Math.sqrt(i) : 0;
      return { type: "Feature", id: hashId(e.uid), properties: { uid: e.uid, category: e.category, title: e.title },
        geometry: { type: "Point", coordinates: [e.lon + r * Math.cos(ang), e.lat + r * Math.sin(ang)] } };
    }) };
  }

  let hlId = null;
  function highlight(uid) {
    if (!mapReady) return;
    if (hlId !== null) map.setFeatureState({ source: "ev", id: hlId }, { hl: false });
    hlId = uid ? hashId(uid) : null;
    if (hlId !== null) map.setFeatureState({ source: "ev", id: hlId }, { hl: true });
  }

  // ---------------------------------------------------------------- selezione
  let onlyUids = null;
  function showOnly(uids) {
    onlyUids = new Set(uids);
    state.selected = null;
    update();
    openSheet(true);
  }

  function select(uid, fly) {
    state.selected = uid;
    onlyUids = null;
    const e = EVENTS.find((x) => x.uid === uid);
    $("#list").hidden = !!e;
    $(".filters").hidden = !!e;
    $("#detail").hidden = !e;
    if (e) {
      renderDetail(e);
      highlight(uid);
      if (fly && mapReady) map.flyTo({ center: [e.lon, e.lat], zoom: Math.max(map.getZoom(), 14.5), speed: 1.4 });
      $("#panel-body").scrollTop = 0;
      openSheet(true);
      history.replaceState(null, "", `#e=${uid}`);
    } else {
      highlight(null);
      history.replaceState(null, "", location.pathname + location.search);
      update();
    }
  }

  function openSheet(open) {
    const p = $("#panel");
    p.classList.toggle("open", open);
    $("#sheet-handle").setAttribute("aria-expanded", String(open));
  }

  // ---------------------------------------------------------------- aggiornamento
  function update(fit) {
    let items = EVENTS.filter((e) => matches(e));
    if (onlyUids) items = items.filter((e) => onlyUids.has(e.uid));
    items.sort((a, b) => {
      const from = state.from || "";
      const ka = (a.start.slice(0, 10) < from ? from : a.start.slice(0, 10)) + (timeOf(a) || "99");
      const kb = (b.start.slice(0, 10) < from ? from : b.start.slice(0, 10)) + (timeOf(b) || "99");
      return ka.localeCompare(kb);
    });
    renderStrip();
    renderChips();
    if (!state.selected) renderList(items);
    const n = items.length;
    $("#count-label").textContent = onlyUids ? `${n} eventi in questo punto` : `${n} ${n === 1 ? "evento" : "eventi"}`;
    const filtered = state.cats.size || state.access || state.audience || state.setting || state.q || state.preset !== "all" || onlyUids;
    $("#reset").hidden = !filtered;
    if (mapReady) {
      map.getSource("ev").setData(geojson(items));
      if (fit && items.length) {
        const b = new maplibregl.LngLatBounds();
        items.forEach((e) => b.extend([e.lon, e.lat]));
        map.fitBounds(b, { padding: 50, maxZoom: 12, duration: 0 });
      }
    }
  }

  // ---------------------------------------------------------------- segnalazioni
  function setupReport() {
    const s = DATA.site, ul = $("#report-options");
    const opts = [];
    if (s.telegram_bot) opts.push([`https://t.me/${s.telegram_bot}`, "Con Telegram", "Manda la foto della locandina o il link: ci pensa il bot."]);
    if (s.form_url) opts.push([s.form_url, "Con il modulo", "Per organizzatori: titolo, data, luogo e link."]);
    if (s.contact_email) opts.push([`mailto:${s.contact_email}?subject=Segnalazione%20evento`, "Per email", s.contact_email]);
    ul.innerHTML = opts.length ? opts.map(([h, t, d]) =>
      `<li><a href="${attr(h)}" target="_blank" rel="noopener"><strong>${esc(t)}</strong><span>${esc(d)}</span></a></li>`).join("")
      : "<li>Le segnalazioni apriranno a breve.</li>";
    $("#report-btn").addEventListener("click", () => $("#report").showModal());
    $("#removal").innerHTML = s.contact_email
      ? `Sei l'organizzatore e vuoi correggere o togliere un evento? <a href="mailto:${attr(s.contact_email)}">Scrivici</a>.` : "";
  }

  // ---------------------------------------------------------------- utilità
  function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function attr(s) { const v = String(s || "#"); return /^(https?:|mailto:)/.test(v) ? esc(v) : "#"; }
  function ics(s) { return String(s || "").replace(/[\\;,]/g, (c) => "\\" + c).replace(/\n/g, "\\n"); }
  function hashId(uid) { return parseInt(uid.slice(0, 8), 16); }

  // ---------------------------------------------------------------- avvio
  async function start() {
    try {
      const r = await fetch("data/events.json", { cache: "no-cache" });
      DATA = await r.json();
    } catch (err) {
      $("#count-label").textContent = "Eventi non disponibili";
      $("#list").innerHTML = `<li class="empty-state"><strong>Non riesco a caricare gli eventi.</strong>Ricarica la pagina tra qualche minuto.</li>`;
      return;
    }
    EVENTS = DATA.events.filter((e) => e.start && e.lat != null);
    DATA.categories.forEach((c) => (CAT[c.id] = c));
    if (DATA.site.title) { $("#site-title").textContent = DATA.site.title; document.title = DATA.site.title; }
    if (DATA.site.tagline) $("#site-tagline").textContent = DATA.site.tagline;
    const fill = (sel, obj) => Object.entries(obj || {}).forEach(([k, v]) => {
      if (k !== "sconosciuto") $(sel).insertAdjacentHTML("beforeend", `<option value="${k}">${esc(v)}</option>`);
    });
    fill("#access", DATA.access);
    fill("#audience", DATA.audiences);
    fill("#setting", DATA.settings);
    const g = new Date(DATA.generated);
    $("#updated").textContent = `Aggiornato il ${g.getDate()} ${MONTHS[g.getMonth()]} alle ${pad(g.getHours())}:${pad(g.getMinutes())}.`;
    setupReport();

    setPreset("all");
    document.querySelectorAll(".presets button").forEach((b) =>
      b.addEventListener("click", () => { setPreset(b.dataset.preset); onlyUids = null; update(); }));
    for (const k of ["access", "audience", "setting"]) {
      $("#" + k).addEventListener("change", (ev) => { state[k] = ev.target.value; update(); });
    }
    let t;
    $("#q").addEventListener("input", (ev) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = ev.target.value.trim().toLowerCase(); select(null); }, 180);
    });
    $("#reset").addEventListener("click", () => {
      state.cats.clear(); state.access = state.audience = state.setting = state.q = ""; onlyUids = null;
      for (const k of ["q", "access", "audience", "setting"]) $("#" + k).value = "";
      setPreset("all"); update(true);
    });
    $("#sheet-handle").addEventListener("click", () => openSheet(!$("#panel").classList.contains("open")));

    update();
    initMap();
    const m = location.hash.match(/e=([0-9a-f]+)/);
    if (m && EVENTS.some((e) => e.uid === m[1])) select(m[1], true);
  }

  start();
})();
