// Bikefit web app: a guided fitting conversation in five steps.
// Plain ES modules, no build step; the Python server serves this file.

import { LANGS, lang, locale, setLang, t } from "./i18n.js";

const main = document.getElementById("main");
const stepper = document.getElementById("stepper");

const ICONS = {
  check: '<path d="M20 6 9 17l-5-5"/>',
  upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
  arrowRight: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  arrowLeft: '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
  wrench: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
  trophy: '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
  alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  plus: '<path d="M5 12h14"/><path d="M12 5v14"/>',
  gauge: '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
  crosshair: '<circle cx="12" cy="12" r="9"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/>',
  angle: '<path d="M4 20h16"/><path d="M4 20 15 5"/><path d="M10 20a6 6 0 0 0-2.4-4.8"/>',
  foot: '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/>',
  trash: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M10 11v6M14 11v6"/>',
  user: '<circle cx="12" cy="7" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/>',
  bike: '<circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-3 11.5V14l-3-3 4-3 2 3h2"/>',
};
const btnIcon = (name) => `<span class="circle">${icon(name, "sm")}</span>`;
const icon = (name, cls = "") => `<svg class="icon ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]}</svg>`;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const num = (v) => (v === "" || v == null ? null : Number(String(v).replace(",", ".")));
const fmt = (v, d = 0) => Number(v).toLocaleString(locale(), { maximumFractionDigits: d, minimumFractionDigits: d });

const date = (iso) => new Date(iso).toLocaleString(locale());
const withLang = (path) => `${path}${path.includes("?") ? "&" : "?"}lang=${lang}`;

async function api(path, options = {}) {
  const res = await fetch(withLang(path), {
    headers: options.body && !(options.body instanceof FormData) ? { "Content-Type": "application/json" } : {},
    ...options,
    body: options.body && !(options.body instanceof FormData) ? JSON.stringify(options.body) : options.body,
  });
  if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || t("error.http", { status: res.status }));
  return res.json();
}

function toast(text) {
  const t = document.getElementById("toast");
  t.textContent = text;
  t.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.remove("show"), 2600);
}

// The fitting currently being worked on, so the stepper can jump back to its
// video and result steps after visiting an earlier step.
let active = null; // { id, bike_id, hasResult }

function stepHref(i) {
  if (i <= 2) return ["#/interview", "#/body", "#/bike"][i];
  if (!active) return null;
  if (i === 3) return `#/session/${active.id}/video`;
  return active.hasResult ? `#/session/${active.id}` : null;
}

function setStep(index) {
  if (index == null) { stepper.hidden = true; active = null; return; }
  stepper.hidden = false;
  stepper.setAttribute("aria-label", t("steps.nav"));
  stepper.innerHTML = `<ol>${t("steps").map((s, i) => {
    const inner = `<span class="num">${i < index ? "✓" : i + 1}</span><span class="label">${s}</span>`;
    const href = i !== index && stepHref(i);
    return `<li class="${i < index ? "done" : ""}" ${i === index ? 'aria-current="step"' : ""}>
      ${href ? `<a href="${href}" aria-label="${esc(t("steps.goto", { n: i + 1, name: s }))}">${inner}</a>` : `<span class="step">${inner}</span>`}</li>`;
  }).join("")}</ol>`;
}

function trackSession(s) {
  active = { id: s.id, bike_id: s.bike_id, hasResult: s.rounds.some((r) => r.status === "done") };
}

function render(html, step) {
  setStep(step);
  drawChrome();
  main.innerHTML = html;
  main.focus({ preventScroll: true });
  window.scrollTo({ top: 0 });
}

// Confirmation in a modal <dialog>; resolves true when the user confirms.
function confirmDialog(title, text, okLabel) {
  return new Promise((resolve) => {
    const d = document.createElement("dialog");
    d.className = "confirm";
    d.setAttribute("aria-labelledby", "confirm-title");
    d.innerHTML = `<h2 id="confirm-title">${esc(title)}</h2><p class="muted">${esc(text)}</p>
      <div class="row"><button class="btn btn-secondary" value="no">${t("cancel")}</button>
      <button class="btn btn-danger" value="yes">${btnIcon("trash")} ${esc(okLabel)}</button></div>`;
    document.body.append(d);
    d.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => d.close(b.value)));
    d.addEventListener("close", () => { resolve(d.returnValue === "yes"); d.remove(); });
    d.showModal();
    d.querySelector('button[value="no"]').focus();
  });
}

