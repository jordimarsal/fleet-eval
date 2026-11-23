I need to understand the existing CLI structure before implementing T1. Let me explore the repository.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed -type f -name "*.py" | head -50 && echo "---TREE---" && ls -la /testbed
</parameter>
<parameter=description>
List Python files and testbed root
</parameter>
</function>
</tool_call>