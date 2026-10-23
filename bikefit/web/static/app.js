// Bikefit web app: a guided fitting conversation in five steps.
// Plain ES modules, no build step; the Python server serves this file.

const main = document.getElementById("main");
const stepper = document.getElementById("stepper");
const STEPS = ["Gespräch", "Körper", "Rad", "Video", "Auswertung"];

const ICONS = {
  check: '<path d="M20 6 9 17l-5-5"/>',
  upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
  arrowRight: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  arrowLeft: '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
  wrench: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
  trophy: '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
  alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  plus: '<path d="M5 12h14"/><path d="M12 5v14"/>',
  bike: '<circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-3 11.5V14l-3-3 4-3 2 3h2"/>',
};
const icon = (name, cls = "") => `<svg class="icon ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]}</svg>`;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const num = (v) => (v === "" || v == null ? null : Number(String(v).replace(",", ".")));
const fmt = (v, d = 0) => Number(v).toLocaleString("de-DE", { maximumFractionDigits: d, minimumFractionDigits: d });

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: options.body && !(options.body instanceof FormData) ? { "Content-Type": "application/json" } : {},
    ...options,
    body: options.body && !(options.body instanceof FormData) ? JSON.stringify(options.body) : options.body,
  });
  if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `Fehler ${res.status}`);
  return res.json();
}

function toast(text) {
  const t = document.getElementById("toast");
  t.textContent = text;
  t.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.remove("show"), 2600);
}

function setStep(index) {
  if (index == null) { stepper.hidden = true; return; }
  stepper.hidden = false;
  stepper.innerHTML = `<ol>${STEPS.map((s, i) => `
    <li class="${i < index ? "done" : ""}" ${i === index ? 'aria-current="step"' : ""}>
      <span class="num">${i < index ? "✓" : i + 1}</span><span class="label">${s}</span>
    </li>`).join("")}</ol>`;
}

function render(html, step) {
  setStep(step);
  main.innerHTML = html;
  main.focus({ preventScroll: true });
  window.scrollTo({ top: 0 });
}

// ---------------------------------------------------------------- start
async function viewStart() {
  const [sessions, bikes] = await Promise.all([api("/api/sitzungen"), api("/api/raeder")]);
  const bikeName = (id) => {
    const b = bikes.find((x) => x.id === id);
    return b ? [b.marke, b.modell].filter(Boolean).join(" ") || "Rad" : "Rad";
  };
  render(`
    <section class="hero">
      <div>
        <h1>Dein Bike-Fit, Schritt für Schritt</h1>
        <p class="lead">Wie beim Fitter im Laden: Erst reden wir über dich und dein Rad, dann filmst du dich auf der Rolle.
        Die Software misst deine Gelenkwinkel und sagt dir, was du verstellen sollst. Danach filmst du erneut, bis alles passt.</p>
        <a class="btn btn-primary" href="#/gespraech">Neues Fitting starten ${icon("arrowRight", "sm")}</a>
      </div>
      <div class="card">
        <h3>So läuft es ab</h3>
        <ol class="steps">
          <li><div><strong>Gespräch</strong><br><span class="muted">Ziel und Beschwerden</span></div></li>
          <li><div><strong>Körper</strong><br><span class="muted">Größe, Schrittlänge, Beweglichkeit</span></div></li>
          <li><div><strong>Rad</strong><br><span class="muted">Modell, Kurbel, aktuelle Einstellungen</span></div></li>
          <li><div><strong>Video</strong><br><span class="muted">1 Minute seitlich auf der Rolle filmen</span></div></li>
          <li><div><strong>Auswertung</strong><br><span class="muted">Eine Änderung, neu filmen, wiederholen</span></div></li>
        </ol>
      </div>
    </section>
    ${sessions.length ? `
    <section class="card">
      <h2>Bisherige Fittings</h2>
      <ul class="session-list">
        ${sessions.map((s) => {
          const last = s.runden[s.runden.length - 1];
          const done = last?.status === "fertig" && s.runden.some((r) => r.status === "fertig");
          return `<li><a href="#/sitzung/${s.id}">
            ${icon("bike")}
            <div><div class="title"><strong>${esc(bikeName(s.rad_id))}</strong></div>
            <div class="muted small">${new Date(s.erstellt).toLocaleString("de-DE")} · ${s.runden.length} Runde${s.runden.length === 1 ? "" : "n"}</div></div>
            <span class="spacer"></span>
            ${done ? '<span class="badge ok">ausgewertet</span>' : last ? `<span class="badge">${esc(last.meldung)}</span>` : '<span class="badge">ohne Video</span>'}
            ${icon("arrowRight", "sm")}
          </a></li>`;
        }).join("")}
      </ul>
    </section>` : ""}
  `, null);
}

