FILES
web/app.js
web/styles.css
tests/test_web.py

TASKS
T1: Derive three-state enrichment state from payload
    depends_on: (none)
    refs: R1, R2, R3, R12
T2: Render the enrichment marker in updateRow with words and title
    depends_on: T1
    refs: R4, R8, R9, R10, R12
T3: Add marker styling using existing palette tokens only
    depends_on: T2
    refs: R5, R6, R7, R11
T4: Extend web tests to lock derivation, rendering and token rules
    depends_on: T1, T2, T3
    refs: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
pytest tests/test_web.py -v
pytest tests/test_quality_gates.py -v
pytest tests/test_module_boundaries.py -v
python harness/tools/scan.py (or equivalent repo lint/security gate as documented in docs/verification.md)
grep checks: no album/date name in web/app.js; no hex colour literal or new :root token introduced by this feature's additions; rowSignature still carries artist, has_cover, enriched_at; enrichButton label/request unchanged