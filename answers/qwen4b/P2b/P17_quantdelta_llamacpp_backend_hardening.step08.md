Looking at T8, I need to ensure `run()` records success for `finish_reason == "length"` or empty content with token counts. Let me examine what's needed and check if there are specific tests for this behavior.

Let me search for any existing tests related to truncation/empty content handling.

<tool_call>
<function=Bash>
<parameter=command>
grep -rn "finish_reason\|truncat\|empty.*content\|length" --include="*.py" src/quantdelta/backends/llamacpp/ tests/unit/backends/llamacpp/ | head -60
</parameter>
<parameter=description>
Search for finish_reason and truncation references
</parameter>
</function>
</tool_call>