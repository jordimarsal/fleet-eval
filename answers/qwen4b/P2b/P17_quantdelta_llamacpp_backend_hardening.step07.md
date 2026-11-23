Looking at T7, I need to add strict `base_url` validation to `LlamaCppConfig`. Let me examine what's needed based on the tests and references.

The key requirements from `test_config.py`:
- Reject non-http(s) schemes (`ftp://`)
- Require hostname
- Port must be integer 1–65535
- No whitespace
- No userinfo/credentials
- No query string
- No fragment
- Normalize uppercase scheme to lowercase
- Strip trailing slashes but preserve path prefix
- Accept IPv6 literals like `[::1]`
- Raise `LlamaCppConfigError` with `.field == "base_url"` and specific `.reason` strings

Let me check the existing config and errors modules first.

<tool_call>
<function=Read>
<parameter=file_path>
src/quantdelta/backends/llamacpp/config.py
</parameter>
</function>
</tool_call>
<tool_call>
<function=Read>
<parameter=file_path>
src/quantdelta/backends/llamacpp/errors.py
</parameter>
</function>
</tool_call>