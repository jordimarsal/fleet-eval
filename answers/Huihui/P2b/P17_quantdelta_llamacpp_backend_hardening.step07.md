Looking at T7, I need to document the adapter scope and update tests for concurrency. Let me examine what's needed by checking the existing source files first.

<tool_call>
<function=read_file>
<parameter=path>
src/quantdelta/backends/llamacpp/backend.py
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=path>
docs/architecture.md
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=path>
tests/unit/backends/llamacpp/test_concurrency.py
</parameter>
</function>
</tool_call>