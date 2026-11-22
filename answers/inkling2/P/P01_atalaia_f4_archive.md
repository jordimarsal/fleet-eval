FILES
src/atalaia/state.py
src/atalaia/api.py
web/index.html
web/app.js
web/style.css
tests/test_archive.py

TASKS
T1: Persistent archived-id store
    depends_on: (none)
    refs: R1, R6, R10
T2: Archive/unarchive endpoints and payload flag
    depends_on: T1
    refs: R2, R3, R4, R5
T3: Actius / Arxivats tabs with counts and filtering
    depends_on: T2
    refs: R7
T4: Detail drawer arxivar/desarxivar actions wired to API
    depends_on: T3
    refs: R8
T5: Immediate UI refresh after archive state change
    depends_on: T4
    refs: R9

GATES
python -m pytest tests/test_archive.py tests/test_api.py tests/test_api_detail.py tests/test_web.py tests/test_web_static.py -q
python -m pytest -q
bash harness/init.sh (or feature verification equivalent) confirming no files under scanned project trees are modified (R10 audit of the working tree before closeout)