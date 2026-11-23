I need to understand the existing rendering surfaces before I can update them. Let me explore the repository state first.

<tool_call>
<function=Bash>
<parameter=command>
git status && echo "---TREE---" && find src -type f | head -100
</parameter>
<parameter=description>
Show git status and source tree
</parameter>
</function>
</tool_call>