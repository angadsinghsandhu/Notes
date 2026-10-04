import astro from 'eslint-plugin-astro';
import tseslint from 'typescript-eslint';
import { ignores } from './eslint.config.mjs';

const contentForbidden = {
  regex:
    '(^|/)(pages|layouts|components|client|scripts)(/|$)|(^|/)lib/catalog(?:\\.[jt]s)?$',
  message: 'Content is independent of UI, the catalog facade, and CLI modules.',
};

const dynamicImport = (restriction) => ({
  selector: `ImportExpression[source.value=/${restriction.regex.replaceAll('/', '\\/')}/]`,
  message: restriction.message,
});

const cliForbidden = {
  regex:
    '(^|/)(pages|layouts|components|client)(/|$)|(^|/)lib/catalog(?:\\.[jt]s)?$',
  message: 'CLI modules call content modules and must not import UI.',
};

export default [
  { ignores },
  { files: ['**/*.ts'], languageOptions: { parser: tseslint.parser } },
  ...astro.configs.base,
  {
    files: ['src/content/**/*.ts', 'tests/src/content/**/*.ts'],
    rules: {
      'no-restricted-imports': ['error', { patterns: [contentForbidden] }],
      'no-restricted-syntax': ['error', dynamicImport(contentForbidden)],
    },
  },
  {
    files: [
      'src/{pages,layouts,components,client}/**/*.{ts,astro}',
      'tests/src/{pages,layouts,components,client}/**/*.ts',
    ],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          paths: [
            {
              name: 'fs',
              message: 'UI consumes prepared content through lib/catalog.ts.',
            },
            {
              name: 'node:fs',
              message: 'UI consumes prepared content through lib/catalog.ts.',
            },
            {
              name: 'fs/promises',
              message: 'UI consumes prepared content through lib/catalog.ts.',
            },
            {
              name: 'node:fs/promises',
              message: 'UI consumes prepared content through lib/catalog.ts.',
            },
          ],
          patterns: [
            {
              regex: '(^|/)content(?:/index(?:\\.[jt]s)?)?$',
              allowTypeImports: true,
              message:
                'Only type imports from the content public barrel are allowed in UI.',
            },
            {
              regex:
                '(^|/)(content/(?!index(?:\\.[jt]s)?$)|scripts(?:/|$)|\\.generated(?:/|$))',
              message:
                'UI uses lib/catalog.ts and the content public type barrel only.',
            },
          ],
        },
      ],
      'no-restricted-syntax': [
        'error',
        dynamicImport({
          regex:
            '(^|/)(content(?:/|$)|scripts(?:/|$)|\\.generated(?:/|$))|^(node:)?fs(?:/|$)',
          message:
            'UI uses lib/catalog.ts and must not load content internals or scan files.',
        }),
        {
          selector:
            'CallExpression[callee.object.type="MetaProperty"][callee.property.name="glob"]',
          message: 'UI must not scan the archive; use lib/catalog.ts.',
        },
        {
          selector:
            'CallExpression[callee.object.name="Astro"][callee.property.name="glob"]',
          message: 'UI must not scan the archive; use lib/catalog.ts.',
        },
      ],
    },
  },
  {
    files: ['scripts/**/*.ts', 'tests/scripts/**/*.ts'],
    rules: {
      'no-restricted-imports': ['error', { patterns: [cliForbidden] }],
      'no-restricted-syntax': ['error', dynamicImport(cliForbidden)],
    },
  },
];
