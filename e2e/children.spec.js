// @ts-check
/**
 * Children management page — `/#/children`
 *
 * Requires authentication.  We use loginViaAPI() in beforeEach to write the
 * Vuex persisted state directly into localStorage, bypassing the login form.
 *
 * Required env vars:
 *   E2E_USER_EMAIL
 *   E2E_USER_PASSWORD
 *
 * If the env vars are not set every test in this file is skipped so the suite
 * does not fail on machines without a seeded DB.
 */

const { test, expect } = require("@playwright/test");
const { loginViaAPI } = require("./helpers/auth");

const EMAIL = process.env.E2E_USER_EMAIL;
const PASSWORD = process.env.E2E_USER_PASSWORD;

// Skip entire file when credentials are absent.
test.beforeAll(async () => {
  if (!EMAIL || !PASSWORD) {
    console.warn(
      "[children.spec.js] E2E_USER_EMAIL / E2E_USER_PASSWORD not set — all tests will be skipped.",
    );
  }
});

// Authenticate before every test and navigate to the children page.
test.beforeEach(async ({ page }) => {
  if (!EMAIL || !PASSWORD) {
    test.skip();
    return;
  }
  await loginViaAPI(page, EMAIL, PASSWORD);
  await page.goto("/#/children");
  // Wait for the profile card to appear — it is the outermost container of the
  // children page and renders synchronously once Vue mounts.
  await page.waitForSelector('[data-testid="add-child-btn"]', { timeout: 15_000 });
});

// ---------------------------------------------------------------------------
// Page structure
// ---------------------------------------------------------------------------

