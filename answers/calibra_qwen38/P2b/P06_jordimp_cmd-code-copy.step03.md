I'll start by exploring the repository to understand the current state before running the full battery for T3.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---GIT STATUS---" && git status && echo "---GIT LOG---" && git log --oneline -10
</parameter>
<parameter=description>
List repo root and check git status/log
</parameter>
</function>
</tool_call>