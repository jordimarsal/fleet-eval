Looking at T1, I need to enhance the `/metrics` parser to accept scientific notation and leading `+` in values. Let me first examine the existing code structure to understand what's there.

Let me check the current state of the backend files.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed/src/quantdelta/backends/llamacpp -type f -name "*.py" | sort && echo "---TESTS---" && find /testbed/tests/unit/backends/llamacpp -type f -name "*.py" | sort
</parameter>
<parameter=description>
List llamacpp source and test files
</parameter>
</function>
</tool_call>