async function deleteSession(sid, label) {
  const ok = await confirmDialog(t("delete.title"), t("delete.text", { label }), t("delete.ok"));
  if (!ok) return false;
  try {
    await api(`/api/sessions/${sid}`, { method: "DELETE" });
    toast(t("delete.done"));
    return true;
  } catch (err) {
    toast(err.message);
    return false;
  }
}

// ---------------------------------------------------------------- start
async function viewStart() {
  const [sessions, bikes] = await Promise.all([api("/api/sessions"), api("/api/bikes")]);
  const bikeName = (id) => {
    const b = bikes.find((x) => x.id === id);
    return (b && [b.brand, b.model].filter(Boolean).join(" ")) || t("bike");
  };
  render(`
    <section class="hero">
      <div class="card lime">
        <span class="wheel" aria-hidden="true">${icon("bike")}</span>
        <h1>${t("start.title")}</h1>
        <p class="lead">${t("start.lead")}</p>
        <a class="btn btn-dark" href="#/interview">${btnIcon("arrowRight")} ${t("start.new")}</a>
      </div>
      <div class="card paper">
        <h3>${t("start.how")}</h3>
        <ol class="steps">
          ${t("steps").map((step) => `<li><div><strong>${step}</strong></div></li>`).join("")}
        </ol>
      </div>
    </section>
    ${sessions.length ? `
    <section class="card">
      <h2>${t("start.past")}</h2>
      <ul class="session-list">
        ${sessions.map((s) => {
          const last = s.rounds[s.rounds.length - 1];
          const done = last?.status === "done";
          const label = t("bike.of", { bike: bikeName(s.bike_id), date: date(s.created) });
          return `<li><a href="#/session/${s.id}">
            <span class="bubble">${icon("bike")}</span>
            <div><div class="title"><strong>${esc(bikeName(s.bike_id))}</strong></div>
            <div class="muted small">${date(s.created)} · ${t("start.rounds", { n: s.rounds.length })}</div></div>
            <span class="spacer"></span>
            ${done ? `<span class="badge ok">${t("start.analysed")}</span>` : last ? `<span class="badge">${esc(last.message)}</span>` : `<span class="badge">${t("start.no_video")}</span>`}
            ${icon("arrowRight", "sm")}
          </a><button class="icon-btn" data-del="${s.id}" data-label="${esc(label)}" aria-label="${t("delete.button")}: ${esc(label)}" title="${t("delete.button")}">${icon("trash", "sm")}</button></li>`;
        }).join("")}
      </ul>
    </section>` : ""}
  `, null);
  main.querySelectorAll("[data-del]").forEach((b) => b.addEventListener("click", async () => {
    if (await deleteSession(b.dataset.del, b.dataset.label)) viewStart();
  }));
}

// ---------------------------------------------------------------- step 1: conversation
const GOALS = ["comfort", "sport", "race"];
const COMPLAINTS = ["knee_front", "knee_back", "lower_back", "neck", "numb_hands", "numb_feet", "saddle_pain"];

// Radio cards; texts come from "<prefix>.<value>" as [title, description].
const radioCards = (name, prefix, values, current) => values.map((v) => {
  const [title, desc] = t(`${prefix}.${v}`);
  return `<label class="choice"><input type="radio" name="${name}" value="${v}" ${current === v ? "checked" : ""}>
    <span><strong>${title}</strong><small>${desc}</small></span></label>`;
}).join("");

async function viewConversation() {
  const r = await api("/api/rider");
  render(`
    <section class="narrow">
      <h1>${t("talk.title")}</h1>
      <p class="lead">${t("talk.lead")}</p>
      <form id="f" class="card stack">
        <fieldset>
          <legend class="legend">${t("talk.goal")}</legend>
          <div class="choices">${radioCards("goal", "goal", GOALS, r.goal)}</div>
        </fieldset>
        <fieldset>
          <legend class="legend">${t("talk.complaints")}</legend>
          <p class="muted small">${t("talk.complaints_hint")}</p>
          <div class="chips">${COMPLAINTS.map((v) => `
            <label class="choice"><input type="checkbox" name="complaints" value="${v}" ${r.complaints.includes(v) ? "checked" : ""}>
            <span>${t("complaint." + v)}</span></label>`).join("")}</div>
        </fieldset>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="#/">${icon("arrowLeft", "sm")} ${t("back")}</a>
        <button class="btn btn-primary" form="f" type="submit">${btnIcon("arrowRight")} ${t("next")}</button>
      </div>
    </section>`, 0);
  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    await api("/api/rider", { method: "PUT", body: { ...r, goal: fd.get("goal") || "sport", complaints: fd.getAll("complaints") } });
    location.hash = "#/body";
  });
}

