Looking at T1, I need to move vendor files into `assets/` and update `build.py` paths accordingly. Let me first inspect the actual repository state to understand what exists before making changes.

<tool_call>
<function=list_files>
<parameter=path>
.
</parameter>
</function>
</tool_call>
<tool_call>
<function=read_file>
<parameter=limit>
60
</parameter>
<parameter=offset>
1
</parameter>
<parameter=path>
build.py
</parameter>
</function>
</tool_call>