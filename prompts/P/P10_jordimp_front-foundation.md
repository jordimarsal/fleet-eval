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
R1: The system shall type-check under the strict TypeScript configuration (`tsconfig.json` extends `astro/tsconfigs/strict`) with `npm run check` reporting 0 errors and 0 warnings.  Verification: `grep -q 'astro/tsconfigs/strict' tsconfig.json && npm run check`

R2: When `npm run build` runs, the system shall exit 0 and validate every content-collection entry against its Zod schema before emitting pages.  Verification: `npm run build && test -d dist/en` — negative check: removing a required field from any `src/content/projects/*.json` makes the build fail with a Zod error naming the file.

R3: When the build completes, the system shall emit `dist/en/index.html`, `dist/es/index.html`, `dist/ca/index.html`, and a `dist/index.html` that redirects to `/en/` (meta refresh, `noindex`).  Verification: `npm run build && ls dist/en/index.html dist/es/index.html dist/ca/index.html && grep -q 'url=/en/' dist/index.html`

R4: The system shall not emit any HTML page outside the locale-prefixed routes, except the root redirect page.  Verification: `find dist -name '*.html' ! -path 'dist/en/*' ! -path 'dist/es/*' ! -path 'dist/ca/*'` → exactly `dist/index.html`.

R5: The system shall define its design tokens in `src/styles/tokens.css` with the locked values: fonts Inter Variable / JetBrains Mono, the spacing/radius/container/prose scale, and the exact dark and light palette hex values (dark `--bg #0b1220`, `--accent #2dd4bf`; light `--accent #0d9488`).  Verification: `grep -q '#0b1220' src/styles/tokens.css && grep -q '#2dd4bf' src/styles/tokens.css && grep -q '#0d9488' src/styles/tokens.css && grep -q "'Inter Variable'" src/styles/tokens.css`

R6: The system shall render every foundation page through `BaseLayout`, with `html[lang]` equal to the page locale and slots for logo, nav, actions, default content, and footer.  Verification: `for l in en es ca; do grep -o "<html lang=\"$l\"" dist/$l/projects/index.html; done` → one match per locale. (The root `dist/{lang}/index.html` placeholder from T1 is a scaffold artifact scheduled for replacement in F2; it does not go through `BaseLayout`.)

R7: Before first paint, the system shall set `data-theme` on `<html>` from `localStorage['theme']`, falling back to the `prefers-color-scheme` preference, via an inline head script that ships as-is (no bundled framework code) on every page rendered through `BaseLayout`.  Verification: `grep -F "localStorage.getItem('theme')" dist/en/projects/index.html` — the inline script sits in `<head>` before any bundled script. (Vite inlines page scripts into the built HTML — `dist/_astro/` holds only fonts + CSS.)

R8: While `localStorage['theme']` holds a stored value, the system shall apply that stored value as the initial theme instead of the system preference on every page rendered through `BaseLayout`.  Verification: `grep -F "matchMedia('(prefers-color-scheme: light)')" dist/en/projects/index.html` — the inlined head script implements `stored ?? (matchMedia(...))`.

