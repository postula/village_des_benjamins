// @ts-check
/**
 * Reservation / inscription page — `/#/reservation`
 *
 * Requires authentication.  Tests that verify the reservation modal or the
 * holidays list are skipped gracefully when no seeded data is present.
 *
 * Required env vars:
 *   E2E_USER_EMAIL
 *   E2E_USER_PASSWORD
 */

const { test, expect } = require("@playwright/test");
const { loginViaAPI } = require("./helpers/auth");

const EMAIL = process.env.E2E_USER_EMAIL;
const PASSWORD = process.env.E2E_USER_PASSWORD;

test.beforeAll(async () => {
  if (!EMAIL || !PASSWORD) {
    console.warn(
      "[reservation.spec.js] E2E_USER_EMAIL / E2E_USER_PASSWORD not set — all tests will be skipped.",
    );
  }
});

test.beforeEach(async ({ page }) => {
  if (!EMAIL || !PASSWORD) {
    test.skip();
    return;
  }
  await loginViaAPI(page, EMAIL, PASSWORD);
  await page.goto("/#/reservation");
  // Wait for the main card to mount.  The page has two cards:
  //   1. "Programme des vacances"
  //   2. "Mes Réservations"
  await page.waitForSelector(".card", { timeout: 10_000 });
});

// ---------------------------------------------------------------------------
// Page structure
// ---------------------------------------------------------------------------

