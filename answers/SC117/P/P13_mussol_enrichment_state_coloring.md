FILES
web/app.js
web/styles.css

TASKS
T1: Implement enrichment state derivation logic in `web/app.js`
    depends_on: (none)
    refs: R1, R2, R3
T2: Add CSS rules for the three enrichment states in `web/styles.css`
    depends_on: T1
    refs: R5, R6, R7
T3: Integrate marker rendering into `updateRow` and verify `buildRow` in `web/app.js`
    depends_on: T1
    refs: R4, R8, R9, R10
T4: Verify palette constraints and dependency safety in `web/styles.css` and `web/app.js`
    depends_on: T2
    refs: R11, R12

GATES
- Run `test_page_has_no_external_network_dependencies` to ensure no new network loads.
- Run `test_scripts_use_safe_sinks_only` to confirm safe DOM sinks.
- Run `test_web.py` to validate static frontend structure and token usage.
- Visual inspection of `web/styles.css` to confirm no hex literals are introduced and only existing tokens (`--color-accent`, `--color-muted`, `--color-destructive`) are used.
- Manual verification that `buildRow` does not render the marker while `updateRow` does.