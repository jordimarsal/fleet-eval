I need to understand what T8 requires before writing code. Let me explore the repository state and the relevant components/tests.

<tool_call>
<function=Bash>
<parameter=command>
git status && echo "---BRANCH---" && git branch -a && echo "---LOG---" && git log --oneline -15
</parameter>
<parameter=description>
Check git status, branches, and recent commits
</parameter>
</function>
</tool_call>
<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---SRC---" && find src tests harness -type f 2>/dev/null | head -100
</parameter>
<parameter=description>
List repo root and source/test/harness files
</parameter>
</function>
</tool_call>