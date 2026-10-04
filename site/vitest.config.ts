import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: [
      'tests/src/content/**/*.test.ts',
      'tests/src/lib/**/*.test.ts',
      'tests/scripts/**/*.test.ts',
    ],
  },
});
