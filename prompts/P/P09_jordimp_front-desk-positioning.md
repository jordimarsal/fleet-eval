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
R1: The system shall set `HOME.kicker` to exactly `SENIOR BACKEND ENGINEER — SYSTEMS YOU CAN AUDIT` (en), `INGENIERO BACKEND SENIOR — SISTEMAS QUE SE PUEDEN AUDITAR` (es) and `ENGINYER BACKEND SÈNIOR — SISTEMES QUE ES PODEN AUDITAR` (ca).

R2: The system shall set `HOME.h1` to `One company. One engineer. <mark>Specs before code.</mark>` (en), `Una empresa. Un ingeniero. <mark>Specs antes que código.</mark>` (es) and `Una empresa. Un enginyer. <mark>Specs abans de codi.</mark>` (ca), preserving the single `<mark>` element in every locale.

R3: The system shall set `HOME.stand` to `Jordimp & Co. is the working name of one engineer: backend systems, event pipelines and applied AI, designed, built and audited by the same pair of hands since <b>2017</b>. Currently inside a telco platform team. Walk-ins: roles, repos, or a short spec-first engagement.` (en), its faithful Spanish translation `Jordimp & Co. es el nombre de trabajo de un solo ingeniero: sistemas backend, pipelines de eventos e IA aplicada, diseñados, construidos y auditados por el mismo par de manos desde <b>2017</b>. Ahora, dentro de un equipo de plataforma telco. Entrada libre: roles, repos o un encargo corto con spec primero.` (es) and the MILLORES §2 Catalan text adapted to the markup `Jordimp & Co. és el nom de feina d’un sol enginyer: sistemes backend, pipelines d’esdeveniments i IA aplicada, dissenyats, construïts i auditats pel mateix parell de mans des del <b>2017</b>. Ara, dins d’un equip de plataforma telco. Entrada lliure: rols, repos, o un encàrrec curt amb spec primer.` (ca) — each preserving the `<b>2017</b>` element.

R4: The system shall expose a new typed `offer` block on `FrontdeskPageContent` (`src/data/types.ts`) whose English strings are exactly:  - `offer.openTitle.en = 'Open for'` - `offer.openItems.en = ['Senior / staff backend roles — platform, events, or applied AI with measurable retrieval.', 'Short spec-first engagements (4–8 weeks). If it can’t be written down, it doesn’t start.', 'Questions about a floor or a repo. No tracking, no funnel.']` - `offer.notOpenTitle.en = 'Not open for'` - `offer.notOpenItems.en = ['Vibe-coded MVPs, “add ChatGPT to our app”, or unbounded retainers.']` - `offer.firmLine.en = 'Jordimp & Co. is how the work is done — currently inside a telco platform team, not a staffing firm.'` - `offer.howLine.en = 'How it works — 01 Brief · 02 Spec · 03 Build (tests first) · 04 Audit.'` - `offer.deskLine.en = 'Desk attended in English, Español or Català.'`  with `openTitle`, `notOpenTitle`, `firmLine`, `howLine`, `deskLine` localized and non-empty in `es` and `ca`, and `openItems`/`notOpenItems` holding the same number of non-empty items in all three locales (3 open items, 1 not-open item).

R5: The system shall set `FRONTDESK_PAGE.cta` to exactly `WALK-INS WELCOME — ROLE, REPO OR A SPEC-FIRST ENGAGEMENT.` (en), `ENTRADA LIBRE — ROL, REPO O ENCARGO CON SPEC.` (es) and `ENTRADA LLIURE — ROL, REPO O ENCÀRREC AMB SPEC.` (ca).

R6: The system shall set `DEPTS.frontdesk.line` to exactly `WALK-INS WELCOME — ROLES, REPOS OR A SPEC-FIRST ENGAGEMENT.` (en), `ENTRADA LIBRE — ROLES, REPOS O UN ENCARGO CON SPEC PRIMERO.` (es) and `ENTRADA LLIURE — ROLS, REPOS O UN ENCÀRREC AMB SPEC PRIMER.` (ca).

