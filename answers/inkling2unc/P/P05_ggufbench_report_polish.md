FILES
html_report.py
tests/test_html_report.py

TASKS
T1: Partition pool into live and retired rows; record both sets for the render pass
    depends_on: (none)
    refs: R1, R3, R8, R10

T2: Sort every per-dimension list best→worst in shared helpers (higher scores desc; latency asc; gen t/s and prompt t/s desc), applied symmetrically to Board and Retired panes
    depends_on: T1
    refs: R7

T3: Render self-contained tab shell: two panes, no JavaScript, pure CSS switchability, Board visible by default; suppress tab bar entirely when there are no retired rows
    depends_on: T2
    refs: R1, R2, R3, R12

T4: Build Board pane content from live rows only (no retired row, gray style and "retired" badge stay inside Retired pane exclusively) with sorted lists
    depends_on: T3
    refs: R7, R8

T5: Build Retired pane as a record-only view: no KPI strip, no Recommendations section, explicit "record only / retired from the bench" notice, gray styling + retired badge retained, and its own sorted per-dimension lists
    depends_on: T2
    refs: R4, R7, R9

T6: Compute KPI strip and place Recommendations section (after KPI strip, before "Weighted global") using live rows only
    depends_on: T4
    refs: R5, R6

T7: Update header chips: "models" chip shows `18 models (+16 retired)` split counts while retired rows exist (single total otherwise); "task sets" chip links only to set blocks present in the Board pane — retired-only signatures rendered as plain text
    depends_on: T4, T5
    refs: R10, R11

GATES
python3 -m unittest tests.test_html_report -v
python3 -m unittest discover -s tests   (full suite green)
grep for external resources in generated report (no http://, https://, src= for scripts/links beyond the single inline script)
Open results/report.html with JavaScript disabled: confirm Board visible by default, no tab bar when pool has zero retired rows, two panes switchable via CSS elsewhere
Regenerate the published report (harness/tools/publish-report.sh or python3 -m ggufbench.run --html equivalent) and visually verify both panes against the approved requirements