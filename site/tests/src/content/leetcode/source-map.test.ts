import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { expect, it } from 'vitest';

interface RecordBase {
  sourcePath: string;
  sha256: string;
  filenameNumber: number | null;
  duplicateFilenameNumber?: number;
  disposition: string;
  reason: string;
  problemId?: string;
  officialSource?: { url: string; checkedAt: string };
}

const archivePrefix = 'Interview/leetcode/Solutions/';
const root = new URL('../../../../../', import.meta.url);

function digest(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex');
}

it('preserves the frozen originals and records the approved archive provenance', async () => {
  const raw = await readFile(
    new URL('site/content/leetcode/source-map.json', root),
    'utf8',
  );
  const map = JSON.parse(raw) as { version: number; records: RecordBase[] };
  expect(Object.keys(map).sort()).toEqual(['records', 'version']);
  expect(map.version).toBe(1);

  const records = map.records;
  const paths = records.map(({ sourcePath }) => sourcePath);
  expect(paths).toHaveLength(366);
  expect(paths).toEqual([...new Set(paths)].sort());
  expect(
    digest(
      records
        .map(({ sourcePath, sha256 }) => `${sourcePath}\0${sha256}\n`)
        .join(''),
    ),
  ).toBe('61e8e9afa3609d34de3004be4014a8e6651b63e3707b732a298303432ffdb3b5');

  // These aggregate hashes pin the frozen path/digest pairs and independent group membership.
  const duplicates = records.filter(
    (record) => record.duplicateFilenameNumber !== undefined,
  );
  expect(duplicates).toHaveLength(164);
  expect(
    new Set(duplicates.map((record) => record.duplicateFilenameNumber)).size,
  ).toBe(77);
  expect(
    digest(
      duplicates
        .map(
          ({ sourcePath, duplicateFilenameNumber }) =>
            `${sourcePath}\0${duplicateFilenameNumber}\n`,
        )
        .join(''),
    ),
  ).toBe('3a06aea4c0a063cf3fbdb31a8b03f7af36e668af5e01ad12e6de26979663685c');

  const approved = [
    [
      '18 Org/meta/LC/1 Two Sum.py',
      1,
      'solver_variant',
      'https://leetcode.com/problems/two-sum/',
    ],
    [
      '1_Two_Sum.py',
      1,
      'solver_variant',
      'https://leetcode.com/problems/two-sum/',
    ],
    [
      '3_Longest_Substring_Without_Repeating_Characters.py',
      3,
      'solver_variant',
      'https://leetcode.com/problems/longest-substring-without-repeating-characters/',
    ],
    [
      '20_Valid_Parentheses.py',
      20,
      'solver_variant',
      'https://leetcode.com/problems/valid-parentheses/',
    ],
    [
      '14 DP/64 Minimum Path Sum.py',
      64,
      'solver_variant',
      'https://leetcode.com/problems/minimum-path-sum/',
    ],
    [
      '18 Org/meta/LC/98 Validate Binary Search Tree.py',
      98,
      'solver_variant',
      'https://leetcode.com/problems/validate-binary-search-tree/',
    ],
    [
      '98_Validate_Binary_Search_Tree.py',
      98,
      'solver_variant',
      'https://leetcode.com/problems/validate-binary-search-tree/',
    ],
    [
      '127_Word_Ladder.py',
      127,
      'solver_variant',
      'https://leetcode.com/problems/word-ladder/',
    ],
    [
      '146_LRU_Cache.py',
      146,
      'solver_variant',
      'https://leetcode.com/problems/lru-cache/',
    ],
    [
      '450_Count_Good_Nodes_in_Binary_Tree.py',
      1448,
      'statement_only',
      'https://leetcode.com/problems/count-good-nodes-in-binary-tree/description/',
    ],
    [
      '11 Graph/Path Sum IV.py',
      666,
      'link_only',
      'https://leetcode.com/articles/?page=62&tag=linked-list',
    ],
    [
      '271_Encode_and_Decode_Strings.py',
      271,
      'statement_only',
      'https://leetcode.com/articles/?page=106',
    ],
    [
      '5 String/271 Encode and Decode Strings.py',
      271,
      'link_only',
      'https://leetcode.com/articles/?page=106',
    ],
  ] as const;
  const allowed = [
    'solver_variant',
    'statement_only',
    'link_only',
    'practice',
    'pending_reconciliation',
    'out_of_range',
    'archive_support',
    'empty',
  ];

  for (const record of records) {
    const {
      sourcePath,
      filenameNumber,
      reason,
      sha256,
      disposition,
      problemId,
      officialSource,
    } = record;
    expect(sourcePath.startsWith(archivePrefix)).toBe(true);
    expect(reason.trim()).not.toBe('');
    expect(allowed).toContain(disposition);
    expect(
      Object.keys(record).every((key) =>
        [
          'sourcePath',
          'sha256',
          'filenameNumber',
          'duplicateFilenameNumber',
          'disposition',
          'reason',
          'problemId',
          'officialSource',
        ].includes(key),
      ),
    ).toBe(true);
    const prefix = /^(\d+)[ _.-]/.exec(basename(sourcePath));
    expect(filenameNumber).toBe(prefix ? Number(prefix[1]) : null);
    expect(
      digest(await readFile(resolve(fileURLToPath(root), sourcePath))),
    ).toBe(sha256);
    if (record.duplicateFilenameNumber !== undefined)
      expect(record.duplicateFilenameNumber).toBe(filenameNumber);
    if (problemId === undefined) {
      expect(officialSource).toBeUndefined();
      expect(disposition).not.toBe('solver_variant');
    } else {
      expect(problemId).toMatch(/^leetcode:[1-9]\d*$/);
      expect(officialSource?.url).toMatch(
        disposition === 'solver_variant'
          ? /^https:\/\/leetcode\.com\/problems\/[a-z0-9-]+\/$/
          : /^https:\/\/leetcode\.com\/(?:problems\/[a-z0-9-]+\/(?:description\/)?|articles\/\?page=\d+(?:&tag=[a-z0-9-]+)?)$/,
      );
      expect(officialSource?.checkedAt).toMatch(
        /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/,
      );
    }
  }

  const mapped = records.filter((record) => record.problemId !== undefined);
  expect(mapped).toHaveLength(approved.length);
  for (const [relativePath, number, disposition, evidenceUrl] of approved) {
    expect(
      mapped.find(
        ({ sourcePath }) => sourcePath === archivePrefix + relativePath,
      ),
    ).toMatchObject({
      problemId: `leetcode:${number}`,
      disposition,
      officialSource: {
        url: evidenceUrl,
      },
    });
  }
  expect(mapped.some(({ problemId }) => problemId === 'leetcode:175')).toBe(
    false,
  );
  expect(raw).not.toMatch(/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/);
});