R7: The system shall set `DEPTS.frontdesk.intro` to the offer (not a biography), exactly `The desk takes three things: senior or staff backend roles, short spec-first engagements, and questions about a floor or a repo. Bring the problem in your own words — if it can’t be written down, it doesn’t start.` (en), `El mostrador acepta tres cosas: roles backend senior o staff, encargos cortos con spec primero y preguntas sobre una planta o un repo. Trae el problema con tus palabras — si no se puede escribir, no se empieza.` (es) and `El mostrador accepta tres coses: rols backend sènior o staff, encàrrecs curts amb spec primer i preguntes sobre una planta o un repo. Porta el problema amb les teves paraules — si no es pot escriure, no comença.` (ca).

R8: The system shall set `FOOTER.line` to exactly `Jordimp & Co. is the working name of one engineer — currently inside a telco platform team. Walk-ins: roles, repos, or a short spec-first engagement.` (en), `Jordimp & Co. es el nombre de trabajo de un solo ingeniero — ahora dentro de un equipo de plataforma telco. Entrada libre: roles, repos o un encargo corto con spec primero.` (es) and `Jordimp & Co. és el nom de feina d’un sol enginyer — ara dins d’un equip de plataforma telco. Entrada lliure: rols, repos o un encàrrec curt amb spec primer.` (ca).

R9: The system shall set `PAGES.home.description` to the plain-text form of R3 — no `<b>`/`<mark>` markup — exactly `Jordimp & Co. is the working name of one engineer: backend systems, event pipelines and applied AI, designed, built and audited by the same pair of hands since 2017. Currently inside a telco platform team. Walk-ins: roles, repos, or a short spec-first engagement.` (en), its faithful Spanish translation (es) and the MILLORES §2 Catalan translation (ca).

R10: The system shall set `PAGES.frontdesk.description` to exactly `Walk-ins welcome: senior or staff backend roles, short spec-first engagements, and questions about a floor or a repo — no tracking, no funnel. Jordimp & Co. is how the work is done, not a staffing firm.` (en), with faithful `es` and `ca` translations.

R11: The system shall append the conflict-of-interest line `Personal study of the Open Gateway telemetry problem. Not Telefónica code. Not production traffic.` to `DEPTS.telemetry.intro.en` (preceded by a single space so the field ends with that exact sentence), and its localized equivalents to the `es` and `ca` fields — so the rendered telemetry intro and the llms endpoints carry the disclaimer.

R12: The system shall not change the four `FRONTDESK_PAGE.how` steps (the `01 — BRIEF` … `04 — AUDIT` `{k,v}` pairs) in any locale.

R13: The system shall not change the contact email: `SITE.email` in `src/data/content.ts` and the `email` constant in `src/config.ts` both remain `jordi.marsal@gmail.com`.

R14: WHEN the Front Desk department page renders in any locale, the system shall render the `offer` block — the CTA tagline, the `openTitle` heading, each `openItems` item, the `notOpenTitle` heading, each `notOpenItems` item, and `firmLine`/`howLine`/`deskLine` — with the localized strings from R4 and R5.

R15: WHEN visible copy changes, the system shall regenerate the committed parity oracle (`tests/fixtures/parity.json`) from the built site with `npm run build && node scripts/distill-parity.mjs`, and the resulting `git diff` shall touch only the `title`/`description`/`h1`/`mainText` of the three home routes, the three Front Desk routes, the three Telemetry routes and the splash `description` — with `_meta.counts` unchanged at `{ "localeRoutes": 63, "pages": 65 }`.

R16: WHEN `llms.txt` and `llms-full.txt` are generated, the system shall emit the updated Front Desk `line`/`intro` and the updated Telemetry `intro` from `src/data/content.ts`, with the committed llms unit snapshot updated to match.

