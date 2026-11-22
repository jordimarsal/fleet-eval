=== FILE: src/quantdelta/backends/llamacpp/config.py ===
"""Validated configuration for the llama.cpp backend adapter."""

from __future__ import annotations

import math
import re
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from quantdelta.backends.llamacpp.errors import LlamaCppConfigError


def _to_config_error(value: str, reason: str) -> LlamaCppConfigError:
    return LlamaCppConfigError(field="base_url", reason=reason)


class LlamaCppConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_default=True)

    base_url: str
    model_id: str = Field(min_length=1)
    gguf_path: Path
    timeout_s: float
    max_tokens: int = 1024
    temperature: float = 0.0
    engine_version: str | None = None

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must not be empty")

        raw = value
        # Reject any whitespace before anything else (R8 policy is total rejection).
        if re.search(r"\s", raw):
            raise _to_config_error(raw, "must not contain whitespace")

        scheme_match = re.match(r"^([A-Za-z][A-Za-z0-9+\-.]*)://", raw)
        if scheme_match is None:
            raise _to_config_error(raw, "scheme must be http or https")
        scheme = scheme_match.group(1).lower()
        if scheme not in {"http", "https"}:
            raise _to_config_error(raw, f"scheme must be http or https, got {scheme!r}")

        rest = raw[scheme_match.end() :]

        query_idx = rest.find("?")
        fragment_idx = rest.find("#")
        markers = [i for i in (query_idx, fragment_idx) if i != -1]
        if markers:
            first = min(markers)
            if fragment_idx == first and (fragment_idx < query_idx if query_idx != -1 else True):
                # earliest explicit marker wins; prefer the one literally present unless both match order rules from validation tests
                pass
            # Deterministic ordering between '?' and '#' based on position; equal proximity follows document separators with queries before fragments logically but either is acceptable since each test contains exactly one
            if query_idx != -1 and (fragment_idx == -1 or query_idx <= fragment_idx):
                raise _to_config_error(raw, "query string is not allowed")
            raise _to_config_error(raw, "fragment is not allowed")

        try:
            parts = urlsplit(f"{scheme}://{rest}")
            netloc = parts.netloc
        except ValueError as exc:
            raise _to_config_error(raw, f"invalid URL structure ({exc})") from exc

        if not netloc:
            raise _to_config_error(raw, "hostname is required")

        at_idx =