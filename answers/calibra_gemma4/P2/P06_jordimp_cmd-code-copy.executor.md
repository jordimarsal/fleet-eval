=== FILE: src/lib/cmd-code.ts ===
export const CMD = 'npx skills add jordimarsal/harness';

export type SplitResult = {
  before: string;
  cmd: string;
  after: string;
};

/**
 * Splits a text line into three segments based on the first occurrence of the install command.
 * Returns null if the command is not found.
 */
export function splitCmdLine(text: string): SplitResult | null {
  const index = text.indexOf(CMD);
  if (index === -1) {
    return null;
  }

  return {
    before: text.slice(0, index),
    cmd: CMD,
    after: text.slice(index + CMD.length),
  };
}
=== END FILE ===

=== FILE: src/components/site/CmdLine.astro ===
---
interface Props {
  text: string;
}

const { text } = Astro.props;
import { splitCmdLine } from '../../lib/cmd-code';

const split = splitCmdLine(text);
---

{split ? (
  <p class="cmd-line">
    <span>{split.before}</span>
    <code class="cmd-copy" data-copy={split.cmd}>{split.cmd}</code>
    <span>{split.after}</span>
  </p>
) : (
  <span>{text}</span>
)}

<style>
  .cmd-line {
    display: inline;
  }
  .cmd-copy {
    position: relative;
    padding: 0.1em 0.3em;
    background: var(--color-bg-subtle, #f4f4f4);
    border-radius: 4px;
    font-family: var(--font-mono, monospace);
    cursor: pointer;
    user-select: all;
    transition: background 0.2s ease;
  }
  .cmd-copy:hover,
  .cmd-copy:focus {
    background: var(--color-accent, #e0e0e0);
    outline: none;
  }
  /* Visual feedback for copy via JS is handled in client scripts if needed, 
     but the requirement focuses on markup and styles */
</style>
=== END FILE ===

=== FILE: src/pages/[lang]/projects/[slug].astro ===
---
import SiteLayout from '../../../layouts/SiteLayout.astro';
import Breadcrumb from '../../../components/site/Breadcrumb.astro';
import SecHead from '../../../components/site/SecHead.astro';
import CmdLine from '../../../components/site/CmdLine.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import { PAGES, PROJECTS } from '../../../data/content';
import { dirRoute } from '../../../lib/paths';

export async function getStaticPaths() {
  return LOCALES.flatMap((lang) =>
    PROJECTS.map((p) => ({
      params: { lang, slug: p.slug },
      props: { lang, project: p },
    })),
  );
}

type Props = { lang: Locale; project: any };
const { lang, project } = Astro.props;
const route = dirRoute(PAGES[project.slug].route);
---

<SiteLayout title={project.title[lang]} description={project.summary[lang]}>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href={`/${lang}/`}>Home</a>
    <a href={`/${lang}/projects/`}>Projects</a>
  </nav>

  <main>
    <SecHead title={project.title[lang]} subtitle={project.sub[lang]} />

    <section class="problem">
      <h2>Problem</h2>
      <p>{project.problem[lang]}</p>
    </section>

    <section class="highlights">
      <h2>Highlights</h2>
      <ul>
        {project.highlights[lang].map((h: string) => <li>{h}</li>)}
      </ul>
    </section>

    <section class="build-log">
      <h2>Build Log</h2>
      <div class="log-content">
        <CmdLine text="Its process ships as six standalone skills, installable with npx skills add jordimarsal/harness." />
      </div>
    </section>

    <section class="metrics">
      <h2>Metrics</h2>
      <dl>
        {project.metrics.map((m: any) => (
          <>
            <dt>{m.label[lang]}</dt>
            <dd>{m.value}</dd>
          </>
        ))}
      </dl>
    </section>
  </main>
</SiteLayout>
=== END FILE ===

=== FILE: src/components/site/DeptCard.astro ===
---
import type { DeptKey } from '../../data/types';
import { DEPTS, PAGES } from '../../data/content';
import { dirRoute } from '../../lib/paths';
import CmdLine from './CmdLine.astro';

interface Props {
  deptKey: DeptKey;
  lang: string;
}

const { deptKey, lang } = Astro.props;
const d = DEPTS[deptKey];
const route = dirRoute(PAGES[deptKey].route);
---

<a href={route} class="dept-card">
  <h3>{d.name[lang]}</h3>
  <p>{d.description[lang]}</p>
  <div class="footer">
    <small>View floor details</small>
    <div class="cmd-preview">
       <CmdLine text="To audit this department, run npx skills add jordimarsal/harness" />
    </div>
  </div>
</a>

<style>
  .dept-card {
    display: block;
    padding: 1.5rem;
    border: 1px solid var(--color-border);
    text-decoration: none;
    color: inherit;
    transition: transform 0.2s ease;
  }
  .dept-card:hover {
    transform: translateY(-4px);
  }
  .cmd-preview {
    margin-top: 1rem;
    font-size: 0.85rem;
    opacity: 0.8;
  }
</style>
=== END FILE ===

=== FILE: src/styles/site.css ===
/* Existing styles... */

.cmd-copy {
  position: relative;
  padding: 0.1em 0.3em;
  background: var(--color-bg-subtle, #f4f4f4);
  border-radius: 4px;
  font-family: var(--font-mono, monospace);
  cursor: pointer;
  user-select: all;
  transition: background 0.2s ease;
}

.cmd-copy:hover,
.cmd-copy:focus {
  background: var(--color-accent, #e0e0e0);
  outline: none;
}
=== END FILE ===