// ---------------------------------------------------------------- step 2: body
const FLEX = ["low", "medium", "high"];

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
  const r = await api("/api/rider");
  render(`
    <section class="narrow">
      <h1>${t("body.title")}</h1>
      <p class="lead">${t("body.lead")}</p>
      <form id="f" class="card stack" novalidate>
        <div class="grid-2">
          ${numberField("height_cm", t("body.height"), r.height_cm, "cm", "", 'min="120" max="220"')}
          ${numberField("inseam_cm", t("body.inseam"), r.inseam_cm, "cm", t("body.inseam_hint"), 'min="50" max="110"')}
        </div>
        <fieldset>
          <legend class="legend">${t("body.flex")}</legend>
          <p class="muted small">${t("body.flex_hint")}</p>
          <div class="choices">${radioCards("flexibility", "flex", FLEX, r.flexibility)}</div>
        </fieldset>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="#/interview">${icon("arrowLeft", "sm")} ${t("back")}</a>
        <button class="btn btn-primary" form="f" type="submit">${btnIcon("arrowRight")} ${t("next")}</button>
      </div>
    </section>`, 1);
  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    const ok = validate(f, {
      height_cm: (v) => (v == null ? t("body.height_missing") : v < 120 || v > 220 ? t("body.height_range") : ""),
      inseam_cm: (v) => (v != null && (v < 50 || v > 110) ? t("body.inseam_range") : ""),
    });
    if (!ok) return;
    const fd = new FormData(f);
    await api("/api/rider", { method: "PUT", body: { ...r, height_cm: num(fd.get("height_cm")),
      inseam_cm: num(fd.get("inseam_cm")), flexibility: fd.get("flexibility") || "medium" } });
    location.hash = "#/bike";
  });
}

// ---------------------------------------------------------------- step 3: bike
const SETTINGS = [["saddle_height_mm", "bike.saddle_height"], ["saddle_setback_mm", "bike.setback"],
  ["stem_mm", "bike.stem"], ["spacer_mm", "bike.spacer"]];

