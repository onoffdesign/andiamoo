/* Apertura di ANDIAMO?: a schermo intero, su carta beige, il logo "ANDIAMO?" lettera per lettera, poi si allarga in
   "DOVE ANDIAMO OGGI?", poi diventa una proposta diversa a ogni visita ("ANDIAMO AL CINEMA?"). Alla fine il foglio
   si strappa in due e si apre in 3D sulla mappa. Circa 3,5 secondi; un tocco, un clic o un tasto la saltano. */
(function () {
  "use strict";
  const root = document.getElementById("intro");
  if (!root) return;
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const IDEAS = ["AL CINEMA", "A TEATRO", "AL CONCERTO", "ALLA SAGRA", "AL MERCATINO", "A BALLARE", "ALLA MOSTRA",
    "AL MUSEO", "A CORRERE", "IN PIAZZA", "AL MERCATO", "A UNA FESTA", "A CAMMINARE", "IN MONTAGNA"];
  let last = "";
  try { last = sessionStorage.getItem("andiamo-intro") || localStorage.getItem("andiamo-intro") || ""; } catch (_) { /* */ }
  const pool = IDEAS.filter((x) => x !== last);
  const idea = pool[Math.floor(Math.random() * pool.length)];
  try { localStorage.setItem("andiamo-intro", idea); } catch (_) { /* privato */ }

  const letters = (t) => [...t].map((ch, i) => `<span class="il" style="--i:${i}">${ch === " " ? "&nbsp;" : ch}</span>`).join("");
  // la stessa scritta in tutte e due le meta' del foglio (quando si strappa, ognuna porta con se' la sua parte)
  const line = `<h1 class="intro-line" aria-label="Andiamo?">
      <span class="iw pre">${letters("DOVE ")}</span><span class="iw core">${letters("ANDIAMO")}</span><span class="iw post a">${letters(" OGGI")}</span><span class="iw post b">${letters(" " + idea)}</span><span class="iw q">${letters("?")}</span>
    </h1>`;
  root.querySelectorAll(".intro-sheet").forEach((s) => { s.innerHTML = line; });

  // strappo: linea a zig-zag dall'alto in basso, poco a sinistra del centro, con piccoli denti irregolari
  const pts = [];
  let x = 49 + Math.random() * 4;
  for (let y = 0; y <= 100; y += 2.5) { x += (Math.random() - 0.5) * 2.6; x = Math.max(44, Math.min(56, x)); pts.push([x + (Math.random() - 0.5) * 0.9, y]); }
  const edge = pts.map(([px, py]) => `${px.toFixed(2)}% ${py}%`).join(",");
  root.querySelector(".intro-half.left .intro-sheet").style.clipPath = `polygon(0 0,${edge},0 100%)`;
  root.querySelector(".intro-half.right .intro-sheet").style.clipPath = `polygon(${edge},100% 100%,100% 0)`;

  const all = (sel) => root.querySelectorAll(sel);
  // le parole si allargano dalla larghezza zero alla loro (e viceversa); finito l'allargamento la larghezza torna libera,
  // cosi' se il carattere arriva in ritardo nulla si taglia
  const fit = (sel, open) => all(sel).forEach((w) => {
    if (!open) { w.style.width = `${w.getBoundingClientRect().width}px`; void w.offsetWidth; }
    w.style.width = open ? `${w.scrollWidth}px` : "0px";
    w.classList.toggle("on", open);
    if (open) w.addEventListener("transitionend", () => { if (w.classList.contains("on")) w.style.width = "auto"; }, { once: true });
  });
  const timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  let done = false;
  function finish(fast) {
    if (done) return;
    done = true;
    timers.forEach(clearTimeout);
    root.classList.add(REDUCED || fast === "fade" ? "fade" : "tear");
    setTimeout(() => { root.remove(); document.documentElement.classList.remove("intro-on"); }, REDUCED ? 450 : 1150);
  }
  // la prima volta in questa scheda si vede tutta; ricaricando, la versione breve
  let seen = false;
  try { seen = !!sessionStorage.getItem("andiamo-intro"); sessionStorage.setItem("andiamo-intro", idea); } catch (_) { /* */ }

  all(".iw").forEach((w) => { if (!w.classList.contains("core") && !w.classList.contains("q")) w.style.width = "0px"; });
  requestAnimationFrame(() => root.classList.add("go"));          // "ANDIAMO?" lettera per lettera
  if (REDUCED) { at(1300, finish); }
  else if (seen) {                                                // breve: subito la proposta, poi lo strappo
    at(450, () => fit(".post.b", true));
    at(1700, () => finish());
  } else {
    at(950, () => { fit(".pre", true); fit(".post.a", true); });   // DOVE ANDIAMO OGGI?
    at(2050, () => { fit(".pre", false); fit(".post.a", false); root.classList.add("swap"); });
    at(2250, () => fit(".post.b", true));                        // ANDIAMO AL CINEMA?
    at(3450, () => finish());
  }
  ["pointerdown", "keydown", "wheel"].forEach((ev) => window.addEventListener(ev, () => finish(), { once: true, passive: true }));
  setTimeout(() => finish("fade"), 7000);                         // in ogni caso, mai bloccati qui
})();
