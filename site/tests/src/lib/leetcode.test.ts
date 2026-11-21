import { expect, it } from 'vitest';
import { createCurriculumCatalog } from '../../../src/lib/leetcode.js';

it('answers all catalog queries for an archive-only publication', () => {
  const catalog = createCurriculumCatalog();
  expect(catalog.listProblems({ status: 'planned' })).toEqual([]);
  expect(catalog.getLesson('leetcode:1')).toBeUndefined();
  expect(catalog.listPaths()).toEqual([]);
  expect(catalog.getPath('unknown')).toBeUndefined();
});

it('elects canonical prepared routes in snapshot order and returns a fresh list', () => {
  const catalog = createCurriculumCatalog({
    version: 1,
    generation: '',
    problems: [],
    lessons: [],
    paths: [],
    sourceVariants: [],
    routes: [
      { route: '/practice/leetcode/', owner: 'index' },
      { route: '/practice/leetcode/1/', owner: 'lesson' },
      { route: '/practice/paths/cafe&/', owner: 'path' },
    ],
  });
  expect(catalog.publishedRoutes()).toEqual([]);
  const elected = ['/practice/paths/cafe&/', '/practice/leetcode/'];
  expect(catalog.publishedRoutes(elected)).toEqual([
    '/practice/leetcode/',
    '/practice/paths/cafe&/',
  ]);
  expect(() => catalog.publishedRoutes(['/practice/missing/'])).toThrow(
    /unclaimed/i,
  );
  expect(() => catalog.publishedRoutes([elected[0]!, elected[0]!])).toThrow(
    /duplicate/i,
  );
});
