FILES  
src/config.ts  
src/data/content.ts  
src/lib/llms.ts  
src/lib/llms-endpoint.ts  
src/lib/seo.ts  
tests/departments.spec.ts  
tests/home.spec.ts  
src/pages/llms.txt.ts  
src/pages/llms-full.txt.ts  

TASKS  
T1: Define CONTACT_EMAIL in src/config.ts and link SITE.email references  
    depends_on: (none)  
    refs: R7, R2, R3, R4, R5  
T2: Update FooterDesk pill href to mailto:hello@jordimp.net in footer components  
    depends_on: T1  
    refs: R2  
T3: Set contact-row email value and copy button data-copy in front-desk department page  
    depends_on: T1  
    refs: R3  
T4: Configure Person JSON-LD email property to mailto:hello@jordimp.net  
    depends_on: T1  
    refs: R4  
T5: Update llms.txt and llms-full.txt endpoints to emit hello@jordimp.net  
    depends_on: T1  
    refs: R5  
T6: Verify no occurrence of gmail.com or hello@jordimp.net in source or output files  
    depends_on: T1  
    refs: R1  
T7: Validate contact-email feature is blocked until deliverability evidence exists  
    depends_on: (none)  
    refs: R6  
T8: Record provider and tier for free inbox forwarding in progress document  
    depends_on: T1  
    refs: R8  

GATES  
- qa:content — runs `rg -n "gmail" src dist` and verifies no matches; checks visible text in all `dist/**/*.html` for `gmail.com`  
- qa:contact-email-deliverable — confirms MX/SPF records exist for jordimp.net and test message received, with evidence in `harness/progress/impl_contact-email.md`  
- manual-review — leader reviews `harness/progress/impl_contact-email.md` to confirm provider, tier, and deliverability proof are present and valid