// ---------------------------------------------------------------- step 1: conversation
const GOALS = [
  ["komfort", "Komfort", "Lange Touren, entspannt sitzen"],
  ["sport", "Sportlich", "Training, schnelle Runden, Ausdauer"],
  ["rennen", "Rennen", "Maximale Leistung und Aerodynamik"],
];
const COMPLAINTS = [
  ["knie_vorne", "Knie vorne"], ["knie_hinten", "Knie hinten"], ["ruecken", "Unterer Rücken"],
  ["nacken", "Nacken / Schultern"], ["taube_haende", "Taube Hände"], ["taube_fuesse", "Taube Füße"],
  ["sitzbeschwerden", "Sitzbeschwerden"],
];

async function viewConversation() {
  const r = await api("/api/fahrer");
  render(`
    <section class="narrow">
      <h1>Erzähl mal: Was willst du auf dem Rad?</h1>
      <p class="lead">Davon hängt ab, wie sportlich deine Position sein darf. Ein Fitter fragt das als Erstes.</p>
      <form id="f" class="card stack">
        <fieldset>
          <legend class="legend">Dein Ziel</legend>
          <div class="choices">${GOALS.map(([v, t, d]) => `
            <label class="choice"><input type="radio" name="ziel" value="${v}" ${r.ziel === v ? "checked" : ""}>
            <span><strong>${t}</strong><small>${d}</small></span></label>`).join("")}</div>
        </fieldset>
        <fieldset>
          <legend class="legend">Hast du Beschwerden auf dem Rad?</legend>
          <p class="muted small">Mehrfachauswahl. Nichts wählen, wenn alles gut ist.</p>
          <div class="chips">${COMPLAINTS.map(([v, t]) => `
            <label class="choice"><input type="checkbox" name="beschwerden" value="${v}" ${r.beschwerden.includes(v) ? "checked" : ""}>
            <span>${t}</span></label>`).join("")}</div>
        </fieldset>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="#/">${icon("arrowLeft", "sm")} Zurück</a>
        <button class="btn btn-primary" form="f" type="submit">Weiter ${icon("arrowRight", "sm")}</button>
      </div>
    </section>`, 0);
  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    await api("/api/fahrer", { method: "PUT", body: { ...r, ziel: fd.get("ziel") || "sport", beschwerden: fd.getAll("beschwerden") } });
    location.hash = "#/koerper";
  });
}

// ---------------------------------------------------------------- step 2: body
const FLEX = [
  ["gering", "Eingeschränkt", "Fingerspitzen kommen höchstens bis zum Schienbein"],
  ["mittel", "Mittel", "Fingerspitzen erreichen Knöchel oder Zehen"],
  ["gut", "Gut", "Handflächen oder Fingerknöchel erreichen den Boden"],
];

function numberField(name, label, value, unit, hint = "", attrs = "") {
  return `<div class="field">
    <label for="${name}">${label}</label>
    <div class="unit"><input id="${name}" name="${name}" type="number" inputmode="decimal" step="any" value="${value ?? ""}" ${attrs} aria-describedby="${name}-hint ${name}-err"><span>${unit}</span></div>
    ${hint ? `<span class="hint" id="${name}-hint">${hint}</span>` : `<span id="${name}-hint" hidden></span>`}
    <span class="error" id="${name}-err" role="alert"></span>
  </div>`;
}

function validate(form, rules) {
  let first = null;
  for (const [name, check] of Object.entries(rules)) {
    const input = form.elements[name];
    const msg = check(num(input.value));
    form.querySelector(`#${name}-err`).textContent = msg || "";
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    if (msg && !first) first = input;
  }
  first?.focus();
  return !first;
}

