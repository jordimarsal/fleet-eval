FILES
src/data/content.ts
src/data/types.ts
tests/fixtures/parity.json

TASKS
T1: Implement HOME.kicker localization with exact strings for en, es, ca
    depends_on: (none)
    refs: R1
T2: Implement HOME.h1 localization with exact strings and preserved <mark> markup for all locales
    depends_on: T1
    refs: R2
T3: Implement HOME.stand localization with faithful translations and preserved <b>2017</b> markup
    depends_on: T2
    refs: R3
T4: Add new offer block to FrontdeskPageContent in src/data/types.ts with full English content
    depends_on: (none)
    refs: R4
T5: Localize offer block fields in src/data/content.ts for es and ca
    depends_on: T4
    refs: R4, R5
T6: Set FRONTDESK_PAGE.cta to exact localized strings across locales
    depends_on: T5
    refs: R5
T7: Set DEPTS.frontdesk.line to exact localized strings across locales
    depends_on: T6
    refs: R6
T8: Set DEPTS.frontdesk.intro to exact localized version of the offer text
    depends_on: T7
    refs: R7
T9: Set FOOTER.line to exact localized strings across locales
    depends_on: T8
    refs: R8
T10: Set PAGES.home.description to plain-text form of R3 with correct locale translations
    depends_on: T9
    refs: R9
T11: Append conflict-of-interest line to DEPTS.telemetry.intro.en and its localized equivalents
    depends_on: T10
    refs: R11
T12: Ensure no changes to existing FRONTDESK_PAGE.how steps in any locale
    depends_on: (none)
    refs: R12
T13: Verify SITE.email remains unchanged in both src/data/content.ts and src/config.ts
    depends_on: (none)
    refs: R13
T14: Confirm offer block renders on Front Desk page in all locales via content references
    depends_on: T13
    refs: R14
T15: Regenerate parity.json after content updates using npm run build && node scripts/distill-parity.mjs
    depends_on: T14
    refs: R15
T16: Update llms.txt and llms-full.txt with new Front Desk and Telemetry intro text
    depends_on: T15
    refs: R16
T17: Validate no modifications are made to site.css or other stylesheets
    depends_on: T16
    refs: R17

GATES
- All required strings are present and exactly match the approved requirements in src/data/content.ts  
- The offer block renders correctly on every language version of the Front Desk page  
- Parity.json reflects only changes to title, description, h1, mainText for home, frontdesk, telemetry routes and splash  
- No changes were made to site.css or any stylesheet files  
- SITE.email remains jordi.marsal@gmail.com in both src/data/content.ts and src/config.ts  
- All translations preserve exact markup (e.g., <mark>, <b>) as specified in requirements  
- Playwright tests pass for department pages, home, and front desk routes across all locales  
- Generated llms.txt and llms-full.txt contain updated intro texts from DEPTS.telemetry.intro and DEPTS.frontdesk.line