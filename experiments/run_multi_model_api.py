"""Explicitly opt-in live multi-model pilot; never sends the expected answer."""
from __future__ import annotations

import argparse
import hashlib
import json

import financial_contract_fixtures
import model_api_clients
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


WORKFLOWS = ("no_skill", "static_skill", "generated_skill", "generated_skill_contract")
DESIGN_LIMITATIONS = {
    "workflow_implementation": "prompt-only variants; workflow identifiers retained for compatibility",
    "generated_skill_persisted": False,
    "external_contract_executed": False,
    "generated_skill_experiment": False,
    "fixture_origin": "constructed test cases, not observed financial data",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run(endpoint: str, key_env: str, models: list[str], out: pathlib.Path, max_tokens: int, timeout: int,
        temperature: float = 0.0) -> int:
    started_at = datetime.now(timezone.utc).isoformat()
    heldout = [x for x in cases() if x["split"] == "heldout"]
    source_hashes = {
        pathlib.Path(path).name: hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
        for path in (__file__, model_api_clients.__file__, financial_contract_fixtures.__file__)
    }
    rows = []
    stop_reason = None
    for model in models:
        for workflow in WORKFLOWS:
            for item in heldout:
                messages = [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt_for(item, workflow)},
                ]
                result = call_chat_completion(endpoint, model, messages, api_key_env=key_env,
                                              max_tokens=max_tokens, temperature=temperature,
                                              timeout_seconds=timeout)
                rows.append({
                    "model": model, "workflow": workflow, "task_id": item["id"],
                    "ok": result.ok, "status_code": result.status_code,
                    "elapsed_ms": result.elapsed_ms, "error": result.error,
                    "text": extract_text(result.response),
                    "usage": result.response.get("usage") if result.response else None,
                    "prompt_sha256": sha256_text(messages[1]["content"]),
                    "messages_sha256": sha256_text(json.dumps(messages, ensure_ascii=False, sort_keys=True)),
                })
                if not result.ok:
                    if result.error and result.error.startswith("missing_environment"):
                        stop_reason = "missing_api_key_environment"
                    elif result.status_code in (401, 403):
                        stop_reason = f"http_{result.status_code}_global_circuit_breaker"
                if stop_reason:
                    break
            if stop_reason:
                break
        if stop_reason:
            break
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark_version": "financial-contract-api-pilot-0.2.0",
        "started_at_utc": started_at,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "stop_reason": stop_reason,
        "planned_calls": len(models) * len(WORKFLOWS) * len(heldout),
        "attempted_calls": len(rows),
        "protocol": {
            "system": SYSTEM,
            "system_sha256": sha256_text(SYSTEM),
            "source_sha256": source_hashes,
            "fixtures_sha256": sha256_text(json.dumps(heldout, ensure_ascii=False, sort_keys=True)),
            "fixtures_hash_scope": "canonical JSON of complete heldout cases, including scoring labels; labels are not sent",
            "max_tokens": max_tokens, "temperature": temperature,
            "timeout_seconds": timeout, "workflow_order": list(WORKFLOWS),
            "task_order": [item["id"] for item in heldout],
        },
        "design_limitations": DESIGN_LIMITATIONS,
        "endpoint": endpoint, "requested_models": models, "key_env": key_env,
        "model_identity": "provider-declared; independently unverified",
        "rows": rows,
        "note": "Live API output is not evidence until parsing, scoring, and provenance review are complete.",
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if rows and all(row["ok"] for row in rows) and not stop_reason else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="https://kw.gaagent.ai/v1/chat/completions")
    parser.add_argument("--key-env", default="GAAGENT_API_KEY")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()
    return run(args.endpoint, args.key_env, args.models, args.out, args.max_tokens, args.timeout, args.temperature)


if __name__ == "__main__":
    sys.exit(main())
