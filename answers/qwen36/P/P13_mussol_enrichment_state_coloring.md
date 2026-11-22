FILES
web/app.js
web/styles.css

TASKS
T1: Derive enrichment state from payload fields in `buildRow`
    depends_on: (none)
    refs: R1, R2, R3, R4, R8, R9, R10, R12
T2: Add CSS rules for the three enrichment marker states
    depends_on: T1
    refs: R5, R6, R7, R11
T3: Wire the marker into `updateRow` and verify no new network dependencies
    depends_on: T1, T2
    refs: R4, R9, R10, R11, R12

GATES
- `test_scripts_use_safe_sinks_only` passes (no external scripts or fonts loaded)
- `test_page_has_no_external_network_dependencies` passes
- `test_web.py::test_root_serves_required_landmarks` still passes (marker does not break existing landmarks)
- Manual audit of `web/styles.css`: zero hex colour literals; only token references (`var(--color-accent)`, `var(--color-muted)`, `var(--color-destructive)`)
- Manual audit of `web/app.js`: no mention of `album` or `date`; `rowSignature` unchanged
- Visual check on a card with `enriched_at` set but missing artist → marker is muted text + destructive border
- Visual check on a card with `enriched_at` set, both fields present → marker is accent-coloured
- Visual check on a card without `enriched_at` → marker is muted text, no border