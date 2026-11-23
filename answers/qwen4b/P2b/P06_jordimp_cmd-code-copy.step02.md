I need to understand what T2 requires before implementing. Let me explore the repository state first.

<tool_call>
<function=Bash>
<parameter=command>
git status && echo "---BRANCH---" && git branch -a && echo "---LOG---" && git log --oneline -10
</parameter>
<parameter=description>
Check git status and history
</parameter>
</function>
</tool_call>
<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---SRC---" && find src -type f | head -100
</parameter>
<parameter=description>
List repo root and source files
</parameter>
</function>
</tool_call>