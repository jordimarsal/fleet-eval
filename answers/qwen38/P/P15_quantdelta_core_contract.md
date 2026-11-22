The feature title is `docs: add the model field notes and the fleet link`. This implies documentation updates rather than code changes. The requirements provided describe the *existing* state of the system (frozen types, serialization, ports, etc.) which serves as context for what the documentation should reflect or reference. Since no new functional requirements are introduced that change behavior, the implementation focuses on updating documentation files to include notes about the "model" field (likely referring to the `model` attribute in `RunRecord` or similar domain concepts) and adding a link to the fleet documentation.

Looking at the file tree:
- `docs/fleet.md` exists.
- `README.md`, `docs/architecture.md`, `docs/conventions.md`, etc., exist.
- There is no explicit "model field notes" document, but `docs/decisions/core-contract-data-model-pydantic.md` likely contains data model details. Or perhaps the README needs a section linking to fleet docs and explaining the model fields.

Given the specific phrasing "add the model field notes and the fleet link", it's highly probable this refers to updating the main `README.md` or a specific doc page to clarify the `model` field in `RunRecord` (as per R7: "identity of the model...") and ensuring there is a clear link to `docs/fleet.md`.

However, looking closer at R7: "Each RunRecord shall carry the identity of the model...". The current code excerpt shows `RunRecord` imports but not its definition. If the feature is purely docs, we modify markdown files.

Let's assume the task is to update `README.md` to include a section on the data model fields (specifically highlighting the `model` field as required by R7) and add a prominent link to `docs/fleet.md`. Alternatively, if `docs/fleet.md` is new or needs linking from elsewhere. Since `docs/fleet.md` already exists in the tree, the "fleet link" part suggests adding a reference *to* it in another document, likely `README.md` or `docs/architecture.md`.

The "model field notes" likely refers to documenting the `model` attribute within the context of `RunRecord` or the general data model documentation.

Plan:
1.  Modify `README.md` to add a "Data Model" or "Key Fields" section noting the `model` field requirement/usage and add a link to `docs/fleet.md`.
2.  Potentially modify `docs/architecture.md` if that's where the fleet integration is described, but README is the primary entry point. Let's stick to `README.md` for the main changes unless specific doc structure implies otherwise. The prompt says "add... the fleet link", implying it might be missing or needs to be more visible.

Wait, looking at the requirements again, they are all about the *code* behavior (R1-R12). But the feature title is `docs:`. This is a common pattern in these prompts where the "requirements" define the system state that the docs must accurately reflect, or the task is simply to write the docs for an already implemented feature. Since the code files (`models.py`, etc.) exist and seem complete based on the tests provided, the implementation plan should focus on creating/modifying the documentation files.

Files to modify:
- `README.md`: Add notes on the `model` field (part of RunRecord) and add a link to `docs/fleet.md`.
- Possibly `docs/fleet.md` itself if it needs updating? No, "add the fleet link" usually means linking *to* it.
- Maybe `docs/decisions/core-contract-data-model-pydantic.md`? It sounds like a place for "field notes".

Let's refine. The most standard interpretation of "add model field notes" in a repo with a data model decision record is to update that record or the main README. Given R7 explicitly mentions the model identity, documenting this is key.

I will propose modifying `README.md` to include a section on the core data model fields (highlighting `model`) and adding a navigation link to `docs/fleet.md`. I will also check if `docs/architecture.md` is a better fit for the fleet link. Usually, architecture docs describe components. Fleet might be a component. Let's assume `README.md` gets both for visibility.

Actually, looking at the file tree, there is no `docs/model-fields.md`. Creating one might be overkill. Updating existing docs is safer.

Revised Plan:
1.  Modify `README.md`: Add a "Data Model" section describing the frozen value types and specifically noting the `model` field in `RunRecord` (R7). Add a "Documentation" or "Related Links" section pointing to `docs/fleet.md`.
2.  Modify `docs/architecture.md`: Ensure it references the fleet documentation appropriately if not already done, but the prompt says "add... the fleet link", implying it's missing.

Let's stick to `README.md` as the primary target for user-facing notes and links.

FILES
README.md

TASKS
T1: Update README with model field notes and fleet link
    depends_on: (none)
    refs: R1, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

GATES
- Verify that `README.md` contains a section documenting the `model` field within `RunRecord` (or equivalent data model context).
- Verify that `README.md` contains a valid relative link to `docs/fleet.md`.
- Run `pytest tests/ -v` to ensure no code changes were accidentally introduced that break existing behavior (though this is a docs-only change, running tests ensures repo integrity).