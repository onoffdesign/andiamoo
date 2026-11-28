/* ANDIAMO?: legge data/events.json, filtra per giorni/categorie/accesso/pubblico/luogo/testo,
   mostra mappa (segnaposti colorati con l'icona della categoria, anello animato per gli eventi in corso, piccoli
   suoni e animazioni), card sulla mappa ed elenco con scheda.
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
    selected: null, detail: false, sort: "distance", me: null, fav: false, place: null,
    radius: (() => { try { return +localStorage.getItem("andiamo-raggio") || 30; } catch (_) { return 30; } })(),   // km, vista lista   // place: nome del luogo di "Vicino a"
    view: "map", pick: null,                 // vista mappa/lista; primo giorno scelto nel calendario (in attesa del secondo)
    sidebarHidden: false, hiddenBeforeDetail: false,
  };
  let API = "", apiOk = false, aiOk = false;
  let DATA = null, EVENTS = [], CAT = {}, map = null, mapReady = false, popup = null, meMarker = null, onlyUids = null;
  let pushedDetail = false;                // la scheda aperta ha una voce nostra nella cronologia?
  const COORDS = {};                       // uid -> [lon, lat] del punto (gli eventi dello stesso posto hanno lo stesso)
  // Eventi nello stesso posto: stesso punto sulla mappa, segnaposti disposti a nido d'ape attorno al centro, vicini
  // ma senza toccarsi a qualsiasi zoom (lo scarto e' in pixel). SLOTS[i] = scarto in pixel del posto i.
  const SLOTS = [[0, 0]];
  for (let r = 1; r <= 5; r++) for (let k = 0; k < 6 * r; k++) {
    const a = -Math.PI / 2 + (k * 2 * Math.PI) / (6 * r);
    SLOTS.push([Math.round(40 * r * Math.cos(a)), Math.round(40 * r * Math.sin(a))]);
  }
  const SLOT = {};                         // uid -> indice in SLOTS
  const slotOff = (uid) => SLOTS[SLOT[uid] || 0];
  let LIVE = new Set();                    // uid degli eventi in corso adesso (ricalcolati ogni minuto)
  // Preferiti: gli eventi salvati col cuore restano in questo browser (nessun account, nessun dato inviato).
  const FAV = new Set((() => { try { return JSON.parse(localStorage.getItem("andiamo-preferiti") || "[]"); } catch (_) { return []; } })());
  const HEART = (on) => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"${on ? ' class="on"' : ""}/></svg>`;
  function favButton(e, cls) {
    const on = FAV.has(e.uid);
    return `<button type="button" class="${cls}" data-fav="${e.uid}" aria-pressed="${on}" aria-label="${on ? "Togli dai preferiti" : "Salva nei preferiti"}" title="${on ? "Togli dai preferiti" : "Salva nei preferiti"}">${HEART(on)}</button>`;
  }
  function toggleFav(uid) {
    const on = !FAV.has(uid);
    on ? FAV.add(uid) : FAV.delete(uid);
    try { localStorage.setItem("andiamo-preferiti", JSON.stringify([...FAV])); } catch (_) { /* privato */ }
    Sound.play(on ? "save-on" : "save-off");
    document.querySelectorAll(`[data-fav="${uid}"]`).forEach((b) => {
      b.setAttribute("aria-pressed", String(on));
      b.setAttribute("aria-label", on ? "Togli dai preferiti" : "Salva nei preferiti");
      b.title = b.getAttribute("aria-label");
      b.innerHTML = HEART(on);
      b.classList.remove("pop"); void b.offsetWidth; b.classList.add("pop");
    });
    toast(on ? "Salvato nei preferiti" : "Tolto dai preferiti");
    if (state.fav || !state.detail) update();
    else renderFavBtn();
  }
  function renderFavBtn() {
    const b = $("#fav-btn");
    if (!b) return;
    const n = [...FAV].filter((u) => EVENTS.some((e) => e.uid === u && !isOver(e))).length;
    b.setAttribute("aria-pressed", String(state.fav));
    b.setAttribute("aria-label", state.fav ? "Mostra tutti gli eventi" : `Preferiti: ${n}`);
    b.innerHTML = `${HEART(state.fav || n > 0)}<span>${n}</span>`;
    // cuore tra i controlli della mappa: solo se c'e' almeno un preferito; acceso = sulla mappa solo i preferiti
    const m = $("#fav-map");
    if (m) {
      if (!n && state.fav) { state.fav = false; setTimeout(() => update(true), 0); }
      m.hidden = !n;
      m.setAttribute("aria-pressed", String(state.fav));
      m.setAttribute("aria-label", state.fav ? "Mostra tutti gli eventi" : "Mostra solo i preferiti");
      m.title = state.fav ? "Mostra tutti gli eventi" : "Solo i miei preferiti";
      m.innerHTML = HEART(true);
    }
  }

  // ---------------------------------------------------------------- date e distanze
  const pad = (n) => String(n).padStart(2, "0");
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseDay = (s) => { const [y, m, d] = s.slice(0, 10).split("-").map(Number); return new Date(y, m - 1, d); };
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  // "oggi" e' sempre la data in Italia (Europe/Rome), anche per chi guarda da un altro fuso orario
  const romeToday = () => new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Rome", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
  const today = () => parseDay(romeToday());
  const timeOf = (e) => (e.start && e.start.length > 10 ? e.start.slice(11, 16) : "");
  const dayLabel = (d) => {
    const diff = Math.round((d - today()) / 86400000);
    const base = `${DAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`;
    return diff === 0 ? `Oggi, ${base}` : diff === 1 ? `Domani, ${base}` : base[0].toUpperCase() + base.slice(1);
  };
  const plainDay = (d) => { const b = `${DAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`; return b[0].toUpperCase() + b.slice(1); };
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

  // ---------------------------------------------------------------- logo animato (lettere separate per l'onda)
  const letters = (text, cls) => [...text].map((ch, i) => ch === "?" && cls === "l"
    ? `<span class="q">?</span>` : `<span class="${cls}" style="--i:${i}">${ch === " " ? "&nbsp;" : esc(ch)}</span>`).join("");

  // Logo e frase "Trova il tuo evento" si alternano: il riquadro cambia larghezza, le lettere entrano a onda.
  function renderWordmark(title) {
    const pill = $(".brand-pill"), logo = $("#site-title"), tag = $("#tagline");
    logo.setAttribute("aria-label", title);
    logo.innerHTML = letters(title, "l");
    tag.innerHTML = letters("Trova il tuo evento", "t");
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const pad = 32;
    const room = () => $("#top-right").getBoundingClientRect().left - pill.getBoundingClientRect().left - 10;
    const widthFor = (el) => {
      pill.classList.toggle("tight", MOBILE() && tag.scrollWidth + pad > room());
      return el.scrollWidth + pad;
    };
    pill.style.width = `${widthFor(logo)}px`;
    pill.classList.add("brand-anim");
    const play = (el) => { el.classList.remove("play"); void el.offsetWidth; el.classList.add("play"); };
    let showTag = false;
    const step = () => {
      showTag = !showTag;
      if (showTag) { widthFor(tag); if (tag.scrollWidth + pad > room()) showTag = false; }   // schermo troppo stretto: solo logo
      pill.classList.toggle("show-tag", showTag);
      pill.style.width = `${widthFor(showTag ? tag : logo)}px`;
      play(showTag ? tag : logo);
      setTimeout(step, showTag ? 3400 : 5200);
    };
    play(logo);
    setTimeout(step, 5200);
    window.addEventListener("resize", () => { pill.style.width = `${widthFor(showTag ? tag : logo)}px`; });
  }

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
  // Eventi passati: restano visibili per tutto il giorno in cui finiscono e spariscono dal giorno dopo
  // (data italiana, qualunque sia il fuso orario di chi guarda).
  function isOver(e) {
    const last = (e.end || e.start || "").slice(0, 10);
    return !!last && last < romeToday();
  }

  function matches(e, skip = {}) {
    if (isOver(e)) return false;
    if (state.fav) return FAV.has(e.uid);        // elenco preferiti: tutti i salvati, senza gli altri filtri
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

  // ---------------------------------------------------------------- calendario (icona che si apre)
  const shortD = (key) => { const d = parseDay(key); return `${DOW[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()].slice(0, 3)}`; };
  function rangeLabel() {
    if (state.preset === "all") return "Tutte le date";
    if (state.preset === "today") return "Oggi";
    if (state.preset === "weekend") return "Weekend";
    if (state.preset === "week") return "Settimana";      // i prossimi 7 giorni
    if (state.from && state.to && state.from === state.to) return shortD(state.from);
    if (state.from && state.to) return `Dal ${shortD(state.from)} al ${shortD(state.to)}`;
    return "Tutte le date";
  }
  function setCalendar(open) {
    $(".days").dataset.open = String(open);
    $("#cal-btn").setAttribute("aria-expanded", String(open));
    if (!open) state.pick = null;
    renderRangeHint();
    if (open) {                                     // si apre sul mese del primo giorno scelto
      const t = today(), f = state.preset !== "all" && state.from ? parseDay(state.from) : t;
      state.calMonth = Math.max(0, (f.getFullYear() - t.getFullYear()) * 12 + f.getMonth() - t.getMonth());
      renderStrip();
    }
  }
  function renderRangeHint() {
    $("#cal-label").textContent = rangeLabel();
    const h = $("#range-hint");
    if (h) h.textContent = state.pick ? `Dal ${shortD(state.pick)}: tocca l'ultimo giorno` : "Tocca il primo e l'ultimo giorno";
  }
  function pickDay(key) {
    if (!state.pick) {                              // primo tocco: inizio (e per ora anche fine)
      state.pick = key; state.preset = "range"; state.from = state.to = key;
    } else {                                        // secondo tocco: fine dell'intervallo
      const a = state.pick;
      state.from = key < a ? key : a; state.to = key < a ? a : key; state.preset = "range"; state.pick = null;
      setTimeout(() => setCalendar(false), 450);
    }
    onlyUids = null; update();
  }

  // ---------------------------------------------------------------- calendario del mese
  // Un riquadro con il mese: ogni giorno e' un numero dentro un cerchio tanto piu' grande quanti piu' eventi ha
  // (nessun cerchio se non ce ne sono). Si scorre mese per mese entro l'orizzonte degli eventi.
  function renderStrip() {
    const grid = $("#strip");
    const t = today(), last = addDays(t, STRIP_DAYS - 1);
    const maxMonth = (last.getFullYear() - t.getFullYear()) * 12 + last.getMonth() - t.getMonth();
    state.calMonth = Math.min(Math.max(0, state.calMonth || 0), maxMonth);
    const first = new Date(t.getFullYear(), t.getMonth() + state.calMonth, 1);
    const ndays = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
    const base = EVENTS.filter((e) => matches(e, { date: true }));
    const tKey = iso(t), lastKey = iso(last);
    const days = [];
    for (let i = 1; i <= ndays; i++) {
      const d = new Date(first.getFullYear(), first.getMonth(), i), key = iso(d);
      const open = key >= tKey && key <= lastKey;
      days.push({ d, key, open, n: open ? base.filter((e) => spans(e, key, key)).length : 0 });
    }
    const max = Math.max(1, ...days.map((x) => x.n));
    grid.innerHTML = "";
    for (let i = 0; i < (first.getDay() + 6) % 7; i++) grid.appendChild(document.createElement("span"));   // da lunedi'
    for (const { d, key, open, n } of days) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "cday" + (d.getDay() === 0 || d.getDay() === 6 ? " weekend" : "") + (key === tKey ? " today" : "");
      b.disabled = !open;
      const on = open && state.preset !== "all" && state.from && key >= state.from && key <= (state.to || state.from);
      b.setAttribute("aria-pressed", String(!!on));
      if (on && key === state.from) b.classList.add("r-start");
      if (on && key === (state.to || state.from)) b.classList.add("r-end");
      const size = n ? Math.round(12 + Math.sqrt(n / max) * 22) : 0;       // da 12 a 34 px
      b.style.setProperty("--blob", `${size}px`);
      b.setAttribute("aria-label", `${dayLabel(d)}: ${n} eventi`);
      b.title = open ? `${n} ${n === 1 ? "evento" : "eventi"}` : "";
      b.innerHTML = `${n ? '<span class="blob" aria-hidden="true"></span>' : ""}<span class="num">${d.getDate()}</span>`;
      if (open) b.addEventListener("click", () => { Sound.play("chip"); pickDay(key); });
      grid.appendChild(b);
    }
    $("#cal-month").textContent = `${MONTHS[first.getMonth()]} ${first.getFullYear()}`;
    $("#cal-prev").disabled = state.calMonth <= 0;
    $("#cal-next").disabled = state.calMonth >= maxMonth;
    document.querySelectorAll(".presets button").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.preset === state.preset)));
    renderRangeHint();
  }
  const updateStripNav = () => {};

  // frecce avanti/indietro (desktop) per le righe che scorrono: giorni e categorie
  function updateScrollNav(sel) {
    const s = $(sel), id = sel.slice(1);
    const atStart = s.scrollLeft <= 2, atEnd = s.scrollLeft + s.clientWidth >= s.scrollWidth - 2;
    $(`#${id}-prev`).disabled = atStart;
    $(`#${id}-next`).disabled = atEnd;
    s.classList.toggle("at-end", atEnd);
  }

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
      b.addEventListener("click", () => { Sound.play("chip"); state.cats.has(c.id) ? state.cats.delete(c.id) : state.cats.add(c.id); onlyUids = null; update(); });
      box.appendChild(b);
    });
    const extra = (state.access.size ? 1 : 0) + state.aud.size;
    $("#more-filters").innerHTML = extra ? `Filtri <span class="badge">${extra}</span>` : "Filtri";
    // nessuna scelta = tutti attivi (e tutti mostrati come attivi)
    document.querySelectorAll("#access button").forEach((b) =>
      b.setAttribute("aria-pressed", String(!state.access.size || state.access.has(b.dataset.v))));
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

  }

  // ---------------------------------------------------------------- elenco
  // Vista lista: toccando un evento si apre la sua card subito sotto (un solo evento aperto per volta).
  function toggleInline(li, e, opts = {}) {
    const next = li.nextElementSibling, open = next && next.classList.contains("inline-card") && next.dataset.uid === e.uid;
    document.querySelectorAll("#list .inline-card").forEach((x) => x.remove());
    document.querySelectorAll("#list .item button[aria-expanded]").forEach((b) => b.setAttribute("aria-expanded", "false"));
    document.querySelectorAll("#list .item.open").forEach((x) => x.classList.remove("open"));
    if (open) return;
    const box = document.createElement("li");
    box.className = "inline-card"; box.dataset.uid = e.uid;
    // il riquadro dell'evento si allunga verso il basso: sotto solo cio' che non c'e' gia' (niente titolo e luogo)
    box.appendChild(buildCard(e, { inline: true }));
    box.style.setProperty("--c", (CAT[e.category] || {}).color || "#ddd");
    li.after(box);
    li.classList.add("open");
    li.querySelector("button").setAttribute("aria-expanded", "true");
    if (!opts.quiet) requestAnimationFrame(() => box.scrollIntoView({ block: "nearest", behavior: "smooth" }));
    else box.querySelector(".card").style.animation = "none";
  }

  function renderList(items) {
    const list = $("#list");
    list.innerHTML = "";
    if (!items.length) {
      list.innerHTML = state.fav
        ? `<li class="empty-state"><strong>Nessun evento nei preferiti.</strong>Tocca il cuore su un evento per salvarlo qui.</li>`
        : `<li class="empty-state"><strong>Nessun evento con questi filtri.</strong>Prova un altro giorno o togli qualche categoria.</li>`;
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
      if (LIVE.has(e.uid)) when = "In corso";
      const dist = kmText(km(e));
      const li = document.createElement("li");
      li.className = "item";
      li.innerHTML = `<button type="button" data-uid="${e.uid}" style="--c:${c.color}">
          <span class="dot" aria-hidden="true"></span>
          <span><h3>${FAV.has(e.uid) ? '<i class="saved" aria-label="Salvato">♥</i> ' : ""}${esc(e.title)}</h3><span class="meta">${esc([e.venue, e.town].filter(Boolean).join(", "))}</span></span>
          <span class="when${LIVE.has(e.uid) ? " live" : ""}">${esc(when)}${dist ? `<small>${dist}</small>` : ""}</span></button>`;
      const btn = li.querySelector("button");
      btn.addEventListener("click", () => { Sound.play("select"); toggleInline(li, e); });
      btn.addEventListener("mouseenter", () => hover(e.uid));
      btn.addEventListener("mouseleave", () => hover(null));
      list.appendChild(li);
    });
  }

  // ---------------------------------------------------------------- vista lista: card complete per giorno
  let cardsShown = 0;
  function renderCards(items, more = false) {
    const box = $("#cards-list");
    if (!more) { box.innerHTML = ""; cardsShown = 0; $("#cards").scrollTop = 0; }
    $("#cards-more")?.remove();
    if (!items.length) {
      box.innerHTML = `<p class="empty-state"><strong>${state.fav ? "Nessun evento nei preferiti." : "Nessun evento con questi filtri."}</strong>${
        state.fav ? "Tocca il cuore su un evento per salvarlo qui." : "Prova altre date o togli qualche categoria."}</p>`;
      return;
    }
    const from = state.from || iso(today());
    const byDistance = state.sort === "distance" && state.me;
    let last = box.dataset.last || "";
    const end = Math.min(items.length, cardsShown + 60);
    for (let i = cardsShown; i < end; i++) {
      const e = items[i];
      if (!byDistance) {
        const day = e.start.slice(0, 10) < from ? from : e.start.slice(0, 10);
        if (day !== last) { last = day; const h = document.createElement("h2"); h.className = "cards-day"; h.textContent = dayLabel(parseDay(day)); box.appendChild(h); }
      }
      box.appendChild(buildCard(e, { onPlace: (x) => { setView("map", { keep: true }); select(x.uid, { fly: true }); } }));
    }
    box.dataset.last = last;
    cardsShown = end;
    if (end < items.length) {
      const b = document.createElement("button");
      b.id = "cards-more"; b.type = "button"; b.className = "pill-btn cards-more";
      b.textContent = `Mostra altri ${Math.min(60, items.length - end)} di ${items.length - end}`;
      b.addEventListener("click", () => renderCards(items, true));
      box.after(b);
    }
  }
  let lastItems = [];
  function setView(v, opts = {}) {
    state.view = v;
    document.body.classList.toggle("view-list", v === "list");
    document.querySelectorAll(".view-seg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === v)));
    try { localStorage.setItem("andiamo-vista", v); } catch (_) { /* privato */ }
    if (v === "list") {
      closeCard(); state.selected = null;
      ensurePlace();
      if (EVENTS.length) update();
      // il titolo del giorno resta fermo subito sotto la riga con preferiti e "Piu' vicini"
      requestAnimationFrame(() => document.documentElement.style.setProperty("--list-head", `${Math.round($("#sheet-head").getBoundingClientRect().height)}px`));
    }
    else if (mapReady) setTimeout(() => map.resize(), 30);
  }

  // ---------------------------------------------------------------- scheda
  function renderDetail(e) {
    const el = $("#detail");
    const c = CAT[e.category] || { label: "Evento", color: "#ddd" };
    const sub = (c.sub || {})[e.subcategory];
    const place = [e.venue, e.address, e.town].filter(Boolean).join(", ");
    const where = DATA.settings[e.setting] || "";
    const g = accessGroup(e);
    const private_ = (DATA.access[e.access] || "").match(/\((.*)\)$/);       // es. "Su invito (evento privato)"
    const price = /^(sconosciut|non (indicat|specificat|disponibil)|n\/?d|nd|-|\?)/i.test((e.price || "").trim()) ? "" : e.price;
    const accessText = g ? [private_ ? private_[1][0].toUpperCase() + private_[1].slice(1) : "", price].filter(Boolean).join(" · ")
      : ["Da verificare sul sito ufficiale", price].filter(Boolean).join(" · ");
    const host = e.action_url ? new URL(e.action_url).hostname.replace(/^www\./, "") : "";
    const also = (e.also_on || []).filter((a) => a.url);
    const dist = kmText(km(e));
    const placeLine2 = [e.address, e.venue ? e.town : ""].filter(Boolean).join(", ");
    const placeLine3 = [where, dist ? `${dist} da te` : ""].filter(Boolean).join(" · ");
    const d0 = parseDay(e.start), t0 = timeOf(e);
    const sameDayEnd = e.end && e.end.slice(0, 10) === e.start.slice(0, 10) && e.end.length > 10 ? e.end.slice(11, 16) : "";
    const multiDay = e.end && e.end.slice(0, 10) !== e.start.slice(0, 10);
    const timeLine = t0 ? (sameDayEnd ? `dalle ${t0} alle ${sameDayEnd}` : `ore ${t0}`) : (multiDay ? "" : "orario da verificare");
    const untilLine = multiDay ? `fino a ${dayLabel(parseDay(e.end)).toLowerCase()}` : "";
    el.innerHTML = `
      <button class="text-btn back" type="button">← Tutti gli eventi</button><br>
      <span class="cat" style="--c:${c.color}">${esc(c.label)}${sub ? ` · ${esc(sub)}` : ""}</span>
      <h2>${esc(e.title)}</h2>
      <div class="when-big">
        <div class="date-tile" aria-hidden="true"><span class="dow">${DOW[d0.getDay()]}</span><span class="d">${d0.getDate()}</span><span class="m">${MONTHS[d0.getMonth()].slice(0, 3)}</span></div>
        <div><strong class="when-main">${esc(dayLabel(d0))}</strong>
          ${timeLine ? `<span class="when-time">${esc(timeLine)}</span>` : ""}${untilLine ? `<span class="when-time">${esc(untilLine)}</span>` : ""}</div>
      </div>
      ${place ? `<div class="place-row"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>
        <div><strong>${esc(e.venue || e.town)}</strong>${placeLine2 ? `<span>${esc(placeLine2)}</span>` : ""}${
          placeLine3 ? `<span class="muted">${esc(placeLine3)}</span>` : ""}</div></div>` : ""}
      <div class="meta-row acc-dd">${accessBadge(e)}${accessText ? `<span>${esc(accessText)}</span>` : ""}${
        (e.audience || []).map((a) => `<span class="who-pill">${esc(DATA.audiences[a] || a)}</span>`).join("")}</div>
      ${e.summary ? `<p class="summary">${esc(e.summary)}</p>` : ""}
      <div class="detail-secondary">
        <p>${e.ai_summary ? "Dettagli riassunti tramite AI. " : ""}Per il programma ufficiale e le iscrizioni fa fede il sito ufficiale${host ? ` (${esc(host)})` : ""}.</p>
        <p>Fonte: <a href="${attr(e.source_url)}" target="_blank" rel="noopener">${esc(e.source_name)}</a>${
          also.length ? ` · Anche su: ${also.map((a) => `<a href="${attr(a.url)}" target="_blank" rel="noopener">${esc(a.source)}</a>`).join(", ")}` : ""}</p>
        ${e.ticket_url && e.ticket_url !== e.action_url ? `<p>Iscrizioni su <a href="${attr(e.ticket_url)}" target="_blank" rel="noopener">${
          esc(new URL(e.ticket_url).hostname.replace(/^www\./, ""))}</a></p>` : ""}
        <button class="report-link" type="button" data-report>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4h11l-1.5 4L16 12H5"/></svg>Segnala una modifica o la rimozione</button>
      </div>
      <div class="detail-actions">
        <a class="cta" href="${attr(e.action_url)}" target="_blank" rel="noopener"><span>Scopri di più</span><i aria-hidden="true">↗</i></a>
        ${favButton(e, "round fav-round")}
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
    el.querySelector("[data-fav]").addEventListener("click", () => toggleFav(e.uid));
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
  // Mappa illustrata, come una stampa su carta: mare color carta, terra verde con grana a puntini (piu' scura lungo
  // le coste), strade principali come file di perline d'inchiostro, solo i nomi di citta' e paesi scritti a mano.
  // Tutto il resto della base (edifici, parchi, binari, stradine, numeri delle strade, aeroporti) e' nascosto.
  const HAND_FONT = ["andiamo-hand"];        // Patrick Hand, convertito in glifi per MapLibre (docs/fonts)
  const LIVE_COLOR = "#f4b942";              // eventi in corso: un alone caldo color sole, niente rosso d'allarme
  const MAP_INK = { paper: "#f4efe3", land: "#5db48b", grain: "#2f8a63", light: "#a6dcbd", coast: "#237652",
    road: "#1d2a24", minor: "#2c7a57", border: "#f4efe3", text: "#16301f" };

  // numeri casuali ripetibili: la grana e i segnaposti sono uguali a ogni caricamento
  const rng = (seed) => () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

  // Grana della terra: tanti puntini casuali piu' scuri e qualcuno piu' chiaro sul verde (effetto stampa riso).
  function grainPattern() {
    const s = 2, size = 96, cv = document.createElement("canvas");
    cv.width = cv.height = size * s;
    const g = cv.getContext("2d"), r = rng(42);
    g.fillStyle = MAP_INK.land; g.fillRect(0, 0, cv.width, cv.height);
    const dots = (n, color, alpha, rad) => {
      g.fillStyle = color;
      for (let i = 0; i < n; i++) {
        g.globalAlpha = alpha * (0.45 + r() * 0.55);
        g.beginPath(); g.arc(r() * cv.width, r() * cv.height, (rad * (0.6 + r() * 0.6)) * s, 0, Math.PI * 2); g.fill();
      }
    };
    dots(2600, MAP_INK.grain, 0.55, 0.55);
    dots(900, MAP_INK.light, 0.5, 0.5);
    g.globalAlpha = 1;
    return { width: cv.width, height: cv.height, data: new Uint8Array(g.getImageData(0, 0, cv.width, cv.height).data.buffer) };
  }
  // Carta del mare: crema con grana fine e qualche fibra, disegnata nella mappa stessa (si sposta con lei).
  function paperPattern() {
    const s = 2, size = 128, cv = document.createElement("canvas");
    cv.width = cv.height = size * s;
    const g = cv.getContext("2d"), r = rng(7);
    g.fillStyle = MAP_INK.paper; g.fillRect(0, 0, cv.width, cv.height);
    for (let i = 0; i < 5200; i++) {
      g.fillStyle = r() < 0.75 ? "#8a7a5a" : "#ffffff";
      g.globalAlpha = 0.05 + r() * 0.1;
      g.fillRect(r() * cv.width, r() * cv.height, 1 + r() * 1.2, 1 + r() * 1.2);
    }
    g.strokeStyle = "#9a8865"; g.lineWidth = 0.8;
    for (let i = 0; i < 40; i++) {                       // fibre corte
      const x = r() * cv.width, y = r() * cv.height, a = r() * Math.PI, l = 6 + r() * 14;
      g.globalAlpha = 0.06 + r() * 0.06;
      g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * l / 2 + r() * 4, y + Math.sin(a) * l / 2 + r() * 4,
        x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
    }
    g.globalAlpha = 1;
    return { width: cv.width, height: cv.height, data: new Uint8Array(g.getImageData(0, 0, cv.width, cv.height).data.buffer) };
  }
  function warmStyle() {
    const set = (id, prop, val) => { try { map.setPaintProperty(id, prop, val); } catch (_) { /* proprieta' assente */ } };
    const lay = (id, prop, val) => { try { map.setLayoutProperty(id, prop, val); } catch (_) { /* proprieta' assente */ } };
    const hide = (id) => lay(id, "visibility", "none");
    const dotted = (id, color, width, gap = 2.2) => {
      lay(id, "line-cap", "round"); lay(id, "line-join", "round");
      set(id, "line-color", color); set(id, "line-width", width); set(id, "line-dasharray", [0, gap]); set(id, "line-opacity", 1);
    };
    if (!map.hasImage("land-grain")) map.addImage("land-grain", grainPattern(), { pixelRatio: 2 });
    if (!map.hasImage("sea-paper")) map.addImage("sea-paper", paperPattern(), { pixelRatio: 2 });
    // scritte della mappa nel carattere a mano del sito (glifi serviti dal sito stesso, cartella fonts/)
    try { map.setGlyphs(`${new URL(window.ANDIAMO_FONTS || "fonts/", location.href).href}{fontstack}/{range}.pbf`); } catch (_) { /* */ }
    const HIDE = /park|landcover|landuse|building|aeroway|pier|path|rail|tunnel|casing|shield|highway-name|airport|label_other|label_village|label_state|waterway_line_label|boundary_disputed|subtle/;
    for (const l of map.getStyle().layers) {
      const id = l.id;
      if (["clusters", "clusters-ink", "clusters-live", "cluster-count", "points", "points-live", "sel-live", "points-hover", "points-selected"].includes(id)) continue;
      if (l.type === "background") { set(id, "background-color", MAP_INK.land); set(id, "background-pattern", "land-grain"); }
      else if (HIDE.test(id)) hide(id);
      else if (l.type === "fill" && /water/.test(id)) { set(id, "fill-color", MAP_INK.paper); set(id, "fill-pattern", "sea-paper"); }
      else if (l.type === "line" && /waterway/.test(id)) { set(id, "line-color", MAP_INK.paper); }
      else if (/motorway/.test(id) && l.type === "line") dotted(id, MAP_INK.road, ["interpolate", ["linear"], ["zoom"], 5, 1.6, 10, 2.4, 14, 3.4], 1.7);
      else if (/highway_major/.test(id) && l.type === "line") dotted(id, MAP_INK.road, ["interpolate", ["linear"], ["zoom"], 9, 1.3, 12, 2, 16, 2.8], 1.9);
      else if (id === "highway_minor") { dotted(id, MAP_INK.minor, ["interpolate", ["linear"], ["zoom"], 13, 1.1, 16, 2], 2.2); try { map.setLayerZoomRange(id, 13, 24); } catch (_) { /* */ } }
      else if (id === "boundary_2") { dotted(id, MAP_INK.border, ["interpolate", ["linear"], ["zoom"], 3, 1.6, 8, 2.6], 2); set(id, "line-opacity", 0.85); }
      else if (id === "boundary_3") { dotted(id, MAP_INK.border, 1.3, 3); set(id, "line-opacity", 0.45); }
      else if (l.type === "line") hide(id);
      else if (l.type === "symbol") {
        lay(id, "text-font", HAND_FONT);
        if (/^label_/.test(id)) lay(id, "text-field", ["coalesce", ["get", "name:it"], ["get", "name:latin"], ["get", "name"]]);
        if (id === "label_town") { try { map.setLayerZoomRange(id, 7, 24); } catch (_) { /* */ } }   // cittadine da zoom medio
        if (/label_city/.test(id)) lay(id, "text-size", ["interpolate", ["linear"], ["zoom"], 4, 12, 8, 16, 12, 20]);
        const sea = /water/.test(id);
        set(id, "text-color", sea ? "#3d8a69" : MAP_INK.text);
        set(id, "text-halo-color", sea ? MAP_INK.paper : "rgba(244, 239, 227, .8)"); set(id, "text-halo-width", sea ? 1.2 : 2);
        set(id, "text-halo-blur", 0.8); lay(id, "text-transform", /country|state/.test(id) ? "uppercase" : "none");
        if (/country|state/.test(id)) lay(id, "text-letter-spacing", 0.12);
      }
    }
    // coste piu' scure: una riga sfumata lungo il bordo dell'acqua, sotto il mare (si vede solo dal lato della terra)
    const water = map.getLayer("water");
    if (water && !map.getLayer("coast-shade")) {
      try {
        map.addLayer({ id: "coast-shade", type: "line", source: water.source, "source-layer": water.sourceLayer || "water",
          paint: { "line-color": MAP_INK.coast, "line-opacity": 0.55,
            "line-width": ["interpolate", ["linear"], ["zoom"], 4, 5, 8, 10, 13, 16], "line-blur": ["interpolate", ["linear"], ["zoom"], 4, 5, 8, 10, 13, 16] } },
        "water");
      } catch (_) { /* stile senza acqua */ }
    }
  }

  // Icone delle categorie: tratti semplici su griglia 24x24, disegnati dentro il cerchio del segnaposto.
  const circ = (x, y, r) => `M${x - r} ${y}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`;
  const ICONS = {
    sport: "M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM7 6H4.5a2.5 2.5 0 0 0 2.5 4M17 6h2.5a2.5 2.5 0 0 1-2.5 4",
    "arte-cultura": "M3 5h18v14H3zM3 17l5-5 4 4 3-3 6 6" + circ(15.5, 9, 1.6),
    musica: "M9 18V6l11-2.5v12.5" + circ(6.5, 18, 2.5) + circ(17.5, 16, 2.5),
    "sagre-feste": "M6 3v7a2 2 0 0 0 4 0V3M8 10v11M17 21V3c-2 1.5-3 4-3 7v3h3",
    "teatro-spettacoli": "M4 4h16v7a8 8 0 0 1-16 0zM8.5 9h1.5M14 9h1.5M8.5 13.5a4.5 4.5 0 0 0 7 0",
    "famiglie-bambini": circ(12, 9, 5.5) + "M12 14.5l-1 1.5h2zM12 16c0 2-2 3-.5 5",
    "mercatini-fiere": "M5 8h14l-1.2 13H6.2zM9 8V6.5a3 3 0 0 1 6 0V8",
    business: "M3 8h18v12H3zM9 8V5.5h6V8M3 13.5h18",
    "natura-outdoor": "M5 20c0-9.5 6.5-15 15-15 0 9-5.5 15-14.5 15M5 20l8-8",
    "": "M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6-4.5-4.2 6.1-.7z",
  };
  // Segnaposti illustrati: tondo pieno con bordo d'inchiostro, ombra a puntini in basso a destra e qualche luce
  // in alto a sinistra (come la grana della terra), icona a tratto pulito. Ogni categoria ha la sua grana fissa.
  const INK = "#1d1b18";
  const seedOf = (t) => [...t].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) % 2147483646, 7) + 1;
  function grainDisc(g, cx, cy, r, color, shade, light, seed, n = 260) {
    g.save();
    g.beginPath(); g.arc(cx, cy, r, 0, Math.PI * 2); g.fillStyle = color; g.fill(); g.clip();
    const rnd = rng(seed);
    for (let i = 0; i < n; i++) {
      const a = rnd() * Math.PI * 2, d = Math.sqrt(rnd()) * r, x = Math.cos(a) * d, y = Math.sin(a) * d;
      const k = (x + y) / (r * 1.25);                       // -1 in alto a sinistra, +1 in basso a destra
      if (k > 0 && rnd() < Math.pow(k, 1.1) * 0.95) { g.fillStyle = shade; g.globalAlpha = 0.5 + rnd() * 0.35; }
      else if (k < -0.35 && rnd() < -k * 0.35) { g.fillStyle = light; g.globalAlpha = 0.45 + rnd() * 0.35; }
      else continue;
      g.beginPath(); g.arc(cx + x, cy + y, 0.35 + rnd() * 0.35, 0, Math.PI * 2); g.fill();
    }
    g.restore(); g.globalAlpha = 1;
  }
  function pinImage(color, icon, selected) {
    const s = 2, r = selected ? 20 : 17, size = (r + 3) * 2;      // tondi piu' grandi
    const cv = document.createElement("canvas");
    cv.width = cv.height = size * s;
    const g = cv.getContext("2d");
    g.scale(s, s);
    const fill = selected ? INK : color, line = selected ? color : INK, d = ICONS[icon] !== undefined ? ICONS[icon] : ICONS[""];
    grainDisc(g, size / 2, size / 2, r, fill, selected ? "#000" : "rgba(20, 16, 10, .9)", "#fff", seedOf(icon + (selected ? "s" : "")));
    g.beginPath(); g.arc(size / 2, size / 2, r, 0, Math.PI * 2);
    g.lineWidth = selected ? 2.5 : 1.6; g.strokeStyle = line; g.stroke();
    const k = (selected ? 20 : 18) / 24;
    g.translate(size / 2 - 12 * k, size / 2 - 12 * k); g.scale(k, k);
    g.lineWidth = 2.2; g.lineCap = "round"; g.lineJoin = "round"; g.strokeStyle = line;
    g.stroke(new Path2D(d));
    g.setTransform(1, 0, 0, 1, 0, 0);
    return { width: cv.width, height: cv.height, data: g.getImageData(0, 0, cv.width, cv.height).data };
  }

  // Gruppi di eventi: tondo d'inchiostro con la stessa grana, in tre grandezze (come i raggi di CLUSTER_R).
  function clusterImage(r, live) {
    const s = 2, size = (r + 4) * 2, cv = document.createElement("canvas");
    cv.width = cv.height = size * s;
    const g = cv.getContext("2d");
    g.scale(s, s);
    grainDisc(g, size / 2, size / 2, r, INK, "#000", "#8a8478", seedOf("c" + r), 420);
    g.beginPath(); g.arc(size / 2, size / 2, r, 0, Math.PI * 2);
    g.lineWidth = live ? 2.6 : 2; g.strokeStyle = live ? LIVE_COLOR : MAP_INK.paper; g.stroke();
    g.setTransform(1, 0, 0, 1, 0, 0);
    return { width: cv.width, height: cv.height, data: g.getImageData(0, 0, cv.width, cv.height).data };
  }

  // Eventi in corso: un alone morbido che "respira" piano attorno al segnaposto (un giro ogni 4 secondi),
  // con un sottile cerchio a matita che si allarga e svanisce. Niente lampeggi ne' colori d'allarme.
  const REDUCED = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function pulseImage(color, base) {
    const s = 2, size = 108, PERIOD = 4000;
    return { width: size * s, height: size * s, data: new Uint8ClampedArray(size * s * size * s * 4),
      onAdd() { const c = document.createElement("canvas"); c.width = c.height = size * s; this.g = c.getContext("2d"); },
      render() {
        const g = this.g, t = REDUCED() ? 0.3 : (performance.now() % PERIOD) / PERIOD;
        const breathe = 0.5 - 0.5 * Math.cos(t * Math.PI * 2);           // 0 -> 1 -> 0, dolce
        g.setTransform(s, 0, 0, s, 0, 0); g.clearRect(0, 0, size, size);
        g.beginPath(); g.arc(size / 2, size / 2, base + 5 + breathe * 5, 0, Math.PI * 2);
        g.fillStyle = color; g.globalAlpha = 0.16 + breathe * 0.1; g.fill();
        const ease = 1 - Math.pow(1 - t, 2), rad = base + 6 + ease * 20;
        g.beginPath(); g.arc(size / 2, size / 2, rad, 0, Math.PI * 2);
        g.globalAlpha = (1 - t) * 0.55; g.lineWidth = 1.6; g.strokeStyle = color; g.stroke();
        g.globalAlpha = 1;
        this.data = g.getImageData(0, 0, size * s, size * s).data;
        if (!REDUCED()) map.triggerRepaint();
        return true;
      } };
  }

  // Eventi in corso adesso: orario d'inizio passato e non ancora finito (senza fine: 2 ore); eventi di un giorno
  // (o di pochi giorni) senza orario: in corso tra le 9 e le 23. Le mostre lunghe non contano.
  const romeNow = () => new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Rome", year: "numeric", month: "2-digit",
    day: "2-digit", hour: "2-digit", minute: "2-digit" }).format(new Date()).replace(" ", "T");
  const plusHours = (s16, h) => new Date(new Date(s16 + ":00Z").getTime() + h * 3600000).toISOString().slice(0, 16);
  function isLive(e, now = romeNow()) {
    const day = now.slice(0, 10), sd = e.start.slice(0, 10), ed = (e.end || e.start).slice(0, 10);
    if (sd > day || ed < day) return false;
    const days = (new Date(ed) - new Date(sd)) / 86400000, hh = now.slice(11, 13);
    const daytime = days <= 3 && hh >= "09" && hh < "23";
    if (e.start.length > 10) {
      const st = e.start.slice(0, 16);
      if (e.end && e.end.length > 10) return st <= now && now <= e.end.slice(0, 16);
      if (ed > sd) return daytime && st <= now;          // piu' giorni, fine senza orario
      return st <= now && now <= plusHours(st, 2);
    }
    return daytime;
  }

  // Animazioni dei segnaposti: una proprieta' di uno strato che va da "from" a "to" con un piccolo rimbalzo.
  const ANIM = {};
  const easeBack = (x) => 1 + 2.4 * Math.pow(x - 1, 3) + 1.4 * Math.pow(x - 1, 2);
  function animateProp(layer, kind, prop, from, to, ms, make = (v) => v) {
    if (!mapReady || !map.getLayer(layer)) return;
    const set = (v) => (kind === "layout" ? map.setLayoutProperty : map.setPaintProperty).call(map, layer, prop, make(v));
    cancelAnimationFrame(ANIM[layer + prop]);
    if (REDUCED()) { set(to); return; }
    const t0 = performance.now();
    const step = (t) => {
      const x = Math.max(0, Math.min(1, (t - t0) / ms));
      set(Math.max(0, from + (to - from) * easeBack(x)));
      if (x < 1) ANIM[layer + prop] = requestAnimationFrame(step);
    };
    ANIM[layer + prop] = requestAnimationFrame(step);
  }
  function animatePin(layer, uid, from, to, ms) {
    if (!mapReady || !map.getLayer(layer)) return;
    const set = (v) => { map.setLayoutProperty(layer, "icon-size", v); setSingleOffset(layer, uid, v); };
    cancelAnimationFrame(ANIM[layer + "pin"]);
    if (REDUCED()) { set(to); return; }
    const t0 = performance.now();
    const step = (t) => {
      const x = Math.max(0, Math.min(1, (t - t0) / ms));
      set(Math.max(0, from + (to - from) * easeBack(x)));
      if (x < 1) ANIM[layer + "pin"] = requestAnimationFrame(step);
    };
    ANIM[layer + "pin"] = requestAnimationFrame(step);
  }
  const CLUSTER_R = (k) => ["*", k, ["step", ["get", "point_count"], 19, 10, 24, 40, 30]];
  function popIn() {
    animateProp("points", "layout", "icon-size", 0.35, 1, 460);
    animateProp("clusters", "paint", "circle-radius", 0.35, 1, 460, CLUSTER_R);
    animateProp("clusters-ink", "layout", "icon-size", 0.35, 1, 460);
  }

  // Suoni di carta e di cose vere, sintetizzati (nessun file): timbro sul foglio, foglio che si apre e si ripiega,
  // matita che segna, gomma che cancella, scatto di una levetta. Rumore filtrato e colpi sordi, niente bip.
  // Si possono spegnere dal pulsante con l'altoparlante.
  const Sound = {
    ctx: null, out: null, noise: null,
    on: (() => { try { return localStorage.getItem("andiamo-suoni") !== "0"; } catch (_) { return true; } })(),
    init() {
      if (this.ctx) return;
      const c = this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      // compressore: suoni pieni e decisi, mai fastidiosi
      const comp = c.createDynamicsCompressor();
      comp.threshold.value = -18; comp.knee.value = 12; comp.ratio.value = 4; comp.attack.value = 0.002; comp.release.value = 0.12;
      this.out = c.createGain(); this.out.gain.value = 0.9;
      this.out.connect(comp).connect(c.destination);
      // 2 secondi di rumore "rosa" (piu' morbido del bianco): la materia prima di carta, matita e gomma
      const len = c.sampleRate * 2, buf = c.createBuffer(1, len, c.sampleRate), d = buf.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0;
      for (let i = 0; i < len; i++) {
        const w = Math.random() * 2 - 1;
        b0 = 0.99765 * b0 + w * 0.099; b1 = 0.963 * b1 + w * 0.2965; b2 = 0.57 * b2 + w * 1.0527;
        d[i] = (b0 + b1 + b2 + w * 0.1848) * 0.22;
      }
      this.noise = buf;
    },
    // rumore filtrato con inviluppo: type/freq del filtro, sweep opzionale della frequenza
    rustle(t, dur, { freq = 2000, to = null, q = 0.9, type = "bandpass", gain = 0.5, attack = 0.004 } = {}) {
      const c = this.ctx, src = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain();
      src.buffer = this.noise; src.playbackRate.value = 0.9 + Math.random() * 0.2;
      f.type = type; f.Q.value = q; f.frequency.setValueAtTime(freq, t);
      if (to) f.frequency.exponentialRampToValueAtTime(to, t + dur);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + attack);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      src.connect(f).connect(g).connect(this.out);
      src.start(t, Math.random() * 1.5); src.stop(t + dur + 0.05);
    },
    // colpo sordo (legno, timbro sul tavolo): sinusoide che scende veloce
    thud(t, { freq = 150, to = 55, dur = 0.12, gain = 0.6 } = {}) {
      const c = this.ctx, o = c.createOscillator(), g = c.createGain();
      o.type = "sine"; o.frequency.setValueAtTime(freq, t); o.frequency.exponentialRampToValueAtTime(to, t + dur);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + 0.003);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(this.out); o.start(t); o.stop(t + dur + 0.02);
    },
    // "pop" tondo: sinusoide breve che scivola di tono, con un attacco morbido (bocca che schiocca, bolla)
    pop(t, { from = 400, to = 800, dur = 0.11, gain = 0.45 } = {}) {
      const c = this.ctx, o = c.createOscillator(), g = c.createGain(), f = c.createBiquadFilter();
      o.type = "sine"; o.frequency.setValueAtTime(from, t); o.frequency.exponentialRampToValueAtTime(to, t + dur * 0.55);
      f.type = "lowpass"; f.frequency.value = 2200;
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + 0.006);
      g.gain.exponentialRampToValueAtTime(gain * 0.35, t + dur * 0.5); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(f).connect(g).connect(this.out); o.start(t); o.stop(t + dur + 0.02);
    },
    play(name) {
      if (!this.on) return;
      try {
        this.init();
        if (this.ctx.state === "suspended") this.ctx.resume();
        const t = this.ctx.currentTime + 0.01;
        // solo carta e grafite: nessun colpo grave (niente "tamburo")
        if (name === "select") {                         // puntina appoggiata sulla carta
          this.rustle(t, 0.035, { freq: 3000, q: 1.6, gain: 0.3, attack: 0.002 });
          this.rustle(t + 0.01, 0.03, { freq: 5200, q: 2.5, gain: 0.12, attack: 0.002 });
        } else if (name === "expand") {                  // foglio che si apre
          this.rustle(t, 0.3, { freq: 900, to: 3800, q: 0.7, gain: 0.4, attack: 0.04 });
          this.rustle(t + 0.2, 0.07, { freq: 3400, q: 2, gain: 0.22 });
        } else if (name === "close") {                   // foglio che si ripiega
          this.rustle(t, 0.2, { freq: 3600, to: 1200, q: 0.8, gain: 0.36, attack: 0.02 });
          this.rustle(t + 0.17, 0.05, { freq: 2400, q: 1.4, gain: 0.16 });
        } else if (name === "chip") {                    // scatto secco di carta
          this.rustle(t, 0.022, { freq: 4400, q: 3, gain: 0.38, attack: 0.001 });
        } else if (name === "save-on") {                 // "pop" tondo, come una bolla che scoppia (verso l'alto)
          this.pop(t, { from: 340, to: 760, dur: 0.11, gain: 0.5 });
        } else if (name === "save-off") {                // "pop" piu' basso e morbido (verso il basso)
          this.pop(t, { from: 520, to: 240, dur: 0.12, gain: 0.4 });
        }
      } catch (_) { /* audio non disponibile */ }
    },
    toggle() {
      this.on = !this.on;
      try { localStorage.setItem("andiamo-suoni", this.on ? "1" : "0"); } catch (_) { /* privato */ }
      renderSoundBtn();
      if (this.on) this.play("chip");
    },
  };
  function renderSoundBtn() {
    const b = $("#sound");
    if (!b) return;
    b.setAttribute("aria-pressed", String(Sound.on));
    b.setAttribute("aria-label", Sound.on ? "Disattiva i suoni" : "Attiva i suoni");
    b.title = Sound.on ? "Suoni attivi" : "Suoni spenti";
    b.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/>${Sound.on
      ? '<path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>' : '<path d="M17 9l5 6M22 9l-5 6"/>'}</svg>`;
  }

  // Spazio occupato dai pannelli sopra la mappa: serve a centrare i punti nella parte visibile.
  function mapPadding(extraBottom = 0) {
    if (MOBILE()) {
      const top = $(".filters").getBoundingClientRect().bottom + 40;
      // l'elenco non sta piu' sopra la mappa: in basso restano solo i controlli
      return { top, bottom: 60 + extraBottom, left: 30, right: 70 };
    }
    return { top: Math.round($(".chips-row").getBoundingClientRect().bottom) + 30, bottom: 120, left: 60, right: 90 };
  }

  // Margini trasformati in spostamento del centro. Non si passa mai "padding" a easeTo/flyTo: MapLibre lo terrebbe
  // anche per i movimenti successivi, e zoom e confini si sfaserebbero.
  function padOffset(p) { return [Math.round((p.left - p.right) / 2), Math.round((p.top - p.bottom) / 2)]; }

  const SHEET_MIN = 34;                      // telefono: altezza dell'elenco ridotto alla sola maniglia

  // Zona della mappa davvero visibile (fuori da testata, giorni, filtri, elenco).
  function visibleArea() {
    const r = $("#map").getBoundingClientRect();
    const v = { left: r.left + 12, right: r.right - 12, top: r.top + 12, bottom: r.bottom - 12 };
    if (MOBILE()) {
      v.top = $(".filters").getBoundingClientRect().bottom + 10;
      // con la card aperta l'elenco scende fino a lasciare solo la maniglia (la posizione finale, non quella animata)
      v.bottom = Math.min(v.bottom, window.innerHeight - 12);
    } else {
      // colonna libera a destra di elenco e filtri di accesso, fino al fondo della mappa
      v.top = $(".chips-row").getBoundingClientRect().bottom + 12;
      v.left = Math.max((state.sidebarHidden ? $("#list-toggle") : $("#panel")).getBoundingClientRect().right,
        $(".filters").getBoundingClientRect().right) + 12;
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
    const box = { left: c.left, right: c.right, top: c.top, bottom: c.bottom + 46 };   // + segnaposto sotto la card
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
      dragRotate: false, pitchWithRotate: false, touchPitch: false, renderWorldCopies: false,
    });
    map.touchZoomRotate.disableRotation();
    // Allontanandosi si arriva al massimo a tutta l'Italia: zoom minimo = quello che fa stare l'Italia nella parte
    // visibile della mappa; i confini di spostamento sono l'Italia con un po' di mare, allargati quanto serve perche'
    // a zoom minimo la finestra ci stia (ricalcolati quando cambia la dimensione della finestra).
    const ITALY = [[6.6, 35.4], [18.6, 47.1]];
    const merc = (lat) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
    const unmerc = (y) => ((2 * Math.atan(Math.exp(y)) - Math.PI / 2) * 180) / Math.PI;
    const fitLimits = () => {
      let cam = null;
      try { cam = map.cameraForBounds(ITALY, { padding: mapPadding() }); } catch (_) { cam = null; }
      if (!cam) cam = map.cameraForBounds(ITALY, { padding: 10 });
      if (!cam) return;
      const z = Math.max(0, cam.zoom), el = map.getContainer();
      const scale = 512 * Math.pow(2, z) / 1.02;                   // 2% di margine sui conti
      const lonSpan = (el.clientWidth * 360) / scale, ySpan = (el.clientHeight * 2 * Math.PI) / scale;
      // centro della finestra quando l'Italia sta tutta nella parte visibile (a destra dell'elenco, sotto i filtri)
      const c = cam.center ? maplibregl.LngLat.convert(cam.center) : null;
      const lonC = c ? c.lng : 12.6, yC = c ? merc(c.lat) : (merc(35.4) + merc(47.1)) / 2;
      map.setMaxBounds(null);
      map.setMinZoom(z);
      map.setMaxBounds([[Math.min(5, lonC - lonSpan / 2), Math.max(-80, Math.min(34.3, unmerc(yC - ySpan / 2)))],
        [Math.max(20.2, lonC + lonSpan / 2), Math.min(80, Math.max(48, unmerc(yC + ySpan / 2)))]]);
    };
    map.once("load", fitLimits);
    map.on("resize", fitLimits);
    // + e -: si avvicina e si allontana attorno al centro della parte di mappa davvero visibile (non sotto i pannelli)
    const zoomBy = (d) => {
      const v = visibleArea(), r = $("#map").getBoundingClientRect();
      const around = map.unproject([(v.left + v.right) / 2 - r.left, (v.top + v.bottom) / 2 - r.top]);
      map.easeTo({ zoom: Math.max(map.getMinZoom(), Math.min(map.getMaxZoom(), map.getZoom() + d)), around, duration: 300 });
    };
    $("#zoom-in").addEventListener("click", () => zoomBy(1));
    renderSoundBtn();
    $("#sound").addEventListener("click", () => Sound.toggle());
    setInterval(() => {                      // ogni minuto: gli eventi iniziano e finiscono
      const now = romeNow(), next = new Set(EVENTS.filter((e) => matches(e) && isLive(e, now)).map((e) => e.uid));
      if (next.size !== LIVE.size || [...next].some((u) => !LIVE.has(u))) update();
    }, 60000);
    $("#zoom-out").addEventListener("click", () => zoomBy(-1));
    map.once("style.load", () => {        // subito, senza aspettare tutte le tessere
      warmStyle();
      DATA.categories.forEach((c) => {
        map.addImage(`pin-${c.id}`, pinImage(c.color, c.id, false), { pixelRatio: 2 });
        map.addImage(`pin-sel-${c.id}`, pinImage(c.color, c.id, true), { pixelRatio: 2 });
        map.addImage(`pulse-${c.id}`, pulseImage(c.color, 17), { pixelRatio: 2 });
      });
      map.addImage("pulse-cluster", pulseImage(LIVE_COLOR, 22), { pixelRatio: 2 });
      for (const r of [19, 24, 30]) {
        map.addImage(`cl-${r}`, clusterImage(r, false), { pixelRatio: 2 });
        map.addImage(`cl-${r}-live`, clusterImage(r, true), { pixelRatio: 2 });
      }
      map.addSource("ev", { type: "geojson", data: geojson([]), cluster: true, clusterRadius: 40, clusterMaxZoom: 13,
        clusterProperties: { live: ["max", ["case", ["==", ["get", "live"], true], 1, 0]] } });
      const ring = (prefix) => ({ "icon-image": ["concat", prefix, ["get", "category"]], "icon-allow-overlap": true,
        "icon-ignore-placement": true, "icon-offset": SLOT_EXPR });
      map.addLayer({ id: "clusters-live", type: "symbol", source: "ev", filter: ["all", ["has", "point_count"], [">", ["get", "live"], 0]],
        layout: { "icon-image": "pulse-cluster", "icon-allow-overlap": true, "icon-ignore-placement": true } });
      map.addLayer({ id: "points-live", type: "symbol", source: "ev",
        filter: ["all", ["!", ["has", "point_count"]], ["==", ["get", "live"], true]], layout: ring("pulse-") });
      map.addLayer({ id: "clusters", type: "circle", source: "ev", filter: ["has", "point_count"],
        // il cerchio resta solo come area da toccare: si vede il tondo a mano dello strato sopra
        paint: { "circle-color": INK, "circle-radius": CLUSTER_R(1), "circle-opacity": 0, "circle-stroke-width": 0 } });
      map.addLayer({ id: "clusters-ink", type: "symbol", source: "ev", filter: ["has", "point_count"],
        layout: { "icon-image": ["concat", "cl-", ["step", ["get", "point_count"], "19", 10, "24", 40, "30"],
          ["case", [">", ["get", "live"], 0], "-live", ""]], "icon-allow-overlap": true, "icon-ignore-placement": true } });
      map.addLayer({ id: "cluster-count", type: "symbol", source: "ev", filter: ["has", "point_count"],
        layout: { "text-field": ["get", "point_count_abbreviated"], "text-size": 18, "text-font": HAND_FONT,
          "text-allow-overlap": true, "text-ignore-placement": true },
        paint: { "text-color": "#fff" } });
      const icon = (prefix) => ["concat", prefix, ["get", "category"]];
      map.addLayer({ id: "points", type: "symbol", source: "ev", filter: pointsFilter(""),
        layout: { "icon-image": icon("pin-"), "icon-allow-overlap": true, "icon-ignore-placement": true, "icon-offset": SLOT_EXPR } });
      // evidenziato e selezionato vivono in sorgenti separate, non raggruppate: restano visibili sopra i gruppi
      map.addSource("hov", { type: "geojson", data: geojson([], true) });
      map.addSource("sel", { type: "geojson", data: geojson([], true) });
      map.addLayer({ id: "sel-live", type: "symbol", source: "sel", filter: ["==", ["get", "live"], true], layout: ring("pulse-") });
      map.addLayer({ id: "points-hover", type: "symbol", source: "hov",
        layout: { "icon-image": icon("pin-"), "icon-size": 1.25, "icon-allow-overlap": true, "icon-ignore-placement": true } });
      map.addLayer({ id: "points-selected", type: "symbol", source: "sel",
        layout: { "icon-image": icon("pin-sel-"), "icon-size": 1.15, "icon-allow-overlap": true, "icon-ignore-placement": true } });
      // nomi delle citta' sotto i segnaposti (i tondi restano sempre in vista), spostati di lato rispetto al punto
      // della citta', cosi' finiscono accanto ai tondi e non sotto
      for (const id of ["label_town", "label_city", "label_city_capital"]) {
        if (!map.getLayer(id)) continue;
        try {
          map.setLayoutProperty(id, "text-variable-anchor", ["top", "bottom", "right", "left"]);
          map.setLayoutProperty(id, "text-radial-offset", 1.75);
          map.setLayoutProperty(id, "text-justify", "auto");
          map.moveLayer(id, "clusters-live");
        } catch (_) { /* stile senza questo strato */ }
      }

      map.on("click", "clusters", (ev) => {
        const f = ev.features[0];
        Sound.play("expand");
        map.getSource("ev").getClusterExpansionZoom(f.properties.cluster_id).then((z) =>
          map.easeTo({ center: f.geometry.coordinates, zoom: z + 0.3, offset: padOffset(mapPadding()) }));
      });
      map.on("click", "points", (ev) => {
        // segnaposti vicini: si apre quello piu' vicino al clic; l'elenco "in questo punto" solo se sono
        // davvero uno sopra l'altro (stessa posizione sullo schermo)
        const seen = new Set(), hits = [];
        for (const f of ev.features) {
          const uid = f.properties.uid;
          if (seen.has(uid)) continue;
          seen.add(uid);
          const p = map.project(f.geometry.coordinates), o = SLOTS[f.properties.slot || 0] || [0, 0];
          p.x += o[0]; p.y += o[1];
          hits.push({ uid, p, d: Math.hypot(p.x - ev.point.x, p.y - ev.point.y) });
        }
        hits.sort((a, b) => a.d - b.d);
        const near = hits[0];
        const stacked = hits.filter((h) => Math.hypot(h.p.x - near.p.x, h.p.y - near.p.y) < 4);
        if (state.detail) closeDetail({ keepHistory: true });          // altro evento: la scheda torna elenco
        Sound.play(stacked.length === 1 ? "select" : "expand");
        if (stacked.length === 1) {
          if (onlyUids) { onlyUids = null; update(); }
          if (MOBILE()) setSheet("peek");
          select(near.uid, { fly: false, detail: false });
        } else { onlyUids = new Set(stacked.map((h) => h.uid)); closeCard(); update(); setSheet("half"); }
      });
      // "−" sul segnaposto aperto, o clic fuori: chiude la card e la sidebar torna all'elenco
      map.on("click", "points-selected", () => { Sound.play("close"); closeAll(); });
      map.on("click", (ev) => {
        if (map.queryRenderedFeatures(ev.point, { layers: ["points", "clusters", "points-selected"] }).length) return;
        if (onlyUids) { onlyUids = null; update(); }                  // l'elenco torna a tutti gli eventi
        if (popup || state.detail) { Sound.play("close"); closeAll(); }
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
      if (state.selected) select(state.selected, { fly: true, fromHistory: true });
    });
  }

  function pointsFilter(selUid) {
    return ["all", ["!", ["has", "point_count"]], ["!=", ["get", "uid"], selUid]];
  }

  function geojson(items, keepCoords) {
    const feat = (e) => ({ type: "Feature", properties: { uid: e.uid, category: e.category, live: LIVE.has(e.uid),
      slot: SLOT[e.uid] || 0 }, geometry: { type: "Point", coordinates: COORDS[e.uid] || [e.lon, e.lat] } });
    if (keepCoords) return { type: "FeatureCollection", features: items.map(feat) };
    // stesso posto = stesso punto entro ~10 m; i posti si assegnano in ordine di data (i primi al centro)
    const groups = {};
    items.forEach((e) => { (groups[`${e.lat.toFixed(4)},${e.lon.toFixed(4)}`] ||= []).push(e); });
    Object.values(groups).forEach((g) => {
      g.sort((a, b) => (a.start + a.uid).localeCompare(b.start + b.uid));
      g.forEach((e, i) => { COORDS[e.uid] = [g[0].lon, g[0].lat]; SLOT[e.uid] = i < SLOTS.length ? i : SLOTS.length - 1; });
    });
    return { type: "FeatureCollection", features: items.map(feat) };
  }
  // scarto in pixel per lo strato dei punti (dal posto della feature); negli strati con un solo punto si usa
  // il valore fisso diviso per la dimensione dell'icona (icon-offset si moltiplica per icon-size)
  const SLOT_EXPR = ["match", ["get", "slot"], ...SLOTS.slice(1).flatMap((o, i) => [i + 1, ["literal", o]]), ["literal", [0, 0]]];
  function setSingleOffset(layer, uid, size) {
    if (!mapReady || !map.getLayer(layer)) return;
    const [x, y] = slotOff(uid);
    map.setLayoutProperty(layer, "icon-offset", [x / size, y / size]);
  }

  const byUid = (uid) => (uid ? EVENTS.filter((e) => e.uid === uid) : []);
  function hover(uid) {
    if (!mapReady) return;
    map.getSource("hov").setData(geojson(byUid(uid), true));
    if (uid) animatePin("points-hover", uid, 1, 1.3, 260);
  }

  // ---------------------------------------------------------------- card completa: popup sulla mappa e vista lista
  // Tutte le informazioni dell'evento, con data e orario in evidenza; "Scopri di piu'" porta alla fonte ufficiale.
  function buildCard(e, opts = {}) {
    const c = CAT[e.category] || { label: "Evento", color: "#ddd" };
    const sub = (c.sub || {})[e.subcategory];
    const el = document.createElement(opts.tag || "div");
    el.className = "card full" + (opts.popup ? " in-popup" : "");
    el.style.setProperty("--c", c.color);
    const d0 = parseDay(e.start), t0 = timeOf(e);
    const sameDayEnd = e.end && e.end.slice(0, 10) === e.start.slice(0, 10) && e.end.length > 10 ? e.end.slice(11, 16) : "";
    const multiDay = e.end && e.end.slice(0, 10) !== e.start.slice(0, 10);
    const timeLine = t0 ? (sameDayEnd ? `dalle ${t0} alle ${sameDayEnd}` : `ore ${t0}`) : (multiDay ? "" : "orario da verificare");
    const untilLine = multiDay ? `fino a ${dayLabel(parseDay(e.end)).toLowerCase()}` : "";
    const g = accessGroup(e);
    const price = /^(sconosciut|non (indicat|specificat|disponibil)|n\/?d|nd|-|\?)/i.test((e.price || "").trim()) ? "" : e.price;
    const dist = kmText(km(e));
    const place2 = [e.address, e.venue ? e.town : ""].filter(Boolean).join(", ");
    const host = e.action_url ? new URL(e.action_url).hostname.replace(/^www\./, "") : "";
    const dirs = `https://www.google.com/maps/dir/?api=1&destination=${e.geo_precision === "town"
      ? encodeURIComponent([e.venue, e.address, e.town].filter(Boolean).join(", ")) : `${e.lat},${e.lon}`}`;
    // in cima a sinistra solo OGGI / DOMANI (e "In corso"); per gli altri giorni niente, la data e' sotto
    const diff = Math.round((d0 - today()) / 86400000);
    const tags = (LIVE.has(e.uid) ? '<span class="live-tag">In corso</span>' : "")
      + (diff <= 0 && !LIVE.has(e.uid) ? '<span class="day-tag">Oggi</span>' : diff === 1 ? '<span class="day-tag">Domani</span>' : "");
    el.innerHTML = `
      ${favButton(e, "fav")}
      ${tags ? `<div class="card-top">${tags}</div>` : ""}
      <div class="card-when">
        <strong class="w-day">${esc(plainDay(d0))}</strong>${timeLine ? `<span class="t">${esc(timeLine)}</span>` : ""}${untilLine ? `<span class="u">${esc(untilLine)}</span>` : ""}
      </div>
      ${opts.inline ? "" : `<h3>${esc(e.title)}</h3>`}
      ${opts.inline ? "" : `<p class="card-place"><b>${esc(e.venue || e.town)}</b>${place2 ? `<br>${esc(place2)}` : ""}${dist ? `<br><span class="muted">${dist} da te</span>` : ""}</p>`}
      <div class="card-acc">${accessBadge(e)}${price ? `<span>${esc(price)}</span>` : ""}</div>
      ${e.summary ? `<p class="card-desc">${esc(e.summary)}</p>` : ""}
      ${e.ticket_url && e.ticket_url !== e.action_url ? `<p class="card-src">Iscrizioni su <a href="${attr(e.ticket_url)}" target="_blank" rel="noopener">${esc(new URL(e.ticket_url).hostname.replace(/^www\./, ""))}</a></p>` : ""}
      <div class="card-actions">
        <a class="more" href="${attr(e.action_url)}" target="_blank" rel="noopener" title="Fonte: ${esc(host)}" aria-label="Scopri di più su ${esc(host)}">Scopri di più <i aria-hidden="true">↗</i></a>
        <button class="mini" type="button" data-ics aria-label="Aggiungi al calendario" title="Aggiungi al calendario"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg></button>
        <a class="mini" href="${attr(dirs)}" target="_blank" rel="noopener" aria-label="Indicazioni" title="Indicazioni"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
        <button class="mini" type="button" data-share aria-label="Condividi" title="Condividi"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3M7.5 7.5 12 3l4.5 4.5M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg></button>
      </div>
      <button class="report-link" type="button" data-report>Segnala una modifica</button>`;
    el.querySelector("[data-fav]").addEventListener("click", (ev) => { ev.stopPropagation(); toggleFav(e.uid); });
    el.querySelector("[data-ics]").addEventListener("click", () => downloadIcs(e));
    el.querySelector("[data-share]").addEventListener("click", () => share(e));
    el.querySelector("[data-report]").addEventListener("click", () => openReport(e));
    if (opts.onPlace && el.querySelector(".card-place")) {
      const pl = el.querySelector(".card-place");
      pl.classList.add("link"); pl.title = "Mostra sulla mappa";
      pl.addEventListener("click", () => opts.onPlace(e));
    }
    return el;
  }

  function showCard(e, opts = {}) {
    const el = buildCard(e, { popup: true });
    if (popup) popup.remove();
    const [ox, oy] = slotOff(e.uid);
    popup = new maplibregl.Popup({ className: "ev-card", closeButton: false, closeOnClick: false, focusAfterOpen: false, anchor: "bottom", offset: [ox, oy - 26], maxWidth: "none" })
      .setLngLat(COORDS[e.uid] || [e.lon, e.lat]).setDOMContent(el).addTo(map);
    fitTitle(el.querySelector("h3"));
    markSelected(e.uid);
    if (!opts.noReveal) requestAnimationFrame(() => ensureCardVisible());
  }

  // Margini per centrare un punto con la card aperta: il punto finisce nella parte bassa della zona visibile,
  // la card sopra di lui resta tutta sotto testata e filtri.
  function cardPadding() {
    const pad = mapPadding(), el = popup && popup.getElement();
    if (!el) return pad;
    const v = visibleArea(), r = $("#map").getBoundingClientRect(), h = el.getBoundingClientRect().height;
    const top = Math.round(v.top - r.top + h + 28), bottom = Math.round(r.bottom - v.bottom + 22);
    // card piu' alta dello spazio: conta che si veda dall'inizio, il segnaposto puo' finire sotto l'elenco
    return { ...pad, top, bottom: top + bottom > r.height - 2 ? Math.max(0, r.height - top) : bottom };
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
    map.setFilter("points-live", ["all", ["!", ["has", "point_count"]], ["==", ["get", "live"], true], ["!=", ["get", "uid"], uid || ""]]);
    if (uid) { setSingleOffset("sel-live", uid, 1); animatePin("points-selected", uid, 0.55, 1.1, 420); }
  }

  function closeCard() {
    if (popup) { popup.remove(); popup = null; }
    if (MOBILE() && $("#panel").dataset.sheet === "min") setSheet("peek");
    markSelected("");
  }

  // ---------------------------------------------------------------- selezione e cronologia
  // opts: fly (centra la mappa), detail (apre la scheda), reveal (porta il punto nella zona visibile),
  //       fromHistory (chiamata dal tasto indietro/avanti: non tocca la cronologia)
  function select(uid, opts = {}) {
    const e = uid && EVENTS.find((x) => x.uid === uid);
    if (!e) { closeDetail(); return; }
    opts = { ...opts, detail: false };       // V1: tutte le informazioni stanno nella card sulla mappa
    if (state.view === "list") setView("map", { keep: true });
    if (MOBILE()) setSheet("min");          // la card ha bisogno di tutto lo schermo: l'elenco scende
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
        map.once("moveend", () => ensureCardVisible());     // prima del volo: se il salto e' immediato, moveend arriva subito
        map.flyTo({ center, zoom: Math.max(map.getZoom(), 14.2), speed: 2, maxDuration: 2200, offset: padOffset(cardPadding()) });
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
    if (onlyUids) { onlyUids = null; if (!state.detail) update(); }
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
    if (uid) select(uid, { fly: true, fromHistory: true });
    else closeDetail({ fromHistory: true });
  });

  // ---------------------------------------------------------------- pannello trascinabile (telefono)
  function setSheet(name) {
    const p = $("#panel");
    if (!MOBILE()) { p.dataset.sheet = "half"; return; }
    if (name === "half") name = "full";      // su telefono solo due posizioni: chiuso in basso o aperto del tutto
    p.dataset.sheet = name;
    p.style.removeProperty("--sheet-y");
    $("#sheet-toggle").setAttribute("aria-expanded", String(name === "full"));
    $("#sheet-toggle").setAttribute("aria-label", name === "full" ? "Riduci l'elenco" : "Apri l'elenco");
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
      if (!MOBILE() || state.view === "list" || (ev.target.closest && ev.target.closest(".sort, .near"))) return;   // in lista si scorre e basta
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
      else target = ["peek", "min"].includes(p.dataset.sheet) ? "peek" : "full";
      setSheet(target);
    }
    // Pannello aperto: trascinando verso il basso da un punto qualsiasi del contenuto (quando e' gia'
    // in cima) il pannello segue il dito e si chiude; verso l'alto il contenuto scorre normalmente.
    const body = $("#panel-body");
    let tY = 0, tStart = 0, tLastY = 0, tLastT = 0, tVel = 0, tDrag = false, tActive = false;
    body.addEventListener("touchstart", (ev) => {
      tActive = MOBILE() && state.view !== "list" && p.dataset.sheet === "full" && ev.touches.length === 1;
      tDrag = false;
      if (!tActive) return;
      tY = tLastY = ev.touches[0].clientY; tLastT = performance.now(); tVel = 0;
      tStart = currentOffset();
    }, { passive: true });
    body.addEventListener("touchmove", (ev) => {
      if (!tActive) return;
      const y = ev.touches[0].clientY, dy = y - tY;
      if (!tDrag) {
        if (body.scrollTop > 0 || dy <= 6) { if (dy < -6 || body.scrollTop > 0) tActive = false; return; }
        tDrag = true; p.classList.add("dragging");
      }
      ev.preventDefault();                       // il contenuto non scorre mentre si trascina il pannello
      const now = performance.now();
      tVel = (y - tLastY) / Math.max(1, now - tLastT); tLastY = y; tLastT = now;
      p.style.setProperty("--sheet-y", `${Math.min(Math.max(0, tStart + dy - 6), offsetOf("peek"))}px`);
    }, { passive: false });
    const tEnd = () => {
      if (!tDrag) { tActive = false; return; }
      tDrag = tActive = false;
      p.classList.remove("dragging");
      const moved = currentOffset() - tStart;
      setSheet(tVel > 0.25 || moved > 50 ? "peek" : "full");
    };
    body.addEventListener("touchend", tEnd);
    body.addEventListener("touchcancel", tEnd);

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
      setPlace({ lat: pos.coords.latitude, lon: pos.coords.longitude }, null, { gps: true });
      if (mapReady) {
        if (!meMarker) { const d = document.createElement("div"); d.className = "me-dot"; meMarker = new maplibregl.Marker({ element: d }); }
        meMarker.setLngLat([state.me.lon, state.me.lat]).addTo(map);
        map.flyTo({ center: [state.me.lon, state.me.lat], zoom: 11, offset: padOffset(mapPadding()), speed: 1.4 });
      }
      update();
      if (MOBILE() && !state.detail) setSheet("half");
    }, (err) => {
      btn.classList.remove("busy");
      toast(err.code === 1 ? "Per vedere gli eventi vicini consenti l'accesso alla posizione" : "Posizione non trovata, riprova");
    }, { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 });
  }

  // ---------------------------------------------------------------- "Vicino a ..." (vista lista)
  // Di default la lista e' ordinata per vicinanza: alla posizione del telefono/computer, oppure al comune scritto a mano
  // (ricordato su questo dispositivo). Il nome viene dal comune piu' vicino (docs/data/comuni.json).
  let TOWNS = null;
  const loadTowns = () => TOWNS || (TOWNS = fetch(new URL("comuni.json", new URL(window.ANDIAMO_DATA || "data/events.json", location.href)))
    .then((r) => r.json()).catch(() => []));
  const fold = (t) => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/['’`]/g, " ").replace(/\s+/g, " ").trim();
  async function nearestTown(lat, lon) {
    const rows = await loadTowns();
    let best = null, bd = Infinity;
    const k = Math.cos(lat * Math.PI / 180);
    for (const t of rows) { const d = (t[2] - lat) ** 2 + ((t[3] - lon) * k) ** 2; if (d < bd) { bd = d; best = t; } }
    return best && bd < 0.5 ? best[0] : null;                       // oltre ~70 km: fuori dall'Italia
  }
  function setPlace(me, name, opts = {}) {
    state.me = me; state.place = name; state.sort = "distance";
    if (opts.save) { try { localStorage.setItem("andiamo-luogo", JSON.stringify({ ...me, name })); } catch (_) { /* privato */ } }
    if (opts.gps) { try { localStorage.removeItem("andiamo-luogo"); } catch (_) { /* privato */ } }
    if (!name) nearestTown(me.lat, me.lon).then((n) => { if (state.me === me) { state.place = n || "la tua posizione"; renderSortBtn(); } });
    update();
  }
  const RMAX = 205;                               // ultima posizione del cursore = tutta Italia
  const ALL_IT = () => state.radius >= RMAX;
  function renderSortBtn() {
    const b = $("#sort-btn");
    const on = state.sort === "distance" && !!state.me;
    b.setAttribute("aria-pressed", String(on));
    b.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg><span>${
      on ? (ALL_IT() ? `Tutta Italia da ${esc(state.place || "…")}` : `Entro ${state.radius} km da ${esc(state.place || "…")}`) : state.me ? "Per data" : "Vicino a…"}</span>`;
    const r = $("#near-radius");
    if (r) {
      r.textContent = ALL_IT() ? "Tutta Italia" : `${state.radius} km`;
      const rg = $("#near-range");
      rg.value = String(Math.min(RMAX, state.radius));
      rg.style.setProperty("--p", `${((Math.min(RMAX, state.radius) - 5) / (RMAX - 5)) * 100}%`);
      $("#near-less").disabled = state.radius <= 5; $("#near-more").disabled = ALL_IT();
    }
    b.title = "Cambia il luogo";
  }
  // prima apertura della lista: posizione salvata, altrimenti quella del dispositivo (se l'utente la concede)
  let askedPlace = false;
  function ensurePlace() {
    if (state.me || askedPlace) return;
    askedPlace = true;
    try { const saved = JSON.parse(localStorage.getItem("andiamo-luogo") || "null"); if (saved && saved.lat) { setPlace({ lat: saved.lat, lon: saved.lon }, saved.name); return; } } catch (_) { /* */ }
    if (!navigator.geolocation) { openNear(); return; }
    navigator.geolocation.getCurrentPosition((pos) => setPlace({ lat: pos.coords.latitude, lon: pos.coords.longitude }, null),
      () => openNear(), { enableHighAccuracy: false, timeout: 10000, maximumAge: 600000 });
  }
  function openNear(open = true) {
    const pop = $("#near-pop");
    pop.hidden = !open;
    $("#sort-btn").setAttribute("aria-expanded", String(open));
    if (open) { $("#near-q").value = ""; renderNearList(""); setTimeout(() => $("#near-q").focus(), 30); loadTowns(); }
  }
  async function renderNearList(q) {
    const ul = $("#near-list"), f = fold(q);
    if (f.length < 2) { ul.innerHTML = `<li class="near-hint">Scrivi almeno due lettere del comune</li>`; return; }
    const rows = await loadTowns();
    if (fold($("#near-q").value) !== f) return;                     // nel frattempo l'utente ha scritto altro
    const starts = [], has = [];
    for (const t of rows) { const n = fold(t[0]); if (n.startsWith(f)) starts.push(t); else if (n.includes(f)) has.push(t); if (starts.length >= 8) break; }
    const hits = [...starts, ...has].slice(0, 8);
    ul.innerHTML = hits.length ? hits.map((t, i) => `<li><button type="button" role="option" data-i="${i}">${esc(t[0])} <small>${esc(t[1])}</small></button></li>`).join("")
      : `<li class="near-hint">Nessun comune trovato</li>`;
    ul.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      const t = hits[+b.dataset.i];
      Sound.play("chip"); openNear(false);
      setPlace({ lat: t[2], lon: t[3] }, t[0], { save: true });
      toast(`Eventi ordinati per distanza da ${t[0]}`);
    }));
  }
  function setupNear() {
    $("#sort-btn").addEventListener("click", (ev) => { ev.stopPropagation(); Sound.play("chip"); openNear($("#near-pop").hidden); });
    $("#near-q").addEventListener("input", (ev) => renderNearList(ev.target.value));
    $("#near-q").addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") { const b = $("#near-list button"); if (b) b.click(); }
      if (ev.key === "Escape") openNear(false);
    });
    $("#near-gps").addEventListener("click", () => { openNear(false); locate(); });
    $("#near-date").addEventListener("click", () => { openNear(false); state.sort = "date"; update(); });
    const setR = (v) => {                          // raggio a scalini di 5 km, da 5 a 200; in fondo "tutta Italia"
      state.radius = Math.min(RMAX, Math.max(5, Math.round(v / 5) * 5)); state.sort = "distance";
      try { localStorage.setItem("andiamo-raggio", String(state.radius)); } catch (_) { /* privato */ }
      Sound.play("chip"); update();
    };
    const step = (d) => setR(state.radius + d);
    $("#near-less").addEventListener("click", () => step(-5));
    $("#near-more").addEventListener("click", () => step(5));
    let rTimer;
    $("#near-range").addEventListener("input", (ev) => {      // trascinando: numero subito, lista appena ci si ferma
      const v = +ev.target.value;
      state.radius = v; renderSortBtn();
      clearTimeout(rTimer); rTimer = setTimeout(() => setR(v), 120);
    });
    document.addEventListener("click", (ev) => { if (!$("#near-pop").hidden && !ev.composedPath().includes($("#near"))) openNear(false); });
  }
  function toggleSort() { openNear($("#near-pop").hidden); }

  let toastTimer;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (t.hidden = true), 3500);
  }

  // ---------------------------------------------------------------- aggiornamento
  let lastMapKey = "";
  function update(fit) {
    const onMap = EVENTS.filter((e) => matches(e));          // la mappa mostra sempre tutti gli eventi filtrati
    const now = romeNow();
    LIVE = new Set(onMap.filter((e) => isLive(e, now)).map((e) => e.uid));
    let items = onlyUids ? onMap.filter((e) => onlyUids.has(e.uid)) : onMap.slice();   // l'elenco puo' restringersi a un punto
    const from = state.from || "";
    // vista lista ordinata per vicinanza: solo gli eventi entro il raggio scelto (i preferiti si vedono tutti)
    if (state.view === "list" && state.sort === "distance" && state.me && !state.fav && !onlyUids)
      { if (!ALL_IT()) items = items.filter((e) => km(e) <= state.radius); }
    if (state.sort === "distance" && state.me) items.sort((a, b) => km(a) - km(b));
    else {
      const key = (e) => (e.start.slice(0, 10) < from ? from : e.start.slice(0, 10)) + (timeOf(e) || "99");
      items.sort((a, b) => key(a).localeCompare(key(b)));
    }
    renderStrip();
    renderChips();
    if (!state.detail) {
      const open = $("#list .inline-card")?.dataset.uid;          // la card aperta nella lista resta aperta
      renderList(items);
      if (open) { const b = $(`#list .item button[data-uid="${open}"]`); const e = EVENTS.find((x) => x.uid === open); if (b && e) toggleInline(b.closest(".item"), e, { quiet: true }); }
    }
    lastItems = items;
    const n = items.length;
    $("#count-label").textContent = onlyUids ? `${n} in questo punto` : state.fav ? `${n} salvati`
      : `${n} ${n === 1 ? "evento" : "eventi"}`;
    $("#panel .kicker").textContent = state.fav ? "Preferiti" : "Eventi";
    renderFavBtn();
    $("#list-toggle-count").textContent = n;
    $("#list-toggle").setAttribute("aria-label", `Mostra l'elenco: ${n} ${n === 1 ? "evento" : "eventi"}`);
    renderSortBtn();
    $("#reset").hidden = !(state.cats.size || state.access.size || state.aud.size || state.q || onlyUids || state.fav);
    if (mapReady) {
      map.getSource("ev").setData(geojson(onMap));
      const key = onMap.map((e) => e.uid).join();
      if (key !== lastMapKey) { lastMapKey = key; popIn(); }
      if (fit && onMap.length && !state.selected) {
        const b = new maplibregl.LngLatBounds();
        onMap.forEach((e) => b.extend([e.lon, e.lat]));
        const sw = b.getSouthWest(), ne = b.getNorthEast();
        if (Math.abs(ne.lng - sw.lng) < 1e-4 && Math.abs(ne.lat - sw.lat) < 1e-4)    // un solo punto: niente adattamento
          map.easeTo({ center: b.getCenter(), zoom: 12, offset: padOffset(mapPadding()), duration: 0 });
        else map.fitBounds(b, { padding: mapPadding(), maxZoom: 12, duration: 0 });
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

  // Modulo Google (senza PC): "Aggiungi evento" e "Segnala" vanno nelle risposte del modulo, che Claude legge di notte.
  // settings.yaml > site.form_url (link del modulo) e site.form_entries (codici entry.NNN dei campi).
  // Il modulo ha quattro domande: tipo, evento (uid), dettagli (una riga "Campo: valore" per dato), contatto.
  const FORM_LABELS = { title: "Titolo", date: "Data", time: "Ora", end_date: "Fine", town: "Comune", venue: "Luogo",
    address: "Indirizzo", category: "Categoria", access: "Accesso", price: "Prezzo", official_url: "Link",
    summary: "Descrizione", description: "Descrizione" };
  function details(obj) { return Object.entries(obj).filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join("\n"); }
  function formOn() { const s = DATA.site || {}; return !!(s.form_url && s.form_entries && Object.keys(s.form_entries).length); }
  async function sendForm(values) {
    const s = DATA.site, body = new URLSearchParams();
    Object.entries(values).forEach(([k, v]) => { const id = s.form_entries[k]; if (id && v) body.append(id, v); });
    const action = s.form_url.replace(/\/viewform.*$/, "/formResponse");
    // il modulo non risponde ai siti esterni (no-cors): l'invio arriva, la risposta non si puo' leggere
    await fetch(action, { method: "POST", mode: "no-cors", body });
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
      if ((!API || !apiOk) && formOn()) {
        addStatus("warn", "Compila i campi a mano: l'evento arriva alla redazione e compare sulla mappa dopo il controllo.");
        setSourceEnabled(false);
        showForm({}, null);
      } else if (!API || !apiOk) {
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
    $("#add-submit").textContent = (!API || !apiOk) && !formOn() && DATA.site.contact_email ? "Invia per email" : "Invia evento";
    return ok;
  }

  async function sendEvent() {
    const d = formData();
    const missingReq = REQUIRED.filter((k) => !d[k]);
    if (missingReq.length) {
      missingReq.forEach((k) => { const f = document.querySelector(`.field[data-f="${k}"]`); f.classList.add("missing"); f.querySelector(".field-badge").textContent = "Mancante"; });
      return;
    }
    if ((!API || !apiOk) && formOn()) { // senza PC: modulo Google
      const btn = $("#add-submit");
      btn.disabled = true; btn.textContent = "Invio…";
      if (d.website) return;            // campo esca per i bot
      const rows = {};
      Object.entries(d).forEach(([k, v]) => { const f = FORM_LABELS[k]; if (f && v) rows[f] = v; });
      const vals = { tipo: "Nuovo evento", dettagli: details(rows), contatto: d.contatto || "" };
      try {
        await sendForm(vals);
        $("#add-step-source").hidden = true; $("#event-form").hidden = true; $("#add-done").hidden = false;
        btn.hidden = true; $("#add-again").hidden = false; $("#add-hint").hidden = true; $("#add-status").hidden = true;
        $("#add-body").scrollTop = 0;
      } catch (_) {
        addStatus("err", "<div><strong>Invio non riuscito.</strong> Controlla la connessione e riprova.</div>");
        validate();
      }
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
    if ((!API || !apiOk) && formOn()) {
      if (data.website) return;
      $("#report-submit").disabled = true;
      try {
        await sendForm({ tipo: data.tipo === "rimozione" ? "Rimozione" : "Correzione", evento: reportEvent.uid,
          dettagli: details({ Titolo: reportEvent.title, Data: reportEvent.start, Comune: reportEvent.town,
            Messaggio: data.messaggio }), contatto: data.contatto });
        show("ok", "<strong>Grazie, la controlliamo al più presto.</strong>");
        setTimeout(() => $("#report-dlg").close(), 1600);
      } catch (_) { show("err", "Invio non riuscito. Controlla la connessione e riprova."); $("#report-submit").disabled = false; }
      return;
    }
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
      DATA = await (await fetch(window.ANDIAMO_DATA || "data/events.json", { cache: "no-cache" })).json();
    } catch (err) {
      $("#count-label").textContent = "non disponibili";
      $("#list").innerHTML = `<li class="empty-state"><strong>Non riesco a caricare gli eventi.</strong>Ricarica la pagina tra qualche minuto.</li>`;
      return;
    }
    if (window.ANDIAMO_INTRO) await window.ANDIAMO_INTRO;   // prima parte l'apertura, poi il lavoro pesante
    EVENTS = DATA.events.filter((e) => e.start && e.lat != null);
    DATA.categories.forEach((c) => (CAT[c.id] = c));
    if (DATA.site.title) { document.title = DATA.site.title; renderWordmark(DATA.site.title); }
    const g = new Date(DATA.generated);
    $("#updated").textContent = `Aggiornato il ${g.getDate()} ${MONTHS[g.getMonth()]} alle ${pad(g.getHours())}:${pad(g.getMinutes())}.`;
    API = (DATA.site.api_url || "").replace(/\/$/, "");
    if (DATA.site.days_ahead) STRIP_DAYS = DATA.site.days_ahead;
    setupAdd();
    setupReport();
    setupSearch();
    $("#cal-prev").addEventListener("click", () => { state.calMonth = (state.calMonth || 0) - 1; renderStrip(); });
    $("#cal-next").addEventListener("click", () => { state.calMonth = (state.calMonth || 0) + 1; renderStrip(); });
    setupScrollNav("#chips");
    setupFilters();
    // barre dei giorni e dei filtri a tutta larghezza: l'elenco (desktop) sta nello spazio tra le due;
    // su telefono i filtri partono sotto la barra dei giorni
    const placePanels = () => {
      const root = document.documentElement.style, gap = MOBILE() ? 8 : 12;
      const bar = $(".days").getBoundingClientRect(), daysBottom = bar.bottom;
      // desktop: le categorie stanno sulla stessa riga del calendario, alla sua destra e alte uguali
      root.setProperty("--cats-top", `${Math.round(bar.top)}px`);
      root.setProperty("--cats-left", `${Math.round(bar.right + 10)}px`);
      root.setProperty("--cats-h", `${Math.round(bar.height)}px`);
      root.setProperty("--view-w", `${Math.round($(".view-box").getBoundingClientRect().width)}px`);   // riquadro Mappa/Lista a destra
      const above = MOBILE() ? daysBottom : Math.max(daysBottom, $(".chips-row").getBoundingClientRect().bottom);
      root.setProperty("--below-days", `${Math.round(above + gap)}px`);
      if (!MOBILE()) root.setProperty("--above-filters", `${Math.round(window.innerHeight - $(".filters").getBoundingClientRect().top + gap)}px`);
      root.setProperty("--below-filters", `${Math.round($(".filters").getBoundingClientRect().bottom + gap)}px`);
    };
    placePanels();
    window.addEventListener("resize", placePanels);
    if (window.ResizeObserver) { const ro = new ResizeObserver(placePanels); ro.observe($(".days")); ro.observe($(".filters")); ro.observe($(".chips-row")); ro.observe($(".view-box")); }
    if (document.fonts) document.fonts.ready.then(placePanels);
    $("#panel-hide").addEventListener("click", () => setSidebar(false));
    $("#list-toggle").addEventListener("click", () => setSidebar(true));
    try { if (localStorage.getItem("andiamo-sidebar") === "0" && !MOBILE()) setSidebar(false, { remember: false }); } catch (_) { /* privato */ }
    setupSheet();
    setSheet(MOBILE() ? "peek" : "half");

    setPreset("week");                        // preselezione: i prossimi 7 giorni
    document.querySelectorAll(".presets button").forEach((b) =>
      b.addEventListener("click", () => { Sound.play("chip"); state.pick = null; setPreset(b.dataset.preset); onlyUids = null; update(); setTimeout(() => setCalendar(false), 250); }));
    $("#cal-btn").addEventListener("click", () => { Sound.play("chip"); setCalendar($(".days").dataset.open !== "true"); });
    document.addEventListener("click", (ev) => {            // clic fuori dal calendario: si chiude
      // il percorso del clic si guarda com'era al momento del clic: i giorni vengono ridisegnati subito dopo
      if ($(".days").dataset.open === "true" && !ev.composedPath().some((n) => n.classList && n.classList.contains("days"))) setCalendar(false);
    });
    document.querySelectorAll(".view-seg button").forEach((b) => b.addEventListener("click", () => { Sound.play("chip"); setView(b.dataset.view); }));
    $("#fav-map").addEventListener("click", () => {
      state.fav = !state.fav; onlyUids = null; Sound.play("chip");
      closeAll();
      update(true);
      toast(state.fav ? "Sulla mappa solo i tuoi preferiti" : "Di nuovo tutti gli eventi");
    });
    $("#fav-btn").addEventListener("click", () => {
      state.fav = !state.fav; onlyUids = null; Sound.play("chip");
      closeAll();
      update(true);
      if (MOBILE()) setSheet("half");
    });
    $("#reset").addEventListener("click", () => {
      state.fav = false;
      state.cats.clear(); state.aud.clear(); state.access.clear(); state.q = ""; onlyUids = null;
      $("#q").value = "";
      state.pick = null; setPreset("week"); closeDetail(); update(true);
    });
    $("#more-filters").addEventListener("click", (ev) => {
      const open = $(".filters").classList.toggle("expanded");
      if (open && MOBILE()) setSheet("peek");          // il pannello eventi non deve coprire i filtri
      ev.currentTarget.setAttribute("aria-expanded", String(open));
    });
    $("#locate").addEventListener("click", locate);
    setupNear();
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && state.detail) closeDetail(); });

    const m = location.hash.match(/e=([0-9a-f]+)/);
    if (m && EVENTS.some((e) => e.uid === m[1])) {
      state.selected = m[1];
      history.replaceState({ uid: m[1] }, "", `#e=${m[1]}`);
    }
    update();
    let v0 = "map";
    try { v0 = localStorage.getItem("andiamo-vista") === "list" ? "list" : "map"; } catch (_) { /* privato */ }
    if (v0 === "list" && !state.selected) setView("list");
    setCalendar(false);
    initMap();
  }

  // accesso di sola lettura per test e debug dalla console
  window.andiamo = { map: () => map, coords: (uid) => COORDS[uid], events: () => EVENTS };

  start();
})();
