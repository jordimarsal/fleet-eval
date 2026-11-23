Let me first explore the repository to understand the current state of the codebase.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed -type f -name "*.py" | head -60 && echo "---TREE---" && ls -la /testbed
</parameter>
<parameter=description>
List Python files and root directory
</parameter>
</function>
</tool_call>