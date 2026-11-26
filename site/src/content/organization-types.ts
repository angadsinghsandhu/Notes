export type Purpose = 'note' | 'exercise' | 'reference' | 'project-file';
export type EditorialStatus = 'unreviewed' | 'outline' | 'draft' | 'reviewed';
export type Topic = {
  id: string;
  title: string;
  summary: string;
  parentId?: string | undefined;
  order?: number | undefined;
};
export type Collection = {
  id: string;
  title: string;
  summary: string;
  type: 'book' | 'university-course' | 'online-course' | 'workshop';
  provider?: string | undefined;
  courseCode?: string | undefined;
  edition?: string | undefined;
  year?: number | undefined;
  semester?: string | undefined;
};
export type Group = {
  id: string;
  collectionId: string;
  parentId?: string | undefined;
  title: string;
  summary: string;
  type: 'chapter' | 'module' | 'project' | 'assessment' | 'reference';
  order?: number | undefined;
};
export type OrganizationRecord = {
  uid: string;
  sourcePath: string;
  topics: string[];
  collectionId?: string | undefined;
  groupId?: string | undefined;
  purpose: Purpose;
  status: EditorialStatus;
  summary?: string | undefined;
  relatedUids?: string[] | undefined;
};
export type PathStep = {
  id: string;
  title: string;
  summary: string;
  entryUids: string[];
  topicIds: string[];
};
export type LearningPath = {
  id: string;
  title: string;
  summary: string;
  steps: PathStep[];
};
export type OrganizationDefinition = {
  taxonomy: { version: 1; topics: Topic[] };
  collections: { version: 1; collections: Collection[]; groups: Group[] };
  entries: { version: 1; entries: OrganizationRecord[] };
  paths: { version: 1; paths: LearningPath[] };
};
export type Membership = {
  entryId: string;
  uid?: string;
  topics: string[];
  collectionId?: string | undefined;
  groupId?: string | undefined;
  purpose: Purpose;
  status: EditorialStatus;
  summary: string;
  relatedUids: string[];
};
export type OrganizationSnapshot = {
  topics: Topic[];
  collections: Collection[];
  groups: Group[];
  paths: LearningPath[];
  memberships: Membership[];
};
