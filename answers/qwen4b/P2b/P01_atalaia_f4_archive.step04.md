I'll analyze the requirements for T4 and check the existing state before implementing.

<tool_call>
<function=Bash>
<parameter=command>
ls -la web/ 2>/dev/null && echo "---INDEX---" && cat web/index.html 2>/dev/null; echo "---APPJS---"; wc -l web/app.js 2>/dev/null; echo "---CSS---"; wc -l web/style.css 2>/dev/null
</parameter>
<parameter=description>
List web directory and inspect index.html
</parameter>
</function>
</tool_call>