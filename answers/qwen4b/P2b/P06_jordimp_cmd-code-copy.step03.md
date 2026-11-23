I'll start by exploring the repository to understand the current state before implementing T3.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---GIT---" && git status && echo "---LOG---" && git log --oneline -10
</parameter>
<parameter=description>
List repo root and git status/log
</parameter>
</function>
</tool_call>