async function viewBody() {
  const r = await api("/api/fahrer");
  render(`
    <section class="narrow">
      <h1>Jetzt zu dir</h1>
      <p class="lead">Mit Größe und Schrittlänge prüft die Software, ob die Messung im Video plausibel ist, und berechnet einen Startwert für die Sattelhöhe.</p>
      <form id="f" class="card stack" novalidate>
        <div class="grid-2">
          ${numberField("groesse_cm", "Körpergröße", r.groesse_cm, "cm", "", 'min="120" max="220"')}
          ${numberField("schrittlaenge_cm", "Schrittlänge", r.schrittlaenge_cm, "cm",
            "Barfuß an die Wand, Buch fest zwischen die Beine ziehen, Oberkante bis Boden messen.", 'min="50" max="110"')}
        </div>
        <fieldset>
          <legend class="legend">Beweglichkeit</legend>
          <p class="muted small">Im Stand mit gestreckten Beinen langsam nach vorn beugen. Wie weit kommst du?</p>
          <div class="choices">${FLEX.map(([v, t, d]) => `
            <label class="choice"><input type="radio" name="beweglichkeit" value="${v}" ${r.beweglichkeit === v ? "checked" : ""}>
            <span><strong>${t}</strong><small>${d}</small></span></label>`).join("")}</div>
        </fieldset>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="#/gespraech">${icon("arrowLeft", "sm")} Zurück</a>
        <button class="btn btn-primary" form="f" type="submit">Weiter ${icon("arrowRight", "sm")}</button>
      </div>
    </section>`, 1);
  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    const ok = validate(f, {
      groesse_cm: (v) => (v == null ? "Bitte deine Körpergröße angeben." : v < 120 || v > 220 ? "Bitte in Zentimetern angeben, z. B. 182." : ""),
      schrittlaenge_cm: (v) => (v != null && (v < 50 || v > 110) ? "Bitte in Zentimetern angeben, z. B. 86." : ""),
    });
    if (!ok) return;
    const fd = new FormData(f);
    await api("/api/fahrer", { method: "PUT", body: { ...r, groesse_cm: num(fd.get("groesse_cm")),
      schrittlaenge_cm: num(fd.get("schrittlaenge_cm")), beweglichkeit: fd.get("beweglichkeit") || "mittel" } });
    location.hash = "#/rad";
  });
}

