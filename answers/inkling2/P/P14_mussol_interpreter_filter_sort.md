FILES
src/mussol/metadata/catalog.py
src/mussol/audio/extractor.py
src/mussol/library/store.py
src/mussol/library/library_record.py
src/mussol/metadata/tagger.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/index.html
web/app.js
web/styles.css
tests/test_library_record.py
tests/test_library_store.py
tests/test_api.py
tests/test_web.py
harness/specs/interpreter_filter_sort/requirements.md
harness/specs/interpreter_filter_sort/design.md
harness/specs/interpreter_filter_sort/tasks.md
harness/tools/check-traceability.py

TASKS
T1: Implement interpreter resolution with catalogue → embedded tags → title pattern priority
    depends_on: (none)
    refs: R1
T2: Persist resolved interpreter on the library record (schema, save, update path)
    depends_on: T1
    refs: R1
T3: Expose interpreter in GET /library DTO and show it on the card
    depends_on: T2
    refs: R2
T4: Add interpreter text filter to the panel
    depends_on: T3
    refs: R3
T5: Add sorting by title, interpreter, date added with asc/desc direction
    depends_on: T3
    refs: R4
T6: Keep active filter and sort across polling refreshes; render checkbox states after refresh
    depends_on: T4, T5
    refs: R3, R4, R5
T7: Update requirements, design, tasks docs and traceability table covering every requirement
    depends_on: T6
    refs: R1, R2, R3, R4, R5

GATES
python3 -m pytest tests/ (full suite green)
python3 harness/tools/check-traceability.py harness/specs/interpreter_filter_sort (every R* row maps to a task and a file/test)
python3 -m py_compile src/mussol/metadata/*.py src/mussol/library/*.py src/mussol/api/*.py main.py && node --check web/app.js
Manual smoke test in browser against GET /library: card shows interpreter; text query narrows the list; clicking headers sorts ascending then descending; values persist after three poll cycles