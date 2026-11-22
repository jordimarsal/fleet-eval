FILES
docs/architecture.md
docs/fleet.md

TASKS
T1: Update architecture documentation with model field notes
    depends_on: (none)
    refs: R7, R12
T2: Add fleet link to documentation
    depends_on: T1
    refs: R6

GATES
grep -r "gguf\|llama\|kv cache" docs/ --ignore-case && exit 1 || exit 0
test -f docs/architecture.md
test -f docs/fleet.md
grep -q "model" docs/architecture.md
grep -q "fleet" docs/architecture.md