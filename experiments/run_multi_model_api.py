"""Explicitly opt-in live multi-model pilot; never sends the expected answer."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

from financial_contract_fixtures import cases
from model_api_clients import call_chat_completion, extract_text

DEFAULT_MODELS = [
    "gpt-6.1-sol", "gpt-6-astra", "grok-4.7", "gemini-3.8-flash-high",
    "gpt-oss-120b-medium",
]

SYSTEM = (
    "You are evaluating a financial time-series calculation. Use only the supplied fields. "
    "Do not invent missing information. If units, currencies, periods, metrics, or availability "
    "are incompatible, return JSON with answer=null and a short reason. Return JSON only."
)


def public_input(item: dict) -> dict:
    """Remove labels that reveal the intended answer or scenario."""
    return {
        "id": item["id"], "decision_at": item["decision_at"],
        "base": item["base"], "current": item["current"],
    }


def prompt_for(item: dict, workflow: str) -> str:
    data = json.dumps(public_input(item), ensure_ascii=False, sort_keys=True)
    if workflow == "no_skill":
        prefix = "Solve the task directly."
    elif workflow == "static_skill":
        prefix = "Apply this fixed skill: validate availability, currency, scale, metric, and period before calculating growth."
    elif workflow == "generated_skill":
        prefix = "First infer a reusable validation-and-calculation skill from this task, then apply it."
    else:
        prefix = "Apply a generated skill, then enforce the validation contract before answering."
    return f"{prefix}\nInput:\n{data}\nOutput JSON keys: answer, status, reason."


def run(endpoint: str, key_env: str, models: list[str], out: pathlib.Path, max_tokens: int, timeout: int) -> int:
    heldout = [x for x in cases() if x["split"] == "heldout"]
    rows = []
    for model in models:
        for workflow in ("no_skill", "static_skill", "generated_skill", "generated_skill_contract"):
            for item in heldout:
                messages = [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt_for(item, workflow)},
                ]
                result = call_chat_completion(endpoint, model, messages, api_key_env=key_env,
                                              max_tokens=max_tokens, timeout_seconds=timeout)
                rows.append({
                    "model": model, "workflow": workflow, "task_id": item["id"],
                    "ok": result.ok, "status_code": result.status_code,
                    "elapsed_ms": result.elapsed_ms, "error": result.error,
                    "text": extract_text(result.response),
                    "usage": result.response.get("usage") if result.response else None,
                })
                if not result.ok and result.error and result.error.startswith("missing_environment"):
                    break
            if rows[-1]["error"] and rows[-1]["error"].startswith("missing_environment"):
                break
        if rows[-1]["error"] and rows[-1]["error"].startswith("missing_environment"):
            break
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark_version": "financial-contract-api-pilot-0.1.0",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint, "requested_models": models, "key_env": key_env,
        "model_identity": "provider-declared; independently unverified",
        "rows": rows,
        "note": "Live API output is not evidence until parsing, scoring, and provenance review are complete.",
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="https://kw.gaagent.ai/v1/chat/completions")
    parser.add_argument("--key-env", default="GAAGENT_API_KEY")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    return run(args.endpoint, args.key_env, args.models, args.out, args.max_tokens, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
