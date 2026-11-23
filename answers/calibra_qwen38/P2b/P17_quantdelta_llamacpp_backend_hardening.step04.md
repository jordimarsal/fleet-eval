I need to understand the current state of the backend implementation before adding the concurrency lock. Let me explore the repository first.

<tool_call>
<function=Bash>
<parameter=command>
find /testbed/src/quantdelta/backends/llamacpp -type f | sort && echo "---TESTS---" && find /testbed/tests/unit/backends/llamacpp -type f | sort
</parameter>
<parameter=description>
List backend and test source files
</parameter>
</function>
</tool_call>