import { createHash } from 'node:crypto';
import { constants } from 'node:fs';
import {
  lstat,
  mkdir,
  mkdtemp,
  open,
  realpath,
  rename,
  rm,
  rmdir,
  writeFile,
} from 'node:fs/promises';
import { basename, dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import {
  MAX_LOCAL_ASSET_BYTES,
  prepareContent,
  readPolicy,
  verifyCurriculumArtifacts,
  type ContentEntry,
  type Manifest,
} from '../src/content/index.js';
import {
  isMissing,
  requireDirectory,
  verifyCheckout,
  verifySourceDirectory,
} from './portfolio-export/checkout.js';
import {
  portfolioSnapshotV1,
  type PortfolioSnapshotV1,
} from './portfolio-export/schema.js';

type Options = {
  rootDir: string;
  out: string;
  revision: string;
  mode?: 'production' | 'preview';
};
const sha256 = (bytes: Buffer) =>
  createHash('sha256').update(bytes).digest('hex');
const localPath =
  /^\/content-assets\/([a-f0-9]{64})\.(?:png|jpg|gif|webp|avif|svg|ico|pdf|ppt|pptx)$/;

async function readRegularFile(
  path: string,
  limit = Infinity,
): Promise<Buffer> {
  const handle = await open(
    path,
    constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK,
  );
  try {
    const stat = await handle.stat();
    if (!stat.isFile() || stat.size > limit)
      throw new Error(`Unsafe generated file or file size: ${path}`);
    const bytes = await handle.readFile();
    if (bytes.length !== stat.size)
      throw new Error(`Generated file changed during export: ${path}`);
    return bytes;
  } finally {
    await handle.close();
  }
}

async function materialize(
  source: string,
  stage: string,
  publicPath: string,
  exportPath: string,
  expectedDigest: string,
  expectedBytes?: number,
) {
  const bytes = await readRegularFile(source, MAX_LOCAL_ASSET_BYTES);
  if (
    sha256(bytes) !== expectedDigest ||
    (expectedBytes !== undefined && bytes.length !== expectedBytes)
  )
    throw new Error(
      `Generated asset does not match its registered digest or size: ${publicPath}`,
    );
  await writeFile(join(stage, exportPath), bytes, { flag: 'wx' });
  return {
    publicPath,
    exportPath,
    bytes: bytes.length,
    sha256: expectedDigest,
  };
}

function projectEntry(
  entry: ContentEntry,
  id: string,
  bodies: Record<string, string>,
) {
  const {
    title,
    kind,
    route,
    aliases,
    headings,
    anchors,
    description,
    tags,
    section,
    groupSegments,
    role,
    order,
    updated,
    bodyFile,
    assetUrl,
    sourceUrl,
  } = entry;
  const bodyHtml = bodyFile ? bodies[bodyFile] : undefined;
  if (
    bodyFile &&
    (bodyFile !== `bodies/${entry.id}.html` || typeof bodyHtml !== 'string')
  )
    throw new Error(`Invalid prepared body for ${route}`);
  return {
    id,
    title,
    kind,
    route,
    aliases,
    headings,
    anchors,
    description,
    tags,
    section,
    groupSegments,
    searchIndexed: true,
    role,
    order,
    updated,
    bodyHtml,
    assetUrl,
    sourceUrl,
  };
}

async function curriculumProjection(
  generated: string,
  stage: string,
  generation: string | undefined,
  ids: ReadonlyMap<string, string>,
) {
  const empty = {
    generation: null,
    problems: [],
    lessons: [],
    paths: [],
    pendingPathLabels: [],
    sourceVariants: [],
    traceAssets: [],
  };
  if (!generation) return empty;
  const curriculum = await verifyCurriculumArtifacts(generated, generation);
  const lessons = curriculum.lessons.filter(
    ({ status }) => status === 'verified',
  );
  const problems = curriculum.problems.filter(
    ({ status }) => status === 'verified',
  );
  const verified = new Set(problems.map(({ id }) => id));
  const pendingPathLabels = [];
  const paths = [];
  for (const { nodes, ...path } of curriculum.paths) {
    const publicNodes = [];
    for (const node of nodes) {
      if (node.kind === 'problem' && !verified.has(node.problemId)) {
        const { title, ...pending } = node;
        publicNodes.push(pending);
        pendingPathLabels.push({
          pathId: path.id,
          nodeId: node.id,
          problemId: node.problemId,
          title,
        });
      } else publicNodes.push(node);
    }
    paths.push({ ...path, nodes: publicNodes });
  }
  const sourceVariants = curriculum.sourceVariants
    .filter(({ problemId }) => verified.has(problemId))
    .map((item) => ({ ...item, sourceId: ids.get(item.sourceId) }));
  const traceRoot = join(
    generated,
    `curriculum-${generation}`,
    'worker-assets/practice-traces',
  );
  await requireDirectory(traceRoot);
  const traceAssets = [];
  for (const { approaches } of lessons) {
    for (const { trace } of approaches) {
      if (!trace) continue;
      const filename = `${trace.sha256}.json`;
      traceAssets.push(
        await materialize(
          join(traceRoot, filename),
          stage,
          trace.url,
          `worker-assets/practice-traces/${filename}`,
          trace.sha256,
          trace.bytes,
        ),
      );
    }
  }
  return {
    generation,
    problems,
    lessons,
    paths,
    pendingPathLabels,
    sourceVariants,
    traceAssets,
  };
}

async function preparationOptions(root: string, revision: string) {
  const site = join(root, 'site');
  const content = join(site, 'content');
  const policyPath = join(content, 'publication.json');
  const organizationDir = join(content, 'organization');
  const curriculumDir = join(content, 'leetcode');
  await requireDirectory(content);
  if (!(await lstat(policyPath)).isFile())
    throw new Error('Unsafe publication policy file');
  await verifySourceDirectory(organizationDir);
  await verifySourceDirectory(curriculumDir);
  const policy = await readPolicy(policyPath);
  if (
    (process.env.SOURCE_REVISION && process.env.SOURCE_REVISION !== revision) ||
    (process.env.REPOSITORY_URL &&
      process.env.REPOSITORY_URL !== policy.repositoryUrl) ||
    (process.env.SITE_URL && process.env.SITE_URL !== policy.siteUrl)
  )
    throw new Error(
      'Publication environment overrides the selected Notes inputs',
    );
  const outputDir = join(site, '.generated');
  const base = {
    rootDir: root,
    outputDir,
    policyPath,
    organizationDir,
    curriculumDir,
    hosted: false,
    revision,
  };
  return { base, policy, site };
}

async function project(
  site: string,
  generated: string,
  stage: string,
  snapshot: Manifest,
) {
  const current = join(generated, 'current');
  await requireDirectory(current);
  const { preparedBodies, ...manifest } = JSON.parse(
    (await readRegularFile(join(current, 'manifest.json'))).toString('utf8'),
  ) as Manifest & { preparedBodies: Record<string, string> };
  if (JSON.stringify(manifest) !== JSON.stringify(snapshot) || !preparedBodies)
    throw new Error(
      'Prepared archive no longer matches the selected publication',
    );
  const currentOrganization = manifest.organization!;
  const uids = new Map(
    currentOrganization.memberships.map(({ entryId, uid }) => [entryId, uid]),
  );
  const publicEntries = manifest.entries.filter(({ draft }) => !draft);
  const ids = new Map(publicEntries.map(({ id }) => [id, uids.get(id) ?? id]));
  const entries = publicEntries.map((entry) =>
    projectEntry(entry, ids.get(entry.id)!, preparedBodies),
  );
  const organization = {
    ...currentOrganization,
    memberships: currentOrganization.memberships.map((item) => ({
      ...item,
      entryId: ids.get(item.entryId),
    })),
  };
  const assetsSource = join(site, 'public/content-assets');
  await requireDirectory(assetsSource);
  const assets = [];
  const paths = new Set<string>();
  for (const asset of manifest.assets) {
    if (asset.mode !== 'local' || paths.has(asset.url)) continue;
    const hash = localPath.exec(asset.url)?.[1];
    if (!hash) throw new Error(`Invalid prepared archive asset: ${asset.url}`);
    const filename = basename(asset.url);
    assets.push(
      await materialize(
        join(assetsSource, filename),
        stage,
        asset.url,
        `assets/${filename}`,
        hash,
      ),
    );
    paths.add(asset.url);
  }
  const curriculum = await curriculumProjection(
    generated,
    stage,
    manifest.curriculumGeneration,
    ids,
  );
  return {
    entries,
    organization,
    assets,
    curriculum,
    verifiedCurriculumIds: curriculum.problems.map(({ number }) => number),
  };
}

async function requireFreshOutput(path: string): Promise<void> {
  if (
    await lstat(path).catch((error: unknown) => {
      if (!isMissing(error)) throw error;
    })
  )
    throw new Error(`Export destination already exists: ${path}`);
}

const manifestBytes = (manifest: PortfolioSnapshotV1) =>
  Buffer.from(`${JSON.stringify(manifest)}\n`);

export async function exportPortfolio(
  options: Options,
): Promise<PortfolioSnapshotV1> {
  const { revision, mode = 'production' } = options;
  if (!/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(revision))
    throw new Error('An exact lowercase checkout SHA is required');
  const root = await realpath(options.rootDir);
  if (mode === 'production') await verifyCheckout(root, revision);

  const destination = resolve(options.out);
  const parent = dirname(destination);
  await requireDirectory(parent);
  const location = relative(root, destination);
  if (
    location.split(sep)[0] !== '..' &&
    !location.startsWith(`.superpowers${sep}`)
  )
    throw new Error(
      'Export destination must be outside the checkout or inside .superpowers',
    );
  await requireFreshOutput(destination);
  const lock = join(parent, `.${basename(destination)}.export-lock`);
  await mkdir(lock);
  let stage: string | undefined;
  try {
    await requireFreshOutput(destination);
    stage = await mkdtemp(join(parent, `.${basename(destination)}.export-`));
    await mkdir(join(stage, 'assets'));
    await mkdir(join(stage, 'worker-assets/practice-traces'), {
      recursive: true,
    });
    const { base, policy, site } = await preparationOptions(root, revision);
    if (mode === 'production') await verifyCheckout(root, revision, policy);
    const { manifest: prepared, diagnostics } = await prepareContent(base);
    if (diagnostics.length)
      throw new Error(
        diagnostics
          .map(({ sourcePath, message }) => `${sourcePath}: ${message}`)
          .join('\n'),
      );
    const manifest = portfolioSnapshotV1.parse({
      schemaVersion: 1,
      mode,
      sourceSha: revision,
      ...(await project(site, base.outputDir, stage, prepared)),
    });
    await writeFile(join(stage, 'manifest.json'), manifestBytes(manifest), {
      flag: 'wx',
    });
    if (mode === 'production') await verifyCheckout(root, revision, policy);
    await requireFreshOutput(destination);
    await rename(stage, destination);
    stage = undefined;
    return manifest;
  } finally {
    try {
      if (stage !== undefined)
        await rm(stage, { recursive: true, force: true });
    } finally {
      await rmdir(lock);
    }
  }
}

export async function runExport(
  args: string[],
  site = process.cwd(),
): Promise<number> {
  try {
    const { values } = parseArgs({
      args,
      options: {
        out: { type: 'string' },
        revision: { type: 'string' },
        preview: { type: 'boolean' },
      },
    });
    if (!values.out || !values.revision)
      throw new Error(
        'Usage: export:portfolio -- --out <staging-dir> --revision <sha> [--preview]',
      );
    const snapshot = await exportPortfolio({
      rootDir: resolve(site, '..'),
      out: resolve(site, values.out),
      revision: values.revision,
      mode: values.preview ? 'preview' : 'production',
    });
    console.log(
      JSON.stringify({
        mode: snapshot.mode,
        sourceSha: snapshot.sourceSha,
        manifestSha256: sha256(manifestBytes(snapshot)),
      }),
    );
    return 0;
  } catch (error) {
    console.error(String(error));
    return 1;
  }
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
)
  process.exitCode = await runExport(process.argv.slice(2));
