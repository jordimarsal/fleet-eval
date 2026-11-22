FILES
src/mussol/metadata/catalog.py
src/mussol/audio/tagger.py
src/mussol/sources/value_objects.py
src/mussol/library/library_record.py
src/mussol/library/store.py
src/mussol/api/dtos.py
src/mussol/api/app.py
web/index.html
web/app.js
web/styles.css
tests/test_library_record.py
tests/test_library_store.py
tests/test_api.py
tests/test_web.py

TASKS
T1: Resolve interpreter from catalogue lookup, embedded audio tags, then title pattern; persist on the library record
    depends_on: (none)
    refs: R1
T2: Expose interpreter in GET /library DTOs and render it on each card
    depends_on: T1
    refs: R2
T3: Add interpreter text filter and title/interpreter/date-added sort controls that survive polling refreshes
    depends_on: T2
    refs: R3, R4, R5
T4: Update traceability table (spec requirements → tasks/tests) for this feature
    depends_on: T1, T2, T3
    refs: R1, R2, R3, R4, R5

GATES
python3 -m pytest tests/test_library_record.py tests/test_library_store.py tests/test_catalog.py tests/test_tagger.py tests/test_api.py tests/test_web.py -q
python3 -m pytest -q
python3 harness/tools/check-traceability.py --feature interpreter_filter_sort (or equivalent check for R1–R5 coverage)
manual smoke check of the panel: filter by interpreter, toggle asc/desc for title/interpreter/date added across a poll refresh