import { describe, expect, it } from 'vitest';
import {
  pathProgress,
  validateLearningPaths,
  type LearningPathDefinition,
  type LearningPathNode,
  type ProblemId,
  type ProblemRecord,
} from '../../../../src/content/index.js';

const problem = (
  number: number,
  status: ProblemRecord['status'] = 'verified',
): ProblemRecord => ({
  number,
  id: `leetcode:${number}`,
  status,
  title: null,
  slug: null,
  officialUrl: null,
  domain: null,
  difficulty: null,
  topics: [],
  evidence: { officialQuestion: null, companies: [] },
});

const stage = (
  id: string,
  childIds: string[],
  prerequisiteIds: string[] = [],
): LearningPathNode => ({
  id,
  title: id,
  kind: 'stage',
  childIds,
  prerequisiteIds,
});

const target = (
  id: string,
  number: number,
  prerequisiteIds: string[] = [],
): LearningPathNode => ({
  id,
  title: id,
  kind: 'problem',
  problemId: `leetcode:${number}`,
  childIds: [],
  prerequisiteIds,
});

const route = (
  rootIds: string[],
  ...nodes: LearningPathNode[]
): LearningPathDefinition => ({
  id: 'curriculum',
  title: 'Curriculum',
  description: 'Editorial sequence',
  rootIds,
  nodes,
});

const catalog = (...problems: ProblemRecord[]) =>
  new Map(problems.map((record) => [record.id, record]));

describe('validateLearningPaths', () => {
  it.each([
    ['hierarchy', route(['a'], stage('a', ['b']), stage('b', ['a']))],
    [
      'prerequisite',
      route(['a', 'b'], stage('a', [], ['b']), stage('b', [], ['a'])),
    ],
    ['mixed', route(['a'], stage('a', ['b'], ['b']), stage('b', []))],
  ])('rejects a %s cycle', (_kind, path) => {
    expect(() => validateLearningPaths([path], [])).toThrow(/cycle/i);
  });

  it.each([
    ['root', route(['missing'])],
    ['child', route(['a'], stage('a', ['missing']))],
    ['prerequisite', route(['a'], stage('a', [], ['missing']))],
  ])('rejects dangling %s references', (_kind, path) => {
    expect(() => validateLearningPaths([path], [])).toThrow(/missing/i);
  });

  it.each([
    ['root', route(['a', 'a'], stage('a', []))],
    ['child', route(['a'], stage('a', ['b', 'b']), stage('b', []))],
    [
      'prerequisite',
      route(['a', 'b'], stage('a', [], ['b', 'b']), stage('b', [])),
    ],
    ['node', route(['a'], stage('a', []), stage('a', []))],
  ])('rejects a duplicate %s reference or identity', (_kind, path) => {
    expect(() => validateLearningPaths([path], [])).toThrow(/duplicate/i);
  });

  it('rejects duplicate path IDs', () => {
    const path = route(['a'], stage('a', []));
    expect(() => validateLearningPaths([path, path], [])).toThrow(/duplicate/i);
  });

  it('rejects nodes unreachable through the hierarchy', () => {
    const path = route(['a'], stage('a', [], ['b']), stage('b', []));
    expect(() => validateLearningPaths([path], [])).toThrow(/unreachable/i);
  });

  it.each([0, 2001, 1.5])('rejects invalid canonical problem %s', (number) => {
    const path = route(['a'], target('a', number));
    expect(() => validateLearningPaths([path], [problem(number)])).toThrow(
      /problem/i,
    );
  });

  it('rejects valid canonical problem IDs missing from the catalog', () => {
    const path = route(['a'], target('a', 1));
    expect(() => validateLearningPaths([path], [])).toThrow(/leetcode:1/);
  });

  it('preserves editorial order and accepts a child requiring its parent', () => {
    const path = route(
      ['b', 'a'],
      target('first', 1),
      target('last', 2000, ['b']),
      stage('a', []),
      stage('b', ['last', 'first']),
    );
    expect(
      validateLearningPaths([path], [problem(1), problem(2000)]).get(path.id),
    ).toEqual(path);
    expect(
      pathProgress(path, new Set(), catalog(problem(1), problem(2000)))
        .nextReady,
    ).toBe('leetcode:2000');
  });
});

