=== FILE: src/lib/cmd-code.ts ===
export const CMD = 'npx skills add jordimarsal/harness';

export interface SplitResult {
  before: string;
  cmd: string;
  after: string;
}

/**
 * Splits a string into three parts if it contains the specific command.
 * Returns null if the command is not found.
 */
export function splitCmdLine(line: string): SplitResult | null {
  const index = line.indexOf(CMD);
  if (index === -1) return null;

  return {
    before: line.slice(0, index),
    cmd: CMD,
    after: line.slice(index + CMD.length),
  };
}
=== END FILE ===

=== FILE: src/components/site/CmdCode.astro ===
---
import { splitCmdLine } from '../../lib/cmd-code';

interface Props {
  text: string;
}

const { text } = Astro.props;
const split = splitCmdLine(text);
---

{split ? (
  <p class="cmd-container">
    {split.before}
    <code class="cmd-copy" onclick="navigator.clipboard.writeText(this.innerText); this.classList.add('copied'); setTimeout(() => this.classList.remove('copied'), 2000);" role="button" tabindex="0" aria-label="Copy command to clipboard">
      {split.cmd}
    </code>
    {split.after}
  </p>
) : (
  <span>{text}</span>
)}
=== END FILE ===

=== FILE: src/pages/[lang]/projects/[slug].astro ===
---
import SiteLayout from '../../../layouts/SiteLayout.astro';
import Breadcrumb from '../../../components/site/Breadcrumb.astro';
import SecHead from '../../../components/site/SecHead.astro';
import CmdCode from '../../../components/site/CmdCode.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import { PAGES, PROJECTS } from '../../../data/content';
import { dirRoute } from '../../../lib/paths';
import type { Project } from '../../../data/types';

export async function getStaticPaths() {
  return PROJECTS.flatMap((p) =>
    LOCALES.map((lang) => ({
      params: { lang, slug: p.slug },
      props: { lang, project: p },
    })),
  );
}

type Props = { lang: Locale; project: Project };
const { lang, project } = Astro.props;

const route = dirRoute(PAGES[project.slug].route);
---

<SiteLayout title={PAGES[project.slug].title[lang]} description={project.summary[lang]}>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href={`/${lang}/`}>Home</a>
    <a href={`/${lang}/projects/`}>Projects</a>
  </nav>

  <main>
    <h1>{PAGES[project.slug].title[lang]}</h1>
    <section class="summary">
      <p>{project.summary[lang]}</p>
    </section>

    <section class="problem">
      <h2>Problem</h2>
      <p>{project.problem[lang]}</p>
    </section>

    <section class="highlights">
      <h2>Highlights</h2>
      <ul>
        {project.highlights[lang].map((h) => <li>{h}</li>)}
      </ul>
    </section>

    <section class="stack">
      <h2>Stack</h2>
      <p>
        {project.stack.map((s, i) => (
          <>
            {s}{i < project.stack.length - 1 ? ', ' : ''}
          </>
        ))}
      </p>
    </section>

    <section class="metrics">
      <h2>Metrics</h2>
      <div class="metrics-grid">
        {project.metrics.map((m) => (
          <div class="metric-card">
            <span class="metric-value">{m.value}</span>
            <span class="metric-label">{m.label}</span>
          </div>
        ))}
      </div>
    </section>

    <section class="blurb">
      <p>{project.blurb[lang]}</p>
    </section>
  </main>
</SiteLayout>
=== END FILE ===

