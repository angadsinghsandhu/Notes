import { readFile } from 'node:fs/promises';
import { posix } from 'node:path';
import { parseDocument } from 'yaml';
import { z } from 'zod';
import type { Metadata, PublicationPolicy, SourceEntry } from './types.js';

export const CONTENT_ROOTS = [
  'Books',
  'Classes',
  'Courses',
  'Interview',
  'Languages',
  'Tutorials',
] as const;

const nonempty = z.string().trim().min(1);
const slug = z
  .string()
  .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*(?:\/[a-z0-9]+(?:-[a-z0-9]+)*)*$/);
const alias = z
  .string()
  .regex(/^\/(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_.-]*\/?$/)
  .refine(
    (value) =>
      !value.split('/').some((segment) => segment === '.' || segment === '..'),
    'Aliases cannot traverse directories',
  );
const uniqueStrings = z
  .array(nonempty)
  .refine(
    (values) => new Set(values).size === values.length,
    'Values must be unique',
  );
const httpsUrl = z.url().refine((value) => {
  const url = new URL(value);
  return url.protocol === 'https:' && !url.username && !url.password;
}, 'Expected a public HTTPS URL without credentials');
const updated = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/)
  .refine((value) => {
    const date = new Date(`${value}T00:00:00Z`);
    return (
      Number.isFinite(date.getTime()) &&
      date.toISOString().slice(0, 10) === value
    );
  }, 'Expected a valid ISO calendar date');
const metadataFields = z
  .object({
    title: nonempty,
    role: z.literal('supplemental').optional(),
    description: z.string().optional(),
    tags: uniqueStrings.optional(),
    draft: z.boolean().optional(),
    slug: slug.optional(),
    order: z.number().optional(),
    updated: updated.optional(),
    aliases: z
      .array(alias)
      .refine(
        (values) =>
          new Set(values.map((value) => value.toLowerCase())).size ===
          values.length,
        'Aliases must be unique',
      )
      .optional(),
  })
  .strict();
const overrideSchema = metadataFields
  .partial()
  .extend({ resourceUrl: httpsUrl.optional() });
const sourcePathSchema = z.string().refine((value) => {
  const segments = value.split('/');
  return (
    segments.length > 1 &&
    CONTENT_ROOTS.some((root) => root === segments[0]) &&
    segments.every(
      (segment) => segment !== '' && segment !== '.' && segment !== '..',
    ) &&
    !value.includes('\\') &&
    Array.from(value).every((character) => character.charCodeAt(0) >= 32)
  );
}, 'Expected a repository-relative path under a content root');
const policySchema = z
  .object({
    roots: z
      .array(z.enum(CONTENT_ROOTS))
      .length(CONTENT_ROOTS.length)
      .refine(
        (values) => new Set(values).size === CONTENT_ROOTS.length,
        'Each of the six roots must appear exactly once',
      ),
    exclude: z.array(z.string()).default([]),
    overrides: z.record(sourcePathSchema, overrideSchema).default({}),
    repositoryPublic: z.boolean().default(false),
    repositoryUrl: httpsUrl.optional(),
    revision: nonempty.optional(),
    siteUrl: httpsUrl.optional(),
  })
  .strict();

function omitUndefined<T extends object>(
  value: T,
): { [K in keyof T]: Exclude<T[K], undefined> } {
  return Object.fromEntries(
    Object.entries(value).filter(([, field]) => field !== undefined),
  ) as { [K in keyof T]: Exclude<T[K], undefined> };
}

export async function readPolicy(
  policyPath: string,
): Promise<PublicationPolicy> {
  try {
    const parsed = policySchema.parse(
      JSON.parse(await readFile(policyPath, 'utf8')),
    );
    return {
      ...omitUndefined(parsed),
      overrides: Object.fromEntries(
        Object.entries(parsed.overrides).map(([path, override]) => [
          path,
          omitUndefined(override),
        ]),
      ),
    };
  } catch (error) {
    throw new Error(
      `${policyPath}: invalid publication policy: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}

function legacyTitle(source: SourceEntry, body: string): string {
  // Fenced examples are not authored headings.
  let fence: { marker: string; length: number } | undefined;
  let previousLine = '';
  for (const line of body.split(/\r?\n/)) {
    const delimiter = /^ {0,3}(`{3,}|~{3,})/.exec(line)?.[1];
    if (delimiter) {
      previousLine = '';
      if (!fence)
        fence = { marker: delimiter[0] ?? '', length: delimiter.length };
      else if (
        delimiter[0] === fence.marker &&
        delimiter.length >= fence.length
      )
        fence = undefined;
      continue;
    }
    if (!fence) {
      if (/^ {0,3}=+[ \t]*$/.test(line) && previousLine.trim())
        return previousLine.trim();
      const heading = /^ {0,3}#[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$/
        .exec(line)?.[1]
        ?.trim();
      if (heading) return heading;
      previousLine = /^ {0,3}\S/.test(line) ? line : '';
    }
  }
  const filename = posix.basename(source.sourcePath);
  return /^readme\.md$/i.test(filename)
    ? posix.basename(posix.dirname(source.sourcePath))
    : filename.slice(0, filename.length - posix.extname(filename).length);
}

export async function readMetadata(
  source: SourceEntry,
  policy: PublicationPolicy,
): Promise<Metadata> {
  try {
    const override = overrideSchema.parse(
      policy.overrides[source.sourcePath] ?? {},
    );
    let frontmatter: Partial<Metadata> = {};
    let body = '';
    if (source.kind === 'markdown') {
      body = (await readFile(source.absolutePath, 'utf8')).replace(
        /^\uFEFF/,
        '',
      );
      if (/^---[ \t]*(?:\r?\n|$)/.test(body)) {
        const match =
          /^---[ \t]*\r?\n([\s\S]*?)\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/.exec(
            body,
          );
        if (!match) throw new Error('Unclosed YAML frontmatter');
        const document = parseDocument(match[1] ?? '', { uniqueKeys: true });
        if (document.errors.length) throw document.errors[0];
        frontmatter = omitUndefined(
          metadataFields.parse(document.toJS({ maxAliasCount: 0 })),
        );
        body = body.slice(match[0].length);
      }
    }
    const descriptiveOverride = metadataFields
      .partial()
      .parse(
        Object.fromEntries(
          Object.entries(override).filter(([key]) => key !== 'resourceUrl'),
        ),
      );
    const merged = metadataFields.parse({
      title: legacyTitle(source, body),
      ...descriptiveOverride,
      ...frontmatter,
    });
    return {
      ...omitUndefined(merged),
      description: merged.description ?? '',
      tags: merged.tags ?? [],
      draft: frontmatter.draft === true || override.draft === true,
      aliases: merged.aliases ?? [],
    };
  } catch (error) {
    throw new Error(
      `${source.sourcePath}: invalid metadata: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}
