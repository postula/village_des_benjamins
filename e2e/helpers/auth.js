/**
 * Authentication helpers for E2E tests.
 *
 * The app uses vuex-persistedstate which serialises the entire Vuex store
 * into localStorage under the key "vuex".  Bypassing the login UI and writing
 * the token directly is faster and keeps auth tests isolated from the login
 * flow tests.
 *
 * Required env vars (set in .env.test or export before running):
 *   E2E_USER_EMAIL    – email of a seeded test user
 *   E2E_USER_PASSWORD – password of that user
 */

const { request } = require("@playwright/test");

const BASE_URL = process.env.BASE_URL || "http://localhost:8000";
const OBTAIN_URL = `${BASE_URL}/api/jwt/obtain`;

/**
 * Obtain a JWT pair by posting credentials to the Django API.
 * Returns { access, refresh } or throws on failure.
 */
async function obtainTokens(email, password) {
  const context = await request.newContext();
  const response = await context.post(OBTAIN_URL, {
    data: { email: email.toLowerCase(), password },
  });

  if (!response.ok()) {
    const body = await response.text();
    throw new Error(
      `Failed to obtain JWT tokens (status ${response.status()}): ${body}`,
    );
  }

  const json = await response.json();
  await context.dispose();
  return { access: json.access, refresh: json.refresh };
}

/**
 * Decode the JWT payload (base64url → JSON).
 * No signature verification — we trust our own server in tests.
 */
function decodeJwtPayload(token) {
  const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
  return JSON.parse(Buffer.from(base64, "base64").toString("utf8"));
}

/**
 * Log in programmatically by writing Vuex persisted state directly into
 * localStorage.  This skips the login form entirely, which keeps auth test
 * concerns separate from the login page tests.
 *
 * Call this inside a beforeEach / test that needs an authenticated session:
 *
 *   await loginViaAPI(page, process.env.E2E_USER_EMAIL, process.env.E2E_USER_PASSWORD);
 *   await page.goto("/#/children");
 */
async function loginViaAPI(page, email, password) {
  const { access, refresh } = await obtainTokens(email, password);
  const userPayload = decodeJwtPayload(access);

  const vuexState = {
    accessToken: access,
    refreshToken: refresh,
    currentUser: {
      user_id: userPayload.user_id,
      email: userPayload.email,
      authenticated: true,
      is_staff: userPayload.is_staff || false,
    },
    users: {},
    children: [],
    holidays: [],
    registrations: [],
    contents: [],
    sections: [],
    team_members: [],
    news: [],
    capacity_loading: false,
  };

  // Navigate to the app to get a valid origin for localStorage.
  await page.goto("/");
  await page.evaluate((state) => {
    localStorage.setItem("vuex", JSON.stringify(state));
  }, vuexState);

  // Force a full page reload (not just hash navigation) so Vue reboots
  // and vuex-persistedstate reads the token from localStorage.
  await page.goto("about:blank");
  await page.goto("/#/children", { waitUntil: "networkidle" });
  await page.waitForSelector('[data-testid="nav-deconnexion"]', { timeout: 15_000 });
}

/**
 * Clear Vuex persisted state so the next test starts unauthenticated.
 *
 * Navigates to the app root first — accessing localStorage from about:blank
 * raises a SecurityError because the page has no valid origin yet.
 */
async function logout(page) {
  await page.goto("/#/");
  await page.evaluate(() => localStorage.removeItem("vuex"));
}

module.exports = { loginViaAPI, logout, obtainTokens };
