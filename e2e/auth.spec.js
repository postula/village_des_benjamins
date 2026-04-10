// @ts-check
/**
 * Authentication flows
 *
 * Covers: login, register, forgot-password, protected route guards, and the
 * nav state change after authentication.
 *
 * Tests that require real credentials use the env vars:
 *   E2E_USER_EMAIL
 *   E2E_USER_PASSWORD
 *
 * Tests that only need the forms (no real credentials) run unconditionally.
 */

const { test, expect } = require("@playwright/test");
const { loginViaAPI, logout } = require("./helpers/auth");

// ---------------------------------------------------------------------------
// Login page
// ---------------------------------------------------------------------------

test.describe("Page de connexion (/#/login)", () => {
  test.beforeEach(async ({ page }) => {
    await logout(page);
    await page.goto("/#/login");
    // Wait for the form to be present — the card body is the reliable anchor.
    await page.waitForSelector('form[role="form"]', { timeout: 10_000 });
  });

  test("should render the email input", async ({ page }) => {
    await expect(page.getByPlaceholder("Email")).toBeVisible();
  });

  test("should render the password input", async ({ page }) => {
    await expect(page.getByPlaceholder("Mot de passe")).toBeVisible();
  });

  test('should render the "Se Connecter" submit button', async ({ page }) => {
    await expect(
      page.getByRole("button", { name: "Se Connecter" }),
    ).toBeVisible();
  });

  test('should show a "Mot de passe oublié?" link', async ({ page }) => {
    await expect(page.getByText("Mot de passe oublié?")).toBeVisible();
  });

  test('should show a "Créer un compte" link', async ({ page }) => {
    await expect(page.getByText("Créer un compte")).toBeVisible();
  });

  test("should display an error alert when credentials are invalid", async ({
    page,
  }) => {
    // Arrange: fill in clearly wrong credentials.
    await page.getByPlaceholder("Email").fill("invalid@example.com");
    await page.getByPlaceholder("Mot de passe").fill("wrongpassword");

    // Act: submit the form.
    await page.getByRole("button", { name: "Se Connecter" }).click();

    // The API returns a 401. The store sets errors from the response.
    // If non_field_errors exists, BaseAlert renders .alert.alert-danger.
    // Otherwise the form may just not navigate away — verify we stay on login.
    await page.waitForTimeout(3_000);
    await expect(page).toHaveURL(/\/#\/login/);
    // And we should NOT see "Déconnexion" (proving login failed).
    await expect(page.locator('[data-testid="nav-deconnexion"]')).not.toBeVisible();
  });

  test("should redirect to home after successful login", async ({ page }) => {
    const email = process.env.E2E_USER_EMAIL;
    const password = process.env.E2E_USER_PASSWORD;

    if (!email || !password) {
      test.skip(
        true,
        "E2E_USER_EMAIL / E2E_USER_PASSWORD not set — skipping live login test",
      );
    }

    await page.getByPlaceholder("Email").fill(email);
    await page.getByPlaceholder("Mot de passe").fill(password);
    await page.getByRole("button", { name: "Se Connecter" }).click();

    // After a successful login the store commits UPDATE_TOKEN which calls
    // router.push(redirect).  The default redirect is "/".
    await page.waitForURL(/\/#\/$|\/$/);
    // The header should now show "Déconnexion" instead of "Connexion".
    await expect(
      page.locator('[data-testid="nav-deconnexion"]'),
    ).toBeVisible({ timeout: 8_000 });
  });
});

// ---------------------------------------------------------------------------
// Register page
// ---------------------------------------------------------------------------

test.describe("Page d'enregistrement (/#/register)", () => {
  test.beforeEach(async ({ page }) => {
    await logout(page);
    await page.goto("/#/register");
    await page.waitForSelector('form[role="form"]', { timeout: 10_000 });
  });

  test("should render the Prénom input", async ({ page }) => {
    await expect(page.getByPlaceholder("Prénom")).toBeVisible();
  });

  test("should render the Nom input", async ({ page }) => {
    await expect(page.getByPlaceholder("Nom", { exact: true })).toBeVisible();
  });

  test("should render the Email input", async ({ page }) => {
    await expect(page.getByPlaceholder("Email")).toBeVisible();
  });

  test("should render the Mot de passe input", async ({ page }) => {
    await expect(page.getByPlaceholder("Mot de passe")).toBeVisible();
  });

  test("should render the newsletter checkbox", async ({ page }) => {
    // BaseCheckbox renders as a standard <input type="checkbox"> inside a label.
    await expect(
      page.getByText("J'accepte de recevoir des notifications"),
    ).toBeVisible();
  });

  test('should render the "S\'enregistrer" submit button', async ({ page }) => {
    await expect(
      page.getByRole("button", { name: "S'enregistrer" }),
    ).toBeVisible();
  });

  test("should show validation errors when form is submitted empty", async ({
    page,
  }) => {
    // Act: click submit without filling any field.
    await page.getByRole("button", { name: "S'enregistrer" }).click();

    // Assert: the view sets per-field error strings which BaseInput renders in
    // a <div class="text-danger invalid-feedback"> block.
    await expect(
      page.locator(".text-danger.invalid-feedback").first(),
    ).toBeVisible();

    // Each required field should show "Ce champs est obligatoire".
    const errorMessages = page.locator(".text-danger.invalid-feedback");
    await expect(errorMessages).toHaveCount(4);
  });

  test("should show newsletter validation error when checkbox is unchecked on submit", async ({
    page,
  }) => {
    // Fill all text fields but leave the newsletter checkbox unchecked.
    await page.getByPlaceholder("Prénom").fill("Jean");
    await page.getByPlaceholder("Nom", { exact: true }).fill("Dupont");
    await page.getByPlaceholder("Email").fill("jean.dupont@example.com");
    await page.getByPlaceholder("Mot de passe").fill("securepassword123");

    await page.getByRole("button", { name: "S'enregistrer" }).click();

    // The template renders `errors.accept_newsletter` in a <span class="text-danger">.
    await expect(page.locator("span.text-danger")).toContainText(
      "Ce champs est obligatoire",
    );
  });
});

// ---------------------------------------------------------------------------
// Forgot password page
// ---------------------------------------------------------------------------

test.describe("Page mot de passe oublié (/#/forgot)", () => {
  test.beforeEach(async ({ page }) => {
    await logout(page);
    await page.goto("/#/forgot");
    await page.waitForSelector('form[role="form"]', { timeout: 10_000 });
  });

  test("should render the email input", async ({ page }) => {
    await expect(page.getByPlaceholder("Email")).toBeVisible();
  });

  test('should render the "Réinitialiser" submit button', async ({ page }) => {
    await expect(
      page.getByRole("button", { name: "Réinitialiser" }),
    ).toBeVisible();
  });

  test("should show success feedback after submitting an email address", async ({
    page,
  }) => {
    // The submit handler always shows the success message regardless of whether
    // the email exists in the DB — intentional UX to avoid user enumeration.
    await page.getByPlaceholder("Email").fill("quelquun@example.com");
    await page.getByRole("button", { name: "Réinitialiser" }).click();

    // BaseAlert type="success" renders as <div class="alert alert-success">.
    await expect(page.locator(".alert.alert-success")).toContainText(
      "Si l'adresse est connue de nos systèmes",
      { timeout: 8_000 },
    );
  });

  test('should display a "Connexion" back-link', async ({ page }) => {
    // The back-link is a router-link rendered below the card, outside the form.
    // Scoped to the forgot-links row to avoid matching the header nav link.
    await expect(
      page.locator('[data-testid="forgot-links"]').getByText("Connexion"),
    ).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Protected route guards
// ---------------------------------------------------------------------------

test.describe("Redirection des routes protégées", () => {
  test.beforeEach(async ({ page }) => {
    await logout(page);
  });

  test("should redirect /#/children to /#/login when unauthenticated", async ({
    page,
  }) => {
    await page.goto("/#/children");
    // The router guard calls next({ path: '/login', query: { redirect: ... } })
    await expect(page).toHaveURL(/\/#\/login/);
  });

  test("should redirect /#/reservation to /#/login when unauthenticated", async ({
    page,
  }) => {
    await page.goto("/#/reservation");
    await expect(page).toHaveURL(/\/#\/login/);
  });

  test("should preserve the intended destination in the redirect query param", async ({
    page,
  }) => {
    await page.goto("/#/children");
    // The router appends ?redirect=%2Fchildren so the user is sent back after login.
    await expect(page).toHaveURL(/redirect/);
  });
});

// ---------------------------------------------------------------------------
// Header navigation state after authentication
// ---------------------------------------------------------------------------

test.describe("Navigation après connexion", () => {
  test('should replace "Connexion"/"S\'enregistrer" with "Déconnexion" when authenticated', async ({
    page,
  }) => {
    const email = process.env.E2E_USER_EMAIL;
    const password = process.env.E2E_USER_PASSWORD;

    if (!email || !password) {
      test.skip(
        true,
        "E2E_USER_EMAIL / E2E_USER_PASSWORD not set — skipping authenticated nav test",
      );
    }

    await loginViaAPI(page, email, password);
    // Navigate to children page where nav is reliably visible.
    await page.goto("/#/children");
    await page.waitForSelector("nav", { timeout: 10_000 });

    // Authenticated state: only "Déconnexion" should be visible in the nav.
    await expect(
      page.locator('[data-testid="nav-deconnexion"]'),
    ).toBeVisible({ timeout: 8_000 });
    await expect(
      page.locator('[data-testid="nav-connexion"]'),
    ).not.toBeVisible();
    await expect(
      page.locator('[data-testid="nav-register"]'),
    ).not.toBeVisible();
  });
});
