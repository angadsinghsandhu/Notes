/** Copy conveniences are added only when JS runs; source remains readable without them. */
export function initCopyCode(document: Document): void {
  for (const pre of document.querySelectorAll<HTMLElement>('pre')) {
    if (pre.dataset['copyReady']) continue;
    pre.dataset['copyReady'] = 'true';
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Copy code';
    const status = document.createElement('span');
    status.setAttribute('role', 'status');
    status.className = 'copy-status';
    const controls = document.createElement('div');
    controls.className = 'code-controls';
    controls.append(button, status);
    pre.before(controls);
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        const clipboard = document.defaultView?.navigator.clipboard;
        if (!clipboard) throw new Error('Clipboard unavailable');
        await clipboard.writeText(pre.textContent);
        status.textContent = 'Code copied.';
      } catch {
        status.textContent = 'Copy failed; select the code and copy manually.';
      } finally {
        button.disabled = false;
      }
    });
  }
}
