FILES  
src/quantdelta/core/models.py  
src/quantdelta/core/ports.py  
src/quantdelta/core/serialization.py  
tests/unit/core/test_models.py  
tests/unit/core/test_public_api.py  
tests/unit/core/test_serialization.py  

TASKS  
T1: Define TokenAlternative and TokenLogprob types with validation rules  
    depends_on: (none)  
    refs: R2, R3  
T2: Implement TaskKL type with field constraints and uniqueness enforcement  
    depends_on: T1  
    refs: R4, R5  
T3: Update TaskOutput to include optional logprobs field  
    depends_on: T1  
    refs: R3  
T4: Modify Scorer port signature to accept keyword-only arguments  
    depends_on: T2  
    refs: R1, R6  
T5: Add KL report fields to Report model with all-or-nothing constraint  
    depends_on: T2  
    refs: R5, R6  
T6: Ensure schema version remains "1" and backward compatibility is preserved  
    depends_on: T4, T5  
    refs: R6  
T7: Pin public exports in core API snapshot including Scorer, TokenAlternative, TokenLogprob, TaskKL  
    depends_on: T4, T5  
    refs: R7  
T8: Implement InvalidDataError for invalid values with field-specific error messages  
    depends_on: T1, T2, T5  
    refs: R8  

GATES  
- All new types (TokenAlternative, TokenLogprob, TaskKL) validate against R2, R4, R5 using unit tests  
- Scorer signature change passes type checking and existing test suite (R1)  
- Round-trip serialization of Report with and without KL fields matches expected behavior (R6)  
- All invalid value cases raise `InvalidDataError` with correct field names (R8)  
- Public API snapshot confirms inclusion of new types and scorer signature (R7)  
- No runtime dependencies or I/O introduced; import boundary unchanged (R7)