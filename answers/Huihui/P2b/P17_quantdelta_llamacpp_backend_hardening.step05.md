Looking at T5, I need to implement manifest caching with dynamic fingerprint resolution. Let me examine what's needed by reviewing the tests and understanding the existing structure.

Let me check the current state of the relevant files first.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed/src/quantdelta/backends/llamacpp -type f 2>/dev/null; echo "---"; ls -la /testbed/src/quantdelta/backends/llamacpp/ 2>/dev/null
</parameter>
<parameter=description>
List llamacpp backend source files
</parameter>
</function>
</tool_call>