// ---------------------------------------------------------------- step 3: bike
async function viewBike() {
  const [bikes, brands] = await Promise.all([api("/api/raeder"), api("/api/marken")]);
  let selected = bikes.length ? bikes[bikes.length - 1].id : "neu";
  const draw = () => {
    const b = bikes.find((x) => x.id === selected) || { typ: "rennrad" };
    render(`
      <section class="narrow">
        <h1>Welches Rad fitten wir?</h1>
        <p class="lead">Wichtig ist vor allem die Kurbellänge: Daraus berechnet die Software den Maßstab in Millimetern.
        Mit den aktuellen Einstellungen bekommst du Empfehlungen als konkrete Zahl, z. B. „Sattel auf 749 mm“.</p>
        ${bikes.length ? `<div class="card"><fieldset><legend class="legend">Deine Garage</legend><div class="choices">
          ${bikes.map((x) => `<label class="choice"><input type="radio" name="sel" value="${x.id}" ${x.id === selected ? "checked" : ""}>
            <span><strong>${esc([x.marke, x.modell].filter(Boolean).join(" ") || "Rad")}</strong><small>${esc(x.rahmengroesse || "")} ${x.kurbel_mm ? "· Kurbel " + fmt(x.kurbel_mm, 1) + " mm" : ""}</small></span></label>`).join("")}
          <label class="choice"><input type="radio" name="sel" value="neu" ${selected === "neu" ? "checked" : ""}><span><strong>${icon("plus", "sm")} Neues Rad</strong><small>Zur Garage hinzufügen</small></span></label>
        </div></fieldset></div>` : ""}
        <form id="f" class="card stack" novalidate>
          <div class="grid-3">
            <div class="field"><label for="marke">Marke</label>
              <input id="marke" name="marke" type="text" list="brands" value="${esc(b.marke)}" autocomplete="off">
              <datalist id="brands">${brands.map((x) => `<option value="${esc(x)}">`).join("")}</datalist></div>
            <div class="field"><label for="modell">Modell</label><input id="modell" name="modell" type="text" value="${esc(b.modell)}"></div>
            <div class="field"><label for="rahmengroesse">Rahmengröße</label><input id="rahmengroesse" name="rahmengroesse" type="text" value="${esc(b.rahmengroesse)}"></div>
          </div>
          <fieldset><legend class="legend">Art des Rads</legend><div class="choices">
            <label class="choice"><input type="radio" name="typ" value="rennrad" ${b.typ !== "zeitfahren" ? "checked" : ""}><span><strong>Rennrad</strong><small>Hände am Bremsgriff oder Unterlenker</small></span></label>
            <label class="choice"><input type="radio" name="typ" value="zeitfahren" ${b.typ === "zeitfahren" ? "checked" : ""}><span><strong>Zeitfahren / Triathlon</strong><small>Mit Aufleger</small></span></label>
          </div></fieldset>
          ${numberField("kurbel_mm", "Kurbellänge", b.kurbel_mm, "mm", "Steht innen auf der Kurbel, meist 165 bis 175.", 'min="150" max="185"')}
          <h3>Aktuelle Einstellungen <span class="muted small">(optional, sehr empfohlen)</span></h3>
          <div class="grid-2">
            ${numberField("sattelhoehe_mm", "Sattelhöhe", b.sattelhoehe_mm, "mm", "Mitte Tretlager bis Oberkante Sattel, entlang des Sitzrohrs.")}
            ${numberField("sattelversatz_mm", "Sattelversatz", b.sattelversatz_mm, "mm", "Waagerecht: Sattelspitze hinter Tretlagermitte.")}
            ${numberField("vorbau_mm", "Vorbaulänge", b.vorbau_mm, "mm", "Steht auf dem Vorbau.")}
            ${numberField("spacer_mm", "Spacer unter dem Vorbau", b.spacer_mm, "mm")}
          </div>
          <details class="more"><summary>Rahmengeometrie (optional)</summary>
            <p class="muted small">Für die Messung nicht nötig. Hilft später, deine Position auf ein anderes Rad zu übertragen.
            Die Werte stehen auf der Herstellerseite unter „Geometrie“ für deine Rahmengröße.</p>
            <div class="grid-3">
              ${numberField("stack_mm", "Stack", b.stack_mm, "mm")}
              ${numberField("reach_mm", "Reach", b.reach_mm, "mm")}
              ${numberField("sitzwinkel_grad", "Sitzwinkel", b.sitzwinkel_grad, "°")}
            </div>
          </details>
        </form>
        <div class="actions">
          <a class="btn btn-ghost" href="#/koerper">${icon("arrowLeft", "sm")} Zurück</a>
          <button class="btn btn-primary" form="f" type="submit">Rad speichern und weiter ${icon("arrowRight", "sm")}</button>
        </div>
      </section>`, 2);
    main.querySelectorAll('input[name="sel"]').forEach((el) => el.addEventListener("change", () => { selected = el.value; draw(); }));
    document.getElementById("f").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target;
      if (!validate(f, { kurbel_mm: (v) => (v == null ? "Ohne Kurbellänge gibt es keine Angaben in Millimetern. Bitte eintragen." : v < 150 || v > 185 ? "Bitte in Millimetern, z. B. 172.5." : "") })) return;
      const fd = new FormData(f);
      const data = { id: selected === "neu" ? undefined : selected, typ: fd.get("typ") };
      for (const k of ["marke", "modell", "rahmengroesse"]) data[k] = fd.get(k).trim();
      for (const k of ["kurbel_mm", "sattelhoehe_mm", "sattelversatz_mm", "vorbau_mm", "spacer_mm", "stack_mm", "reach_mm", "sitzwinkel_grad"]) data[k] = num(fd.get(k));
      const bike = await api("/api/raeder", { method: "POST", body: data });
      const session = await api("/api/sitzungen", { method: "POST", body: { rad_id: bike.id } });
      location.hash = `#/sitzung/${session.id}/video`;
    });
  };
  draw();
}

// ---------------------------------------------------------------- step 4: video
const RECORDING = [
  "Handy seitlich vom Rad, 2,5 bis 4 m entfernt, genau quer zum Rad",
  "Kamera auf Höhe von Hüfte bis Tretlager, gerade (nicht gekippt)",
  "Du und das ganze Rad im Bild, Querformat",
  "Eng anliegende Kleidung, helles Licht",
  "2 Minuten warm fahren, dann mindestens 60 Sekunden bei 85 bis 95 U/min filmen",
  "Hände ruhig am Bremsgriff lassen, nicht in die Kamera winken",
];

