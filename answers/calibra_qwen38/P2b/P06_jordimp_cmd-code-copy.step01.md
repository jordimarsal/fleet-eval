I'll start by exploring the repository structure to understand conventions before implementing T1.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---SRC---" && ls -la src/ 2>/dev/null && echo "---LIB---" && ls -la src/lib/ 2>/dev/null
</parameter>
<parameter=description>
List repo root and src directories
</parameter>
</function>
</tool_call>