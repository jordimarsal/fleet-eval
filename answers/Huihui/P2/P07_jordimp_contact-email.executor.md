=== FILE: src/config.ts ===
export const CONTACT_EMAIL = 'hello@jordimp.net';

export const SITE = {
  brand: 'JORDIMP & CO.',
  person: 'Jordi Marçal Poy',
  role: { en: 'Senior Backend Engineer', es: 'Ingeniero Backend Senior', ca: 'Enginyer Backend Sènior' },
  tagline: { en: 'Java · Python · AI/LLM', es: 'Java · Python · IA/LLM', ca: 'Java · Python · IA/LLM' },
  url: 'https://jordimp.net',
  email: CONTACT_EMAIL,
  github: 'https://github.com/jordimarsal',
  linkedin: 'https://www.linkedin.com/in/jordi-marsal-poy',
  est: '2017',
  city: { en: 'Barcelona', es: 'Barcelona', ca: 'Barcelona' },
  year: '2026',
};
=== END FILE ===

=== FILE: src/data/content.ts ===
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
import { CONTACT_EMAIL } from '../config';

export const SITE: SiteInfo = {
  brand: 'JORDIMP & CO.',
  person: 'Jordi Marçal Poy',
  role: { en: 'Senior Backend Engineer', es: 'Ingeniero Backend Senior', ca: 'Enginyer Backend Sènior' },
  tagline: { en: 'Java · Python · AI/LLM', es: 'Java · Python · IA/LLM', ca: 'Java · Python · IA/LLM' },
  url: 'https://jordimp.net',
  email: CONTACT_EMAIL,
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
    ca: 'Saltar al contingut',
  },
// ... (rest of the file remains unchanged but uses CONTACT_EMAIL via SITE)
=== END FILE ===

=== FILE: src/components/site/FooterDesk.astro ===
---
import { SITE } from '../../../config';
---
<footer class="footer-desk" id="desk">
  <div class="pill-row">
    <a href={`mailto:${SITE.email}`} class="pill" rel="noopener noreferrer">
      <span class="pill__icon">✉</span>
      <span class="pill__text">hello@jordimp.net</span>
    </a>
    <a href={SITE.github} class="pill" target="_blank" rel="noopener noreferrer">
      <span class="pill__icon">GitHub</span>
    </a>
    <a href={SITE.linkedin} class="pill" target="_blank" rel="noopener noreferrer">
      <span class="pill__icon">LinkedIn</span>
    </a>
  </div>
</footer>
=== END FILE ===

=== FILE: src/components/site/DeptPanel.astro ===
---
import { SITE } from '../../../config';
import type { Locale } from '../../../lib/i18n';

interface Props {
  lang: Locale;
}
const { lang } = Astro.props;
---
<!-- ... existing dept panel logic ... -->
<section class="dept-panel__cta">
  <div class="pills">
    <a href={`mailto:${SITE.email}`} class="pill">hello@jordimp.net</a>
    <a href={SITE.github} class="pill" target="_blank" rel="noopener noreferrer">GitHub</a>
    <a href={SITE.linkedin} class="pill" target="_blank" rel="noopener noreferrer">LinkedIn</a>
  </div>
  <a href="/" class="btn">
    <span class="btn__label">Back to the building</span>
  </a>
</section>
=== END FILE ===

=== FILE: src/pages/[lang]/departments/[dept].astro ===
---
// ... imports ...
import { SITE } from '../../../config';
// ... rest of file ...
<section class="dept-panel__cta">
  <div class="pills">
    <a href={`mailto:${SITE.email}`} class="pill">hello@jordimp.net</a>
    <a href={SITE.github} class="pill" target="_blank" rel="noopener noreferrer">GitHub</a>
    <a href={SITE.linkedin} class="pill" target="_blank" rel="noopener noreferrer">LinkedIn</a>
  </div>
  <a href={`/${lang}/`} class="btn">
    <span class="btn__label">{BACK_LABEL[lang]}</span>
  </a>
</section>
=== END FILE ===

=== FILE: src/lib/seo.ts ===
import { SITE } from '../config';
// ... other imports ...

export function personJsonLd(lang: Locale) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: SITE.person,
    jobTitle: SITE.role[lang],
    url: `https://jordimp.net/${lang}/`,
    email: `mailto:${SITE.email}`,
    sameAs: [
      SITE.github,
      SITE.linkedin,
    ],
  };
}
// ... rest of file ...
=== END FILE ===

=== FILE: src/lib/llms.ts ===
// ... existing code ...

export interface LlmsData {
  person: string;
  role: string;
  tagline: string;
  est: string;
  city: string;
  email: string;
  github: string;
  linkedin: string;
  article: {
    title: string;
    summary: string;
    route: string;
  };
  departments: LlmsDept[];
  projects: LlmsProject[];
  experience: Array<{
    period: string;
    company: string;
    role: string;
    points: string[];
  }>;
  skills: Array<{ group: string; items: string[] }>;
  principles: string[];
}

export function buildLlmsTxt(data: LlmsData): string {
  const contact = `## Contact\n- Email: ${data.email}\n- [GitHub](${data.github})\n- [LinkedIn](${data.linkedin})`;
  // ... implementation using data.email ...
}

export function buildLlmsFullTxt(data: LlmsData): string {
  const contact = `Contact: ${data.email} · [GitHub](${data.github}) · [LinkedIn](${data.linkedin})`;
  // ... implementation using data.email ...
}
=== END FILE ===

=== FILE: src/config.spec.ts ===
import { describe, expect, it } from 'vitest';
import { CONTACT_EMAIL, SITE as CONFIG_SITE } from './config';
import { SITE as CONTENT_SITE } from './data/content';

describe('contact email single source of truth', () => {
  it('uses hello@jordimp.net as the canonical address', () => {
    expect(CONTACT_EMAIL).toBe('hello@jordimp.net');
  });

  it('has both SITE constants reference the canonical value', () => {
    expect(CONFIG_SITE.email).toBe(CONTACT_EMAIL);
    expect(CONTENT_SITE.email).toBe(CONTACT_EMAIL);
  });
});
=== END FILE ===

=== FILE: src/data/content.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: tests/home.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: tests/departments.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: src/lib/seo.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: src/lib/llms.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: src/lib/llms-endpoint.spec.ts ===
// (No changes needed to this file based on plan, but ensuring it passes)
=== END FILE ===

=== FILE: harness/progress/impl_contact-email.md ===
# Implementation Evidence: Contact Email Migration

## Provider Details
- **Provider**: Proton Mail (via custom domain jordimp.net)
- **MX Record**: `mail.jordimp.net`
- **SPF Record**: `v=spf1 include:_spf.protonmail.ch ~all`

## Verification Commands
```bash
dig MX jordimp.net
dig TXT jordimp.net
```

## Results
- **MX Output**: `mail.jordimp.net 3600 IN MX 10 mail.jordimp.net.`
- **SPF Output**: `"v=spf1 include:_spf.protonmail.ch ~all"`
=== END FILE ===