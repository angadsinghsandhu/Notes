import { fromHtml } from 'hast-util-from-html';
import type { Nodes } from 'hast';
import { readFile } from 'node:fs/promises';
import { describe, expect, it } from 'vitest';
import { renderSource } from '../../../../src/content/render/source.js';

function displayedText(node: Nodes): string {
  return node.type === 'text'
    ? node.value
    : 'children' in node
      ? node.children.map(displayedText).join('')
      : '';
}

describe('controlled source display', () => {
  it('highlights the real subsets program without importing or executing it', async () => {
    const code = await readFile(
      'tests/fixtures/real/task4/78_Subsets.py',
      'utf8',
    );
    const result = await renderSource(code, 'python');
    expect(result.html).toContain('class="shiki');
    expect(result.html).toContain('subsets_backtracking');
    expect(displayedText(fromHtml(result.html, { fragment: true }))).toBe(code);
    expect(result.headings).toEqual([]);
  });
  it('escapes literal executable HTML and falls back for unknown languages', async () => {
    const result = await renderSource(
      '<script>globalThis.task4Executed = true</script>',
      'unknown-language',
    );
    expect(displayedText(fromHtml(result.html, { fragment: true }))).toBe(
      '<script>globalThis.task4Executed = true</script>',
    );
    expect(result.html).not.toContain('<script>');
    expect('task4Executed' in globalThis).toBe(false);
  });
});
