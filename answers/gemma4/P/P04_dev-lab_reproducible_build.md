FILES
vendor/marked.min.js
vendor/highlight.min.js
vendor/fonts/fonts-local.css
vendor/fonts/font1.woff2
vendor/fonts/font2.woff2
build.py

TASKS
T1: Setup vendor directory and update paths
    depends_on: (none)
    refs: R1
T2: Implement vendor existence validation
    depends_on: T1
    refs: R2
T3: Implement content validation logic (groups and questions)
    depends_on: (none)
    refs: R3, R4
T4: Implement --check mode and remove build date from output
    depends_on: T3
    refs: R5, R6

GATES
- Verify `vendor/` contains all required files and `build.py` uses them.
- Run `build.py` with missing vendor files to ensure non-zero exit and clean error message.
- Run `build.py` with unassigned note slugs to ensure non-zero exit.
- Run `build.py` with invalid question schema in `src/questions/*.js` to ensure non-zero exit.
- Run `python3 build.py --check` and verify it exits 0 on valid content and non-zero on invalid content without writing files.
- Perform two consecutive builds and compare SHA256 hashes of the output directory to ensure byte-identity (R5).