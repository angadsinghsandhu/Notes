import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts', 'scripts/**/*.ts'],
      reporter: ['text', 'json', 'json-summary'],
    },
    exclude: ['**/*.browser.test.ts', '**/node_modules/**'],
    include: [
      'tests/astro.config.test.ts',
      'tests/src/content/**/*.test.ts',
      'tests/src/lib/**/*.test.ts',
      'tests/scripts/**/*.test.ts',
      'tests/src/client/**/*.test.ts',
      'tests/src/pages/**/*.unit.test.ts',
    ],
  },
});
