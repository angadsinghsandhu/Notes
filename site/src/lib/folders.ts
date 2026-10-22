import type { ContentEntry, Section } from '../content/index.js';
import {
  assertUniqueRoutes,
  compareSourcePaths,
  sourceFolderRoute as folderRoute,
} from '../content/index.js';
import { isLearningNote, sectionLabels } from './catalog.js';

export type Folder = {
  label: string;
  section: Section;
  segments: string[];
  route: string;
  children: Folder[];
  entries: ContentEntry[];
  noteCount: number;
  resourceCount: number;
};

export { sourceFolderRoute as folderRoute } from '../content/index.js';

export function buildFolders(entries: ContentEntry[]): Folder[] {
  const folders = new Map<string, Folder>();
  const make = (
    section: Section,
    segments: string[],
    label: string,
  ): Folder => {
    const folder: Folder = {
      label,
      section,
      segments,
      route: folderRoute(section, segments),
      children: [],
      entries: [],
      noteCount: 0,
      resourceCount: 0,
    };
    folders.set(folder.route, folder);
    return folder;
  };
  const roots = (Object.keys(sectionLabels) as Section[]).map((section) =>
    make(section, [], sectionLabels[section]),
  );
  const published = entries.filter((entry) => !entry.draft);
  for (const entry of published) {
    let parent = folders.get(folderRoute(entry.section, []))!;
    const count = isLearningNote(entry) ? 'noteCount' : 'resourceCount';
    parent[count]++;
    entry.groupSegments.forEach((label, index) => {
      const segments = entry.groupSegments.slice(0, index + 1);
      const route = folderRoute(entry.section, segments);
      let folder = folders.get(route);
      if (!folder) {
        folder = make(entry.section, segments, label);
        parent.children.push(folder);
      }
      folder[count]++;
      parent = folder;
    });
    parent.entries.push(entry);
  }
  for (const folder of folders.values())
    folder.children.sort((a, b) => compareSourcePaths(a.label, b.label));
  assertUniqueRoutes(
    published,
    flattenFolders(roots)
      .filter((folder) => folder.segments.length > 0)
      .map((folder) => ({
        route: folder.route,
        owner: `folder ${sectionLabels[folder.section]}/${folder.segments.join('/')}`,
      })),
  );
  return roots;
}

export function flattenFolders(roots: Folder[]): Folder[] {
  return roots.flatMap((folder) => [
    folder,
    ...flattenFolders(folder.children),
  ]);
}
