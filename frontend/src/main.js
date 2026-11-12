import "./style.css";
import "./theme.css";
import { loginPage } from "./login.js";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const app = document.querySelector("#app");

const state = {
  workspaceEntered: false,
  profileEmail: "",
  view: "overview",
  file: null,
  previewUrl: "",
  busy: false,
  result: null,
  error: "",
  service: "checking",
};

const icons = {
  overview: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  analyze: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v3m0 12v3M3 12h3m12 0h3"/><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2"/></svg>',
  model: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 7v10l8 4 8-4V7l-8-4Z"/><path d="m4 7 8 4 8-4m-8 4v10"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
  upload: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4m-5 5 5-5 5 5"/><path d="M4 16v4h16v-4"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg>',
  shield: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z"/><path d="m9 12 2 2 4-4"/></svg>',
  logout: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/><path d="M12 3h6a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-6"/></svg>',
};

const metricCards = [
  { value: "7,909", label: "Histology images", note: "BreakHis dataset" },
  { value: "82", label: "Unique patients", note: "Patient-level splits" },
  { value: "4", label: "Magnifications", note: "40× to 400×" },
  { value: "224 px", label: "Model input", note: "RGB image tiles" },
];

function navButton(view, label) {
  return `<button class="nav-link ${state.view === view ? "active" : ""}" data-view="${view}" ${state.view === view ? 'aria-current="page"' : ""}>
    ${icons[view]}<span>${label}</span>
  </button>`;
}

function profileDisplayName() {
  const localPart = state.profileEmail.split("@", 1)[0].replace(/[._+-]+/g, " ").trim();
  if (!localPart) return "Researcher";
  return localPart
    .split(/\s+/)
    .map((part) => part.charAt(0).toLocaleUpperCase() + part.slice(1))
    .join(" ");
}

function profileInitials() {
  return profileDisplayName()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join("")
    .toLocaleUpperCase();
}

function shell(content) {
  app.innerHTML = `
    <div class="workspace">
      <aside class="sidebar">
        <a class="brand" href="#" data-view="overview" aria-label="Tissue Research home">
          <span class="brand-mark">t<span>.</span></span>
          <span class="brand-copy"><strong>tissue</strong><small>RESEARCH WORKSPACE</small></span>
        </a>
        <div class="sidebar-label">WORKSPACE</div>
        <nav class="navigation" aria-label="Main navigation">
          ${navButton("overview", "Overview")}
          ${navButton("analyze", "Image analysis")}
          ${navButton("model", "Model & methods")}
        </nav>
        <div class="sidebar-spacer"></div>
        <div class="sidebar-note">
          <span class="note-icon">${icons.shield}</span>
          <strong>Research use only</strong>
          <p>Not designed for diagnosis or clinical decision-making.</p>
        </div>
        <div class="sidebar-profile">
          <span class="profile-avatar">TR</span>
          <span><strong>Research portal</strong><small>Educational prototype</small></span>
          <button class="sign-out-button" type="button" data-action="sign-out" aria-label="Sign out" title="Sign out">${icons.logout}</button>
        </div>
      </aside>

      <main class="main">
        <header class="topbar">
          <div class="breadcrumb"><span>Workspace</span><i>/</i><strong>${state.view === "overview" ? "Overview" : state.view === "analyze" ? "Image analysis" : "Model & methods"}</strong></div>
          <div class="topbar-right">
            <span class="service-indicator ${state.service}" role="status"><i></i>${state.service === "ready" ? "Model available" : state.service === "unavailable" ? "Model unavailable" : state.service === "offline" ? "Service offline" : "Checking service"}</span>
            <span class="topbar-divider"></span>
            <span class="header-avatar">TR</span>
          </div>
        </header>
        ${content}
        <footer class="page-footer">
          <span>Histology image classification · Educational research prototype</span>
          <span>Not a medical device</span>
        </footer>
      </main>
    </div>`;
  bindNavigation();
}

