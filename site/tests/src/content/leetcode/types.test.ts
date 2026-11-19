import { expectTypeOf, test } from 'vitest';
import type {
  CurriculumDefinition,
  LearningPathDefinition,
  LessonRecord,
  LessonStatus,
  ProblemId,
  ProblemRecord,
} from '../../../../src/content/leetcode/types.js';

test('carries canonical identities, records and statuses through the definition', () => {
  expectTypeOf<ProblemId>().toEqualTypeOf<`leetcode:${number}`>();
  expectTypeOf<LessonStatus>().toEqualTypeOf<
    'planned' | 'draft' | 'verified'
  >();
  expectTypeOf<ProblemRecord['id']>().toEqualTypeOf<ProblemId>();
  expectTypeOf<ProblemRecord['status']>().toEqualTypeOf<LessonStatus>();
  expectTypeOf<LessonRecord['problemId']>().toEqualTypeOf<ProblemId>();
  expectTypeOf<CurriculumDefinition['version']>().toEqualTypeOf<1>();
  expectTypeOf<CurriculumDefinition['problems']>().toEqualTypeOf<
    ProblemRecord[]
  >();
  expectTypeOf<CurriculumDefinition['lessons']>().toEqualTypeOf<
    LessonRecord[]
  >();
  expectTypeOf<CurriculumDefinition['paths']>().toEqualTypeOf<
    LearningPathDefinition[]
  >();
});