async function viewVideo(sid) {
  const s = await api(`/api/sitzungen/${sid}`);
  const next = s.runden.length + 1;
  const bike = s.rad || {};
  const last = [...s.runden].reverse().find((r) => r.status === "fertig");
  render(`
    <section class="narrow">
      <h1>${next === 1 ? "Zeit fürs Video" : `Runde ${next}: Hast du etwas verstellt?`}</h1>
      <p class="lead">${next === 1 ? "Ein gutes Video ist die halbe Miete. Achte auf diese Punkte:" :
        "Trag ein, was du geändert hast, und lade ein neues Video hoch. Die Software vergleicht dann mit der letzten Runde."}</p>
      ${next === 1 ? `<div class="card"><ul class="checklist">${RECORDING.map((t) => `<li>${icon("check", "sm")}<span>${t}</span></li>`).join("")}</ul></div>` : `
      ${last?.ergebnis ? `<div class="card"><h3>Letzte Empfehlung</h3>${last.ergebnis.recommendations.map((t) => `<p class="tip">${esc(t)}</p>`).join("")}</div>` : ""}`}
      <form id="f" class="card stack" novalidate>
        ${next > 1 ? `
        <div class="grid-2">
          ${numberField("sattelhoehe_mm", "Sattelhöhe jetzt", bike.sattelhoehe_mm, "mm")}
          ${numberField("sattelversatz_mm", "Sattelversatz jetzt", bike.sattelversatz_mm, "mm")}
          ${numberField("vorbau_mm", "Vorbaulänge jetzt", bike.vorbau_mm, "mm")}
          ${numberField("spacer_mm", "Spacer jetzt", bike.spacer_mm, "mm")}
        </div>
        <div class="field"><label for="aenderung">Was hast du sonst verändert?</label><input id="aenderung" name="aenderung" type="text" placeholder="z. B. Sattel 5 mm tiefer"></div>` : ""}
        <label class="drop" id="drop" for="video">
          ${icon("upload")}
          <strong id="drop-text">Video hier ablegen oder klicken zum Auswählen</strong>
          <span class="muted small">MP4 oder MOV direkt vom Handy</span>
          <input id="video" name="video" type="file" accept="video/*" hidden>
        </label>
        <div id="up" hidden><div class="progress" role="progressbar" aria-label="Hochladen" aria-valuemin="0" aria-valuemax="100"><div></div></div>
          <p class="muted small" id="up-text">Lade hoch ...</p></div>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="${next === 1 ? "#/rad" : `#/sitzung/${sid}`}">${icon("arrowLeft", "sm")} Zurück</a>
        <button class="btn btn-primary" form="f" type="submit" id="go" disabled>Analyse starten ${icon("arrowRight", "sm")}</button>
      </div>
    </section>`, 3);
  const input = document.getElementById("video");
  const drop = document.getElementById("drop");
  const go = document.getElementById("go");
  const pick = (file) => {
    if (!file) return;
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    document.getElementById("drop-text").textContent = `${file.name} (${fmt(file.size / 1e6)} MB)`;
    go.disabled = false;
  };
  input.addEventListener("change", () => pick(input.files[0]));
  ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => pick(e.dataTransfer.files[0]));
  document.getElementById("f").addEventListener("submit", (e) => {
    e.preventDefault();
    if (!input.files[0]) return;
    go.disabled = true;
    const fd = new FormData(e.target);
    for (const [k, v] of [...fd.entries()]) if (v === "") fd.delete(k);
    const xhr = new XMLHttpRequest();
    const bar = document.querySelector("#up .progress");
    document.getElementById("up").hidden = false;
    xhr.upload.onprogress = (ev) => {
      const p = Math.round((ev.loaded / ev.total) * 100);
      bar.firstElementChild.style.width = p + "%";
      bar.setAttribute("aria-valuenow", p);
      document.getElementById("up-text").textContent = `Lade hoch ... ${p} %`;
    };
    xhr.onload = () => {
      if (xhr.status < 300) location.hash = `#/sitzung/${sid}`;
      else { toast("Hochladen fehlgeschlagen. Bitte erneut versuchen."); go.disabled = false; }
    };
    xhr.onerror = () => { toast("Verbindung zum Programm verloren."); go.disabled = false; };
    xhr.open("POST", `/api/sitzungen/${sid}/runden`);
    xhr.send(fd);
  });
}

// ---------------------------------------------------------------- step 5: analysis + results
let pollTimer = null;

