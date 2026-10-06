import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: [
    'src/pages/**/*.test.ts',
    'src/layouts/**/*.test.ts',
    'src/components/**/*.test.ts',
    'src/lib/**/*.browser.test.ts',
  ],
  workers: 1,
  forbidOnly: Boolean(process.env['CI']),
  retries: process.env['CI'] ? 2 : 0,
  reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4328', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npm run preview -- --port 4328 --ignore-lock',
    port: 4328,
    reuseExistingServer: false,
    timeout: 30_000,
  },
});
