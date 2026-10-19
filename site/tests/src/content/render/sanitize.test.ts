import { describe, expect, it } from 'vitest';
import { sanitizeAuthorHtml } from '../../../../src/content/render/sanitize.js';

describe('author HTML allowlist', () => {
  it('preserves safe disclosure anchors, underline and bounded image attributes', () => {
    const html = sanitizeAuthorHtml(
      '<details open><summary id="faq-how-to-get-update">Help</summary><u>under</u><ins>insert</ins><img src="https://example.com/a.png" alt="pic" width="20" height="10"></details>',
    );
    expect(html).toContain('<details open>');
    expect(html).toContain('id="faq-how-to-get-update"');
    expect(html).toContain('<u>under</u><ins>insert</ins>');
    expect(html).toContain('width="20" height="10"');
  });
  it('removes active elements, event handlers, unsafe URLs and forged renderer classes', () => {
    const html = sanitizeAuthorHtml(
      '<script>alert(1)</script><style>body{display:none}</style><iframe src="https://evil.test"></iframe><svg onload="evil()"><script>x()</script></svg><a href="javascript:alert(1)" onclick="x()">bad</a><img src="data:image/svg+xml,x" onerror="x()"><span class="katex" style="display:none" id="bad id">text</span><input type="text" value="steal">',
    );
    expect(html).not.toMatch(
      /script|alert|iframe|svg|onload|onclick|onerror|javascript:|data:|style=|class=|bad id|input/,
    );
    expect(html).toContain('bad</a>');
    expect(html).toContain('text');
  });
  it('blocks encoded and obfuscated schemes while preserving normal relative URLs', () => {
    const html = sanitizeAuthorHtml(
      '<a href="java&#x73;cript:alert(1)">one</a><a href="java&#x0a;script:alert(1)">two</a><img src="//evil.test/img"><a href="../note.md#ok">safe</a>',
    );
    expect(html).not.toMatch(/javascript|alert|evil|&#x0a;/);
    expect(html).toContain('href="../note.md#ok"');
  });
});

it('rejects malformed network URLs and invalid image dimensions but retains disabled task checkboxes', () => {
  const html = sanitizeAuthorHtml(
    '<a href="http://[">bad</a><img src="https://example.test/a.png" width="0" height="40000001"><input type="checkbox" checked><input type="text">',
  );
  expect(html).not.toContain('href=');
  expect(html).not.toContain('width=');
  expect(html).not.toContain('height=');
  expect(html).toContain('type="checkbox"');
  expect(html).toContain('disabled');
  expect(html).not.toContain('type="text"');
});
