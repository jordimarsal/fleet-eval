FILES
docs/model-field-notes.md
docs/fleet-link-reference.md

TASKS
T1: Create model field notes documentation
    depends_on: (none)
    refs: R7, R8
T2: Create fleet link reference documentation
    depends_on: T1
    refs: R6, R9, R10

GATES
Verify docs/model-field-notes.md contains all fields specified in R7 (model identity, backend name/version, command, seed, timestamps, scores, resources).
Verify docs/fleet-link-reference.md uses no engine-specific vocabulary (gguf, llama, kv cache) as per R6.
Verify that adding these docs does not introduce dependencies on httpx, subprocess, numpy, or typer during import of quantdelta.core (R5).
Verify that the new documentation files do not alter the frozen value types or public API signatures defined in src/quantdelta/core/models.py and ports.py (R1, R11).