async function viewBike() {
  const [bikes, brands, models] = await Promise.all([api("/api/bikes"), api("/api/brands"), api("/api/models")]);
  const byBrand = {};
  for (const m of models) (byBrand[m.brand] ||= []).push(m);
  let selected = bikes.length ? bikes[bikes.length - 1].id : "new";
  const draw = () => {
    const b = bikes.find((x) => x.id === selected) || { type: "road" };
    render(`
      <section class="narrow">
        <h1>${t("bike.title")}</h1>
        <p class="lead">${t("bike.lead")}</p>
        ${bikes.length ? `<div class="card"><fieldset><legend class="legend">${t("bike.garage")}</legend><div class="choices">
          ${bikes.map((x) => `<label class="choice"><input type="radio" name="sel" value="${x.id}" ${x.id === selected ? "checked" : ""}>
            <span><strong>${esc([x.brand, x.model].filter(Boolean).join(" ") || t("bike"))}</strong><small>${esc(x.frame_size || "")} ${x.crank_mm ? "· " + t("bike.crank_short", { mm: fmt(x.crank_mm, 1) }) : ""}</small></span></label>`).join("")}
          <label class="choice"><input type="radio" name="sel" value="new" ${selected === "new" ? "checked" : ""}><span><strong>${icon("plus", "sm")} ${t("bike.new")}</strong><small>${t("bike.new_hint")}</small></span></label>
        </div></fieldset></div>` : ""}
        <form id="f" class="card stack" novalidate>
          <div class="preset">
            <h3>${t("bike.catalog")} <span class="muted small">${t("bike.catalog_hint")}</span></h3>
            <div class="grid-2">
              <div class="field"><label for="preset">${t("bike.model")}</label>
                <select id="preset"><option value="">${t("bike.other")}</option>
                  ${Object.keys(byBrand).sort((a, z) => a.localeCompare(z)).map((brand) => `<optgroup label="${esc(brand)}">
                    ${byBrand[brand].map((m) => `<option value="${m.id}">${esc(m.brand + " " + m.model)} (${esc(m.years)})</option>`).join("")}</optgroup>`).join("")}
                </select></div>
              <div class="field"><label for="preset-size">${t("bike.size")}</label>
                <select id="preset-size" disabled><option value="">${t("bike.pick_model")}</option></select></div>
            </div>
            <p class="muted small" id="preset-note" hidden>${t("bike.preset_note")}</p>
          </div>
          <div class="grid-3">
            <div class="field"><label for="brand">${t("bike.brand")}</label>
              <input id="brand" name="brand" type="text" list="brands" value="${esc(b.brand)}" autocomplete="off">
              <datalist id="brands">${brands.map((x) => `<option value="${esc(x)}">`).join("")}</datalist></div>
            <div class="field"><label for="model">${t("bike.model")}</label><input id="model" name="model" type="text" value="${esc(b.model)}"></div>
            <div class="field"><label for="frame_size">${t("bike.size")}</label><input id="frame_size" name="frame_size" type="text" value="${esc(b.frame_size)}"></div>
          </div>
          <fieldset><legend class="legend">${t("bike.type")}</legend><div class="choices">
            ${radioCards("type", "type", ["road", "tt"], b.type === "tt" ? "tt" : "road")}
          </div></fieldset>
          ${numberField("crank_mm", t("bike.crank"), b.crank_mm, "mm", t("bike.crank_hint"), 'min="150" max="185"')}
          <h3>${t("bike.settings")} <span class="muted small">${t("bike.settings_hint")}</span></h3>
          <div class="grid-2">
            ${numberField("saddle_height_mm", t("bike.saddle_height"), b.saddle_height_mm, "mm", t("bike.saddle_height_hint"))}
            ${numberField("saddle_setback_mm", t("bike.setback"), b.saddle_setback_mm, "mm", t("bike.setback_hint"))}
            ${numberField("stem_mm", t("bike.stem"), b.stem_mm, "mm", t("bike.stem_hint"))}
            ${numberField("spacer_mm", t("bike.spacer"), b.spacer_mm, "mm")}
          </div>
          <details class="more"><summary>${t("bike.geometry")}</summary>
            <p class="muted small">${t("bike.geometry_hint")}</p>
            <div class="grid-3">
              ${numberField("stack_mm", "Stack", b.stack_mm, "mm")}
              ${numberField("reach_mm", "Reach", b.reach_mm, "mm")}
              ${numberField("seat_angle_deg", t("bike.seat_angle"), b.seat_angle_deg, "°")}
            </div>
          </details>
        </form>
        <div class="actions">
          <a class="btn btn-ghost" href="#/body">${icon("arrowLeft", "sm")} ${t("back")}</a>
          <button class="btn btn-primary" form="f" type="submit">${btnIcon("arrowRight")} ${t("bike.save")}</button>
        </div>
      </section>`, 2);
    main.querySelectorAll('input[name="sel"]').forEach((el) => el.addEventListener("change", () => { selected = el.value; draw(); }));
    const presetSel = document.getElementById("preset"), sizeSel = document.getElementById("preset-size");
    presetSel.addEventListener("change", () => {
      const m = models[presetSel.value];
      sizeSel.disabled = !m;
      sizeSel.innerHTML = m ? `<option value="">${t("bike.pick_size")}</option>` + m.sizes.map((g, i) => `<option value="${i}">${esc(g.size)}</option>`).join("")
        : `<option value="">${t("bike.pick_model")}</option>`;
      if (!m) return;
      const f = document.getElementById("f");
      f.elements.brand.value = m.brand;
      f.elements.model.value = `${m.model} (${m.years})`;
      sizeSel.focus();
    });
    sizeSel.addEventListener("change", () => {
      const m = models[presetSel.value], g = m && m.sizes[sizeSel.value];
      if (!g) return;
      const f = document.getElementById("f");
      f.elements.frame_size.value = g.size;
      for (const k of ["stack_mm", "reach_mm", "seat_angle_deg"]) f.elements[k].value = g[k] ?? "";
      if (g.crank_mm != null) f.elements.crank_mm.value = g.crank_mm;  // keep the rider's own value otherwise
      f.querySelector("details.more").open = true;
      document.getElementById("preset-note").hidden = false;
    });
    document.getElementById("f").addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target;
      if (!validate(f, { crank_mm: (v) => (v == null ? t("bike.crank_missing") : v < 150 || v > 185 ? t("bike.crank_range") : "") })) return;
      const fd = new FormData(f);
      const data = { id: selected === "new" ? undefined : selected, type: fd.get("type") };
      for (const k of ["brand", "model", "frame_size"]) data[k] = fd.get(k).trim();
      for (const k of ["crank_mm", "saddle_height_mm", "saddle_setback_mm", "stem_mm", "spacer_mm", "stack_mm", "reach_mm", "seat_angle_deg"]) data[k] = num(fd.get(k));
      const bike = await api("/api/bikes", { method: "POST", body: data });
      // Coming back from a running fitting with the same bike continues it.
      const sid = active && active.bike_id === bike.id ? active.id
        : (await api("/api/sessions", { method: "POST", body: { bike_id: bike.id } })).id;
      location.hash = `#/session/${sid}/video`;
    });
  };
  draw();
}