function overviewPage() {
  const metrics = metricCards.map((metric, index) => `
    <article class="metric-card">
      <div class="metric-top"><span class="metric-index">0${index + 1}</span><span class="metric-dot"></span></div>
      <strong class="metric-value">${metric.value}</strong>
      <span class="metric-label">${metric.label}</span>
      <span class="metric-note">${metric.note}</span>
    </article>`).join("");

  return `
    <section class="page-content">
      <div class="eyebrow"><span class="eyebrow-line"></span> BREAST HISTOPATHOLOGY · MODEL OVERVIEW</div>
      <section class="hero">
        <div class="hero-copy">
          <span class="hero-kicker">IMAGE CLASSIFICATION WORKSPACE</span>
          <h1>A closer look at<br /><em>tissue patterns.</em></h1>
          <p>Explore an educational deep-learning workflow for classifying breast histopathology images.</p>
          <button class="button button-primary" data-view="analyze">Open image analysis ${icons.arrow}</button>
          <div class="hero-caption"><span class="caption-dot"></span> MobileNetV2 · Transfer learning · BreakHis dataset</div>
        </div>
        <div class="hero-art" aria-hidden="true">
          <div class="art-label"><span>SPECIMEN</span><strong>BH-RESEARCH / 01</strong></div>
          <svg class="tissue-art" viewBox="0 0 440 330" fill="none">
            <defs><clipPath id="slide"><rect x="38" y="28" width="364" height="268" rx="8"/></clipPath><linearGradient id="glass" x1="30" y1="25" x2="410" y2="310" gradientUnits="userSpaceOnUse"><stop stop-color="#DAB5AF"/><stop offset="1" stop-color="#76566C"/></linearGradient></defs>
            <rect x="25" y="17" width="390" height="296" rx="14" fill="#302832" stroke="#5C4B5B"/>
            <rect x="38" y="28" width="364" height="268" rx="8" fill="url(#glass)"/>
            <g clip-path="url(#slide)" opacity=".93">
              <path d="M16 162C45 112 78 132 95 94c17-39 49-41 74-8 24 33 46 28 67-8 21-37 52-41 77-7 25 35 60 17 96 4v239H12L16 162Z" fill="#A96779"/>
              <path d="M36 143c27-37 48-5 70-41 19-30 47-18 54 11 9 38 40 33 62 1 17-25 34-28 45-3 16 37 40 40 61 10 20-30 43-14 66 8v109H31l5-95Z" fill="#DEA99F"/>
              <g fill="#523B64">
                <ellipse cx="70" cy="165" rx="12" ry="7" transform="rotate(-33 70 165)"/><ellipse cx="113" cy="132" rx="10" ry="6" transform="rotate(18 113 132)"/><ellipse cx="146" cy="188" rx="13" ry="8" transform="rotate(-26 146 188)"/><ellipse cx="193" cy="136" rx="10" ry="7" transform="rotate(27 193 136)"/><ellipse cx="222" cy="194" rx="14" ry="8" transform="rotate(-12 222 194)"/><ellipse cx="276" cy="148" rx="11" ry="7" transform="rotate(31 276 148)"/><ellipse cx="320" cy="184" rx="13" ry="7" transform="rotate(-29 320 184)"/><ellipse cx="359" cy="131" rx="10" ry="6" transform="rotate(22 359 131)"/>
                <ellipse cx="94" cy="225" rx="11" ry="7" transform="rotate(22 94 225)"/><ellipse cx="174" cy="244" rx="13" ry="8" transform="rotate(-22 174 244)"/><ellipse cx="255" cy="233" rx="11" ry="6" transform="rotate(16 255 233)"/><ellipse cx="337" cy="244" rx="14" ry="8" transform="rotate(-31 337 244)"/>
              </g>
              <g fill="#F2D7CF" opacity=".85"><circle cx="80" cy="91" r="22"/><circle cx="254" cy="89" r="18"/><circle cx="331" cy="104" r="24"/><circle cx="128" cy="260" r="18"/></g>
              <path d="M39 201c49-27 79-2 111-28s47 8 82-2 47-38 79-19 57 17 94-7" stroke="#F5DDD4" stroke-width="8" stroke-linecap="round" opacity=".72"/>
            </g>
            <path d="M294 279h83" stroke="#D3BBC8" stroke-width="2"/><path d="M294 275v8m83-8v8" stroke="#D3BBC8" stroke-width="2"/>
            <circle cx="362" cy="43" r="4" fill="#E98D54"/><circle cx="376" cy="43" r="4" fill="#D9B3AE"/>
          </svg>
          <div class="art-meta"><span>ILLUSTRATIVE TISSUE VIEW</span><span>40× — 400×</span></div>
        </div>
      </section>

      <section class="metrics-section">
        <div class="section-heading"><div><span class="section-kicker">AT A GLANCE</span><h2>Dataset & model context</h2></div><span class="section-aside">01 — 04</span></div>
        <div class="metric-grid">${metrics}</div>
      </section>

      <section class="overview-bottom">
        <article class="performance-card">
          <div class="section-heading compact"><div><span class="section-kicker">RECORDED EVALUATION</span><h2>Baseline test results</h2></div><span class="data-badge">Held-out test split</span></div>
          <p class="card-description">Previously recorded metrics for the original model at a 0.50 threshold.</p>
          <div class="performance-list">
            ${[
              ["Accuracy", "69.54%", 69.54],
              ["Precision", "85.62%", 85.62],
              ["Recall", "67.39%", 67.39],
              ["F1 score", "75.42%", 75.42],
            ].map(([label, value, width]) => `<div class="performance-row"><span>${label}</span><div class="bar-track"><i style="width:${width}%"></i></div><strong>${value}</strong></div>`).join("")}
          </div>
          <p class="fine-print">Experimental results. Performance does not indicate clinical suitability.</p>
        </article>
        <article class="threshold-card">
          <span class="threshold-icon">${icons.analyze}</span>
          <span class="section-kicker">SELECTED CLASSIFICATION THRESHOLD</span>
          <div class="threshold-number">0.30</div>
          <p>Chosen using validation data to compare the malignant-class output score.</p>
          <button class="text-button" data-view="model">Review model notes ${icons.arrow}</button>
        </article>
      </section>
    </section>`;
}

