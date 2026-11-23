I'll examine the existing CSS to match conventions before adding the new styles.

<tool_call>
<function=read_file>
<parameter=path>
src/styles/site.css
</parameter>
</function>
</tool_call>
<tool_call>
<function=glob_files>
<parameter=pattern>
**/*.css
</parameter>
<parameter=path>
src
</parameter>
</function>
</tool_call>