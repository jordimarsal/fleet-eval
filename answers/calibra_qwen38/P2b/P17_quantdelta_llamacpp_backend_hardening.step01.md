I'll examine the repository structure to understand what exists before implementing T1.

<tool_call>
<function=Bash>
<parameter=command>
find . -type f -name "*.py" | grep -v __pycache__ | head -100 && echo "---TREE---" && ls -la
</parameter>
<parameter=description>
List Python files and root directory
</parameter>
</function>
</tool_call>