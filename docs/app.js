/* Andiamoo: legge data/events.json, filtra per giorni/categorie/accesso/pubblico/luogo/testo,
   mostra mappa (segnaposti colorati con "+", card sulla mappa) ed elenco con scheda. */
(() => {
  "use strict";

  const $ = (s) => document.querySelector(s);
  const DOW = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];
  const DAYS = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"];
  const MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
    "settembre", "ottobre", "novembre", "dicembre"];
  const STRIP_DAYS = 45;
  const MOBILE = () => window.innerWidth <= 760;

  const state = { from: null, to: null, preset: "all", cats: new Set(), access: "", audience: "", setting: "", q: "", selected: null };
  let DATA = null, EVENTS = [], CAT = {}, map = null, mapReady = false, popup = null, onlyUids = null;
  const COORDS = {};                       // uid -> [lon, lat] mostrati (con il piccolo scarto anti-sovrapposizione)

  // ---------------------------------------------------------------- date
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
      const b = document.createElement("button");
      b.type = "button"; b.className = "chip";
      b.style.setProperty("--c", c.color);
      b.setAttribute("aria-pressed", String(state.cats.has(c.id)));
      if (n === 0 && !state.cats.has(c.id)) return;          // categorie vuote: nascoste
      b.innerHTML = `<span class="dot"></span>${esc(c.label)} <span class="n">${n}</span>`;
      b.addEventListener("click", () => { state.cats.has(c.id) ? state.cats.delete(c.id) : state.cats.add(c.id); onlyUids = null; update(); });
      box.appendChild(b);
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
    items.forEach((e) => {
      const groupDay = e.start.slice(0, 10) < from ? from : e.start.slice(0, 10);
      if (groupDay !== lastGroup) {
        lastGroup = groupDay;
        const g = document.createElement("li");
        g.className = "group"; g.textContent = dayLabel(parseDay(groupDay));
        list.appendChild(g);
      }
      const c = CAT[e.category] || {};
      const longRun = e.end && e.end.slice(0, 10) !== e.start.slice(0, 10);
      const when = timeOf(e) || (longRun ? `fino al ${shortDate(e.end)}` : "");
      const li = document.createElement("li");
      li.className = "item";
      li.innerHTML = `<button type="button" data-uid="${e.uid}" style="--c:${c.color}">
          <span class="dot" aria-hidden="true"></span>
          <span><h3>${esc(e.title)}</h3><span class="meta">${esc([e.venue, e.town].filter(Boolean).join(", "))}</span></span>
          <span class="when">${esc(when)}</span></button>`;
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
    el.innerHTML = `
      <button class="text-btn back" type="button">← Tutti gli eventi</button><br>
      <span class="cat" style="--c:${c.color}">${esc(c.label)}${sub ? ` · ${esc(sub)}` : ""}</span>
      <h2>${esc(e.title)}</h2>
      <dl class="facts">
        <dt>Quando</dt><dd>${esc(whenText(e))}</dd>
        ${place ? `<dt>Dove</dt><dd>${esc(place)}${e.geo_precision === "town" ? " <small>(posizione indicativa)</small>" : ""}</dd>` : ""}
        ${accessLabel || e.price ? `<dt>Ingresso</dt><dd>${esc([accessLabel, e.price].filter(Boolean).join(" · "))}</dd>` : ""}
        ${who ? `<dt>Per chi</dt><dd>${esc(who)}</dd>` : ""}
      </dl>
      ${e.summary ? `<p class="summary">${esc(e.summary)}</p>` : ""}
      <div class="official">
        <p>${e.ai_summary ? "Dettagli riassunti tramite AI. " : ""}Per il programma ufficiale e le iscrizioni, visita il sito ufficiale${host ? ` (${esc(host)})` : ""}.</p>
        <a class="cta" href="${attr(e.action_url)}" target="_blank" rel="noopener"><span>Sito ufficiale</span><i aria-hidden="true">↗</i></a>
      </div>
      <div class="actions">
        <button class="ghost" type="button" data-ics>Aggiungi al calendario</button>
        <a class="ghost" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=${e.lat},${e.lon}">Indicazioni</a>
      </div>
      <p class="also">Fonte: <a href="${attr(e.source_url)}" target="_blank" rel="noopener">${esc(e.source_name)}</a>${
        also.length ? `. Anche su: ${also.map((a) => `<a href="${attr(a.url)}" target="_blank" rel="noopener">${esc(a.source)}</a>`).join(", ")}` : ""}</p>
      <p class="small-print">Dati non corretti o evento da rimuovere? ${removalLink(e)}</p>`;
    el.querySelector(".back").addEventListener("click", () => select(null));
    el.querySelector("[data-ics]").addEventListener("click", () => downloadIcs(e));
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
  // Toni caldi e desaturati sopra lo stile "positron" di OpenFreeMap.
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

  // Segnaposto disegnato: cerchio nel colore della categoria con "+" (o "−" se selezionato).
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

  function initMap() {
    const s = DATA.site;
    map = new maplibregl.Map({
      container: "map",
      style: "https://tiles.openfreemap.org/styles/positron",
      center: [s.center[1], s.center[0]],
      zoom: s.zoom - (MOBILE() ? 1 : 0),
      attributionControl: { compact: true },
    });
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
      map.addLayer({ id: "points-hover", type: "symbol", source: "ev", filter: ["==", ["get", "uid"], ""],
        layout: { "icon-image": icon("pin-"), "icon-size": 1.25, "icon-allow-overlap": true } });
      map.addLayer({ id: "points-selected", type: "symbol", source: "ev", filter: ["==", ["get", "uid"], ""],
        layout: { "icon-image": icon("pin-sel-"), "icon-size": 1.15, "icon-allow-overlap": true } });

      map.on("click", "clusters", (ev) => {
        const f = ev.features[0];
        map.getSource("ev").getClusterExpansionZoom(f.properties.cluster_id).then((z) =>
          map.easeTo({ center: f.geometry.coordinates, zoom: z + 0.3 }));
      });
      map.on("click", "points", (ev) => {
        const uids = [...new Set(ev.features.map((f) => f.properties.uid))];
        if (uids.length === 1) select(uids[0], { fly: false, detail: false });
        else { onlyUids = new Set(uids); select(null); openSheet(true); }
      });
      map.on("click", (ev) => {
        if (!map.queryRenderedFeatures(ev.point, { layers: ["points", "clusters"] }).length && popup) closeCard();
      });
      for (const l of ["clusters", "points"]) {
        map.on("mouseenter", l, () => (map.getCanvas().style.cursor = "pointer"));
        map.on("mouseleave", l, () => (map.getCanvas().style.cursor = ""));
      }
      mapReady = true;
      update(true);
      if (state.selected) select(state.selected, { fly: true, detail: true });
    });
  }

  function geojson(items) {
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

  function pointsFilter(selUid) {
    return ["all", ["!", ["has", "point_count"]], ["!=", ["get", "uid"], selUid]];
  }

  function hover(uid) {
    if (mapReady) map.setFilter("points-hover", ["==", ["get", "uid"], uid || ""]);
  }

  // ---------------------------------------------------------------- card sulla mappa
  function showCard(e) {
    const c = CAT[e.category] || { color: "#ddd" };
    const el = document.createElement("div");
    el.className = "card";
    el.style.setProperty("--c", c.color);
    el.innerHTML = `<h3>${esc(e.title)}</h3>
      <p>${esc(whenText(e))}</p><p>${esc([e.venue, e.town].filter(Boolean).join(", "))}</p>
      <button class="more" type="button">Dettagli</button>`;
    el.querySelector(".more").addEventListener("click", () => select(e.uid, { fly: false, detail: true }));
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ className: "ev-card", closeButton: false, closeOnClick: false, anchor: "bottom", offset: 22, maxWidth: "none" })
      .setLngLat(COORDS[e.uid] || [e.lon, e.lat]).setDOMContent(el).addTo(map);
    map.setFilter("points-selected", ["==", ["get", "uid"], e.uid]);
    map.setFilter("points", pointsFilter(e.uid));
  }

  function closeCard() {
    if (popup) { popup.remove(); popup = null; }
    if (mapReady) { map.setFilter("points-selected", ["==", ["get", "uid"], ""]); map.setFilter("points", pointsFilter("")); }
  }

  // ---------------------------------------------------------------- selezione
  function select(uid, opts = {}) {
    state.selected = uid;
    const e = uid && EVENTS.find((x) => x.uid === uid);
    const showDetail = e && opts.detail;
    $("#list").hidden = !!showDetail;
    $("#detail").hidden = !showDetail;
    if (!e) {
      closeCard();
      history.replaceState(null, "", location.pathname + location.search);
      update();
      return;
    }
    if (showDetail) { renderDetail(e); $("#panel-body").scrollTop = 0; openSheet(true); }
    if (mapReady) {
      // su telefono la scheda copre la mappa: basta il segnaposto evidenziato, senza card
      if (MOBILE() && showDetail) {
        if (popup) { popup.remove(); popup = null; }
        map.setFilter("points-selected", ["==", ["get", "uid"], e.uid]);
        map.setFilter("points", pointsFilter(e.uid));
      } else showCard(e);
      if (opts.fly) {
        const pad = MOBILE() ? { top: 200, bottom: window.innerHeight * 0.62 } : { left: 440, top: 140 };
        map.flyTo({ center: COORDS[uid] || [e.lon, e.lat], zoom: Math.max(map.getZoom(), 14.2), speed: 1.4, padding: pad });
      }
    }
    history.replaceState(null, "", `#e=${uid}`);
  }

  function openSheet(open) {
    $("#panel").classList.toggle("open", open);
    $("#sheet-handle").setAttribute("aria-expanded", String(open));
  }

  // ---------------------------------------------------------------- aggiornamento
  function update(fit) {
    let items = EVENTS.filter((e) => matches(e));
    if (onlyUids) items = items.filter((e) => onlyUids.has(e.uid));
    const from = state.from || "";
    const key = (e) => (e.start.slice(0, 10) < from ? from : e.start.slice(0, 10)) + (timeOf(e) || "99");
    items.sort((a, b) => key(a).localeCompare(key(b)));
    renderStrip();
    renderChips();
    if (!state.selected || $("#detail").hidden) renderList(items);
    const n = items.length;
    $("#count-label").textContent = onlyUids ? `${n} in questo punto` : `${n} ${n === 1 ? "evento" : "eventi"}`;
    $("#reset").hidden = !(state.cats.size || state.access || state.audience || state.setting || state.q || onlyUids);
    if (mapReady) {
      map.getSource("ev").setData(geojson(items));
      if (fit && items.length && !state.selected) {
        const b = new maplibregl.LngLatBounds();
        items.forEach((e) => b.extend([e.lon, e.lat]));
        const pad = MOBILE() ? { top: 220, bottom: 80, left: 30, right: 30 } : { top: 170, bottom: 150, left: 470, right: 90 };
        map.fitBounds(b, { padding: pad, maxZoom: 12, duration: 0 });
      }
    }
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
    const fill = (sel, obj, prefix) => Object.entries(obj || {}).forEach(([k, v]) => {
      if (k !== "sconosciuto") $(sel).insertAdjacentHTML("beforeend", `<option value="${k}">${esc(prefix + v)}</option>`);
    });
    fill("#access", DATA.access, "");
    fill("#audience", DATA.audiences, "");
    fill("#setting", DATA.settings, "");
    const g = new Date(DATA.generated);
    $("#updated").textContent = `Aggiornato il ${g.getDate()} ${MONTHS[g.getMonth()]} alle ${pad(g.getHours())}:${pad(g.getMinutes())}.`;
    setupReport();

    setPreset("all");
    document.querySelectorAll(".presets button").forEach((b) =>
      b.addEventListener("click", () => { setPreset(b.dataset.preset); onlyUids = null; update(); }));
    for (const k of ["access", "audience", "setting"]) {
      $("#" + k).addEventListener("change", (ev) => { state[k] = ev.target.value; onlyUids = null; update(); });
    }
    let t;
    $("#q").addEventListener("input", (ev) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = ev.target.value.trim().toLowerCase(); onlyUids = null; select(null); }, 180);
    });
    $("#reset").addEventListener("click", () => {
      state.cats.clear(); state.access = state.audience = state.setting = state.q = ""; onlyUids = null;
      for (const k of ["q", "access", "audience", "setting"]) $("#" + k).value = "";
      setPreset("all"); select(null); update(true);
    });
    $("#sheet-handle").addEventListener("click", () => { if (MOBILE()) openSheet(!$("#panel").classList.contains("open")); });
    $("#more-filters").addEventListener("click", (ev) => {
      const open = $(".filters").classList.toggle("expanded");
      ev.currentTarget.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && state.selected) select(null); });

    const m = location.hash.match(/e=([0-9a-f]+)/);
    if (m && EVENTS.some((e) => e.uid === m[1])) state.selected = m[1];
    update();
    initMap();
  }

  start();
})();
