I'll start by exploring the repository to understand the current state before implementing T6.

<tool_call>
<function=Bash>
<parameter=command>
find . -type f -not -path './node_modules/*' -not -path './.git/*' | head -100
</parameter>
<parameter=description>
List all files in the repo
</parameter>
</function>
</tool_call>