test.describe("Structure de la page Réservation", () => {
  test("should load the reservation page without redirecting to login", async ({
    page,
  }) => {
    await expect(page).not.toHaveURL(/\/#\/login/);
    await expect(page).toHaveURL(/\/#\/reservation/);
  });

  test('should display the "Programme des vacances" card header', async ({
    page,
  }) => {
    // Reservation.vue renders <h5 slot="header">Programme des vacances</h5>
    // inside the first Card component.
    await expect(page.getByText("Programme des vacances")).toBeVisible({
      timeout: 8_000,
    });
  });

  test('should display the "Mes Réservations" card header', async ({
    page,
  }) => {
    await expect(page.getByText("Mes Réservations")).toBeVisible({
      timeout: 8_000,
    });
  });

  test("should display the reservation info alert", async ({ page }) => {
    // The page has a static informational alert about when reservations open.
    await expect(page.locator(".alert.alert-info")).toContainText(
      "Information importante",
    );
  });

  test('should display the "Mes Réservations" confirmation alert', async ({
    page,
  }) => {
    await expect(page.locator(".alert.alert-success")).toContainText(
      "Confirmation de réservation",
    );
  });
});

// ---------------------------------------------------------------------------
// Holidays list (data-dependent)
// ---------------------------------------------------------------------------

test.describe("Liste des vacances (données requises)", () => {
  async function getHolidayItems(page) {
    // Each holiday is a list-group-item inside the first card's list-group.
    return page
      .locator(".card .list-group .list-group-item")
      .count()
      .catch(() => 0);
  }

  test("should render a holiday entry for each holiday from the API", async ({
    page,
  }) => {
    // Wait for the API call to complete — the list-group is empty while loading.
    await page.waitForTimeout(2_000);
    const count = await getHolidayItems(page);

    if (count === 0) {
      // No holidays in the DB is a valid state — we just verify no error occurred.
      await expect(page.locator(".alert.alert-danger")).not.toBeVisible();
      return;
    }

    // Each holiday item should show the holiday name and dates.
    const firstItem = page
      .locator(".card .list-group .list-group-item")
      .first();
    await expect(firstItem).toBeVisible();
    // The holiday template renders a <h5 class="mb-1"> with the name.
    await expect(firstItem.locator("h5.mb-1").first()).toBeVisible();
  });

  test("should display tabs inside each holiday when holidays exist", async ({
    page,
  }) => {
    await page.waitForTimeout(2_000);
    const count = await getHolidayItems(page);

    if (count === 0) {
      test.skip(true, "No holidays in DB — skipping tabs test");
    }

    // The Tabs component renders <ul class="nav"> with tab triggers.
    const tabs = page
      .locator(".card .list-group .list-group-item")
      .first()
      .locator(".nav");
    await expect(tabs).toBeVisible({ timeout: 5_000 });

    // "Informations Générales" tab is always present.
    await expect(tabs.getByText("Informations Générales")).toBeVisible();
  });

  test("should switch to a section tab when clicking it", async ({ page }) => {
    await page.waitForTimeout(2_000);
    const count = await getHolidayItems(page);

    if (count === 0) {
      test.skip(true, "No holidays in DB — skipping tab switch test");
    }

    const firstItem = page
      .locator(".card .list-group .list-group-item")
      .first();

    // Count available tabs — if only "Informations Générales" exists there is
    // nothing to switch to.
    const tabCount = await firstItem.locator(".nav .nav-item").count();
    if (tabCount < 2) {
      test.skip(true, "Holiday has no section tabs — skipping switch test");
    }

    // Click the second tab (first section).
    const secondTab = firstItem.locator(".nav .nav-item").nth(1).locator("a, button, span");
    await secondTab.first().click();

    // After clicking, the active tab pane should be visible.
    await expect(firstItem.locator(".tab-pane.active")).toBeVisible({
      timeout: 5_000,
    });
  });
});

// ---------------------------------------------------------------------------
// Reservation modal (requires both holidays and eligible children)
// ---------------------------------------------------------------------------

test.describe("Modal de réservation", () => {
  /**
   * Find the first "Réserver" button that is enabled (not disabled because
   * all children are already booked).  Returns null if none found.
   */
  async function findEnabledReserveButton(page) {
    const buttons = page.getByRole("button", { name: "Réserver" });
    const count = await buttons.count();
    for (let i = 0; i < count; i++) {
      const btn = buttons.nth(i);
      const isDisabled = await btn.isDisabled();
      if (!isDisabled) {
        return btn;
      }
    }
    return null;
  }

  test.beforeEach(async ({ page }) => {
    // Give the API time to populate holidays and children.
    await page.waitForTimeout(2_000);
  });

  test('should show the "Réserver" button on holidays when registration is open', async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);

    if (!reserveButton) {
      // Either no holidays, registration is closed, or all children are booked.
      // Verify no JS error crashed the page.
      await expect(page.locator(".alert.alert-danger")).not.toBeVisible();
      test.skip(
        true,
        "No enabled Réserver button available — skipping modal open test",
      );
    }

    await expect(reserveButton).toBeVisible();
  });

  test('should open the reservation modal when clicking "Réserver"', async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);

    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button available — skipping modal open test",
      );
    }

    await reserveButton.click();

    // Scope all assertions to the reservation modal wrapper.
    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    await expect(reservationModal.locator(".modal-header")).toContainText(
      "Ajouter une réservation pour",
      { timeout: 5_000 },
    );
  });

  test("should show the child dropdown in the reservation modal", async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping modal field tests",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    // BaseInput with label="Enfant" wraps a <select class="form-control">.
    // We wait for the capacity API call to finish before the select appears.
    await expect(
      reservationModal.locator("select.form-control").first(),
    ).toBeVisible({ timeout: 8_000 });
  });

  test("should show the date picker in the reservation modal", async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping date picker test",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    // flat-picker input for dates.
    await expect(
      reservationModal.locator("input.form-control.datepicker"),
    ).toBeVisible({ timeout: 8_000 });
  });

  test("should show the health notes textarea in the reservation modal", async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping notes textarea test",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    const textarea = reservationModal.locator("textarea.form-control");
    await expect(textarea).toBeVisible({ timeout: 8_000 });
    await expect(textarea).toHaveAttribute(
      "placeholder",
      /allergies|santé/i,
    );
  });

  test("should show the price calculation table in the reservation modal", async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping price table test",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    // The prix section renders a <table class="table table-borderless"> with a
    // "Total" row.
    const priceTable = reservationModal.locator(".table.table-borderless");
    await expect(priceTable).toBeVisible({ timeout: 8_000 });
    await expect(priceTable).toContainText("Total");
  });

  test("should show validation errors when submitting the modal without selecting a child", async ({
    page,
  }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping modal validation test",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    // Click confirm without choosing a child or dates.
    await reservationModal
      .locator(".modal-footer")
      .getByText("Réserver")
      .click();

    // Validation prevents submission — the modal should remain open.
    await expect(
      reservationModal.locator(".modal.show"),
    ).toBeVisible({ timeout: 3_000 });
  });

  test("should close the modal when clicking Annuler", async ({ page }) => {
    const reserveButton = await findEnabledReserveButton(page);
    if (!reserveButton) {
      test.skip(
        true,
        "No enabled Réserver button — skipping cancel test",
      );
    }
    await reserveButton.click();
    await page.waitForSelector('[data-testid="reservation-modal"] .modal.show');

    const reservationModal = page.locator('[data-testid="reservation-modal"]');
    await reservationModal
      .locator(".modal-footer")
      .getByText("Annuler")
      .click();

    await expect(reservationModal.locator(".modal.show")).not.toBeVisible({
      timeout: 5_000,
    });
  });
});