// ---------------------------------------------------------------- step 4: video
async function viewVideo(sid) {
  const s = await api(`/api/sessions/${sid}`);
  trackSession(s);
  const next = s.rounds.length + 1;
  const bike = s.bike || {};
  const last = [...s.rounds].reverse().find((r) => r.status === "done");
  render(`
    <section class="narrow">
      <h1>${next === 1 ? t("video.title_first") : t("video.title_next", { n: next })}</h1>
      <p class="lead">${next === 1 ? t("video.lead_first") : t("video.lead_next")}</p>
      ${next === 1 ? `<div class="card"><ul class="checklist">${t("video.recording").map((x) => `<li><span class="tick">${icon("check", "sm")}</span><span>${x}</span></li>`).join("")}</ul></div>` : `
      ${last?.result ? `<div class="card"><h3>${t("video.last_advice")}</h3>${last.result.recommendations.map((x) => `<p class="tip">${esc(x)}</p>`).join("")}</div>` : ""}`}
      <form id="f" class="card stack" novalidate>
        <input type="hidden" name="lang" value="${lang}">
        ${next > 1 ? `
        <div class="grid-2">
          ${SETTINGS.map(([k, label]) => numberField(k, k === "spacer_mm" ? t("video.spacer_now") : t("video.now", { field: t(label) }), bike[k], "mm")).join("")}
        </div>
        <div class="field"><label for="change">${t("video.change")}</label><input id="change" name="change" type="text" placeholder="${esc(t("video.change_placeholder"))}"></div>` : ""}
        <label class="drop" id="drop" for="video">
          <span class="bubble">${icon("upload")}</span>
          <strong id="drop-text">${t("video.drop")}</strong>
          <span class="muted small">${t("video.formats")}</span>
          <input id="video" name="video" type="file" accept="video/*" hidden>
        </label>
        <div id="up" hidden><div class="progress" role="progressbar" aria-label="${t("video.upload_label")}" aria-valuemin="0" aria-valuemax="100"><div></div></div>
          <p class="muted small" id="up-text">${t("video.uploading")}</p></div>
      </form>
      <div class="actions">
        <a class="btn btn-ghost" href="${next === 1 ? "#/bike" : `#/session/${sid}`}">${icon("arrowLeft", "sm")} ${t("back")}</a>
        <button class="btn btn-primary" form="f" type="submit" id="go" disabled>${btnIcon("arrowRight")} ${t("video.start")}</button>
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
      document.getElementById("up-text").textContent = `${t("video.uploading")} ${p} %`;
    };
    xhr.onload = () => {
      if (xhr.status < 300) location.hash = `#/session/${sid}`;
      else { toast(t("video.upload_failed")); go.disabled = false; }
    };
    xhr.onerror = () => { toast(t("video.connection_lost")); go.disabled = false; };
    xhr.open("POST", withLang(`/api/sessions/${sid}/rounds`));
    xhr.send(fd);
  });
}

// ---------------------------------------------------------------- step 5: analysis + results
let pollTimer = null;

async function viewSession(sid, shownNr) {
  clearTimeout(pollTimer);
  const s = await api(`/api/sessions/${sid}`);
  trackSession(s);
  if (!s.rounds.length) { location.hash = `#/session/${sid}/video`; return; }
  const last = s.rounds[s.rounds.length - 1];
  if (last.status === "queued" || last.status === "running") return viewProgress(s, last);
  const finished = s.rounds.filter((r) => r.status === "done");
  if (last.status === "error" && (!finished.length || shownNr == null)) return viewError(s, last);
  const nr = shownNr ?? finished[finished.length - 1].nr;
  return viewResult(s, finished, nr);
}

