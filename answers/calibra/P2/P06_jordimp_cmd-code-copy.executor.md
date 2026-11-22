=== FILE: src/lib/cmd-code.ts ===
export function splitCmdLine(text: string): [string, string, string] | null {
  const match = text.match(/^(.*?)\s*(npx skills add jordimarsal\/harness)\s*(.*)$/);
  if (!match) return null;
  return [match[1], match[2], match[3]];
}

=== END FILE ===

=== FILE: src/lib/cmd-code.spec.ts ===
import { describe, expect, it } from 'vitest';
import { splitCmdLine } from './cmd-code';

describe('splitCmdLine', () => {
  it('returns null for no-match input', () => {
    expect(splitCmdLine('hello world')).toBeNull();
    expect(splitCmdLine('npm run build')).toBeNull();
    expect(splitCmdLine('')).toBeNull();
  });

  it('matches command at line start with empty prefix and suffix', () => {
    const result = splitCmdLine('npx skills add jordimarsal/harness');
    expect(result).toEqual(['', 'npx skills add jordimarsal/harness', '']);
  });

  it('matches command at line end with prefix and empty suffix', () => {
    const result = splitCmdLine('Run this: npx skills add jordimarsal/harness');
    expect(result).toEqual(['Run this:', 'npx skills add jordimarsal/harness', '']);
  });

  it('matches command in the middle with both segments', () => {
    const result = splitCmdLine('Before npx skills add jordimarsal/harness after');
    expect(result).toEqual(['Before ', 'npx skills add jordimarsal/harness', ' after']);
  });

  it('preserves case exactly on the command segment', () => {
    const result = splitCmdLine('prefix npx skills add jordimarsal/harness suffix');
    expect(result![1]).toBe('npx skills add jordimarsal/harness');
  });
});

=== END FILE ===

=== FILE: src/components/site/CmdLine.astro ===
---
import type { Props } from '../../data/types';

export interface CmdLineProps extends Props {
  text: string;
}

const { text } = Astro.props;

function renderSegments(text: string): import('astro').AstroComponentFactory | null {
  // Import the util at runtime to avoid circular deps during build
  const { splitCmdLine } = await import('../../lib/cmd-code.ts');
  const match = splitCmdLine(text);
  if (!match) return null;

  const [before, cmd, after] = match;

  return (
    <>
      {before && <span>{before}</span>}
      <code class="cmd-copy" data-copy={cmd}>{cmd}</code>
      {after && <span>{after}</span>}
    </>
  );
}

const segments = renderSegments(text);
---
{segments}

=== END FILE ===

=== FILE: src/pages/[lang]/projects/[slug].astro ===
---
import SiteLayout from '../../../layouts/SiteLayout.astro';
import Breadcrumb from '../../../components/site/Breadcrumb.astro';
import BackBuilding from '../../../components/site/BackBuilding.astro';
import CmdLine from '../../../components/site/CmdLine.astro';
import SecHead from '../../../components/site/SecHead.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import {
  BREADCRUMB_HOME,
  BLOG_UI,
  CV,
  DEPTS,
  FLOOR_ORDER,
  FOOTER,
  FRONTDESK_PAGE,
  INSPECTIONS_PAGE,
  OPERATIONS_PAGE,
  PAGES,
  PEOPLE_PAGE,
  PRINCIPLES,
  RESEARCH_PAGE,
  TELEMETRY_PAGE,
  TOOLING_PAGE,
  UI,
  post,
  project,
} from '../../../data/content';
import type { ProjectKey } from '../../../data/types';
import { assetPath, dirRoute, srcPath } from '../../../lib/paths';
import { externalLinkAttrs } from '../../../lib/links';
import { SITE } from '../../../config';

export async function getStaticPaths() {
  const slug = (key: ProjectKey): string => dirRoute(PAGES[key].route).replace(/^projects\//, '');
  return LOCALES.flatMap((lang) =>
    PROJECTS.map((p) => ({
      params: { lang, slug: p.slug },
      props: { lang, key: p.key },
    })),
  );
}

type Props = { lang: Locale; key: ProjectKey };
const { lang, key } = Astro.props;

const p = project(key);
const route = dirRoute(PAGES[key].route);
---
<SiteLayout lang={lang}>
  <Breadcrumb items={[{ text: BREADCRUMB_HOME[lang], href: `/${lang}/` }, { text: PAGES[key].title[lang] }]} />
  <SecHead title={PAGES[key].title[lang]} description={p.blurb[lang]} />
  <article>
    <h1>{p.blurb[lang]}</h1>
    <section class="problem">{p.problem[lang]}</section>
    <section class="summary">{p.summary[lang]}</section>
    <ul class="highlights">
      {p.highlights[lang].map((item) => (
        <li>{item}</li>
      ))}
    </ul>
    <CmdLine text={p.blurb[lang]} />
  </article>
</SiteLayout>

=== END FILE ===

=== FILE: src/components/site/DeptCard.astro ===
---
import type { Props } from '../../data/types';
import CmdLine from './CmdLine.astro';

export interface DeptCardProps extends Props {
  deptKey: string;
  title: string;
  blurb: string;
  highlights?: string[];
  cmdText?: string;
}

const { deptKey, title, blurb, highlights = [], cmdText } = Astro.props;
---
<div class="dept-card" data-dept={deptKey}>
  <h2>{title}</h2>
  <p>{blurb}</p>
  {cmdText && <CmdLine text={cmdText} />}
  {highlights.length > 0 && (
    <ul class="highlights">
      {highlights.map((item) => (
        <li>{item}</li>
      ))}
    </ul>
  )}
</div>

=== END FILE ===

=== FILE: src/styles/site.css ===
/* ... existing styles ... */

.cmd-copy {
  font-family: 'Space Mono', monospace;
  background: var(--surface-1);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.cmd-copy:hover,
.cmd-copy:focus-visible {
  background: var(--accent);
  outline: none;
}

/* ... rest of existing styles ... */

=== END FILE ===