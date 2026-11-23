I need to understand the exact API expected by the tests before implementing T3. Let me examine the relevant source files and specs.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed -type f -name "*.py" | head -50 && echo "---SPECS---" && find /testbed/harness -type f 2>/dev/null | head -50
</parameter>
<parameter=description>
List Python files and spec files
</parameter>
</function>
</tool_call>
<tool_call>
<function=Grep>
<parameter=pattern>
stale_open_applications|def stale
</parameter>
<parameter=output_mode>
files_with_matches
</parameter>
</function>
</tool_call>