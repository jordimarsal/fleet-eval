I'll examine the existing UI files to understand the current state before implementing T2.

<tool_call>
<function=list_files>
<parameter=path>
web
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=limit>
2000
</parameter>
<parameter=offset>
1
</parameter>
<parameter=path>
tests/test_web.py
</parameter>
</function>
</tool_call>