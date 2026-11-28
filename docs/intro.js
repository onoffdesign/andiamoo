/* Apertura di ANDIAMO?: a schermo intero, su carta beige, "ANDIAMO?" lettera per lettera, poi si allarga in
   "DOVE ANDIAMO OGGI?", poi diventa una proposta diversa a ogni visita ("ANDIAMO AL CINEMA?"); alla fine il foglio
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
  const IDEAS = ["AL CINEMA", "A TEATRO", "AL CONCERTO", "ALLA SAGRA", "AL MERCATINO", "A BALLARE", "ALLA MOSTRA",
    "AL MUSEO", "A CORRERE", "IN PIAZZA", "AL MERCATO", "A UNA FESTA", "A CAMMINARE", "IN MONTAGNA"];
  const store = (k, v) => { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) { return null; } return null; };
  const last = store("andiamo-intro") || "";
  const pool = IDEAS.filter((x) => x !== last);
  const idea = pool[Math.floor(Math.random() * pool.length)];
  store("andiamo-intro", idea);
  let seen = false;                       // gia' vista in questa scheda (ricarica): versione breve
  try { seen = !!sessionStorage.getItem("andiamo-intro-vista"); sessionStorage.setItem("andiamo-intro-vista", "1"); } catch (_) { /* */ }

  const WORDS = { pre: "DOVE ", core: "ANDIAMO", a: " OGGI", b: " " + idea, q: "?" };
  const word = (k) => `<span class="iw" data-w="${k}">${[...WORDS[k]].map((ch) => `<span class="il">${ch === " " ? "\u00a0" : ch}</span>`).join("")}</span>`;
  const line = `<div class="intro-line">${Object.keys(WORDS).map(word).join("")}</div>`;
  root.querySelectorAll(".intro-sheet").forEach((s) => { s.innerHTML = line; });

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
    started();
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
  function cleanup() { root.remove(); document.documentElement.classList.remove("intro-on"); }

  function run() {
    // misure (una volta sola, a carattere pronto): larghezza di ogni parola e dimensione che fa stare la frase piu'
    // lunga nel 88% dello schermo; poi le parole si spostano solo con translate
    const sheet = root.querySelector(".intro-sheet");
    const w = {};
    Object.keys(WORDS).forEach((k) => { w[k] = sheet.querySelector(`.iw[data-w="${k}"]`).getBoundingClientRect().width; });
    const widest = Math.max(w.pre + w.core + w.a + w.q, w.core + w.b + w.q);
    const scale = Math.min(1, (window.innerWidth * 0.88) / widest);
    root.style.setProperty("--intro-scale", String(scale));
    Object.keys(w).forEach((k) => { w[k] *= scale; });
    const layout = (keys) => { const tot = keys.reduce((s, k) => s + w[k], 0); let x = -tot / 2; const o = {}; keys.forEach((k) => { o[k] = x; x += w[k]; }); return o; };
    const S1 = layout(["core", "q"]), S2 = layout(["pre", "core", "a", "q"]), S3 = layout(["core", "b", "q"]);
    const place = (k, x0) => ws(k).forEach((el) => { el.style.transform = `translateX(${x0}px)`; });
    place("pre", S2.pre); place("a", S2.a); place("b", S3.b); place("core", S1.core); place("q", S1.q);
    const move = (k, from, to, t0) => ws(k).forEach((el) => play(el,
      [{ transform: `translateX(${from}px)` }, { transform: `translateX(${to}px)` }], { duration: 560, delay: t0, easing: MOVE }));
    root.classList.add("go");

    letterIn("core", 0, 55);
    letterIn("q", 430, 0);
    ws("q").forEach((el) => play(el.firstChild, [{ transform: "rotate(0)" }, { transform: "rotate(14deg)" }, { transform: "rotate(-8deg)" }, { transform: "rotate(0)" }],
      { duration: 900, delay: 950, easing: "ease-in-out", fill: "none", composite: "add" }));
    let tear;
    if (REDUCED) {
      tear = 1300;
    } else if (seen) {                                    // breve: subito la proposta
      move("core", S1.core, S3.core, 650); move("q", S1.q, S3.q, 650);
      letterIn("b", 760, 35);
      tear = 2150;
    } else {
      move("core", S1.core, S2.core, 950); move("q", S1.q, S2.q, 950);      // DOVE ANDIAMO OGGI?
      letterIn("pre", 1000, 45); letterIn("a", 1080, 45);
      letterOut("pre", 2150); letterOut("a", 2150);
      move("core", S2.core, S3.core, 2250); move("q", S2.q, S3.q, 2250);    // ANDIAMO AL CINEMA?
      letterIn("b", 2330, 38);
      tear = 3550;
    }
    // il sito parte con il suo lavoro pesante solo ora: le animazioni sono gia' consegnate alla scheda grafica
    requestAnimationFrame(() => requestAnimationFrame(started));
    // lo strappo e' agganciato al tempo dell'animazione (non a un timer che il caricamento potrebbe ritardare)
    const clock = root.animate([{ opacity: 1 }, { opacity: 1 }], { duration: tear });
    clock.finished.then(() => finish(), () => {});
  }

  const fontReady = document.fonts && document.fonts.load ? document.fonts.load('400 64px "Andiamo Intro"') : Promise.resolve();
  Promise.race([fontReady, new Promise((r) => setTimeout(r, 1200))]).then(() => requestAnimationFrame(run));
  ["pointerdown", "keydown", "wheel"].forEach((ev) => window.addEventListener(ev, () => finish(), { once: true, passive: true }));
  setTimeout(() => finish("fade"), 9000);                         // in ogni caso, mai bloccati qui
})();
