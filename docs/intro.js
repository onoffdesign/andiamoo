/* Apertura di ANDIAMO?: a schermo intero, su carta beige, "ANDIAMO?" lettera per lettera, poi si apre e accoglie
   una proposta presa dagli eventi veri dei prossimi giorni ("ANDIAMO AL CINEMA?"), diversa a ogni visita; alla fine il foglio
   si strappa in due e si apre in 3D sulla mappa.

   Fluidita': il carattere e' sul sito (fonts/patrick-hand-latin.woff2, precaricato) e l'animazione parte solo quando
   e' pronto; tutto si muove solo con transform e opacity (Web Animations), programmato tutto insieme all'avvio, cosi'
   gira sulla scheda grafica anche mentre il sito carica mappa ed eventi; il sito aspetta che l'animazione sia partita
   (window.ANDIAMO_INTRO) prima di fare il lavoro pesante. Un tocco, un clic o un tasto la saltano. */
(function () {
  "use strict";
  const root = document.getElementById("intro");
  if (!root) return;
  let started;
  window.ANDIAMO_INTRO = new Promise((res) => { started = res; });
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FALLBACK = ["AL CINEMA", "A TEATRO", "A UN CONCERTO", "ALLA SAGRA", "AL MERCATINO", "A UNA MOSTRA", "AL MUSEO", "A UNA FESTA"];
  const store = (k, v) => { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) { return null; } return null; };
  let seen = false;                       // gia' vista in questa scheda (ricarica): un po' piu' svelta
  try { seen = !!sessionStorage.getItem("andiamo-intro-vista"); sessionStorage.setItem("andiamo-intro-vista", "1"); } catch (_) { /* */ }
  // proposte vere: le sottocategorie con eventi nei prossimi giorni (data/intro.json, scritto a ogni pubblicazione)
  const introUrl = new URL("intro.json", new URL(window.ANDIAMO_DATA || "data/sito.json", location.href));
  const ideas = fetch(introUrl).then((r) => r.json()).then((j) => (j.frasi && j.frasi.length ? j.frasi : FALLBACK)).catch(() => FALLBACK);
  let idea = "";
  function pickIdea(list) {
    const last = store("andiamo-intro") || "";
    const pool = list.filter((x) => x !== last);
    idea = (pool.length ? pool : list)[Math.floor(Math.random() * (pool.length || list.length))];
    store("andiamo-intro", idea);
  }

  const WORDS = () => ({ core: "ANDIAMO", b: "\u00a0" + idea, q: "?" });
  const word = (k, w) => `<span class="iw" data-w="${k}">${[...w[k]].map((ch) => `<span class="il">${ch === " " ? "\u00a0" : ch}</span>`).join("")}</span>`;
  function build() {
    const w = WORDS();
    const line = `<div class="intro-line">${Object.keys(w).map((k) => word(k, w)).join("")}</div>`;
    root.querySelectorAll(".intro-sheet").forEach((s) => { s.innerHTML = line; });
  }

  // strappo: linea a zig-zag dall'alto in basso, vicino al centro, con piccoli denti irregolari
  const pts = [];
  let x = 49 + Math.random() * 4;
  for (let y = 0; y <= 100; y += 2.5) { x += (Math.random() - 0.5) * 2.6; x = Math.max(44, Math.min(56, x)); pts.push([x + (Math.random() - 0.5) * 0.9, y]); }
  const edge = pts.map(([px, py]) => `${px.toFixed(2)}% ${py}%`).join(",");
  root.querySelector(".intro-half.left .intro-sheet").style.clipPath = `polygon(0 0,${edge},0 100%)`;
  // la meta' destra resta intera (sotto quella sinistra) finche' non si strappa: nessuna riga visibile sulla cucitura
  const tearRight = () => { root.querySelector(".intro-half.right .intro-sheet").style.clipPath = `polygon(${edge},100% 100%,100% 0)`; };

  const anims = [];
  const play = (el, frames, opts) => { anims.push(el.animate(frames, { fill: "both", ...opts })); };
  const ws = (k) => [...root.querySelectorAll(`.iw[data-w="${k}"]`)];
  const POP = "cubic-bezier(.34, 1.56, .64, 1)", MOVE = "cubic-bezier(.65, 0, .25, 1)";
  const letterIn = (k, t0, step) => ws(k).forEach((w) => [...w.children].forEach((l, i) => play(l,
    [{ opacity: 0, transform: "translateY(.45em) rotate(-8deg) scale(.6)" }, { opacity: 1, transform: "none" }],
    { duration: 460, delay: t0 + i * step, easing: POP })));
  const letterOut = (k, t0) => ws(k).forEach((w) => [...w.children].forEach((l, i) => play(l,
    [{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(-.5em) rotate(6deg) scale(.7)" }],
    { duration: 260, delay: t0 + i * 22, easing: "ease-in", fill: "forwards" })));

  let done = false;
  function finish(how) {
    if (done) return;
    if (window.__introLog) window.__introLog.push(["finish", how, Math.round(performance.now())]);
    done = true;
    const halves = root.querySelectorAll(".intro-half");
    if (REDUCED || how === "fade") {
      root.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 350, fill: "forwards" }).finished.then(cleanup, cleanup);
      return;
    }
    tearRight();
    root.classList.add("tear");
    const fly = (el, dir) => el.animate([
      { transform: "translate3d(0,0,0) rotateY(0) rotateZ(0)", opacity: 1 },
      { transform: `translate3d(${dir * 18}vw, ${dir * 2}vh, 120px) rotateY(${-dir * 18}deg) rotateZ(${dir * 4}deg)`, opacity: 1, offset: 0.35 },
      { transform: `translate3d(${dir * 62}vw, ${dir * 5}vh, 180px) rotateY(${-dir * 40}deg) rotateZ(${dir * 10}deg)`, opacity: 0 },
    ], { duration: 1000, easing: "cubic-bezier(.5, 0, .3, 1)", fill: "forwards" });
    const a = fly(halves[0], -1);
    fly(halves[1], 1);
    root.style.pointerEvents = "none";
    a.finished.then(cleanup, cleanup);
  }
  function cleanup() {
    if (cleanup.done) return; cleanup.done = true;
    root.remove(); document.documentElement.classList.remove("intro-on");
    // solo ora il sito costruisce mappa ed elenco (dopo che lo schermo ha mostrato il foglio sparito)
    requestAnimationFrame(() => setTimeout(started, 30));
  }

  function run() {
    build();
    // misure (una volta sola, a carattere pronto): larghezza di ogni parola e dimensione che fa stare la frase piu'
    // lunga nel 88% dello schermo; poi le parole si spostano solo con translate
    const sheet = root.querySelector(".intro-sheet");
    const w = {};
    ["core", "b", "q"].forEach((k) => { w[k] = sheet.querySelector(`.iw[data-w="${k}"]`).getBoundingClientRect().width; });
    const scale = Math.min(1, (window.innerWidth * 0.88) / (w.core + w.b + w.q));
    root.style.setProperty("--intro-scale", String(scale));
    Object.keys(w).forEach((k) => { w[k] *= scale; });
    const layout = (keys) => { const tot = keys.reduce((s, k) => s + w[k], 0); let x0 = -tot / 2; const o = {}; keys.forEach((k) => { o[k] = x0; x0 += w[k]; }); return o; };
    const S1 = layout(["core", "q"]), S2 = layout(["core", "b", "q"]);
    const place = (k, x0) => ws(k).forEach((el) => { el.style.transform = `translateX(${x0}px)`; });
    place("b", S2.b); place("core", S1.core); place("q", S1.q);
    const move = (k, from, to, t0) => ws(k).forEach((el) => play(el,
      [{ transform: `translateX(${from}px)` }, { transform: `translateX(${to}px)` }], { duration: 560, delay: t0, easing: MOVE }));
    root.classList.add("go");

    // "ANDIAMO?" lettera per lettera, il "?" oscilla; poi ANDIAMO e "?" si aprono e in mezzo entra la proposta
    const k = seen ? 0.8 : 1;
    letterIn("core", 0, 55);
    letterIn("q", 430, 0);
    if (CSS.supports && CSS.supports("rotate", "1deg")) ws("q").forEach((el) => play(el.firstChild, [{ rotate: "0deg" }, { rotate: "14deg" }, { rotate: "-8deg" }, { rotate: "0deg" }],
      { duration: 900, delay: 900, easing: "ease-in-out", fill: "none" }));
    let tear = 1300;
    if (!REDUCED) {
      move("core", S1.core, S2.core, 1050 * k); move("q", S1.q, S2.q, 1050 * k);
      letterIn("b", 1130 * k, 38);
      tear = 1130 * k + idea.length * 38 + 1350;
    } else { letterIn("b", 0, 0); place("core", S2.core); place("q", S2.q); }
    // il sito parte con il suo lavoro pesante solo ora: le animazioni sono gia' consegnate alla scheda grafica
    // lo strappo e' agganciato al tempo dell'animazione (non a un timer che il caricamento potrebbe ritardare)
    const clock = root.animate([{ opacity: 1 }, { opacity: 1 }], { duration: tear });
    clock.finished.then(() => finish(), () => {});
  }

  const fontReady = document.fonts && document.fonts.load ? document.fonts.load('400 64px "Andiamo Intro"') : Promise.resolve();
  const wait = (pr, ms, fallback) => Promise.race([pr, new Promise((r) => setTimeout(() => r(fallback), ms))]);
  Promise.all([wait(fontReady, 700), wait(ideas, 500, FALLBACK)]).then(([, list]) => { pickIdea(list); requestAnimationFrame(run); });
  ["pointerdown", "keydown", "wheel"].forEach((ev) => window.addEventListener(ev, () => finish(), { once: true, passive: true }));
  setTimeout(() => finish("fade"), 9000);
  setTimeout(() => started(), 7000);                         // in ogni caso, mai bloccati qui
})();