function analyzePage() {
  const preview = state.previewUrl
    ? `<div class="preview-frame"><img src="${state.previewUrl}" alt="Preview of selected histopathology image" /><button class="remove-file" data-action="remove" aria-label="Remove image">×</button></div>`
    : `<div class="upload-symbol">${icons.upload}</div><strong>Drop a tissue image here</strong><span>or <button class="inline-button" data-action="browse">browse files</button></span><small>PNG or JPEG · Maximum 10 MB</small>`;

  const result = state.result
    ? `<div class="result-card ${state.result.predicted_class.toLowerCase()}">
        <div class="result-heading"><span class="result-mark">${icons.check}</span><div><span class="section-kicker">MODEL OUTPUT</span><h3>${escapeHtml(state.result.predicted_class)} pattern</h3></div></div>
        <div class="result-numbers"><div><strong>${Number(state.result.confidence_percent).toFixed(2)}%</strong><span>Model confidence*</span></div><div><strong>${Number(state.result.malignant_score_percent).toFixed(2)}%</strong><span>Malignant-class score*</span></div></div>
        <div class="score-track"><i style="width:${clamp(Number(state.result.malignant_score_percent), 0, 100)}%"></i><span style="left:${clamp(Number(state.result.threshold) * 100, 0, 100)}%"></span></div>
        <div class="score-caption"><span>Benign range</span><span>Threshold ${Number(state.result.threshold).toFixed(2)}</span><span>Malignant range</span></div>
        <p class="result-disclaimer">* Experimental model outputs, not clinically calibrated probabilities or a diagnosis.</p>
      </div>`
    : "";

  return `
    <section class="page-content">
      <div class="eyebrow"><span class="eyebrow-line"></span> ANALYSIS · IMAGE CLASSIFICATION</div>
      <div class="page-title-row"><div><h1 class="page-title">Image analysis</h1><p class="page-subtitle">Explore a model-generated classification for one histopathology image.</p></div><span class="protocol-tag">PROTOCOL 01 <i></i> MOBILE NET V2</span></div>
      <div class="analysis-layout">
        <section class="panel upload-panel">
          <div class="panel-heading"><div><span class="section-kicker">STEP 01</span><h2>Select a specimen image</h2></div><span class="panel-icon">${icons.upload}</span></div>
          <p class="card-description">Choose a tissue image in PNG or JPEG format. The image is processed by the research model on this local service.</p>
          <input id="image-input" type="file" accept="image/png,image/jpeg,.png,.jpg,.jpeg" hidden />
          <div class="dropzone ${state.file ? "has-file" : ""}" id="dropzone" role="button" tabindex="0" aria-label="Choose a PNG or JPEG histopathology image">
            ${preview}
            ${state.file ? `<div class="file-meta"><strong>${escapeHtml(state.file.name)}</strong><span>${formatBytes(state.file.size)}</span></div>` : ""}
          </div>
          ${state.error ? `<p class="inline-error" role="alert">${escapeHtml(state.error)}</p>` : ""}
          <button class="button button-primary analyze-button" data-action="analyze" ${!state.file || state.busy ? "disabled" : ""}>
            ${state.busy ? '<span class="spinner"></span> Analyzing image…' : `Run classification ${icons.arrow}`}
          </button>
          <p class="privacy-note">${icons.shield}<span>Images are sent only to the backend configured for this application and are not saved by the API.</span></p>
        </section>
        <aside class="analysis-aside">
          <section class="panel method-panel">
            <span class="section-kicker">MODEL CONFIGURATION</span>
            <div class="method-row"><span>Architecture</span><strong>MobileNetV2</strong></div>
            <div class="method-row"><span>Input dimensions</span><strong>224 × 224 px</strong></div>
            <div class="method-row"><span>Output classes</span><strong>Benign / Malignant</strong></div>
            <div class="method-row"><span>Decision threshold</span><strong>0.30</strong></div>
            <div class="method-status ${state.service}"><i></i>${state.service === "ready" ? "Prediction service ready" : state.service === "unavailable" ? "Model file not found" : state.service === "offline" ? "Prediction service offline" : "Connecting to prediction service"}</div>
          </section>
          <section class="caution-card"><span class="caution-symbol">!</span><div><strong>Educational use only</strong><p>This model is not clinically validated. Results must not be used to guide care or replace professional medical advice.</p></div></section>
        </aside>
      </div>
      ${result}
    </section>`;
}

