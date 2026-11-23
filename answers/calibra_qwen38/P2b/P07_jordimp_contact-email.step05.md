Looking at T4, I need to regenerate the parity fixture and verify the diff shows only the expected email address changes. Let me first examine the current state of the relevant files.

<tool_call>
<function=Read>
<parameter=file_path>
/home/user/jordimp/tests/fixtures/parity.json
</parameter>
</function>
</tool_call>
<tool_call>
<function=Glob>
<parameter=pattern>
scripts/distill-parity.mjs
</parameter>
</function>
</tool_call>