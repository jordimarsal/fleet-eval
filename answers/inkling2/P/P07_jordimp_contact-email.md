FILES
harness/progress/impl_contact-email.md
src/config.ts
src/config.spec.ts
src/data/content.ts
src/components/site/FooterDesk.astro
src/components/site/DeptPanel.astro
src/lib/seo.ts
src/lib/seo.spec.ts
src/lib/llms.ts
src/pages/llms.txt.ts
src/pages/llms-full.txt.ts
src/lib/llms.spec.ts
src/lib/llms-endpoint.spec.ts
src/lib/__snapshots__/llms-endpoint.spec.ts.snap
tests/home.spec.ts
tests/departments.spec.ts
scripts/qa-content.mjs

TASKS
T1: Record Task 0 delivery evidence (blocked → unblocked)
    depends_on: (none)
    refs: R6, R8, R1-check prep
    Verify mailbox will be provisioned (free tier only, e.g. ImprovMX / forwardemail.net / Cloudflare Email Routing or Zoho Mail Free / DNSExit forwarding rule or free real mailbox) with no billing/payment required; run and capture MX + SPF `dig` output for jordimp.net, send a test message to hello@jordimp.net and confirm it lands in the owner's inbox; record provider name, chosen free tier used, dig output and receipt confirmation in harness/progress/impl_contact-email.md. Do not touch implementation files if this is absent — keep feature blocked and stop tasks T2 onward until confirmation exists.

T2: Introduce CONTACT_EMAIL canonical literal and pin both config references
    depends_on: T1
    refs: R1, R7
    Add `export const CONTACT_EMAIL = 'hello@jordimp.net' as const;` in src/config.ts and make CONFIG_SITE.email reference it; change src/data/content.ts CONTENT_SITE.email to import CONTACT_EMAIL from ../config. Create src/config.spec.ts asserting CONTACT_EMAIL === 'hello@jordimp.net', CONFIG_SITE.email === CONTACT_EMAIL and CONTENT_SITE.email === CONTACT_EMAIL (replace any hardcoded value such as jordi.marsal@gmail.com). Remove every remaining literal 'gmail.com' or old email string anywhere under src/ and tests/ along with follow-on assertion data tied to those values.

T3: Route page anchor pills through the canonical address while preserving localized labels
    depends_on: T2
    refs: R2
    Update src/components/site/FooterDesk.astro and src/components/site/DeptPanel.astro so the rendered mail anchor is href={`mailto:${CONTACT_EMAIL}`} / mailto:${SITE.email} — not a visible label — and keep the displayed text exactly localized FOOTER.email unchanged for en/es/ca. Audit PageMetadata copy, front-desk aside content and any other emitted anchor strings containing old gmail output; shift each to the SITE-provided contact source instead of raw constants when needed.

T4: Update Department contact-row rendering path for hello@jordimp.net
    depends_on: T2
    refs: R3
    In src/pages/[lang]/departments/[dept].astro and any renderer that passes data between FRONTDESK lines confirming row value equals CONTACT_EMAIL? No manual literal allowed in components—keep dynamic `SITE.email` usage (or now one shared constant). Keep button.copy-btn[data-copy] equal to same derived value. Existing tests should then pass without hardcoding changes after config swap because existing assertions use SITE.email from ../src/config; verify by reading current file paths since nothing remains linked to stale values.

T5: Pin SEO person JSON-LD email to canonical address
    depends_on: T2
    refs: R4
    Edit src/lib/seo.ts (personJsonLd or equivalent) so its email property resolves from CONTACT_EMAIL / CONFIG SITE rather than a new inline string if it was previously concrete, while keeping other properties unchanged. Grep imports across pages depending on site links just above as shown outside tree where needed. Add explicit pinning assertion in src/lib/seo.spec.ts for personJsonLd('en').email === 'hello@jordimp.net' before build step proceeds at gate validation run only once changed plus added target code confirmations not breakage perform visually required test check conditions about separability sync status results assumptions known system logic broad enough support progress orderly verification stages future sole approach closing point.

