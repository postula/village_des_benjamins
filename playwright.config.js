// @ts-check
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./e2e",
  // Each test has up to 30 seconds. Async API calls and Vue rendering need time.
  timeout: 30_000,
  expect: {
    // Generous assertion timeout for content that loads from the API.
    timeout: 8_000,
  },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 1,
  // Serial workers: auth state in localStorage must not bleed between tests
  // in different spec files when running in the same browser context.
  workers: 1,
  reporter: [["html", { open: "never" }], ["list"]],
  use: {
    baseURL: "http://localhost:8000",
    // Vue 2 data binding takes a moment after actions.
    actionTimeout: 10_000,
    screenshot: "only-on-failure",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  // Uncomment to auto-start the Django dev server in CI:
  // webServer: {
  //   command: "python manage.py runserver",
  //   url: "http://localhost:8000",
  //   reuseExistingServer: !process.env.CI,
  // },
});