function modelPage() {
  return `
    <section class="page-content">
      <div class="eyebrow"><span class="eyebrow-line"></span> DOCUMENTATION · EXPERIMENTAL MODEL</div>
      <div class="page-title-row"><div><h1 class="page-title">Model & methods</h1><p class="page-subtitle">A transparent summary of the research setup and its limitations.</p></div><span class="protocol-tag">EDUCATIONAL RESEARCH</span></div>
      <section class="panel model-intro">
        <div class="model-badge">${icons.model}</div><div><span class="section-kicker">IMAGE CLASSIFICATION</span><h2>MobileNetV2 transfer learning</h2><p>A binary image classifier trained on breast histopathology images from the BreakHis dataset. Model output scores are not calibrated clinical probabilities.</p></div>
      </section>
      <div class="model-grid">
        <section class="panel detail-panel"><span class="section-kicker">MODEL SPECIFICATION</span><h2>Inference settings</h2><div class="method-row"><span>Architecture</span><strong>MobileNetV2</strong></div><div class="method-row"><span>Image input</span><strong>224 × 224 · RGB</strong></div><div class="method-row"><span>Classes</span><strong>Benign / Malignant</strong></div><div class="method-row"><span>Decision threshold</span><strong>0.30</strong></div><div class="method-row"><span>Dataset</span><strong>BreakHis</strong></div></section>
        <section class="panel detail-panel"><span class="section-kicker">VALIDATION SNAPSHOT</span><h2>Selected threshold results</h2><p class="card-description">Recorded on validation data using a 0.30 threshold.</p><div class="validation-stat"><span>Accuracy</span><strong>74.40%</strong></div><div class="validation-stat"><span>Precision</span><strong>75.36%</strong></div><div class="validation-stat"><span>Recall</span><strong>92.50%</strong></div><div class="validation-stat"><span>F1 score</span><strong>83.05%</strong></div><p class="fine-print">Validation results, not independent test performance.</p></section>
      </div>
      <section class="method-note"><span class="note-icon">${icons.shield}</span><div><strong>Important limitations</strong><p>This project is an educational research prototype, not a medical device. The model has limited performance and has not been clinically validated. Do not use its outputs for screening, diagnosis, treatment, or other healthcare decisions. Consult qualified medical professionals for health concerns.</p></div></section>
    </section>`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]);
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, Number.isFinite(value) ? value : min));
}

function formatBytes(bytes) {
  return bytes >= 1024 * 1024
    ? `${(bytes / (1024 * 1024)).toFixed(1)} MB`
    : `${Math.max(1, Math.round(bytes / 1024))} KB`;
}

