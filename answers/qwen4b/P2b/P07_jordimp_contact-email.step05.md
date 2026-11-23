I need to understand what T5 requires. Let me examine the existing llms implementation and related files first.

<tool_call>
<function=Read>
<parameter=file_path>
/home/user/src/lib/llms.ts
</parameter>
</function>
</tool_call>
<tool_call>
<function=Glob>
<parameter=pattern>
src/pages/**/*
</parameter>
</function>
</tool_call>