Looking at T2, I need to refactor memory recognition in `LlamaCppBackend.metrics()` to use strict `_bytes` suffix matching instead of case-insensitive substring matching. Let me first examine the existing backend implementation.

<tool_call>
<function=read_file>
<parameter=path>
src/quantdelta/backends/llamacpp/backend.py
</parameter>
</function>
</tool_call>