function viewProgress(s, r) {
  const pct = Math.round((r.progress || 0) * 100);
  const same = document.getElementById("analysis-progress");
  if (same) {
    same.firstElementChild.style.width = pct + "%";
    same.setAttribute("aria-valuenow", pct);
    document.getElementById("analysis-text").textContent = `${r.message} · ${pct} %`;
  } else {
    render(`
      <section class="narrow">
        <h1>${t("progress.title", { n: r.nr })}</h1>
        <p class="lead">${t("progress.lead")}</p>
        <div class="card stack">
          <div class="progress" id="analysis-progress" role="progressbar" aria-label="${t("progress.label")}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><div style="width:${pct}%"></div></div>
          <p class="muted" id="analysis-text" aria-live="polite">${esc(r.message)} · ${pct} %</p>
        </div>
      </section>`, 4);
  }
  pollTimer = setTimeout(() => route(), 1500);
}

function viewError(s, r) {
  render(`
    <section class="narrow">
      <h1>${t("failed.title")}</h1>
      <div class="card verdict">${icon("alert")}<div><p class="tip">${esc(r.message)}</p>
      <p class="muted">${t("failed.hint")}</p></div></div>
      <div class="actions"><a class="btn btn-ghost" href="#/">${t("overview")}</a>
      <a class="btn btn-primary" href="#/session/${s.id}/video">${btnIcon("upload")} ${t("failed.upload")}</a></div>
    </section>`, 3);
}