async function viewSession(sid, shownNr) {
  clearTimeout(pollTimer);
  const s = await api(`/api/sitzungen/${sid}`);
  if (!s.runden.length) { location.hash = `#/sitzung/${sid}/video`; return; }
  const last = s.runden[s.runden.length - 1];
  if (last.status === "wartet" || last.status === "laeuft") return viewProgress(s, last);
  const finished = s.runden.filter((r) => r.status === "fertig");
  if (last.status === "fehler" && (!finished.length || shownNr == null)) return viewError(s, last);
  const nr = shownNr ?? finished[finished.length - 1].nr;
  return viewResult(s, finished, nr);
}

function viewProgress(s, r) {
  const pct = Math.round((r.fortschritt || 0) * 100);
  const same = document.getElementById("analysis-progress");
  if (same) {
    same.firstElementChild.style.width = pct + "%";
    same.setAttribute("aria-valuenow", pct);
    document.getElementById("analysis-text").textContent = `${r.meldung} · ${pct} %`;
  } else {
    render(`
      <section class="narrow">
        <h1>Runde ${r.nr} wird ausgewertet</h1>
        <p class="lead">Die Software sucht in jedem Bild deine Gelenke, erkennt die Kurbelumdrehungen und berechnet die Winkel.
        Das dauert etwa so lange wie das Video, manchmal etwas länger. Du kannst das Fenster offen lassen.</p>
        <div class="card stack">
          <div class="progress" id="analysis-progress" role="progressbar" aria-label="Analyse" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><div style="width:${pct}%"></div></div>
          <p class="muted" id="analysis-text" aria-live="polite">${esc(r.meldung)} · ${pct} %</p>
        </div>
      </section>`, 4);
  }
  pollTimer = setTimeout(() => route(), 1500);
}

function viewError(s, r) {
  render(`
    <section class="narrow">
      <h1>Das hat nicht geklappt</h1>
      <div class="card verdict">${icon("alert")}<div><p class="tip">${esc(r.meldung)}</p>
      <p class="muted">Meist hilft ein neues Video: länger, gleichmäßig treten, ganze Person im Bild.</p></div></div>
      <div class="actions"><a class="btn btn-ghost" href="#/">Zur Übersicht</a>
      <a class="btn btn-primary" href="#/sitzung/${s.id}/video">Neues Video hochladen ${icon("upload", "sm")}</a></div>
    </section>`, 3);
}

const KEY_ORDER = ["knee_extension", "kops_mm", "knee_flexion_max", "hip_closed", "ankle_range", "torso_angle", "shoulder_angle", "elbow_flexion"];

function metricBar(e, prev) {
  const vals = [e.lo, e.hi, e.value, prev?.value].filter((v) => v != null);
  const span = Math.max(...vals) - Math.min(...vals);
  const lo = Math.min(...vals) - span * 0.25 - 1;
  const hi = Math.max(...vals) + span * 0.25 + 1;
  const pos = (v) => ((v - lo) / (hi - lo)) * 100;
  return `<div class="bar" aria-hidden="true">
    <div class="band" style="left:${pos(e.lo)}%;width:${pos(e.hi) - pos(e.lo)}%"></div>
    ${prev ? `<div class="mark prev" style="left:${pos(prev.value)}%"></div>` : ""}
    <div class="mark" style="left:${pos(e.value)}%"></div></div>`;
}

