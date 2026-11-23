Looking at T6, I need to update the LLMs text generation endpoints (`src/lib/llms.ts`) so they use the canonical `CONTACT_EMAIL` from config instead of any hardcoded email literal. Let me examine what's needed based on the tests.

The tests reference `buildLlmsTxt`, `buildLlmsFullTxt`, and types `LlmsData`, `LlmsDept`. The contact block must emit `- Email: hello@jordimp.net` and the full txt header line `Contact: hello@jordimp.net · ...`. Since the data object carries an `email` field, the builders should render it. To satisfy R5 (use canonical email), the data source (`llms.txt` page) should populate `email` from `SITE.email` / `CONTACT_EMAIL`. But T6 scope is specifically the llms lib. Let me check whether the current `llms.ts` exists in repo state — it's referenced by tests but not shown as existing content. I'll create/update it to ensure the email flows through correctly and no gmail literal remains.

Let me look more carefully. The task says "Update LLMs text generation endpoints" with ref R5. The key requirement: the generated llms.txt / llms-full.txt text uses the canonical email. The builders take a `data` param that includes `email`. So the fix is ensuring `buildLlmsTxt`/`buildLlmsFullTxt` use `data.email` (not a hardcoded string). 

Since the file isn't provided in the repo state excerpt, I need to reconstruct it fully based on all test expectations. Let me build it to pass every assertion in both spec files.

=== FILE: src/lib/llms.ts ===
import { SITE } from '../config';

export interface LlmsProjectRef {
  slug: string;
  name: string;
  year: string;
  summary: string;
  stack: readonly string[];
  github: string;
}

export interface LlmsDept {
  code: string;
  name: string;
  line: string;
  intro: string;
  route: string;
  projects: readonly LlmsProjectRef[];
}

export interface LlmsExperienceEntry {
  period: string;
  company: string;
  role: string;
  points: readonly string[];
}

export interface LlmsSkillGroup {
  group: string;
  items: readonly string[];
}

export interface LlmsArticle {
  title: string;
  summary: string;
  route: string;
}

export interface LlmsData {
  person: string;
  role: string;
  tagline: string;
  est: string;
  city: string;
  email: string;
  github: string;
  linkedin: string;
  article: LlmsArticle;
  departments: readonly LlmsDept[];
  projects: readonly LlmsProjectRef[];
  experience: readonly LlmsExperienceEntry[];
  skills: readonly LlmsSkillGroup[];
  principles: readonly string[];
}

const ORIGIN = 'https://jordimp.net';

function dirUrl(path: string): string {
  return `${ORIGIN}/en/${path}`;
}

/**
 * Canonical contact address for the LLMs endpoints. The data object carries an
 * `email` field, but we fall back to the single source of truth so a missing or
 * stale value can never reintroduce a non-canonical literal (R5).
 */
function canonicalEmail(data: LlmsData): string {
  const fromData = typeof data.email === 'string' ? data.email.trim() : '';
  return fromData.length > 0 ? fromData : SITE.email;
}

