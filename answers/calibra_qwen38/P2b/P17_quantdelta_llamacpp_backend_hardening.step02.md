Looking at T2, I need to replace the `"memory"` substring rule with `name.endswith("_bytes")` for gauge recognition. Let me first examine the current backend implementation to understand what's there.

<tool_call>
<function=read_file>
<parameter=path>
src/quantdelta/backends/llamacpp/backend.py
</parameter>
</function>
</tool_call>