import type { z } from 'zod';
import type {
  approach,
  companyAssociation,
  curriculum,
  learningPath,
  lesson,
  pathNode,
  problem,
} from './schema.js';

export type ProblemId = `leetcode:${number}`;
export type LessonStatus = 'planned' | 'draft' | 'verified';

export type ProblemRecord = z.infer<typeof problem>;
export type CompanyAssociation = z.infer<typeof companyAssociation>;
export type LessonApproachDefinition = z.infer<typeof approach>;
export type LessonRecord = z.infer<typeof lesson>;
export type LearningPathNode = z.infer<typeof pathNode>;
export type LearningPathDefinition = z.infer<typeof learningPath>;
export type CurriculumDefinition = z.infer<typeof curriculum>;
