ROLE: implementation planner. A feature has been approved. You get the
approved requirements and the repository file tree BEFORE implementation.
Write the implementation plan with EXACTLY these three sections:

FILES
<repo-relative path of every file you would create or modify, one per line>

TASKS
T1: <short title>
    depends_on: (none)
    refs: R1, R2
T2: <short title>
    depends_on: T1
    refs: R3
(... ordered so dependencies come first; every requirement must be covered
 by the refs of at least one task)

GATES
<the verification gates you would run before closing the feature>

--- APPROVED REQUIREMENTS ---
R1: The system shall not emit the string `gmail.com` in any source file under `src/`, any test file under `tests/`, or any built HTML file under `dist/`.  Verification: the unit test `src/config.spec.ts` pins the value; the `qa:content` gate scans both the `src/` + `tests/` sources and the visible text of every `dist/**/*.html` for `gmail.com`; the manual command `rg -n "gmail" src dist` returns no match.

R2: WHEN any page renders an email pill (the `FooterDesk` footer pill, or the front-desk `DeptPanel` pill on the home building page), the system shall set that pill's `href` to `mailto:hello@jordimp.net`, while the pill's visible label stays the localized `FOOTER.email` string in the page locale.  Verification: `tests/home.spec.ts` asserts, on each of `/en/`, `/es/`, `/ca/`, that `.footer-desk .pill[href^="mailto:"]` has `href="mailto:hello@jordimp.net"`.

R3: WHEN the front desk department page (`/{lang}/departments/front-desk/`) renders in any of the three locales, the system shall display `hello@jordimp.net` as the email contact-row value, and set the row's copy button `data-copy` to `hello@jordimp.net`.  Verification: `tests/departments.spec.ts` asserts, for all three locales, that the first `.contact-row .contact-row__v` has text `hello@jordimp.net` and that `button.copy-btn[data-copy]` equals `hello@jordimp.net` (the existing assertions already use `SITE.email`, which must resolve to the same value).

R4: WHEN a page emits the `Person` JSON-LD block, the system shall set its `email` property to `mailto:hello@jordimp.net`.  Verification: `src/lib/seo.spec.ts` pins `personJsonLd('en').email` to the literal.

R5: WHEN the site builds the `llms.txt` and `llms-full.txt` endpoints, the system shall emit `hello@jordimp.net` in the `llms.txt` contact block (`- Email:`) and in the `llms-full.txt` contact line (`Contact:`).  Verification: `src/lib/llms.spec.ts` and `src/lib/llms-endpoint.spec.ts` pin the literal in both builders; the committed oracle `src/lib/__snapshots__/llms-endpoint.spec.ts.snap` is refreshed with `vitest -u` and reviewed for the address-only change.

R6: WHILE the `hello@jordimp.net` mailbox is not verified deliverable — MX and SPF records present for `jordimp.net` and a forwarded test message received in the owner's inbox, with the evidence recorded in `harness/progress/impl_contact-email.md` — the system shall not emit `hello@jordimp.net` in `src/` or `dist/` (the contact-email feature stays `blocked`).  Verification: Task 0 of `tasks.md` records the evidence (the `dig` output for MX/SPF and a confirmation that the test message reached the inbox). If the evidence is absent, the `rg -n "hello@jordimp.net" src dist` check must be empty and no implementation task runs; the leader keeps the feature in `blocked`.

R7: The system shall define the canonical address exactly once as a `CONTACT_EMAIL` literal in `src/config.ts`, and have both `src/config.ts` `SITE.email` and `src/data/content.ts` `SITE.email` reference it.  Verification: `src/config.spec.ts` asserts `CONTACT_EMAIL === 'hello@jordimp.net'`, `CONFIG_SITE.email === CONTACT_EMAIL` and `CONTENT_SITE.email === CONTACT_EMAIL`.

R8: The receiving path for `hello@jordimp.net` shall be provisioned on a provider's free tier (no paid mail plan required) — either free custom-domain forwarding (e.g. ImprovMX, forwardemail.net, Cloudflare Email Routing) or a free real mailbox (e.g. Zoho Mail Free, DNSExit) — with the chosen provider and tier recorded in the Task 0 evidence.  Verification: `harness/progress/impl_contact-email.md` names the provider and states the free tier used (forwarding rule or mailbox plan); no billing/payment method is required. This is a human-evidence requirement, checked at the completion gate alongside R6.