R9: When the theme toggle is clicked, the system shall switch `data-theme` between `dark` and `light` and persist the new value to `localStorage['theme']`.  Verification: `grep -rlF 'document.getElementById("theme-toggle")' dist/ | wc -l` → 36 and `grep -rlF 'localStorage.setItem(t,e)' dist/ | wc -l` → 36 (the toggle script is inlined into each BaseLayout page's HTML — `dist/_astro/` holds only fonts + CSS — and esbuild hoisted the `'theme'` key into a variable). Toggle rendered via `BaseLayout` since commit `531ed92`.

R10: When the requested locale has no value for a localized field, the system shall return the `en` value (`L()` fallback).  Verification: `npx vitest run` — `src/lib/i18n.spec.ts` › "falls back to en for a missing locale".

R11: The `ui` dictionary shall declare exactly the same key set (`UiKey`) for `en`, `es`, and `ca`, with no empty string values.  Verification: `npm run check` (compile-time `Record<UiKey, string>` on `es`/`ca`) plus `npx vitest run` (runtime key-parity and non-empty tests).

R12: Every foundation page that includes `LocaleSwitcher` shall render one link per locale to the same page path under `/{locale}/`, each carrying `hreflang`, with `aria-current="true"` on the active locale.  Verification: `grep -o 'hreflang="' dist/en/projects/index.html | wc -l` → 3 (minified single-line HTML — use `grep -o … | wc -l`, not `grep -c`), and `grep -q 'aria-current="true"' dist/en/projects/index.html`.

R13: The system shall declare typed Astro content collections (`projects`, `experience`, `skills`) whose Zod schemas validate at build time, with a `localized()` helper requiring an `en`, `es`, and `ca` value for every localized field.  Verification: `npm run build` green — negative check: deleting the `es` key of a localized field in any content JSON fails the build.

R14: The system shall ship exactly 11 project entries: 5 with `featured: true` and 6 with `featured: false`.  Verification: `ls src/content/projects/*.json | wc -l` → 11; `grep -l '"featured": true' src/content/projects/*.json | wc -l` → 5.

R15: For each locale, the system shall emit a projects index (`dist/{lang}/projects/index.html`) rendering all 11 projects in a featured section followed by a secondary section, sorted featured first, then year descending, then name ascending.  Verification: `grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html | wc -l` → 11 cards (minified single-line HTML — `grep -o … | wc -l`, not `grep -c`; the plain prefix `href="/en/projects/` also matches the index's own nav link, giving 12); ordering checked with `grep -o 'href="/en/projects/[a-z0-9-]*/"' dist/en/projects/index.html` (featured slugs appear before secondary ones).

R16: The projects index shall render one filter button per distinct stack tag (sorted alphabetically) plus an `All` reset button, each with an `aria-pressed` state.  Verification: `jq -r '.stack[]' src/content/projects/*.json | sort -u | wc -l` → 42 distinct stacks; `grep -o 'data-stack=' dist/en/projects/index.html | wc -l` → 53 = 42 filter buttons + 11 cards, one `data-stack=` each (minified single-line HTML — `grep -o … | wc -l`, not `grep -c`), and `grep -q 'data-reset' dist/en/projects/index.html`.

R17: When a stack filter button is toggled, the system shall update the visibility of every project card and the `aria-pressed` state of every filter button to reflect the set of active tags.  Verification: extract the module script inlined into `dist/en/projects/index.html` (Vite inlines page scripts into the HTML — `dist/_astro/` holds only fonts + CSS — and esbuild minifies identifiers): the apply function sets card visibility and button `aria-pressed` together, e.g. `grep -oF 'e.hidden=t.size>0&&!s.some(d=>t.has(d))' dist/en/projects/index.html` and `grep -oF 'setAttribute("aria-pressed",String(t.has(e.dataset.stack??"")))' dist/en/projects/index.html`, each → 1 match.

R18: When the reset (`All`) button is clicked, the system shall show every project card and mark the reset as the only pressed filter.  Verification: `grep -oF 't.clear(),o()' dist/en/projects/index.html` → 1 match — the reset handler inlined in the page clears the active tag set and reapplies (identifiers as minified by esbuild).

R19: For every project and locale, the system shall emit `dist/{lang}/projects/{id}/index.html` (id = JSON filename slug) rendering the project name, year, localized summary, problem, highlights, stack chips, metrics, and a repository link whose text is the `links.github` URL path.  Verification: `ls dist/en/projects | wc -l` → 12 (11 dirs + `index.html`); `grep -q 'github.com/jordimarsal/kafka-adapter-telemetry' dist/en/projects/kafka-adapter-telemetry/index.html` and `grep -q '>Problem<' dist/en/projects/kafka-adapter-telemetry/index.html`.

R20: Every foundation page shall render `<title>`, `<meta name="description">`, and `<link rel="canonical">` pointing at `https://jordimp.net/{lang}/{path}`.  Verification: `grep -q 'rel="canonical" href="https://jordimp.net/en/projects/"' dist/en/projects/index.html`.

R21: The system shall not ship any built page containing the owner's phone number.  Verification: `! grep -rq '609 940 649' dist/` — plus `npx vitest run` bans any 9-digit run inside `ui` dictionary strings.

--- FEATURE TITLE ---
docs(harness): F1 front-foundation spec (spec_ready) + feature list

--- REPOSITORY FILE TREE (before implementation) ---
.gitignore
.opencode/agent/implementer.md
.opencode/agent/leader.md
.opencode/agent/reviewer.md
.opencode/agent/spec-author.md
.opencode/skill/wekan-tasks/SKILL.md
.vscode/extensions.json
.vscode/launch.json
AGENTS.md
README.md
astro.config.mjs
docs/architecture.md
docs/conventions.md
docs/iteration-protocol.md
docs/specs.md
docs/superpowers/plans/2026-09-16-portfolio-phase0-1-front.md
docs/superpowers/specs/2026-09-16-portfolio-web-design.md
docs/verification.md
harness/CHECKPOINTS.md
harness/feature_list.json
harness/init.sh
harness/progress/current.md
harness/progress/history.md
harness/tools/audit-security.sh
harness/tools/check-traceability.py
harness/tools/validate-feature-list.py
harness/wekan.json
opencode.json
package.json
src/components/LocaleSwitcher.astro
src/components/Monogram.astro
src/components/ProjectCard.astro
src/components/SEO.astro
src/components/ThemeToggle.astro
src/config.ts
src/content.config.ts
src/content/projects/bible-text-analysis.json
src/content/projects/codebaserag.json
src/content/projects/harness-standard.json
src/content/projects/interview-simulator.json
src/content/projects/kafka-adapter-telemetry.json
src/content/projects/mcp-transparent-png.json
src/content/projects/md-mermaid-pdf.json
src/content/projects/product-offers.json
src/content/projects/redis-toolkit.json
src/content/projects/rustcut.json
src/content/projects/spring-boot-casino.json
src/env.d.ts
src/i18n/ui.ts
src/layouts/BaseLayout.astro
src/lib/i18n.spec.ts
src/lib/i18n.ts
src/pages/[lang]/index.astro
src/pages/[lang]/projects/[slug].astro
src/pages/[lang]/projects/index.astro
src/pages/index.astro
src/styles/global.css
src/styles/tokens.css
tsconfig.json
vitest.config.ts

--- KEY SOURCE FILES (before implementation, excerpts) ---
--- harness/tools/audit-security.sh (first 60 lines of 8940 bytes) ---
#!/usr/bin/env bash
# audit-security.sh — SAST + dependency scan for the security-audit module.
#
# Runs the stack-appropriate tools that are available and degrades to
# checklist-only when they are not (§6.3). The installer never runs this script;
# a non-zero exit means HIGH findings and the reviewer must reject approval.
#
# Usage: bash harness/tools/audit-security.sh [--stack=<stack>]
# Exit codes: 0 = no HIGH findings (or checklist-only), 1 = HIGH findings, 2 = usage error

set -uo pipefail

JSON=0
STACK=""
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --stack=*) STACK="${arg#--stack=}" ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [ -z "$STACK" ]; then
  if [ -f "tsconfig.json" ]; then STACK="typescript"
  elif [ -f "package.json" ]; then STACK="node"
  elif [ -f "build.gradle" ] && { [ -f "AndroidManifest.xml" ] || [ -f "app/src/main/AndroidManifest.xml" ]; }; then STACK="android"
  elif [ -f "build.gradle" ] || [ -f "pom.xml" ]; then STACK="java"
  elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then STACK="python"
  elif [ -f "Cargo.toml" ]; then STACK="rust"
  else STACK="generic"
  fi
fi

REPORT="$(mktemp)"
trap 'rm -f "$REPORT"' EXIT
HIGH=0
SKIPPED=()

if [ "$JSON" -eq 0 ]; then
  echo "# Security Audit Report (stack: $STACK)"
  echo ""
fi

FINDINGS_JSON="[]"
MODE="automated"

json_escape() {  # json_escape <string> — quote for embedding in JSON
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' '
}

extract_bandit_json() {  # <report-file-with-bandit-json> → findings array fragment
  python3 - "$1" <<'PYEOF' 2>/dev/null || true
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("[]")
    raise SystemExit(0)
out = []
for r in d.get("results", []):
--- harness/tools/check-traceability.py (first 60 lines of 5558 bytes) ---
#!/usr/bin/env python3
"""Check requirement traceability for harness specs (Protocol v1).

For each feature with a spec (harness/specs/<name>/requirements.md), collects
the R<n> identifiers, merges the traceability tables from every
harness/progress/impl_*.md, and verifies:
  1. every R<n> appears in at least one table row;
  2. every test identifier referenced by a row exists literally under tests/
     (file name or file content match).

Per Protocol §5, requirements whose table Status is not "done" are reported
as unresolved (they do not create gaps).

Usage:
  check-traceability.py --all [--json] [root]
  check-traceability.py --feature NAME [--json] [root]

Exit codes: 0 covered, 1 gaps, 2 usage error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQ_RE = re.compile(r"\bR(\d+)\b")
ROW_RE = re.compile(r"^\|\s*(R\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|")


def find_requirements(root: Path, feature: str) -> set[str]:
    req_file = root / "harness" / "specs" / feature / "requirements.md"
    if not req_file.is_file():
        return set()
    return {f"R{m}" for m in REQ_RE.findall(req_file.read_text(encoding="utf-8"))}


def collect_tables(root: Path) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Merge every impl_*.md table into {requirement: [test identifiers]} plus status."""
    merged: dict[str, list[str]] = {}
    statuses: dict[str, str] = {}
    progress = root / "harness" / "progress"
    if not progress.is_dir():
        return merged, statuses
    for impl in sorted(progress.glob("impl_*.md")):
        for line in impl.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if m is None:
                continue
            req = m.group(1)
            tests = [t for t in re.split(r"[,\s]+", m.group(2).strip()) if t]
            # first-seen row wins if a requirement appears in multiple tables
            statuses.setdefault(req, m.group(4).strip())
            merged.setdefault(req, [])
            for t in tests:
                if t not in merged[req]:
                    merged[req].append(t)
    return merged, statuses

--- harness/tools/validate-feature-list.py (first 60 lines of 5223 bytes) ---
#!/usr/bin/env python3
"""Validate a harness feature_list.json against Protocol v1 rules.

The JSON Schema (templates/feature_list.schema.json) is the documented
contract; this script enforces the same rules with the stdlib only — no
jsonschema dependency on installed projects.

Usage: validate-feature-list.py [--json] <feature-list.json>
Exit codes: 0 valid, 1 invalid, 2 usage error.
"""

from __future__ import annotations

import json
import re
import sys

STATUSES = ("pending", "spec_ready", "in_progress", "blocked", "done")
AUDIT_LEVELS = ("basic", "standard", "strict")
NAME_RE = re.compile(r"^[a-z0-9_]+$")


def main(argv: list[str]) -> int:
    as_json = False
    path: str | None = None
    for a in argv:
        if a == "--json":
            as_json = True
        elif a.startswith("-"):
            print(f"unknown argument: {a}", file=sys.stderr)
            return 2
        else:
            if path is not None:
                print("usage: validate-feature-list.py [--json] <feature-list.json>", file=sys.stderr)
                return 2
            path = a
    if path is None:
        print("usage: validate-feature-list.py [--json] <feature-list.json>", file=sys.stderr)
        return 2

    errors: list[dict[str, str]] = []

    def err(path_in_doc: str, code: str, message: str) -> None:
        errors.append({"path": path_in_doc, "code": code, "message": message})

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        err("", "invalid_json", f"not valid JSON: {e}")
        data = None

    if isinstance(data, dict):
        project = data.get("project")
        if not isinstance(project, dict):
            err("project", "missing", "project section is required")
        else:
--- src/i18n/ui.ts (first 60 lines of 4881 bytes) ---
import type { Locale } from '../lib/i18n';

const en = {
  'nav.projects': 'Projects',
  'nav.experience': 'Experience',
  'nav.skills': 'Skills',
  'nav.about': 'About',
  'nav.cv': 'CV',
  'hero.role': 'Senior Backend Engineer',
  'hero.tagline': 'Java · Python · AI/LLM',
  'hero.pillar1.title': 'Backend & APIs',
  'hero.pillar1.desc': 'REST APIs and microservices in Java and Python, built to last.',
  'hero.pillar2.title': 'Data & AI',
  'hero.pillar2.desc': 'Data analysis and ML applied to real products, with LLM-powered tooling.',
  'hero.pillar3.title': 'Quality & Craft',
  'hero.pillar3.desc': 'TDD, clean code and CI/CD as daily practice, not an afterthought.',
  'hero.cta.projects': 'View projects',
  'hero.cta.ask': 'Ask my AI',
  'hero.cta.cv': 'Download CV',
  'projects.title': 'Projects',
  'projects.subtitle': 'Selected personal and open source work.',
  'projects.filter.all': 'All',
  'projects.problem': 'Problem',
  'projects.highlights': 'Highlights',
  'projects.metrics': 'Metrics',
  'projects.stack': 'Stack',
  'experience.title': 'Experience',
  'skills.title': 'Skills',
  'about.title': 'About me',
  'about.values.title': 'How I work',
  'cv.title': 'CV',
  'cv.download.en': 'Download CV (English)',
  'cv.download.es': 'Download CV (Spanish)',
  'cv.print': 'Print',
  'footer.builtWith': 'Built with Astro, Java 25 & a local LLM',
  'footer.contact': 'Contact',
  'theme.toggle': 'Toggle theme',
  'notfound.title': 'Page not found',
  'notfound.body': 'The page you are looking for does not exist.',
} as const;

export type UiKey = keyof typeof en;

const es: Record<UiKey, string> = {
  'nav.projects': 'Proyectos',
  'nav.experience': 'Experiencia',
  'nav.skills': 'Habilidades',
  'nav.about': 'Sobre mí',
  'nav.cv': 'CV',
  'hero.role': 'Ingeniero de Software Senior',
  'hero.tagline': 'Java · Python · IA/LLM',
  'hero.pillar1.title': 'Backend y APIs',
  'hero.pillar1.desc': 'APIs REST y microservicios en Java y Python, construidos para durar.',
  'hero.pillar2.title': 'Datos e IA',
  'hero.pillar2.desc': 'Análisis de datos y ML aplicados a productos reales, con herramientas basadas en LLM.',
  'hero.pillar3.title': 'Calidad y oficio',
  'hero.pillar3.desc': 'TDD, código limpio y CI/CD como práctica diaria, no como añadido.',
  'hero.cta.projects': 'Ver proyectos',
  'hero.cta.ask': 'Pregunta a mi IA',
  'hero.cta.cv': 'Descargar CV',
--- harness/init.sh (first 60 lines of 4449 bytes) ---
#!/usr/bin/env bash
# init-verify.sh — Project verification script
#
# This script is copied to harness/init.sh during harness installation.
# Run from the project root: ./harness/init.sh
# Run at session start and before marking any feature as done.

set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }

EXIT_CODE=0

echo "── 1. Checking harness files ──────────────────────────"

# Entry point + tool directory at the project root (claude or opencode)
if [ -f "CLAUDE.md" ]; then
  ok "Exists CLAUDE.md"
  ENTRY_OK=1
elif [ -f "AGENTS.md" ]; then
  ok "Exists AGENTS.md"
  ENTRY_OK=1
else
  fail "Missing entry point: CLAUDE.md or AGENTS.md"
  EXIT_CODE=1
  ENTRY_OK=0
fi

if [ -d ".claude" ] || [ -d ".opencode" ]; then
  ok "Exists .claude/ or .opencode/"
else
  fail "Missing tool directory: .claude/ or .opencode/"
  EXIT_CODE=1
fi

for f in harness/CHECKPOINTS.md harness/feature_list.json harness/progress/current.md docs/architecture.md docs/conventions.md docs/verification.md docs/specs.md; do
  if [ ! -f "$f" ]; then
    fail "Missing base file: $f"
    EXIT_CODE=1
  else
    ok "Exists $f"
  fi
done

if [ -d "harness/specs" ]; then
  ok "Exists harness/specs/"
else
  fail "Missing directory: harness/specs/"
  EXIT_CODE=1
fi

echo ""
echo "── 2. Validating harness/feature_list.json ────────────"

--- src/pages/[lang]/projects/index.astro (first 60 lines of 3866 bytes) ---
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import LocaleSwitcher from '../../../components/LocaleSwitcher.astro';
import ProjectCard from '../../../components/ProjectCard.astro';
import { LOCALES, type Locale } from '../../../lib/i18n';
import { ui } from '../../../i18n/ui';

export async function getStaticPaths() {
  return LOCALES.map((lang) => ({ params: { lang }, props: { lang } }));
}

type Props = { lang: Locale };
const { lang } = Astro.props;
const t = ui[lang];

const projects = await getCollection('projects');
const sorted = [...projects].sort(
  (a, b) =>
    Number(b.data.featured) - Number(a.data.featured) ||
    b.data.year - a.data.year ||
    a.data.name.localeCompare(b.data.name),
);
const featured = sorted.filter((p) => p.data.featured);
const secondary = sorted.filter((p) => !p.data.featured);
const stacks = [...new Set(sorted.flatMap((p) => p.data.stack))].sort((a, b) => a.localeCompare(b));
---
<BaseLayout
  lang={lang}
  title={`${t['projects.title']} — Jordi Marçal Poy`}
  description={t['projects.subtitle']}
  path="projects/"
>
  <LocaleSwitcher slot="actions" {lang} path="projects/" />
  <h1>{t['projects.title']}</h1>
  <p class="muted">{t['projects.subtitle']}</p>
  <div class="stack-filter">
    <button type="button" data-reset aria-pressed="true">{t['projects.filter.all']}</button>
    {stacks.map((s) => (
      <button type="button" data-stack={s} aria-pressed="false">{s}</button>
    ))}
  </div>
  <section class="grid">
    {featured.map((p) => <ProjectCard project={p} {lang} />)}
  </section>
  <section class="grid">
    {secondary.map((p) => <ProjectCard project={p} {lang} />)}
  </section>
</BaseLayout>

<style>
  h1 {
    margin: var(--space-8) 0 var(--space-2);
  }

  .stack-filter {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
    margin: var(--space-4) 0 var(--space-8);
--- src/pages/[lang]/projects/[slug].astro (first 60 lines of 2309 bytes) ---
---
import { getCollection, type CollectionEntry } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import { L, LOCALES, type Locale } from '../../../lib/i18n';
import { ui } from '../../../i18n/ui';

export async function getStaticPaths() {
  const projects = await getCollection('projects');
  return LOCALES.flatMap((lang) =>
    projects.map((project) => ({ params: { lang, slug: project.id }, props: { lang, project } })),
  );
}

type Props = { lang: Locale; project: CollectionEntry<'projects'> };
const { lang, project } = Astro.props;
const d = project.data;
const repo = new URL(d.links.github).pathname.replace(/^\//, '');
---
<BaseLayout
  lang={lang}
  title={`${d.name} — Jordi Marçal Poy`}
  description={L(d.summary, lang)}
  path={`projects/${project.id}/`}
>
  <article class="prose">
    <p class="muted mono">{d.year} · <a href={d.links.github}>{repo}</a></p>
    <h1>{d.name}</h1>
    <p><strong>{L(d.summary, lang)}</strong></p>
    <h2>{ui[lang]['projects.problem']}</h2>
    <p>{L(d.problem, lang)}</p>
    <h2>{ui[lang]['projects.highlights']}</h2>
    <ul>{L(d.highlights, lang).map((h) => <li>{h}</li>)}</ul>
    <h2>{ui[lang]['projects.stack']}</h2>
    <ul class="chips">{d.stack.map((s) => <li class="chip mono">{s}</li>)}</ul>
    <h2>{ui[lang]['projects.metrics']}</h2>
    <dl class="metrics">
      {d.metrics.map((m) => (
        <div>
          <dt class="mono">{m.value}</dt>
          <dd>{m.label}</dd>
        </div>
      ))}
    </dl>
  </article>
</BaseLayout>

<style>
  .prose h1 {
    margin: var(--space-2) 0;
    font-size: 2rem;
  }

  .prose h2 {
    margin: var(--space-8) 0 var(--space-2);
    font-size: 1.25rem;
  }

  .prose > p:first-child {
    margin-top: var(--space-8);
  }
--- src/styles/global.css (first 60 lines of 1474 bytes) ---
@import '@fontsource-variable/inter';
@import '@fontsource/jetbrains-mono/400.css';
@import '@fontsource/jetbrains-mono/600.css';
@import './tokens.css';

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
}

img,
svg {
  display: block;
  max-width: 100%;
}

.container {
  max-width: var(--container);
  margin-inline: auto;
  padding-inline: var(--space-4);
}

.prose {
  max-width: var(--prose);
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.muted {
  color: var(--muted);
}

[hidden] {
  display: none !important;
}

.mono {
  font-family: var(--font-mono);
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

Write ONLY the plan (the three sections). No prose outside them.