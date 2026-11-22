import { describe, expect, test } from 'vitest';
import {
  hashLessonForReview,
  validateCurriculum,
} from '../../../../src/content/index.js';
import type { CurriculumDefinition } from '../../../../src/content/index.js';
import {
  curriculum,
  firstProblem,
  implementationSha256,
  lessonChange,
  pathDefinition,
  problemChange,
  signedLesson,
  verifiedContent,
  verifiedLesson,
} from './schema-fixtures.js';

describe('validateCurriculum', () => {
  test('accounts for every frontend number and allows unknown planned metadata', () => {
    const input = curriculum();
    const result: CurriculumDefinition = validateCurriculum(input);
    expect(result).toEqual(input);
    expect(result.problems.map(({ number }) => number)).toEqual(
      Array.from({ length: 2000 }, (_, index) => index + 1),
    );
    expect(
      result.problems.filter(({ officialUrl }) => officialUrl === null),
    ).toHaveLength(1999);
    expect(result.problems[1999]).toMatchObject({
      id: 'leetcode:2000',
      officialUrl: null,
      slug: null,
      title: null,
      status: 'planned',
    });
  });

  test('rejects_missing_or_duplicate_frontend_ids', () => {
    const input = curriculum();
    expect(() =>
      validateCurriculum({ ...input, problems: input.problems.slice(0, -1) }),
    ).toThrow(/missing frontend number 2000/i);
    expect(() =>
      validateCurriculum({
        ...input,
        problems: [...input.problems.slice(0, -1), input.problems[1]],
      }),
    ).toThrow(/duplicate frontend number 2/i);
    expect(() =>
      validateCurriculum(problemChange({ id: 'leetcode:2' })),
    ).toThrow(/must match frontend number/i);
    expect(() =>
      validateCurriculum(problemChange({ id: 'leetcode:2001', number: 2001 })),
    ).toThrow(/2000/);
  });

  test('rejects_url_identity_mismatch', () => {
    const evidence = curriculum().problems[0]!.evidence;
    for (const changes of [
      { officialUrl: 'https://leetcode.com/problems/three-sum/' },
      { officialUrl: 'https://leetcode.com/problems/two-sum/?source=test' },
      { slug: null },
      { title: 'Your Sum' },
      { evidence: { ...evidence, officialQuestion: null } },
      {
        evidence: {
          ...evidence,
          officialQuestion: { ...evidence.officialQuestion, frontendNumber: 2 },
        },
      },
      {
        evidence: {
          ...evidence,
          officialQuestion: {
            ...evidence.officialQuestion,
            sourceUrl: 'https://other.example/problems/two-sum/',
          },
        },
      },
    ]) {
      expect(() => validateCurriculum(problemChange(changes))).toThrow(
        /official|identity/i,
      );
    }
  });

  test('rejects one official question claimed by two frontend numbers', () => {
    const { title, slug, officialUrl, evidence } = firstProblem();
    expect(() =>
      validateCurriculum(
        problemChange(
          {
            title,
            slug,
            officialUrl,
            evidence: {
              ...evidence,
              officialQuestion: {
                ...evidence.officialQuestion,
                frontendNumber: 2,
              },
            },
          },
          2,
        ),
      ),
    ).toThrow(/duplicate official question.*two-sum/i);
  });

  test('rejects a pending title without official identity evidence', () => {
    expect(() =>
      validateCurriculum(problemChange({ title: 'Unsupported title' }, 2)),
    ).toThrow(/leetcode:2.*official question.*evidence/i);
  });

  test('requires_company_source_and_observation_date', () => {
    const evidence = curriculum().problems[0]!.evidence;
    const company = {
      companyId: 'example-company',
      companyName: 'Example Company',
      source: { type: 'public', url: 'https://example.org/report' },
      observedOn: '2026-10-24',
      reportingPeriod: 'October 2026',
    };

    for (const invalid of [
      { ...company, source: undefined },
      { ...company, observedOn: undefined },
      { ...company, observedOn: '2026-02-30' },
      { ...company, source: { type: 'public', url: 'file:///private/report' } },
      { ...company, confidence: 42 },
    ]) {
      expect(() =>
        validateCurriculum(
          problemChange({ evidence: { ...evidence, companies: [invalid] } }),
        ),
      ).toThrow(/companies/);
    }
    const associations = [
      company,
      {
        ...company,
        source: {
          type: 'user-supplied',
          reference: 'Interview notes supplied by owner',
        },
      },
    ];
    expect(
      validateCurriculum(
        problemChange({ evidence: { ...evidence, companies: associations } }),
      ).problems[0]?.evidence.companies,
    ).toEqual(associations);
  });

  test('rejects_escape_paths_and_unknown_keys', () => {
    for (const path of [
      '../lesson.md',
      'dir/../../lesson.md',
      '/private/lesson.md',
      'C:/lesson.md',
      'dir\\lesson.md',
      'dir//lesson.md',
      './lesson.md',
      'dir/%2e%2e/lesson.md',
      'lesson.mdx',
    ]) {
      expect(() =>
        validateCurriculum(
          lessonChange({ prose: { path, sha256: 'b'.repeat(64) } }),
        ),
      ).toThrow(/prose.path/);
    }
    expect(() => validateCurriculum({ ...curriculum(), extra: true })).toThrow(
      /extra/,
    );
    expect(() => validateCurriculum(lessonChange({ extra: true }))).toThrow(
      /extra/,
    );
    expect(() => validateCurriculum(problemChange({ extra: true }))).toThrow(
      /extra/,
    );
  });

  test('rejects_verified_lesson_without_approach_evidence', () => {
    const lesson = verifiedLesson();
    const approach = lesson.approaches[0]!;
    for (const changes of [
      { prose: null },
      { examples: null },
      { review: null },
      { review: { reviewer: 'Editor', reviewedOn: 'yesterday' } },
      { approaches: [] },
      { approaches: [{ ...approach, traces: [] }] },
      {
        approaches: [
          {
            ...approach,
            implementation: { ...approach.implementation, sha256: 'unknown' },
          },
        ],
      },
      {
        approaches: [
          {
            ...approach,
            traces: [
              { ...approach.traces[0], implementationSha256: 'e'.repeat(64) },
            ],
          },
        ],
      },
      { approaches: [{ ...approach, language: 'sql' }] },
    ]) {
      expect(() => validateCurriculum(lessonChange(changes))).toThrow(
        /lesson|approach/i,
      );
    }
    expect(() => validateCurriculum({ ...curriculum(), lessons: [] })).toThrow(
      /requires a lesson record/i,
    );
    expect(() =>
      validateCurriculum(problemChange({ difficulty: null })),
    ).toThrow(/catalog metadata/i);
  });

  test('requires passing tests bound to the implementation, entry point and curated examples', () => {
    const { approaches } = verifiedLesson();
    const approach = approaches[0]!;
    for (const verification of [
      null,
      { ...approach.verification, implementationSha256: 'e'.repeat(64) },
      { ...approach.verification, entryPoint: 'other_function' },
      { ...approach.verification, examplesSha256: 'e'.repeat(64) },
      { ...approach.verification, passedExampleIds: ['another-pair'] },
      { ...approach.verification, passedExampleIds: ['pair', 'pair'] },
    ]) {
      expect(() =>
        validateCurriculum(
          lessonChange({ approaches: [{ ...approach, verification }] }),
        ),
      ).toThrow(/approach|example/i);
    }
  });

  test('binds editorial review to the current lesson and catalog evidence', () => {
    const input = curriculum();
    const lesson = verifiedLesson();
    const { review, ...content } = lesson;
    expect(hashLessonForReview(firstProblem(), content)).toBe(
      'e81260e57768a2456a4aacdfce889f2ec38ddaa335b83e0c8b07721c072404cd',
    );
    const { approaches, prose, ...fields } = content;
    expect(
      hashLessonForReview(firstProblem(), { ...fields, prose, approaches }),
    ).toBe(review.contentSha256);
    expect(() =>
      validateCurriculum(
        lessonChange({ prose: { ...lesson.prose, sha256: 'e'.repeat(64) } }),
      ),
    ).toThrow(/stale.*review/i);
    expect(() =>
      validateCurriculum({
        ...input,
        problems: [
          { ...firstProblem(), topics: ['math'] },
          ...input.problems.slice(1),
        ],
      }),
    ).toThrow(/stale.*review/i);
  });

  function sharedPythonContent(alternativeDigest = implementationSha256) {
    const content = verifiedContent();
    const approach = content.approaches[0]!;
    const entryPoint = 'two_sum_nested_loop';
    const alternative = {
      ...approach,
      id: 'nested-loop',
      implementation: {
        ...approach.implementation,
        entryPoint,
        sha256: alternativeDigest,
      },
      traces: [
        {
          ...approach.traces[0]!,
          path: 'traces/nested-loop/pair.json',
          implementationSha256: alternativeDigest,
        },
      ],
      verification: {
        ...approach.verification!,
        entryPoint,
        implementationSha256: alternativeDigest,
      },
    };
    return { ...content, approaches: [approach, alternative] };
  }

  test('rejects conflicting file digests for distinct callables in one implementation', () => {
    const content = sharedPythonContent('e'.repeat(64));
    const lesson = signedLesson(firstProblem(), content);
    expect(() =>
      validateCurriculum({ ...curriculum(), lessons: [lesson] }),
    ).toThrow(/conflicting.*digest.*solutions\.py/i);
  });

  test('supports distinct approaches in the same Python module by callable name', () => {
    const content = sharedPythonContent();
    const [approach, alternative] = content.approaches;
    const lesson = signedLesson(firstProblem(), content);
    const input = { ...curriculum(), lessons: [lesson] };
    expect(validateCurriculum(input)).toEqual(input);
    expect(() =>
      validateCurriculum(
        lessonChange({
          approaches: [
            approach,
            { ...alternative, implementation: approach!.implementation },
          ],
        }),
      ),
    ).toThrow(/duplicate implementation/i);
    expect(() =>
      validateCurriculum(
        lessonChange({
          approaches: [
            {
              ...approach,
              implementation: { ...approach!.implementation, entryPoint: null },
            },
          ],
        }),
      ),
    ).toThrow(/entry point/i);
  });

  test('keeps draft lesson evidence distinct from verified readiness', () => {
    const input = {
      ...problemChange({ status: 'draft' }),
      lessons: [
        {
          problemId: 'leetcode:1',
          prose: null,
          examples: null,
          approaches: [],
          review: null,
        },
      ],
    };
    expect(validateCurriculum(input)).toEqual(input);
    expect(() =>
      validateCurriculum(problemChange({ status: 'planned' })),
    ).toThrow(/planned problem/i);
  });

  test('rejects duplicate records and duplicate curations within a verified lesson', () => {
    const input = curriculum();
    const lesson = verifiedLesson();
    const approach = lesson.approaches[0]!;
    expect(() =>
      validateCurriculum({ ...input, lessons: [lesson, lesson] }),
    ).toThrow(/duplicate lesson/i);
    expect(() =>
      validateCurriculum({
        ...input,
        paths: [pathDefinition(), pathDefinition()],
      }),
    ).toThrow(/duplicate path/i);
    expect(() =>
      validateCurriculum(lessonChange({ approaches: [approach, approach] })),
    ).toThrow(/duplicate approach/i);
    expect(() =>
      validateCurriculum(
        lessonChange({
          approaches: [
            { ...approach, traces: [...approach.traces, ...approach.traces] },
          ],
        }),
      ),
    ).toThrow(/duplicate example/i);
  });

  test('accepts reviewed SQL and shell implementations for their domains', () => {
    const content = verifiedContent();
    const approach = content.approaches[0]!;
    for (const [domain, extension] of [
      ['sql', 'sql'],
      ['shell', 'sh'],
    ] as const) {
      const input = {
        ...problemChange({ domain }),
        lessons: [
          signedLesson(
            { ...firstProblem(), domain },
            {
              ...content,
              approaches: [
                {
                  ...approach,
                  language: domain,
                  implementation: {
                    ...approach.implementation,
                    path: `solutions.${extension}`,
                    entryPoint: null,
                  },
                  verification: { ...approach.verification!, entryPoint: null },
                },
              ],
            },
          ),
        ],
      };
      expect(validateCurriculum(input)).toEqual(input);
      expect(() => validateCurriculum(problemChange({ domain }))).toThrow(
        /requires .* implementation/i,
      );
    }
  });
});