describe('pathProgress', () => {
  it('counts a shared problem once across appearances', () => {
    const path = route(
      ['arrays', 'hashing'],
      stage('arrays', ['pairs']),
      stage('hashing', ['pairs', 'second-pairs']),
      target('pairs', 1),
      target('second-pairs', 1),
    );
    const records = [problem(1)];
    validateLearningPaths([path], records);
    expect(
      pathProgress(
        path,
        new Set(['leetcode:1', 'leetcode:99']),
        catalog(...records),
      ),
    ).toEqual({
      required: 1,
      available: 1,
      verified: 1,
      studied: 1,
      complete: true,
      nextReady: null,
    });
  });

  it('keeps draft and planned targets in the completion denominator', () => {
    const path = route(
      ['a', 'b', 'c'],
      target('a', 1),
      target('b', 2),
      target('c', 3),
    );
    const studied = new Set<ProblemId>([
      'leetcode:1',
      'leetcode:2',
      'leetcode:3',
    ]);
    expect(
      pathProgress(
        path,
        studied,
        catalog(problem(1), problem(2, 'draft'), problem(3, 'planned')),
      ),
    ).toEqual({
      required: 3,
      available: 1,
      verified: 1,
      studied: 1,
      complete: false,
      nextReady: null,
    });
  });

  it('skips pending targets and follows explicit stage and transitive prerequisites', () => {
    const path = route(
      ['curriculum-stage', 'later', 'pending', 'early', 'middle', 'final'],
      stage('curriculum-stage', ['advanced'], ['later']),
      target('advanced', 1, ['curriculum-stage']),
      target('later', 2, ['middle']),
      target('pending', 3),
      target('early', 4),
      target('middle', 5, ['early']),
      target('final', 6, ['pending']),
    );
    const records = [
      problem(1),
      problem(2),
      problem(3, 'planned'),
      problem(4),
      problem(5),
      problem(6),
    ];
    const studied = new Set<ProblemId>(['leetcode:5']);
    expect(pathProgress(path, studied, catalog(...records)).nextReady).toBe(
      'leetcode:4',
    );
    studied.add('leetcode:4');
    expect(pathProgress(path, studied, catalog(...records)).nextReady).toBe(
      'leetcode:2',
    );
    studied.add('leetcode:2');
    expect(pathProgress(path, studied, catalog(...records)).nextReady).toBe(
      'leetcode:1',
    );
    studied.add('leetcode:1');
    expect(pathProgress(path, studied, catalog(...records)).nextReady).toBe(
      'leetcode:6',
    );
  });

  it('recommends a stage prerequisite ahead of descendants without their own prerequisites', () => {
    const path = route(
      ['advanced', 'basics'],
      stage('advanced', ['exercise'], ['basics']),
      target('exercise', 1),
      target('basics', 2),
    );
    const records = [problem(1), problem(2)];
    validateLearningPaths([path], records);
    expect(pathProgress(path, new Set(), catalog(...records)).nextReady).toBe(
      'leetcode:2',
    );
    expect(
      pathProgress(path, new Set(['leetcode:2']), catalog(...records))
        .nextReady,
    ).toBe('leetcode:1');
  });

  it('keeps a shared child ready through an eligible parent and preserves eligible appearance order', () => {
    const path = route(
      ['advanced', 'exercise-first', 'practice', 'basics'],
      stage('advanced', ['shared'], ['basics']),
      target('exercise-first', 3),
      stage('practice', ['shared']),
      target('shared', 1),
      target('basics', 2),
    );
    const records = [problem(1), problem(2), problem(3)];
    validateLearningPaths([path], records);
    expect(pathProgress(path, new Set(), catalog(...records)).nextReady).toBe(
      'leetcode:3',
    );
    expect(
      pathProgress(path, new Set(['leetcode:3']), catalog(...records))
        .nextReady,
    ).toBe('leetcode:1');
  });

  it('recommends a shared problem through its first eligible appearance', () => {
    const path = route(
      ['blocked', 'available', 'prerequisite'],
      target('blocked', 1, ['prerequisite']),
      target('available', 1),
      target('prerequisite', 2),
    );
    expect(
      pathProgress(path, new Set(), catalog(problem(1), problem(2))).nextReady,
    ).toBe('leetcode:1');
  });
});
