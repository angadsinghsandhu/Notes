import { constants } from 'node:fs';
import { open, realpath } from 'node:fs/promises';
import { join } from 'node:path';
import { z } from 'zod';

export const shardIndex = z.strictObject({
  shards: z.array(z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*\.json$/)).min(1),
});

export async function readShards<Schema extends z.ZodType>(
  root: string,
  catalog: string,
  { shards }: z.infer<typeof shardIndex>,
  record: Schema,
): Promise<z.infer<Schema>[]> {
  if (new Set(shards).size !== shards.length)
    throw new Error(`${catalog}: Duplicate shard reference`);

  const directory = join(
    await realpath(root),
    catalog.slice(0, -'.json'.length),
  );
  if ((await realpath(directory)) !== directory)
    throw new Error(
      `${directory}: Shard directory resolves outside its declared path`,
    );

  const chunk = z.array(record).min(1);
  const records: z.infer<Schema>[] = [];
  for (const shard of shards) {
    const filename = join(directory, shard);
    try {
      const file = await open(
        filename,
        constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK,
      );
      try {
        if (!(await file.stat()).isFile())
          throw new Error('Expected a regular file');
        const value: unknown = JSON.parse(await file.readFile('utf8'));
        for (const record of chunk.parse(value)) records.push(record);
      } finally {
        await file.close();
      }
    } catch (error) {
      throw new Error(
        `${filename}: cannot read curriculum shard: ${String(error)}`,
        {
          cause: error,
        },
      );
    }
  }
  return records;
}
