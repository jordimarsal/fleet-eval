Looking at T1, I need to harden the Prometheus parser for numeric and label edge cases. Let me first examine the existing code structure to understand what's there.

<tool_call>
<function=list_files>
<parameter=path>
src/quantdelta/backends/llamacpp
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=limit>
200
</parameter>
<parameter=offset>
1
</parameter>
<parameter=path>
tests/unit/backends/llamacpp/test_metrics.py
</parameter>
</function>
</tool_call>