const METRIC_ICON = { knee_extension: "gauge", knee_flexion_max: "gauge", kops_mm: "crosshair", hip_closed: "angle",
  ankle_range: "foot", torso_angle: "user", shoulder_angle: "angle", elbow_flexion: "angle" };
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
  const res = round.result;
  const prevRound = [...finished].reverse().find((r) => r.nr < nr);
  const prevEval = Object.fromEntries((prevRound?.result?.evaluation || []).map((e) => [e.key, e]));
  const isLatest = nr === finished[finished.length - 1].nr;
  const evals = [...res.evaluation].sort((a, b) => KEY_ORDER.indexOf(a.key) - KEY_ORDER.indexOf(b.key));
  const value = (v, u) => `${fmt(v)}<small>${u}</small>`;
  const unit = (u) => (u === "°" ? "°" : " " + u);
  render(`
    <div class="result-head">
      <div><h1>${res.done ? t("result.great") : t("result.title")}</h1>
      <p class="muted" style="margin:0">${t("result.round", { n: nr })}${round.change ? " · " + esc(t("result.changed", { change: round.change })) : ""}</p></div>
      <div class="facts">
        <span class="fact">${res.cycles}<small>${t("result.cycles")}</small></span>
        <span class="fact">${fmt(res.cadence_rpm)}<small>${t("result.rpm")}</small></span>
        <span class="fact">${evals.filter((e) => e.status === "ok").length}/${evals.length}<small>${t("result.in_target")}</small></span>
      </div>
    </div>
    <div class="result">
      <div class="video-wrap">
        <div class="card video-card">
          <video controls playsinline preload="metadata" src="/media/${s.id}/${nr}/analysis.mp4" aria-label="${t("result.video_label", { n: nr })}"></video>
          <p class="muted small">${t("result.video_legend")}</p>
        </div>
        ${finished.length > 1 ? `<div class="rounds" role="group" aria-label="${t("result.pick_round")}">${finished.map((r) =>
          `<button class="btn btn-secondary" aria-pressed="${r.nr === nr}" data-nr="${r.nr}">${t("result.round", { n: r.nr })}</button>`).join("")}</div>` : ""}
      </div>
      <div class="stack">
        <section class="card lime verdict">
          <div class="top"><span class="bubble">${icon(res.done ? "trophy" : "wrench")}</span>
            <h2>${res.done ? t("result.all_good") : t("result.next_step")}</h2></div>
          ${res.recommendations.map((x) => `<p class="tip">${esc(x)}</p>`).join("")}
          ${isLatest ? (res.done
            ? `<p class="muted" style="margin:0">${t("result.note_settings")}</p>
               <a class="btn btn-dark" href="#/session/${s.id}/video">${btnIcon("upload")} ${t("result.control_round")}</a>`
            : `<a class="btn btn-dark" href="#/session/${s.id}/video">${btnIcon("upload")} ${t("result.applied")}</a>`) : ""}
        </section>
        <section class="card">
          <h2>${t("result.metrics")}</h2>
          <p class="muted small">${t("result.legend")}${prevRound ? t("result.legend_prev", { n: prevRound.nr }) : ""}.
          ${t("result.legend_fix")}</p>
          <ul class="metrics">${evals.map((e) => {
            const p = prevEval[e.key];
            const d = p ? e.value - p.value : null;
            const off = e.status !== "ok";
            return `<li class="metric ${off ? "off" : ""}">
              <div class="head"><span class="dot">${icon(METRIC_ICON[e.key] || "gauge", "sm")}</span>
                <span class="label">${esc(e.label)}</span></div>
              <div class="value">${value(e.value, e.unit)}</div>
              ${metricBar(e, p)}
              <div class="foot">
                <span class="status ${off ? "off" : "ok"}">${t("status." + e.status)} · ${fmt(e.lo)}–${fmt(e.hi)}${unit(e.unit)}</span>
                ${d != null ? `<span class="delta">${d >= 0 ? "+" : "−"}${fmt(Math.abs(d), 1)}${unit(e.unit)} ${t("result.vs_round", { n: prevRound.nr })}</span>` : ""}
              </div>
              ${off && e.fix ? `<div class="fix">${icon("wrench", "sm")}<div><span class="step">${t("result.fix")}${e.step ? t("result.fix_step", { n: e.step }) : ""}</span>${esc(e.fix)}</div></div>` : ""}
            </li>`;
          }).join("")}</ul>
        </section>
        ${res.warnings.length ? `<section class="card"><h3>${icon("alert", "sm")} ${t("result.quality")}</h3><ul class="notes">${res.warnings.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></section>` : ""}
        ${res.notes.length ? `<section class="card"><h3>${t("result.info")}</h3><ul class="notes muted">${res.notes.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></section>` : ""}
        <p class="muted small">${t("result.footer", { s: fmt(res.offset_s, 1) })}</p>
        <button class="btn btn-ghost" id="del">${icon("trash", "sm")} ${t("delete.this")}</button>
      </div>
    </div>`, 4);
  main.querySelectorAll(".rounds button").forEach((b) => b.addEventListener("click", () => {
    location.hash = `#/session/${s.id}/round/${b.dataset.nr}`;
  }));
  document.getElementById("del").addEventListener("click", async () => {
    if (await deleteSession(s.id, t("fitting.of", { date: date(s.created) }))) location.hash = "#/";
  });
}

// ---------------------------------------------------------------- chrome + router
// Texts outside <main> and the language switch in the top bar.
function drawChrome() {
  document.documentElement.lang = lang;
  document.querySelector(".skip").textContent = t("skip");
  document.querySelector(".brand").setAttribute("aria-label", t("home"));
  const sw = document.getElementById("lang");
  sw.setAttribute("aria-label", t("lang.switch"));
  sw.innerHTML = Object.keys(LANGS).map((code) =>
    `<button type="button" lang="${code}" aria-pressed="${code === lang}" title="${LANGS[code]}">${code.toUpperCase()}</button>`).join("");
  sw.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
    if (b.lang === lang) return;
    setLang(b.lang);
    route();
  }));
}

async function route() {
  const h = location.hash.replace(/^#\/?/, "").split("/");
  try {
    if (h[0] === "interview") await viewConversation();
    else if (h[0] === "body") await viewBody();
    else if (h[0] === "bike") await viewBike();
    else if (h[0] === "session" && h[2] === "video") await viewVideo(h[1]);
    else if (h[0] === "session" && h[2] === "round") await viewSession(h[1], Number(h[3]));
    else if (h[0] === "session") await viewSession(h[1]);
    else await viewStart();
  } catch (err) {
    render(`<section class="narrow"><h1>${t("error.title")}</h1><div class="card"><p>${esc(err.message)}</p>
      <a class="btn btn-secondary" href="#/">${t("overview")}</a></div></section>`, null);
  }
}
window.addEventListener("hashchange", () => { clearTimeout(pollTimer); route(); });
setLang(lang);
route();