export function buildLlmsTxt(data: LlmsData): string {
  const email = canonicalEmail(data);
  const lines: string[] = [];

  // Brand header + person blockquote
  lines.push(`# ${SITE.name.replace(/&/g, '&')}`);
  lines.push('');
  lines.push(
    `> ${data.person} — ${data.role} (${data.tagline}). A one-person engineering firm: backend systems, event pipelines and applied AI, designed, built and audited by the same pair of hands since ${data.est}. ${data.city}. Business in English, Español or Català.`,
  );
  lines.push('');

  // Departments
  lines.push('## Departments');
  lines.push('');
  for (const dept of data.departments) {
    lines.push(`- ${dept.code} ${dept.name} — ${dept.line}`);
  }
  lines.push('');

  // Key pages as linked directory URLs
  lines.push('## Pages');
  lines.push('');
  lines.push(
    `- [Home](${dirUrl('en/')}) (also [Español](${dirUrl('es/')}), [Català](${dirUrl('ca/')}))`,
  );
  lines.push(`- [Projects](${dirUrl('projects/')})`);
  lines.push(`- [CV](${dirUrl('cv/')})`);
  for (const dept of data.departments) {
    lines.push(`- [${dept.code} ${dept.name}](${dirUrl(dept.route)})`);
  }
  lines.push(
    `- [Project case pages](${dirUrl('projects/<slug>/')}) — one per project, ${data.projects.length} total`,
  );
  lines.push(
    `- [Writing: ${data.article.title}](${dirUrl(data.article.route)}) — ${data.article.summary}`,
  );
  lines.push('');

  // Contact block
  lines.push('## Contact');
  lines.push('');
  lines.push(`- Email: ${email}`);
  lines.push(`- [GitHub](${data.github})`);
  lines.push(`- [LinkedIn](${data.linkedin})`);
  lines.push('');
  lines.push('Full details in llms-full.txt.');

  return lines.join('\n');
}

export function buildLlmsFullTxt(data: LlmsData): string {
  const email = canonicalEmail(data);
  const lines: string[] = [];

  // Full-reference header + contact line
  lines.push(`# ${SITE.name.replace(/&/g, '&')} — full reference`);
  lines.push('');
  lines.push(`${data.person} — ${data.role} (${data.tagline}).`);
  lines.push('');
  lines.push(
    `Contact: ${email} · [GitHub](${data.github}) · [LinkedIn](${data.linkedin})`,
  );
  lines.push('');

  // The building (departments)
  lines.push('## The building');
  lines.push('');
  for (const dept of data.departments) {
    lines.push(`## ${dept.code} — ${dept.name}`);
    lines.push('');
    lines.push(dept.intro);
    if (dept.projects.length > 0) {
      lines.push('');
      lines.push('Projects:');
      for (const p of dept.projects) {
        lines.push(
          `  - ${p.slug} (${p.year}): ${p.summary} Stack: ${p.stack.join(', ')}. [repo](${p.github})`,
        );
      }
    }
    lines.push('');
  }

  // All repos
  lines.push('## All repos');
  lines.push('');
  for (const p of data.projects) {
    lines.push(`- ${p.name} (${p.year}): ${p.summary} [repo](${p.github})`);
  }
  lines.push('');

  // Career ledger
  lines.push('## Career ledger (Operations, F0)');
  lines.push('');
  for (const entry of data.experience) {
    lines.push(
      `- ${entry.period} — ${entry.company}, ${entry.role}: ${entry.points.join(' ')}`,
    );
  }
  lines.push('');

  // Skills
  lines.push('## Skills (Mezzanine)');
  lines.push('');
  for (const group of data.skills) {
    lines.push(`- ${group.group}: ${group.items.join(', ')}`);
  }
  lines.push('');

  // Working principles
  lines.push('## Working principles (Mezzanine)');
  lines.push('');
  for (const principle of data.principles) {
    lines.push(`- ${principle}`);
  }
  lines.push('');

  // Writing
  lines.push('## Writing');
  lines.push('');
  lines.push(`- [${data.article.title}](${dirUrl(data.article.route)})`);
  lines.push('');

  // Pages
  lines.push('## Pages');
  lines.push('');
  lines.push(
    `- [Home](${dirUrl('en/')}) · [Español](${dirUrl('es/')}) · [Català](${dirUrl('ca/')}) (home, trilingual)`,
  );
  lines.push(`- [Projects](${dirUrl('projects/')}) — all projects with stack filter`);
  lines.push(`- [CV](${dirUrl('cv/')}) — CV summary with PDF downloads`);
  for (const dept of data.departments) {
    const label =
      dept.code === 'M' ? 'Mezzanine' : dept.code === 'B' ? 'Front Desk' : `${dept.name} department page`;
    lines.push(`- [${label}](${dirUrl(dept.route)})`);
  }

  return lines.join('\n');
}
=== END FILE ===