function viewResult(s, finished, nr) {
  const round = finished.find((r) => r.nr === nr);
  const res = round.ergebnis;
  const prevRound = [...finished].reverse().find((r) => r.nr < nr);
  const prevEval = Object.fromEntries((prevRound?.ergebnis?.evaluation || []).map((e) => [e.key, e]));
  const isLatest = nr === finished[finished.length - 1].nr;
  const evals = [...res.evaluation].sort((a, b) => KEY_ORDER.indexOf(a.key) - KEY_ORDER.indexOf(b.key));
  const unit = (u) => (u === "°" ? "°" : " " + u);
  render(`
    <div class="row" style="margin-bottom:var(--space-lg)">
      <div><h1>${res.done ? "Du sitzt gut!" : "Deine Auswertung"}</h1>
      <p class="muted" style="margin:0">Runde ${nr} · ${res.cycles} Kurbelumdrehungen · ${fmt(res.cadence_rpm)} U/min${round.aenderung ? " · Geändert: " + esc(round.aenderung) : ""}</p></div>
    </div>
    <div class="result">
      <div class="video-wrap">
        <video controls playsinline preload="metadata" src="/medien/${s.id}/${nr}/analyse.mp4" aria-label="Video mit erkannten Gelenken, Runde ${nr}"></video>
        <p class="muted small">Weiß: erkannte Gelenke · Gelb: Pedalkreis und Tretlager</p>
        ${finished.length > 1 ? `<div class="rounds" role="group" aria-label="Runde wählen">${finished.map((r) =>
          `<button class="btn btn-secondary" aria-pressed="${r.nr === nr}" data-nr="${r.nr}">Runde ${r.nr}</button>`).join("")}</div>` : ""}
      </div>
      <div class="stack">
        <section class="card verdict ${res.done ? "good" : ""}">
          ${icon(res.done ? "trophy" : "wrench")}
          <div>
            <h2>${res.done ? "Alles im Zielbereich" : "Nächster Schritt"}</h2>
            ${res.recommendations.map((t) => `<p class="tip">${esc(t)}</p>`).join("")}
            ${isLatest ? (res.done
              ? `<p class="muted">Notier dir deine Einstellungen. Wenn du magst, kannst du zur Kontrolle noch eine Runde filmen.</p>
                 <a class="btn btn-secondary" href="#/sitzung/${s.id}/video">Kontrollrunde filmen</a>`
              : `<a class="btn btn-primary" href="#/sitzung/${s.id}/video">Umgesetzt, neues Video hochladen ${icon("upload", "sm")}</a>`) : ""}
          </div>
        </section>
        <section class="card">
          <h2>Messwerte</h2>
          <p class="muted small">Grüner Bereich = Ziel. Strich = dein Wert${prevRound ? ", grauer Strich = Runde " + prevRound.nr : ""}.</p>
          <ul class="metrics">${evals.map((e) => {
            const p = prevEval[e.key];
            const d = p ? e.value - p.value : null;
            return `<li class="metric">
              <div class="head"><span>${esc(e.label)}</span>
                <span class="value">${fmt(e.value)}${unit(e.unit)}</span></div>
              ${metricBar(e, p)}
              <div class="row" style="justify-content:space-between;margin-top:6px">
                <span class="status ${e.status === "ok" ? "ok" : "off"}">${e.status === "ok" ? "Im Zielbereich" : e.status === "hoch" ? "Über dem Ziel" : "Unter dem Ziel"} (${fmt(e.lo)}–${fmt(e.hi)}${unit(e.unit)})</span>
                ${d != null ? `<span class="delta">${d >= 0 ? "+" : "−"}${fmt(Math.abs(d), 1)}${unit(e.unit)} zu Runde ${prevRound.nr}</span>` : ""}
              </div></li>`;
          }).join("")}</ul>
        </section>
        ${res.warnings.length ? `<section class="card"><h3>${icon("alert", "sm")} Zur Messqualität</h3><ul class="notes">${res.warnings.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></section>` : ""}
        ${res.notes.length ? `<section class="card"><h3>Info</h3><ul class="notes muted">${res.notes.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></section>` : ""}
        <p class="muted small">Ausgewertet ab Sekunde ${fmt(res.offset_s, 1)} des Videos (Auf- und Absteigen werden automatisch weggeschnitten). Die Software ersetzt keine medizinische Beratung.</p>
      </div>
    </div>`, 4);
  main.querySelectorAll(".rounds button").forEach((b) => b.addEventListener("click", () => {
    location.hash = `#/sitzung/${s.id}/runde/${b.dataset.nr}`;
  }));
}

// ---------------------------------------------------------------- router
async function route() {
  const h = location.hash.replace(/^#\/?/, "").split("/");
  try {
    if (h[0] === "gespraech") await viewConversation();
    else if (h[0] === "koerper") await viewBody();
    else if (h[0] === "rad") await viewBike();
    else if (h[0] === "sitzung" && h[2] === "video") await viewVideo(h[1]);
    else if (h[0] === "sitzung" && h[2] === "runde") await viewSession(h[1], Number(h[3]));
    else if (h[0] === "sitzung") await viewSession(h[1]);
    else await viewStart();
  } catch (err) {
    render(`<section class="narrow"><h1>Fehler</h1><div class="card"><p>${esc(err.message)}</p>
      <a class="btn btn-secondary" href="#/">Zur Übersicht</a></div></section>`, null);
  }
}
window.addEventListener("hashchange", () => { clearTimeout(pollTimer); route(); });
route();
