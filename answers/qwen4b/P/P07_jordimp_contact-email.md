FILES  
src/config.ts  
src/data/content.ts  
src/lib/llms.spec.ts  
src/lib/llms-endpoint.spec.ts  
tests/departments.spec.ts  
tests/home.spec.ts  

TASKS  
T1: Update CONTACT_EMAIL in src/config.ts and ensure SITE.email references it  
    depends_on: (none)  
    refs: R1, R7  
T2: Modify FooterDesk component to set href to mailto:hello@jordimp.net while preserving localized label  
    depends_on: T1  
    refs: R2  
T3: Adjust front-desk department page to display hello@jordimp.net in contact-row and set copy button data-copy attribute  
    depends_on: T1  
    refs: R3  
T4: Patch personJsonLd email property to use mailto:hello@jordimp.net  
    depends_on: T1  
    refs: R4  
T5: Verify llms.txt and llms-full.txt endpoints emit correct contact text  
    depends_on: T1  
    refs: R5  
T6: Validate that no occurrence of gmail.com or hello@jordimp.net exists in src/, tests/, or dist/ before build  
    depends_on: T1  
    refs: R1, R6, R8  

GATES  
- qa:content gate runs on all source and built HTML files; must return zero matches for "gmail.com" or "hello@jordimp.net"  
- Manual check: `rg -n "hello@jordimp.net" src dist` returns no output  
- Evidence in harness/progress/impl_contact-email.md confirms MX/SPF records are present and test message received  
- Oracle snapshot from src/lib/__snapshots__/llms-endpoint.spec.ts.snap is refreshed with vitest -u and reviewed for address-only change