R17: The system shall not modify `src/styles/site.css` or any other stylesheet — the offer block is rendered with the existing `.section`, `.section-title`, `.dept-line`, `.prose`, `.oncall` classes.

--- FEATURE TITLE ---
Merge feature/f11-front-desk-positioning: reposition positioning copy (F11)

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
--- src/data/content.ts (first 60 lines of 91361 bytes) ---
import type {
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
    es: 'Saltar al contenido',
    ca: 'Salta al contingut',
--- src/styles/site.css (first 60 lines of 44315 bytes) ---
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
--- tests/departments.spec.ts (first 60 lines of 18746 bytes) ---
import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import {
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

--- tests/smoke.spec.ts (first 60 lines of 15769 bytes) ---
import { readFileSync } from 'node:fs';
import { expect, test, type ConsoleMessage, type Page } from '@playwright/test';
import { FLOOR_ORDER, PAGES, PROJECTS } from '../src/data/content';

const LOCALES = ['en', 'es', 'ca'] as const;
type Locale = (typeof LOCALES)[number];

const STATIC_ROUTES = ['', 'cv', 'projects'];
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
--- src/pages/[lang]/departments/[dept].astro (first 60 lines of 12620 bytes) ---
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
  qualityReport && qualityReport.history.length >= 2
--- tests/projects.spec.ts (first 60 lines of 11199 bytes) ---
import { expect, test } from '@playwright/test';
import { PROJECTS } from '../src/data/content';

const ROUTES = ['/en/projects/', '/es/projects/', '/ca/projects/'] as const;

const EXPECTED: Record<
  (typeof ROUTES)[number],
  {
    lang: string;
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
    sub: '11 PROJECTS · FILTER BY STACK',
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
    sub: '11 PROYECTOS · FILTRA POR STACK',
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
    sub: '11 PROJECTES · FILTRA PER STACK',
    summary: 'FILTRA PER STACK (42)',
    all: 'Tots',
    initialStatus: '11 PROJECTES A LA VISTA',
    oneStatus: '1 PROJECTE A LA VISTA',
    twoStatus: '2 PROJECTES A LA VISTA',
    emptyStatus: 'CAP PROJECTE COINCIDEIX AMB AQUESTA COMBINACIÓ — TREU ALGUN FILTRE',
    github: 'Veure a GitHub',
  },
--- src/lib/quality.ts (first 60 lines of 10350 bytes) ---
import type { Locale } from './i18n';
import type {
  QualityError,
  QualityHistoryEntry,
  QualityReport,
  QualityResult,
  QualityScores,
} from '../data/types';
// Explicit .ts extension: the zero-dep collector adapter loads this module with
// Node type-stripping, which does not resolve extensionless specifiers.
import { INSPECTIONS_PAGE } from '../data/content.ts';

const ESCAPES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

const esc = (value: string): string =>
  value.replace(/[&<>"']/g, (char) => ESCAPES[char] ?? char);

export interface VerdictThresholds {
  readonly performance: number;
  readonly accessibility: number;
  readonly bestPractices: number;
  readonly seo: number;
}

export const VERDICT_THRESHOLDS: VerdictThresholds = {
  performance: 0.9,
  accessibility: 0.95,
  bestPractices: 0.95,
  seo: 0.95,
};

export const HISTORY_CAP = 30;

export const CATEGORY_KEYS = ['performance', 'accessibility', 'bestPractices', 'seo'] as const;

export type CategoryKey = (typeof CATEGORY_KEYS)[number];

export function formatScore(score: number): string {
  return String(Math.round(score * 100));
}

export function sparklinePath(
  values: readonly number[],
  width: number,
  height: number,
  min?: number,
  max?: number,
): string {
  if (values.length < 2) return '';
  const lo = min ?? Math.min(...values);
  const hi = max ?? Math.max(...values);
  const range = hi - lo;
  const coord = (value: number): number => Math.round(value * 100) / 100;
  return values

Write ONLY the plan (the three sections). No prose outside them.