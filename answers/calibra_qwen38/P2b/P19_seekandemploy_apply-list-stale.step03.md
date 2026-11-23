I'll start by exploring the repository to understand the existing structure and what's been implemented so far.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---" && find . -type f -name "*.py" | head -50
</parameter>
<parameter=description>
List repo root and Python files
</parameter>
</function>
</tool_call>