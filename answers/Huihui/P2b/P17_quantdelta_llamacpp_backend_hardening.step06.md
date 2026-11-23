Looking at T6, I need to add thread-safety locks to `LlamaCppBackend`. Let me first examine the existing source files to understand the current implementation before making changes.

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
src/quantdelta/backends/llamacpp/config.py
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=path>
src/quantdelta/backends/llamacpp/manifest.py
</parameter>
</function>
</tool_call>