function render() {
  if (!state.workspaceEntered) {
    app.innerHTML = loginPage();
    bindLogin();
    return;
  }

  const content = state.view === "analyze"
    ? analyzePage()
    : state.view === "model"
      ? modelPage()
      : overviewPage();
  shell(content);
  app.querySelector("[data-action='sign-out']").addEventListener("click", () => {
    if (state.previewUrl) URL.revokeObjectURL(state.previewUrl);
    state.workspaceEntered = false;
    state.profileEmail = "";
    state.view = "overview";
    state.file = null;
    state.previewUrl = "";
    state.result = null;
    state.error = "";
    render();
  });
  if (state.view === "analyze") bindUploader();
}

function bindLogin() {
  const form = app.querySelector("#login-form");
  const password = form.querySelector("#login-password");
  const passwordToggle = form.querySelector("[data-action='toggle-password']");
  passwordToggle.addEventListener("click", () => {
    const showPassword = password.type === "password";
    password.type = showPassword ? "text" : "password";
    passwordToggle.textContent = showPassword ? "Hide" : "Show";
    passwordToggle.setAttribute("aria-label", `${showPassword ? "Hide" : "Show"} password`);
    passwordToggle.setAttribute("aria-pressed", String(showPassword));
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    state.profileEmail = form.querySelector("#login-email").value.trim();
    state.workspaceEntered = true;
    render();
  });
}

function bindNavigation() {
  app.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      state.view = button.dataset.view;
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
}

function setFile(file) {
  state.error = "";
  state.result = null;
  if (!file) return;
  if (!["image/png", "image/jpeg"].includes(file.type)) {
    state.error = "Choose a PNG or JPEG image.";
  } else if (file.size > 10 * 1024 * 1024) {
    state.error = "The image must be smaller than 10 MB.";
  } else {
    if (state.previewUrl) URL.revokeObjectURL(state.previewUrl);
    state.file = file;
    state.previewUrl = URL.createObjectURL(file);
  }
  if (state.error) {
    state.file = null;
    if (state.previewUrl) URL.revokeObjectURL(state.previewUrl);
    state.previewUrl = "";
  }
  render();
}

function bindUploader() {
  const input = app.querySelector("#image-input");
  const dropzone = app.querySelector("#dropzone");
  dropzone.addEventListener("click", (event) => {
    if (event.target.closest("[data-action='remove']")) {
      state.file = null;
      state.result = null;
      state.error = "";
      URL.revokeObjectURL(state.previewUrl);
      state.previewUrl = "";
      render();
      return;
    }
    if (!state.file) input.click();
  });
  dropzone.addEventListener("keydown", (event) => {
    if (!state.file && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      input.click();
    }
  });
  input.addEventListener("change", () => setFile(input.files?.[0]));
  for (const eventName of ["dragenter", "dragover"]) {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add("dragging");
    });
  }
  for (const eventName of ["dragleave", "drop"]) {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.remove("dragging");
    });
  }
  dropzone.addEventListener("drop", (event) => setFile(event.dataTransfer.files[0]));
  app.querySelector("[data-action='browse']")?.addEventListener("click", (event) => {
    event.stopPropagation();
    input.click();
  });
  app.querySelector("[data-action='analyze']")?.addEventListener("click", runAnalysis);
}

async function runAnalysis() {
  if (!state.file || state.busy) return;
  state.busy = true;
  state.error = "";
  state.result = null;
  render();
  const body = new FormData();
  body.append("file", state.file);
  try {
    const response = await fetch(`${API_URL}/api/predict`, { method: "POST", body });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "The prediction request failed.");
    state.result = payload;
  } catch (error) {
    state.error = error instanceof TypeError
      ? "Could not reach the prediction service. Check that the backend is running."
      : error.message;
  } finally {
    state.busy = false;
    render();
  }
}

async function checkService() {
  try {
    const response = await fetch(`${API_URL}/api/health`);
    if (!response.ok) throw new Error(`Health check returned ${response.status}.`);
    const payload = await response.json();
    state.service = payload.model_available ? "ready" : "unavailable";
  } catch (error) {
    console.warn("Prediction service health check failed:", error);
    state.service = "offline";
  }
  render();
}

render();
checkService();
