I'll start by exploring the repository to understand the project structure and conventions before writing the README.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---" && cat package.json 2>/dev/null | head -60
</parameter>
<parameter=description>
List repo root and show package.json
</parameter>
</function>
</tool_call>