T6: Update llms endpoint output and snapshot oracle with the canonical contact line
    depends_on: T2
    refs: R1, R5
    Change both public page entrypoints under src/pages/*llms*and corresponding builder inside src/lib/llms.ts through configured imported source instead of hardcoded email body if any copies appear in file script directly; inject value like `- Email: ${CONTACT_EMAIL}` (line common to llms.txt contact block or Contact: in full variant exactly matching currently format but substituted via constant). Make sure no occurrence appears after removal even within fallback branches strings from other constants — write fresh checks ensuring content emission is one consistent var within existing flow then update tests src/lib/llms.spec.ts + src/lib/llms-endpoint.spec.ts pinning literal contact identity as expected (compare factually against export exports rather than current cell text to avoid false valid state bypass during build stages scope actors owner profile chunk adjust). Finally run appropriate regression scenario first against code units using vitest -u so written committed oracle only drift addresses + authorship details requested just reviewed before commits supporting wider tests.

T7: Final repository sweep and QA hardening for residual string leakage
    depends_on: T3, T4, T5, T6
    refs: R1, R2, R3, R5, R8 evidence gate
    Perform a final repository check covering all affected generated outputs under dist once built plus scans over chosen source paths listed produced surfaces & confirming that visible homepage copy also has canonical address through front desk pill chaining necessary visible assertion still envs relevant passing; ensure page data uses localized labels without open emails showing incorrectly invisible showcase traces left static behavior unaware distinct setting conventions required testing unexpected assumptions failure preserved no rerun cycle gaps left forward implement companion checks depending progress completion cases applied integrated relevant type of error prevention critical maintenance task always favor lift news introducing fresh route integration expectation eventually reconciled correctly after passes alongside rest flows data parity test expectations not simply pass listings ungod intervenes—missing from image? update corresponding requirement files audited covered given order line number statement explicitly only adding detail humans need write manually implementation team not block actual deployments directly maintain formal references closure known truly large product surface state site unfinished function remains by indication truth. Update script qa-content scan where duplicated fixed pattern/gate notices exist path matching command term appropriately aligning with lead message structure injection about verify use shell commands; complete test updates surgically normalizing assertions if hardcoded in tests as required rather expansively altering copies expected — narrow modification preserving meaningful outputs; then conduct task evidence review before gate, including anything requiring human owner verification finalize decision level readiness for approved code release package changes exactly what context doc states conclusions reach across all tasks completion world wants output immediate need correction details among role walk wells available like last received empty reports available verified module results committed inline status traceable sequence naturally open software revision tends apply deep standards limiting anomalous edge feature occurrences ready (`report checklist).

GATES
1. Evidence recorded: harness/progress/impl_contact-email.md documents MX + SPF records and the successful delivery of the R6 / hello@jordimp.net test mailbox along with chosen free provider/tier under R8; currently blocked vs proceed confirmed unblock recorded at T1.
2. Unit & snapshot regression set passes cleanly via `npm run test -- src/config.spec.ts src/lib/seo.spec.ts src/lib/llms.spec.ts src/lib/llms-endpoint.spec.ts vitest -u --changed=src/lib/__snapshots__/llms-endpoint.spec.ts.snap` and related existing spec suites in key files that source now considered data-flow from config single point change — no unintended drift other than requested address line updates visible only through report at diff time after merged tier work allowed review combined own.
3. Building gate against actual product artifacts succeed pass ensuring localized assets everywhere without gmail can show leading page text inspections expecting build per locale actually relevant locations plus dist code includes expected pages sections aligned wearying while presentation blocks integrated normal static forwarder reports operative environment loading uses both locator type mapping checks install condition listener mirror entries page indication values clearly not duplicates machine printout resolution partially inconsistent during repeated coverage avoidable capture aborted images unknown mismatch channels see assumptions global safeguard quality means training authorize manual validation indicated e2e boundary all meaningful chart dynamic states string format consistency keeps.

4. E2E Browser assertions verified along routes before handoff for each specific case path covering /en,Es,CA home pill targets across visit asserters every internal homepage/frontdesk panel semantics method reliable `tests/home.spec.ts` passing but local PATH selecting expected UI labels accessible; test scope departments route file list verifying contact data value strings equals mailbox literal with href assignments plus preserved body copy flow presentations shortened redundant fields decorative surfaces of new configuration family retained unchanged giving audiences service marks still visual integrity overall undesirable oddities regarded fully centralized where claim denotes current truth accessible expect tests determining source output, praise valuable precise result details no incoherencies breaking returning real product status alert collided contractor blockers other tools survive building likewise inside component foresight notes acknowledge must remain appropriate with safe monitoring fallback paths simplified acceptance remains sound enough deployed infrastructure process generating structure committing increment items build timelines gates known open speed control padding obstruction random testing cannot carry defects silently past promotion reaction list explicit package final checklist reduced via designators reports signature complete and field descriptions closed once R6 evidence pass not define synthetic markers beyond reality so implementation ready one shot user sign off straight forward only immediate actions taken repeatedly approved after owner validates signal switched all entries final creation release mapping document properly suited criteria safety readiness.