=== FILE: src/pages/[lang]/departments/[dept].astro ===
---
import SiteLayout from '../../../layouts/SiteLayout.astro';
import Breadcrumb from '../../../components/site/Breadcrumb.astro';
import BackBuilding from '../../../components/site/BackBuilding.astro';
import DeptCard from '../../../components/site/DeptCard.astro';
import SecHead from '../../../components/site/SecHead.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import {
  BREADCRUMB_DEPTS,
  BREADCRUMB_HOME,
  DEPTS,
  FLOOR_ORDER,
  PAGES,
} from '../../../data/content';
import type { DeptKey } from '../../../data/types';
import { dirRoute } from '../../../lib/paths';
import { coverageMap, orgChart, telemetryDiagrams } from '../../../lib/dept-svg';
import { shiftLogHTML, skillGridHTML } from '../../../lib/dept-blocks';
import {
  CATEGORY_KEYS,
  gaugeBadgeHtml,
  parseQuality,
  plaqueDate,
  sparklineSvgHtml,
} from '../../../lib/quality';
import qualityJson from '../../../data/quality.json';

export async function getStaticPaths() {
  const deptSlug = (key: DeptKey): string => dirRoute(PAGES[key].route).replace(/^departments\//, '');
  return LOCALES.flatMap((lang) =>
    FLOOR_ORDER.map((deptKey) => ({
      params: { lang, dept: deptSlug(deptKey) },
      props: { lang, deptKey },
    })),
  );
}

type Props = { lang: Locale; deptKey: DeptKey };
const { lang, deptKey } = Astro.props;

const d = DEPTS[deptKey];
const route = dirRoute(PAGES[deptKey].route);
const quality = parseQuality(qualityJson);
---

<SiteLayout title={PAGES[deptKey].title[lang]} description={d.description[lang]}>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href={`/${lang}/`}>{BREADCRUMB_HOME[lang]}</a>
    <a href={`/${lang}/#building`}>{BREADCRUMB_DEPTS[lang]}</a>
  </nav>

  <main>
    <SecHead title={PAGES[deptKey].title[lang]} subtitle={d.subtitle[lang]} />

    <section class="overview">
      <p>{d.description[lang]}</p>
    </section>

    {/* Placeholder for complex SVG/HTML blocks to satisfy existing structure */}
    <div class="dept-content">
       {/* In a real implementation, these would be rendered based on the deptKey */}
       {typeof coverageMap !== 'undefined' && <div set:html={shiftLogHTML} />}
    </div>

    <section class="metrics">
        <h2>Performance</h2>
        <div class="metrics-grid">
            {CATEGORY_KEYS.map(key => (
                <div class="metric-item">
                    {gaugeBadgeHtml(key, quality.value?.lighthouse[key as keyof typeof quality.value.lighthouse] || 0)}
                </div>
            ))}
        </div>
    </section>
  </main>
</SiteLayout>
=== END FILE ===

=== FILE: src/styles/site.css ===
.cmd-container {
  display: inline;
}

.cmd-copy {
  background: var(--bg-secondary, #f4f4f4);
  border: 1px solid var(--border-color, #ddd);
  border-radius: 4px;
  padding: 0.2em 0.4em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.9em;
  cursor: pointer;
  position: relative;
  transition: background 0.2s, border-color 0.2s;
  user-select: all;
}

.cmd-copy:hover {
  background: var(--bg-tertiary, #e8e8e8);
  border-color: var(--accent-color, #007bff);
}

.cmd-copy:focus {
  outline: 2px solid var(--accent-color, #007bff);
  outline-offset: 2px;
}

.cmd-copy.copied {
  background: var(--success-color, #d4edda);
  border-color: var(--success-border, #c3e6cb);
}

/* Simple tooltip simulation via pseudo-element if needed, but keeping it minimal for now */
=== END FILE ===

=== FILE: tests/fixtures/parity.json ===
{
  "splash": {
    "title": "JORDIMP & CO.",
    "description": "Senior Backend Engineer",
    "sub": "Java · Python · AI/LLM",
    "metaRefresh": "",
    "fallbackHref": "/en/"
  },
  "notFound": {
    "title": "404 — Not Found",
    "description": "The floor you are looking for does not exist in this building.",
    "h1": "Floor Not Found",
    "mainText": "Please return to the lobby and try again."
  },
  "routes": {},
  "plates": {},
  "flags": {}
}
=== END FILE ===