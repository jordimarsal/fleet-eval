=== FILE: src/lib/cmd-code.ts ===
export const CMD = 'npx skills add jordimarsal/harness';

export interface CmdLineParts {
  before: string;
  cmd: string;
  after: string;
}

export function splitCmdLine(text: string): CmdLineParts | null {
  const idx = text.indexOf(CMD);
  if (idx === -1) return null;
  return {
    before: text.slice(0, idx),
    cmd: CMD,
    after: text.slice(idx + CMD.length),
  };
}
=== END FILE ===

=== FILE: src/components/site/CmdLine.astro ===
---
import { splitCmdLine } from '../../lib/cmd-code';

interface Props {
  line: string;
}

const { line } = Astro.props;
const parts = splitCmdLine(line);
---
{parts ? (
  <span class="cmd-copy-wrap">
    {parts.before && <span class="cmd-copy__segment">{parts.before}</span>}
    <span class="cmd-copy__control">
      <code class="cmd-copy" data-copy={parts.cmd}>{parts.cmd}</code>
      <button type="button" class="cmd-copy__btn" aria-label="Copy install command" title="Copy">COPY</button>
    </span>
    {parts.after && <span class="cmd-copy__segment">{parts.after}</span>}
  </span>
) : (
  <span class="cmd-copy__plain">{line}</span>
)}

<script is:inline define:vars={{}}>
  if (!document.body.dataset.cmdCopyWired) {
    document.body.dataset.cmdCopyWired = 'true';
    document.addEventListener('click', async (event) => {
      const btn = event.target && event.target.closest ? event.target.closest('.cmd-copy__btn') : null;
      if (!btn) return;
      const code = btn.parentElement?.querySelector('.cmd-copy[data-copy]');
      const text = code?.getAttribute('data-copy') ?? '';
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = 'COPIED';
      } catch {
        btn.textContent = 'COPY FAILED';
      }
      window.setTimeout(() => {
        btn.textContent = 'COPY';
      }, 1600);
    });
  }
</script>
=== END FILE ===