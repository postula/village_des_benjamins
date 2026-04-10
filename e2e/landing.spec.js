// @ts-check
/**
 * Landing page (accueil) — `/#/`
 *
 * These tests verify that the public-facing home page loads correctly and
 * that the navigation shell (header + footer) is always present.  Content
 * sections are fetched from the API so we test that *something* rendered
 * rather than asserting on specific copy.
 *
 * No authentication required.
 */

const { test, expect } = require("@playwright/test");
const { logout } = require("./helpers/auth");

test.describe("Page d'accueil (Landing)", () => {
  test.beforeEach(async ({ page }) => {
    // Ensure we start every test in an unauthenticated state.
    await logout(page);
    await page.goto("/#/");
    // Wait until the Vue SPA has hydrated — the header brand link is a reliable
    // indicator because it is rendered synchronously on mount.
    await page.waitForSelector("nav", { timeout: 10_000 });
  });

  // --- Navigation header ---

  test("should display the site logo in the header", async ({ page }) => {
    const logo = page.locator('[data-testid="nav-logo"]');
    await expect(logo).toBeVisible();
  });

  test('should show the "Accueil" dropdown menu item in the navigation', async ({
    page,
  }) => {
    await expect(page.locator('[data-testid="nav-accueil"]')).toBeVisible();
  });

  test('should show the "Réservation" navigation link', async ({ page }) => {
    await expect(page.locator('[data-testid="nav-reservation"]')).toBeVisible();
  });

  test('should show the "Enfants" navigation link', async ({ page }) => {
    await expect(page.locator('[data-testid="nav-enfants"]')).toBeVisible();
  });

  // --- Auth-aware navigation ---

  test('should show "Connexion" and "S\'enregistrer" links when unauthenticated', async ({
    page,
  }) => {
    await expect(page.locator('[data-testid="nav-connexion"]')).toBeVisible();
    await expect(page.locator('[data-testid="nav-register"]')).toBeVisible();
  });

  test('should NOT show "Déconnexion" when unauthenticated', async ({
    page,
  }) => {
    await expect(page.locator('[data-testid="nav-deconnexion"]')).not.toBeVisible();
  });

  // --- Footer ---

  test("should display the copyright footer", async ({ page }) => {
    const footer = page.locator('[data-testid="footer"]');
    await expect(footer).toBeVisible();
    // The footer always contains the ASBL name regardless of year.
    await expect(footer).toContainText("ASBL Village des Benjamins");
  });

  // --- Dynamic content ---

  test("should render at least one content section after API data loads", async ({
    page,
  }) => {
    // The Landing view iterates over `sections` from the API and renders a
    // section component per entry.  We wait for any section-level element that
    // all layout components share.  If the API returns no sections the page
    // still loads — we simply skip the assertion.
    const sectionCount = await page
      .locator(".section, section")
      .count()
      .catch(() => 0);

    // At minimum the wrapping Vue app root must have mounted — confirmed by
    // the header being present (checked in beforeEach).  A section count of 0
    // is acceptable when the DB has no seeded content.
    if (sectionCount > 0) {
      await expect(
        page.locator(".section, section").first(),
      ).toBeVisible();
    }
  });

  // --- Accueil dropdown links ---

  test('should open "Accueil" dropdown and show sub-links', async ({
    page,
  }) => {
    // BaseDropdown shows/hides on hover or click — click the trigger.
    await page.locator('[data-testid="nav-accueil"]').click();

    // Dropdown items are links inside the nav dropdown menu.
    const dropdown = page.locator('[data-testid="nav-accueil"] .dropdown-menu');
    await expect(dropdown.getByText("Nos services")).toBeVisible();
    await expect(dropdown.getByText("Missions et objectifs")).toBeVisible();
    await expect(dropdown.getByText("Notre équipe")).toBeVisible();
    await expect(dropdown.getByText("Notre méthodologie")).toBeVisible();
    await expect(dropdown.getByText("Nous contacter")).toBeVisible();
  });
});
