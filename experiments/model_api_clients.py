"""Minimal OpenAI-compatible client with redacted, auditable responses."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class APIResult:
    ok: bool
    status_code: int | None
    response: dict[str, Any] | None
    error: str | None
    elapsed_ms: int


def call_chat_completion(
    endpoint: str,
    model: str,
    messages: list[dict[str, str]],
    *,
    api_key_env: str = "GAAGENT_API_KEY",
    max_tokens: int = 512,
    temperature: float = 0.0,
    timeout_seconds: int = 120,
    opener: Any = urllib.request.urlopen,
) -> APIResult:
    """Call an OpenAI-compatible endpoint without ever recording the key."""
    api_key = os.environ.get(api_key_env)
    if not api_key:
        return APIResult(False, None, None, f"missing_environment:{api_key_env}", 0)
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with opener(request, timeout=timeout_seconds) as raw:
            status = getattr(raw, "status", 200)
            body = raw.read().decode("utf-8")
        response = json.loads(body)
        elapsed = round((time.perf_counter() - started) * 1000)
        return APIResult(True, status, response, None, elapsed)
    except urllib.error.HTTPError as exc:
        elapsed = round((time.perf_counter() - started) * 1000)
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        return APIResult(False, exc.code, None, f"http_error:{detail}", elapsed)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000)
        return APIResult(False, None, None, f"transport_error:{exc}", elapsed)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000)
        return APIResult(False, None, None, f"invalid_json:{exc}", elapsed)


def extract_text(response: dict[str, Any] | None) -> str | None:
    if not response:
        return None
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None
    return content if isinstance(content, str) else None