test.describe("Structure de la page Mes Enfants", () => {
  test("should load the children page without redirecting to login", async ({
    page,
  }) => {
    // If we ended up on the login page the auth helper failed.
    await expect(page).not.toHaveURL(/\/#\/login/);
    await expect(page).toHaveURL(/\/#\/children/);
  });

  test("should display the user profile card", async ({ page }) => {
    const profileCard = page.locator('[data-testid="profile-card"]');
    await expect(profileCard).toBeVisible({ timeout: 8_000 });
  });

  test("should display the child count statistic", async ({ page }) => {
    // The card shows "<number> Enfant(s)" even when count is 0.
    const heading = page.locator(".card-profile-stats .heading");
    await expect(heading).toBeVisible({ timeout: 8_000 });
  });

  test('should show the "Ajouter un enfant" button', async ({ page }) => {
    await expect(
      page.locator('[data-testid="add-child-btn"]'),
    ).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Add child modal
// ---------------------------------------------------------------------------

test.describe("Modal d'ajout d'un enfant", () => {
  test('should open the modal when clicking "Ajouter un enfant"', async ({
    page,
  }) => {
    await page.locator('[data-testid="add-child-btn"]').click();

    // Modal renders as <div class="modal fade show d-block"> when visible.
    const childModal = page.locator('[data-testid="child-modal"]');
    await expect(childModal.locator(".modal.show")).toBeVisible({ timeout: 5_000 });
    // The modal header should say "Ajouter un enfant".
    await expect(childModal.locator(".modal-header")).toContainText(
      "Ajouter un enfant",
    );
  });

  test("should show the Prénom input in the add modal", async ({ page }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    const childModal = page.locator('[data-testid="child-modal"]');
    await expect(childModal.getByPlaceholder("Prénom")).toBeVisible();
  });

  test("should show the Nom input in the add modal", async ({ page }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    const childModal = page.locator('[data-testid="child-modal"]');
    await expect(childModal.getByPlaceholder("Nom", { exact: true })).toBeVisible();
  });

  test("should show the gender select in the add modal", async ({ page }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    // BaseInput with label="Sexe" wraps a <select class="form-control">.
    const childModal = page.locator('[data-testid="child-modal"]');
    const genderSelect = childModal.locator("select.form-control");
    await expect(genderSelect).toBeVisible();
    // Should contain the two gender options.
    await expect(genderSelect.locator("option[value='male']")).toHaveCount(1);
    await expect(genderSelect.locator("option[value='female']")).toHaveCount(1);
  });

  test("should show the birth date picker in the add modal", async ({
    page,
  }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    // flat-picker renders as an <input class="form-control datepicker">.
    const childModal = page.locator('[data-testid="child-modal"]');
    await expect(
      childModal.locator("input.form-control.datepicker"),
    ).toBeVisible();
  });

  test("should close the modal when clicking Annuler", async ({ page }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    await page.getByRole("button", { name: "Annuler" }).click();

    // The modal should disappear — it uses v-show so the element remains in the
    // DOM but gets the class "d-none".
    const childModal = page.locator('[data-testid="child-modal"]');
    await expect(childModal.locator(".modal.show")).not.toBeVisible({ timeout: 5_000 });
  });

  test("should not close the modal when submitting empty", async ({
    page,
  }) => {
    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    // Submit without filling any field.
    const childModal = page.locator('[data-testid="child-modal"]');
    await childModal.locator(".modal-footer").getByText("Ajouter").click();

    // The modal should remain open because validation prevents submission.
    await expect(childModal.locator(".modal.show")).toBeVisible({ timeout: 3_000 });
  });
});

// ---------------------------------------------------------------------------
// Children list — edit and delete (data-dependent)
// ---------------------------------------------------------------------------

test.describe("Gestion des enfants existants (données requises)", () => {
  /**
   * Helper: check if the children table / list has any rows.
   * The table (desktop) is shown via d-none d-md-block; the list (mobile) via
   * d-block d-md-none.  We check the table rows in the tbody.
   */
  async function hasChildren(page) {
    const tableRows = await page.locator("table tbody tr").count();
    const listItems = await page
      .locator(".d-block.d-md-none .list-group-item")
      .count();
    return tableRows > 0 || listItems > 0;
  }

  test("should open the edit modal with pre-filled data when clicking the edit button", async ({
    page,
  }) => {
    if (!(await hasChildren(page))) {
      test.skip(true, "No children in DB — skipping edit test");
    }

    // The edit button is a BaseButton with icon="fa fa-pencil".  On desktop it
    // renders as a <button> inside a table <td>.
    const editButton = page
      .locator("table tbody tr")
      .first()
      .locator("button")
      .first();
    await editButton.click();

    const childModal = page.locator('[data-testid="child-modal"]');
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');
    await expect(childModal.locator(".modal-header")).toContainText(
      "Modifier un enfant",
    );

    // The Prénom field should be pre-filled (not empty).
    const prenom = childModal.getByPlaceholder("Prénom");
    await expect(prenom).not.toHaveValue("");
  });

  test("should open the delete confirmation modal when clicking the delete button", async ({
    page,
  }) => {
    if (!(await hasChildren(page))) {
      test.skip(true, "No children in DB — skipping delete test");
    }

    // The delete button is the second button in the last column of the first row.
    const deleteButton = page
      .locator("table tbody tr")
      .first()
      .locator("button")
      .last();
    await deleteButton.click();

    const childModal = page.locator('[data-testid="child-modal"]');
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');
    await expect(childModal.locator(".modal-header")).toContainText(
      "Retirer un enfant",
    );
    await expect(childModal.locator(".modal-body")).toContainText(
      "Êtes-vous sûr de vouloir retirer",
    );
  });

  test("should add a child and show it in the list", async ({ page }) => {
    // Wait for children to load from API before counting.
    await page.waitForSelector('[data-testid="children-table"]', { timeout: 8_000 }).catch(() => {});
    const beforeCount = await page.locator('[data-testid="children-table"] tbody tr').count();

    await page.locator('[data-testid="add-child-btn"]').click();
    await page.waitForSelector('[data-testid="child-modal"] .modal.show');

    const childModal = page.locator('[data-testid="child-modal"]');

    // Fill in valid child data.
    await childModal.getByPlaceholder("Prénom").fill("Testine");
    await childModal.getByPlaceholder("Nom", { exact: true }).fill("Dupont");
    await childModal.locator("select.form-control").selectOption("female");

    // Type a date directly into the flat-picker input (allowInput: true).
    const dateInput = childModal.locator("input.form-control.datepicker");
    await dateInput.fill("2018-06-15");
    await dateInput.press("Escape");

    await childModal.locator(".modal-footer").getByText("Ajouter").click();

    // The modal should close after a successful API response.
    await expect(childModal.locator(".modal.show")).not.toBeVisible({ timeout: 8_000 });

    // The new child should appear in the table (API POST + store commit).
    await expect(page.locator('[data-testid="children-table"] tbody tr')).toHaveCount(
      beforeCount + 1,
      { timeout: 8_000 },
    );
    await expect(page.locator('[data-testid="children-table"] tbody')).toContainText("Testine");
  });
});