--- FEATURE TITLE ---
Merge feature/f14-contact-email: publish hello@jordimp.net from a single CONTACT_EMAIL literal

--- REPOSITORY FILE TREE (before implementation) ---
.github/workflows/deploy.yml
.github/workflows/qa.yml
.github/workflows/quality.yml
.gitignore
AGENTS.md
README.md
astro.config.mjs
docs/architecture.md
docs/conventions.md
docs/deploy-dns-checklist.md
docs/iteration-protocol.md
docs/specs.md
docs/superpowers/plans/2026-09-16-portfolio-phase0-1-front.md
docs/superpowers/plans/2026-09-22-contact-email.md
docs/superpowers/plans/2026-09-22-external-brand-hygiene.md
docs/superpowers/plans/2026-09-22-external-public-artifacts.md
docs/superpowers/plans/2026-09-22-front-desk-positioning.md
docs/superpowers/plans/2026-09-22-millores-master.md
docs/superpowers/plans/2026-09-22-rag-eval-article.md
docs/superpowers/plans/2026-09-22-showcase-curation.md
docs/superpowers/specs/2026-09-16-portfolio-web-design.md
docs/verification.md
lighthouserc.json
package.json
playwright.config.ts
public/CNAME
public/cv/Jordi-Marcal-Poy-CV-EN.pdf
public/cv/Jordi-Marcal-Poy-CV-ES.pdf
public/robots.txt
scripts/check-links.mjs
scripts/collect-quality.mjs
scripts/distill-parity.mjs
scripts/qa-content.mjs
src/components/Analytics.astro
src/components/SEO.astro
src/components/site/BackBuilding.astro
src/components/site/Breadcrumb.astro
src/components/site/Building.astro
src/components/site/CaseMotif.astro
src/components/site/DeptCard.astro
src/components/site/DeptPanel.astro
src/components/site/DeptStrip.astro
src/components/site/FooterDesk.astro
src/components/site/Navbar.astro
src/components/site/ProjectCard.astro
src/components/site/SecHead.astro
src/components/site/Ticker.astro
src/config.ts
src/data/content.spec.ts
src/data/content.ts
src/data/quality.json
src/data/types.ts
src/env.d.ts
src/layouts/SiteLayout.astro
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
src/lib/analytics.spec.ts
src/lib/analytics.ts
src/lib/building-svg.spec.ts
src/lib/building-svg.ts
src/lib/case-svg.spec.ts
src/lib/case-svg.ts
src/lib/dept-blocks.spec.ts
src/lib/dept-blocks.ts
src/lib/dept-svg.spec.ts
src/lib/dept-svg.ts
src/lib/font-face.spec.ts
src/lib/font-face.ts
src/lib/i18n.spec.ts
src/lib/i18n.ts
src/lib/links.spec.ts
src/lib/links.ts
src/lib/llms-endpoint.spec.ts
src/lib/llms.spec.ts
src/lib/llms.ts
src/lib/night-boot.spec.ts
src/lib/night-boot.ts
src/lib/paths.spec.ts
src/lib/paths.ts
src/lib/quality.spec.ts
src/lib/quality.ts
src/lib/seo.spec.ts
src/lib/seo.ts
src/lib/sitemap.spec.ts
src/lib/sitemap.ts
src/pages/404.astro
src/pages/[lang]/cv.astro
src/pages/[lang]/departments/[dept].astro
src/pages/[lang]/index.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/projects/index.astro
src/pages/[lang]/writing/rag-eval-gate.astro
src/pages/index.astro
src/pages/llms-full.txt.ts
src/pages/llms.txt.ts
src/robots.spec.ts
src/scripts/building.ts
src/scripts/copy.ts
src/scripts/filter.ts
src/scripts/theme.ts
src/styles/contrast.spec.ts
src/styles/site.css
tests/cases.spec.ts
tests/cv.spec.ts
tests/departments.spec.ts
tests/fixtures/parity.json
tests/home.spec.ts
tests/interactions.spec.ts
tests/notfound.spec.ts
tests/projects.spec.ts
tests/seo-head.spec.ts
tests/smoke.spec.ts
tests/splash.spec.ts
tsconfig.json
vitest.config.ts

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- src/data/content.ts (first 60 lines of 117847 bytes) ---
import type {
  ArticleContent,
  CaseBuildStep,
  CaseUiStrings,
  CvContent,
  Dept,
  DeptKey,
  ExperienceEntry,
  FooterContent,
  FrontdeskPageContent,
  HomeContent,
  InspectionsPageContent,
  L10n,
  Locale,
  LocaleInfo,
  NotFoundContent,
  OperationsPageContent,
  PageLabels,
  PageMeta,
  PeoplePageContent,
  PrinciplesContent,
  Project,
  ProjectL10n,
  ResearchPageContent,
  SkillGroup,
  SiteInfo,
  TelemetryPageContent,
  Tier,
  ToolingPageContent,
  UiStrings,
  WorkContent,
  KVEntry,
} from './types';

