FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Add enrichment state derivation function in app.js (none when `enriched_at` absent — checked first; partial when `enriched_at` present but artist empty or has_cover false; complete otherwise; reads only enriched_at, artist and has_cover)
    depends_on: (none)
    refs: R1, R2, R3, R12

T2: Render the marker inside updateRow on every library card, built from the current item, with text from {untagged|partial|tagged}, title naming the state and (for partial) which fields are missing
    depends_on: T1
    refs: R4, R8

T3: Style the three states in styles.css using palette tokens only (accent for complete; muted + destructive border for partial; muted without border/background for none)
    depends_on: T2
    refs: R5, R6, R7, R11

T4: Verify no action changes leak into the feature (enrichButton untouched, no disabling of actions based on state)
    depends_on: T1
    refs: R10

T5: Update tests in test_web.py covering derivation order and field read set, render site/buildRow guard, token usage and absence of hex literals, reconciliation via updateRow
    depends_on: T1, T2
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R12

GATES
Run pytest tests/test_web.py -q (existing external-network and safe-sink sink tests stay green); run full suite pytest -q if time permits; confirm web/app.js contains neither `album` nor `date` references and that LibraryDto/LibraryRecord/columns are unchanged; scan added CSS rules for var(--color-*) tokens only with no new :root entries or hex literals; manual check that marker appears on every library card and updates across poll refresh.