I need to understand what T4 requires before implementing it. Let me examine the repository state and relevant specs.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed -type f -name "*.py" | head -50 && echo "---TREE---" && ls -la /testbed
</parameter>
<parameter=description>
List Python files and root directory
</parameter>
</function>
</tool_call>
<tool_call>
<function=Glob>
<parameter=pattern>
harness/specs/application-tracking/**/*
</parameter>
</function>
</tool_call>