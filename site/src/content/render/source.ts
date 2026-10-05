import { bundledLanguages, bundledLanguagesAlias, codeToHtml } from 'shiki';
import type { BundledLanguage } from 'shiki';
import type { RenderResult } from '../types.js';

/** Highlight text only; language identifiers never load author code. */
export async function renderSource(
  code: string,
  language: string,
): Promise<RenderResult> {
  const requested = language.toLowerCase();
  const lang =
    Object.hasOwn(bundledLanguages, requested) ||
    Object.hasOwn(bundledLanguagesAlias, requested)
      ? (requested as BundledLanguage)
      : 'text';
  return {
    html: await codeToHtml(code, { lang, theme: 'github-dark' }),
    headings: [],
  };
}
