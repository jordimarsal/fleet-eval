I'll examine the existing documentation structure to match conventions before writing T4's deliverables.

<tool_call>
<function=list_files>
<parameter=path>
harness/specs/f8_ram_summary
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
harness/progress/impl_f8_ram_summary.md
</parameter>
</function>
</tool_call>