export const SITE: SiteInfo = {
  brand: 'JORDIMP & CO.',
  person: 'Jordi Marçal Poy',
  role: { en: 'Senior Backend Engineer', es: 'Ingeniero Backend Senior', ca: 'Enginyer Backend Sènior' },
  tagline: { en: 'Java · Python · AI/LLM', es: 'Java · Python · IA/LLM', ca: 'Java · Python · IA/LLM' },
  url: 'https://jordimp.net',
  email: 'jordi.marsal@gmail.com',
  github: 'https://github.com/jordimarsal',
  linkedin: 'https://www.linkedin.com/in/jordi-marsal-poy',
  est: '2017',
  city: { en: 'Barcelona', es: 'Barcelona', ca: 'Barcelona' },
  year: '2026',
};

export const LOCALES: readonly Locale[] = ['en', 'es', 'ca'];
export const DEFAULT_LOCALE: Locale = 'en';

export const L: Record<Locale, LocaleInfo> = {
  en: { name: 'English', short: 'EN', htmlLang: 'en', og: 'en_US' },
  es: { name: 'Español', short: 'ES', htmlLang: 'es', og: 'es_ES' },
  ca: { name: 'Català', short: 'CA', htmlLang: 'ca', og: 'ca_ES' },
};

export const UI: UiStrings = {
  skip: {
    en: 'Skip to content',
--- src/styles/site.css (first 60 lines of 45472 bytes) ---
:root {
  --paper: #f6f5f2;
  --paper2: #fffdf6;
  --lite: #fff3b0;
  --ink: #0c0b0a;
  --ink2: #2f2b29;
  --y1: #ffd54f;
  --y2: #fbe435;
  --y3: #f4c430;
  --line: #0c0b0a;
  --meta-line: #b9b2a4;
  --shc: #0c0b0a;
  --chip-bg: #0c0b0a;
  --chip-fg: #ffd54f;
  --rule: rgba(12, 11, 10, 0.035);
  --sky: #eceade;
  --star: #0c0b0a;
  --street: #fffdf6;
  --street-line: #0c0b0a;
  --b-ink: #0c0b0a;
  --b-wall: #fffdf6;
  --b-accent: #fbe435;
  --b-plate: #0c0b0a;
  --b-plate-fg: #f6f5f2;
  --disp: 'Bricolage Grotesque', 'Arial Black', sans-serif;
  --body: 'Instrument Sans', system-ui, 'Segoe UI', sans-serif;
  --mono: 'Space Mono', ui-monospace, Menlo, monospace;
  --bd: 3px solid var(--line);
  --sh: 6px 6px 0 var(--shc);
  --sh-lg: 10px 10px 0 var(--shc);
  --sp-1: 8px;
  --sp-2: 16px;
  --sp-3: 24px;
  --sp-4: 32px;
  --sp-5: 48px;
  --sp-6: 64px;
  --sp-7: 96px;
}

html[data-night='1'] {
  --paper: #16130d;
  --paper2: #201c13;
  --lite: #2e2714;
  --ink: #f1ecdc;
  --ink2: #cfc7b0;
  --line: #f1ecdc;
  --meta-line: #5a5446;
  --shc: #000;
  --chip-bg: #f1ecdc;
  --chip-fg: #16130d;
  --rule: rgba(241, 236, 220, 0.06);
  --sky: #1c1b3a;
  --star: #ffd54f;
  --street: #12100b;
  --street-line: #f1ecdc;
}

*,
*::before,
*::after {
--- src/data/content.spec.ts (first 60 lines of 26514 bytes) ---
import { describe, expect, it } from 'vitest';
import {
  ARTICLE,
  CASE_BUILD,
  CASE_NOTES,
  DEPTS,
  EXPERIENCE,
  FEATURED,
  FLOOR_LABELS,
  FLOOR_ORDER,
  FOOTER,
  FRONTDESK_PAGE,
  HOME,
  INSPECTIONS_PAGE,
  LOCALES,
  OPERATIONS_PAGE,
  PAGES,
  PEOPLE_PAGE,
  PROJECTS,
  RESEARCH_PAGE,
  SITE,
  SKILLS,
  TICKER,
  TIER_LABELS,
  TIER_ORDER,
  TOOLING_PAGE,
  UI,
  WORK,
  project,
  tierProjects,
} from './content';
import { SITE as CONFIG_SITE } from '../config';
import type { Tier } from './types';

const PROJECT_COUNT = 11;
const FEATURED_COUNT = 3;
const DEPT_COUNT = 7;
const EXPERIENCE_COUNT = 4;

describe('projects data', () => {
  it('ships exactly 11 projects with unique slugs', () => {
    expect(PROJECTS).toHaveLength(PROJECT_COUNT);
    expect(new Set(PROJECTS.map((p) => p.slug)).size).toBe(PROJECT_COUNT);
  });

  it('gives every project trilingual blurb, summary, problem, highlights and metrics', () => {
    for (const p of PROJECTS) {
      for (const lang of LOCALES) {
        expect(p.blurb[lang].trim(), `${p.slug}:blurb.${lang}`).not.toBe('');
        expect(p.summary[lang].trim(), `${p.slug}:summary.${lang}`).not.toBe('');
        expect(p.problem[lang].trim(), `${p.slug}:problem.${lang}`).not.toBe('');
        expect(p.highlights[lang].length, `${p.slug}:highlights.${lang}`).toBeGreaterThan(0);
      }
      expect(p.stack.length, p.slug).toBeGreaterThan(0);
      expect(Array.isArray(p.metrics), `${p.slug}:metrics`).toBe(true);
      for (const metric of p.metrics) {
        expect(metric.value.trim(), `${p.slug}:metric.value`).not.toBe('');
        for (const lang of LOCALES) {
          expect(metric.label[lang].trim(), `${p.slug}:metric.label.${lang}`).not.toBe('');
        }
--- tests/departments.spec.ts (first 60 lines of 20566 bytes) ---
import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import {
  ARTICLE,
  BREADCRUMB_DEPTS,
  BREADCRUMB_HOME,
  DEPTS,
  EXPERIENCE,
  FLOOR_ORDER,
  FRONTDESK_PAGE,
  INSPECTIONS_PAGE,
  OPERATIONS_PAGE,
  PAGES,
  PAGE_LABELS,
  PEOPLE_PAGE,
  PRINCIPLES,
  RESEARCH_PAGE,
  SKILLS,
  TELEMETRY_PAGE,
  TOOLING_PAGE,
  UI,
  project,
} from '../src/data/content';
import { LOCALES, type Locale } from '../src/lib/i18n';
import type { DeptKey } from '../src/data/types';
import { SITE } from '../src/config';
import { CATEGORY_KEYS, formatScore, parseQuality, plaqueText } from '../src/lib/quality';

const qualityJson: unknown = JSON.parse(
  readFileSync(new URL('../src/data/quality.json', import.meta.url), 'utf8'),
);

const deptSlug = (key: DeptKey): string =>
  PAGES[key].route.replace(/^departments\//, '').replace(/\.html$/, '');
const deptRoute = (lang: Locale, key: DeptKey): string => `/${lang}/departments/${deptSlug(key)}/`;

const CURRENT_ENTRIES = EXPERIENCE.filter((e) => e.current);

const BACK_LABEL: Record<Locale, string> = {
  en: 'Back to the building',
  es: 'Volver al edificio',
  ca: 'Torna a l’edifici',
};

test.describe('department pages (T8)', () => {
  test('renders the research floor structure', async ({ page }) => {
    const key: DeptKey = 'research';
    const d = DEPTS[key];
    await page.goto(deptRoute('en', key));

    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    expect(await page.title()).toBe(PAGES[key].title.en);

    const breadcrumb = page.locator('nav.breadcrumb[aria-label="Breadcrumb"]');
    await expect(breadcrumb.locator('a')).toHaveCount(2);
    await expect(breadcrumb.locator('a').nth(0)).toHaveText(BREADCRUMB_HOME.en);
    await expect(breadcrumb.locator('a').nth(0)).toHaveAttribute('href', '/en/');
    await expect(breadcrumb.locator('a').nth(1)).toHaveText(BREADCRUMB_DEPTS.en);
    await expect(breadcrumb.locator('a').nth(1)).toHaveAttribute('href', '/en/#building');
    await expect(breadcrumb.locator('span[aria-current="page"]')).toHaveText(d.name.en);
--- tests/smoke.spec.ts (first 60 lines of 15794 bytes) ---
import { readFileSync } from 'node:fs';
import { expect, test, type ConsoleMessage, type Page } from '@playwright/test';
import { FLOOR_ORDER, PAGES, PROJECTS } from '../src/data/content';

const LOCALES = ['en', 'es', 'ca'] as const;
type Locale = (typeof LOCALES)[number];

const STATIC_ROUTES = ['', 'cv', 'projects', 'writing/rag-eval-gate'];
const PROJECT_SLUGS = PROJECTS.map((p) => p.slug);
const DEPT_SLUGS = FLOOR_ORDER.map((key) =>
  PAGES[key].route.replace(/^departments\//, '').replace(/\.html$/, '')
);
const OLD_SLUGS = ['about', 'experience', 'skills'];
const UNKNOWN_PATH = '/nonexistent/';
const REDIRECT_TARGET = /\/en\/$/;

interface RouteFixture {
  title: string;
  description: string;
  h1: string;
  mainText: string;
}

interface ParityFixture {
  splash: {
    title: string;
    description: string;
    sub: string;
    metaRefresh: string;
    fallbackHref: string;
  };
  notFound: RouteFixture;
  routes: Record<string, RouteFixture>;
  plates: Record<string, Record<string, { code: string; name: string; suffix: string }>>;
  flags: Record<string, string[]>;
}

// Validated boundary: the fixture is committed oracle data (ADR-6), its shape is
// enforced by the assertions below and by scripts/distill-parity.mjs, which distilled
// it from the built site (never hand-edit).
const parity = JSON.parse(
  readFileSync(new URL('./fixtures/parity.json', import.meta.url), 'utf8')
) as ParityFixture;

function localeRoutes(): string[] {
  const paths = [
    ...STATIC_ROUTES.map((r) => (r ? `${r}/` : '')),
    ...PROJECT_SLUGS.map((slug) => `projects/${slug}/`),
    ...DEPT_SLUGS.map((slug) => `departments/${slug}/`),
  ];
  return LOCALES.flatMap((locale) => paths.map((p) => `/${locale}/${p}`));
}

const SWEEP_TARGETS: ReadonlyArray<{ url: string; status: number }> = [
  ...localeRoutes().map((url) => ({ url, status: 200 })),
  { url: '/', status: 200 },
  { url: UNKNOWN_PATH, status: 404 },
];

// Chromium logs one inherent resource error when the document itself answers
--- src/pages/[lang]/departments/[dept].astro (first 60 lines of 14607 bytes) ---
---
import SiteLayout from '../../../layouts/SiteLayout.astro';
import Breadcrumb from '../../../components/site/Breadcrumb.astro';
import BackBuilding from '../../../components/site/BackBuilding.astro';
import DeptCard from '../../../components/site/DeptCard.astro';
import SecHead from '../../../components/site/SecHead.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import {
  ARTICLE,
  BREADCRUMB_DEPTS,
  BREADCRUMB_HOME,
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
  project,
} from '../../../data/content';
import type { DeptKey, StatEntry } from '../../../data/types';
import { dirRoute, srcPath } from '../../../lib/paths';
import { externalLinkAttrs } from '../../../lib/links';
import { SITE } from '../../../config';
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
const qualityReport = quality.ok ? quality.value : null;
const qualityCats = INSPECTIONS_PAGE.categories[lang];
const qualitySparks =
--- src/lib/quality.spec.ts (first 60 lines of 13062 bytes) ---
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { INSPECTIONS_PAGE } from '../data/content';
import type { QualityHistoryEntry, QualityReport } from '../data/types';
import qualityJson from '../data/quality.json';
import lighthouserc from '../../lighthouserc.json';
import {
  formatScore,
  gaugeBadgeHtml,
  inspectionVerdict,
  itePlaqueLabel,
  mergeHistory,
  parseQuality,
  plaqueText,
  sparklinePath,
  sparklineSvgHtml,
  VERDICT_THRESHOLDS,
} from './quality';
import { LOCALES } from './i18n';

const AUDIT: QualityReport = {
  generatedAt: '2026-09-20T08:00:00+02:00',
  commit: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
  lighthouse: { performance: 0.98, accessibility: 1, bestPractices: 0.96, seo: 1 },
  history: [
    { date: '2026-09-20', scores: { performance: 0.98, accessibility: 1, bestPractices: 0.96, seo: 1 } },
  ],
  tests: { unit: { total: 185, passed: 185 }, e2e: { total: 130, passed: 130 } },
  repo: { pagesGenerated: 65, bundleKb: 12, deps: { prod: 2, dev: 5 } },
};

function without(report: QualityReport, key: keyof QualityReport): Record<string, unknown> {
  const clone: Record<string, unknown> = { ...report };
  delete clone[key];
  return clone;
}

describe('parseQuality', () => {
  it('accepts a fully valid report', () => {
    expect(parseQuality(AUDIT)).toEqual({ ok: true, value: AUDIT });
  });

  it('rejects a non-object root as bad-shape', () => {
    expect(parseQuality(null)).toEqual({ ok: false, error: { kind: 'bad-shape', field: 'root' } });
    expect(parseQuality('nope')).toEqual({ ok: false, error: { kind: 'bad-shape', field: 'root' } });
    expect(parseQuality([AUDIT])).toEqual({ ok: false, error: { kind: 'bad-shape', field: 'root' } });
  });

  it('names a missing top-level field', () => {
    expect(parseQuality(without(AUDIT, 'generatedAt'))).toEqual({
      ok: false,
      error: { kind: 'missing-field', field: 'generatedAt' },
    });
    expect(parseQuality(without(AUDIT, 'lighthouse'))).toEqual({
      ok: false,
      error: { kind: 'missing-field', field: 'lighthouse' },
    });
    expect(parseQuality(without(AUDIT, 'history'))).toEqual({
      ok: false,
      error: { kind: 'missing-field', field: 'history' },
--- tests/projects.spec.ts (first 60 lines of 12812 bytes) ---
import { expect, test } from '@playwright/test';
import { PROJECTS, TIER_ORDER, tierProjects, WORK } from '../src/data/content';
import type { Locale } from '../src/lib/i18n';

const ROUTES = ['/en/projects/', '/es/projects/', '/ca/projects/'] as const;

const EXPECTED: Record<
  (typeof ROUTES)[number],
  {
    lang: Locale;
    title: string;
    crumbHome: string;
    sub: string;
    summary: string;
    all: string;
    initialStatus: string;
    oneStatus: string;
    twoStatus: string;
    emptyStatus: string;
    github: string;
  }
> = {
  '/en/projects/': {
    lang: 'en',
    title: 'Projects — Jordimp & Co.',
    crumbHome: 'Home',
    sub: '11 PROJECTS · 3 TIERS · FILTER BY STACK',
    summary: 'FILTER BY STACK (42)',
    all: 'All',
    initialStatus: '11 PROJECTS ON SHOW',
    oneStatus: '1 PROJECT ON SHOW',
    twoStatus: '2 PROJECTS ON SHOW',
    emptyStatus: 'NO PROJECTS MATCH THAT COMBINATION — LOOSEN A FILTER',
    github: 'View on GitHub',
  },
  '/es/projects/': {
    lang: 'es',
    title: 'Proyectos — Jordimp & Co.',
    crumbHome: 'Inicio',
    sub: '11 PROYECTOS · 3 NIVELES · FILTRA POR STACK',
    summary: 'FILTRA POR STACK (42)',
    all: 'Todos',
    initialStatus: '11 PROYECTOS A LA VISTA',
    oneStatus: '1 PROYECTO A LA VISTA',
    twoStatus: '2 PROYECTOS A LA VISTA',
    emptyStatus: 'NINGÚN PROYECTO COINCIDE CON ESA COMBINACIÓN — QUITA ALGÚN FILTRO',
    github: 'Ver en GitHub',
  },
  '/ca/projects/': {
    lang: 'ca',
    title: 'Projectes — Jordimp & Co.',
    crumbHome: 'Inici',
    sub: '11 PROJECTES · 3 NIVELLS · FILTRA PER STACK',
    summary: 'FILTRA PER STACK (42)',
    all: 'Tots',
    initialStatus: '11 PROJECTES A LA VISTA',
    oneStatus: '1 PROJECTE A LA VISTA',
    twoStatus: '2 PROJECTES A LA VISTA',
    emptyStatus: 'CAP PROJECTE COINCIDEIX AMB AQUESTA COMBINACIÓ — TREU ALGUN FILTRE',
    github: 'Veure a GitHub',

Write ONLY the plan (the three sections). No prose outside them.