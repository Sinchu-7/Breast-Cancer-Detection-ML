import "./login.css";

const galaxyStars = Array.from({ length: 56 }, (_, index) => {
  const x = ((index * 47 + 11) % 97) + 1;
  const y = ((index * 61 + 23) % 95) + 2;
  const driftX = (index * 17) % 111 - 55;
  const driftY = (index * 29) % 101 - 50;
  const points = [
    [driftX, driftY],
    [-driftX * 0.65, driftY * 0.85],
    [driftX * 0.55, -driftY],
    [0, 0],
  ];
  const path = points
    .map(([offsetX, offsetY], point) =>
      `--star-x${point + 1}:${offsetX.toFixed(1)}px;--star-y${point + 1}:${offsetY.toFixed(1)}px`,
    )
    .join(";");
  const size = index % 13 === 0 ? 3.5 : index % 4 === 0 ? 2.5 : 1.5;

  return `<span style="--star-x:${x}%;--star-y:${y}%;--star-size:${size}px;--star-duration:${55 + (index * 19) % 39}s;--star-delay:-${(index * 13) % 83}s;${path}"></span>`;
}).join("");

export function loginPage() {
  return `
    <main class="login-page">
      <div class="login-starfield" aria-hidden="true">${galaxyStars}</div>
      <a class="login-brand" href="#" aria-label="Tissue Research home">
        <span class="brand-mark">t<span>.</span></span>
        <span class="brand-copy"><strong>tissue</strong><small>RESEARCH WORKSPACE</small></span>
      </a>

      <div class="login-layout">
        <section class="login-intro" aria-labelledby="login-intro-title">
          <div class="login-specimen">
            <span class="login-specimen-label">BREAST HISTOPATHOLOGY · BREAKHIS</span>
            <svg viewBox="0 0 440 280" fill="none" aria-hidden="true">
              <defs>
                <linearGradient id="login-glass" x1="30" y1="20" x2="410" y2="260" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#DAB5AF"/>
                  <stop offset="1" stop-color="#76566C"/>
                </linearGradient>
                <clipPath id="login-slide"><rect x="34" y="26" width="372" height="226" rx="8"/></clipPath>
              </defs>
              <rect x="21" y="14" width="398" height="252" rx="14" fill="#302832" stroke="#5C4B5B"/>
              <rect x="34" y="26" width="372" height="226" rx="8" fill="url(#login-glass)"/>
              <g clip-path="url(#login-slide)" opacity=".93">
                <path d="M12 149C50 104 79 133 102 87c22-43 50-32 73 0 24 33 49 24 69-12 21-38 50-38 76-5 25 33 53 20 94-4v216H12V149Z" fill="#A96779"/>
                <path d="M23 154c35-45 60-2 82-43 18-33 48-15 58 16 11 35 38 23 62-8 20-26 39-29 54-1 16 31 37 35 60 7 24-29 48-18 77 5v112H23v-88Z" fill="#DEA99F"/>
                <g fill="#523B64">
                  <ellipse cx="70" cy="158" rx="12" ry="7" transform="rotate(-33 70 158)"/>
                  <ellipse cx="113" cy="126" rx="10" ry="6" transform="rotate(18 113 126)"/>
                  <ellipse cx="153" cy="184" rx="13" ry="8" transform="rotate(-26 153 184)"/>
                  <ellipse cx="201" cy="133" rx="10" ry="7" transform="rotate(27 201 133)"/>
                  <ellipse cx="241" cy="194" rx="14" ry="8" transform="rotate(-12 241 194)"/>
                  <ellipse cx="292" cy="149" rx="11" ry="7" transform="rotate(31 292 149)"/>
                  <ellipse cx="345" cy="187" rx="13" ry="7" transform="rotate(-29 345 187)"/>
                  <ellipse cx="94" cy="218" rx="11" ry="7" transform="rotate(22 94 218)"/>
                  <ellipse cx="181" cy="229" rx="13" ry="8" transform="rotate(-22 181 229)"/>
                  <ellipse cx="276" cy="224" rx="11" ry="6" transform="rotate(16 276 224)"/>
                  <ellipse cx="363" cy="226" rx="14" ry="8" transform="rotate(-31 363 226)"/>
                </g>
                <g fill="#F2D7CF" opacity=".85">
                  <circle cx="80" cy="83" r="22"/>
                  <circle cx="254" cy="82" r="18"/>
                  <circle cx="335" cy="97" r="24"/>
                  <circle cx="128" cy="242" r="18"/>
                </g>
                <path d="M27 196c49-27 79-2 111-28s47 8 82-2 47-38 79-19 57 17 107-7" stroke="#F5DDD4" stroke-width="8" stroke-linecap="round" opacity=".72"/>
              </g>
            </svg>
            <div class="login-intro-copy">
              <span class="login-eyebrow">A RESEARCH WORKSPACE</span>
              <h1 id="login-intro-title">A closer look at <em>tissue patterns.</em></h1>
              <p>Explore an educational deep-learning workflow for breast histopathology images.</p>
            </div>
          </div>
          <p class="login-disclaimer">For educational research only · Not a medical diagnostic tool</p>
        </section>

        <section class="login-panel" aria-labelledby="login-title">
          <div class="login-panel-heading">
            <span class="login-eyebrow">WELCOME</span>
            <h2 id="login-title">Sign in to continue</h2>
            <p>Enter any email and password to open the demo workspace.</p>
          </div>

          <div class="demo-notice" id="demo-notice" role="note">
            <strong>Demo sign-in</strong>
            <span>No account is verified. Your credentials are not sent or saved.</span>
          </div>

          <form class="login-form" id="login-form" aria-describedby="demo-notice">
            <label for="login-email">Email address</label>
            <input id="login-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required />

            <div class="login-password-label">
              <label for="login-password">Password</label>
            </div>
            <div class="login-password-field">
              <input id="login-password" name="password" type="password" autocomplete="current-password" placeholder="Enter any password" required />
              <button class="password-toggle" type="button" data-action="toggle-password" aria-controls="login-password" aria-label="Show password" aria-pressed="false">Show</button>
            </div>

            <button class="button button-primary login-submit" type="submit">
              Enter workspace
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>
            </button>
          </form>

          <p class="login-footnote">This prototype does not provide account security or authentication.</p>
        </section>
      </div>
    </main>`;
}
