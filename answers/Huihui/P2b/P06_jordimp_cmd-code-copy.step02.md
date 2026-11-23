I'll start by exploring the repository to understand the existing patterns before implementing T2.

<tool_call>
<function=Bash>
<parameter=command>
ls -la && echo "---ASTRO CONFIG---" && cat astro.config.* 2>/dev/null | head -50
</parameter>
<parameter=description>
List repo root and view astro config
</parameter>
</function>
</tool_call>
<tool_call>
<function=Glob>
<parameter=pattern>
src/components/**/*.astro
</parameter>
</function>
</tool_call>