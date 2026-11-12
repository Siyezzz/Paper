#!/usr/bin/env python3
"""确定性财务契约程序试验；手写策略，非 LLM 或真实金融数据实验。"""
import argparse
from datetime import date
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import platform
import sys

from financial_contract_fixtures import cases

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_config():
    return json.loads((ROOT / "financial_contract_config.json").read_text(encoding="utf-8"))


def check_splits(items, config):
    ids = [c["id"] for c in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate ID or split overlap")
    for c in items:
        when = date.fromisoformat(c["decision_at"])
        if c["fixture_type"] != "constructed_test_case_not_observed_financial_data":
            raise ValueError("fixture must be explicitly constructed")
        if c["split"] == "discovery":
            valid = when <= date.fromisoformat(config["discovery_end"])
        elif c["split"] == "validation":
            valid = date.fromisoformat(config["discovery_end"]) < when <= date.fromisoformat(config["validation_end"])
        elif c["split"] == "heldout":
            valid = when > date.fromisoformat(config["freeze_at"])
        else:
            valid = False
        if not valid:
            raise ValueError("chronological split violation")
    if config["validation_end"] > config["freeze_at"]:
        raise ValueError("validation extends beyond freeze")


def period_compatible(b, c):
    return (b["convention"] == c["convention"] and
            all(date.fromisoformat(c[k]) == date.fromisoformat(b[k]).replace(
                year=date.fromisoformat(b[k]).year + 1) for k in ("start", "end")))


def violations(item):
    b, c = item["base"], item["current"]
    checks = {
        "availability": any(x["available_at"] > item["decision_at"] or
                            x["end"] > item["decision_at"] or
                            x["available_at"] < x["end"] for x in (b, c)),
        "unit": any(b[k] != c[k] for k in ("currency", "scale")),
        "period": not period_compatible(b, c),
        "metric": b["metric"] != c["metric"],
        "zero_base": Decimal(b["value"]) == 0,
    }
    return [key for key, failed in checks.items() if failed]


def growth(item, normalize=False):
    b, c = item["base"], item["current"]
    base, current = Decimal(b["value"]), Decimal(c["value"])
    if base == 0:
        return None
    if normalize:
        base *= Decimal(b["scale"])
        current *= Decimal(c["scale"])
    return str((current / base - 1) * 100)


def metadata_solver(item):
    # 独立手写解算器逐次读元数据，不使用技能准入结果或夹具标准答案。
    b, c = item["base"], item["current"]
    if any(x["available_at"] > item["decision_at"] or x["end"] > item["decision_at"]
           or x["available_at"] < x["end"] for x in (b, c)):
        return None
    if b["currency"] != c["currency"] or b["metric"] != c["metric"]:
        return None
    if b["convention"] != c["convention"]:
        return None
    for key in ("start", "end"):
        bd, cd = date.fromisoformat(b[key]), date.fromisoformat(c[key])
        if (cd.year, cd.month, cd.day) != (bd.year + 1, bd.month, bd.day):
            return None
    return growth(item, normalize=True)


def freeze(discovery, validation, config):
    if any(c["split"] != "discovery" for c in discovery) or any(c["split"] != "validation" for c in validation):
        raise ValueError("heldout forbidden during discovery/admission")
    if any(c["decision_at"] > config["freeze_at"] or
           any(x["available_at"] > config["freeze_at"] for x in (c["base"], c["current"]))
           for c in discovery + validation):
        raise ValueError("training/admission temporal leakage")
    correct = sum(c["expected"] is not None and growth(c) is not None and
                  Decimal(growth(c)) == Decimal(c["expected"]) for c in validation)
    admitted = correct >= config["admission_min_correct"] and all(not violations(c) for c in validation)
    return {"freeze_at": config["freeze_at"], "admitted": admitted,
            "admission_validation_correct": correct,
            "config_sha256": digest(config), "discovery_sha256": digest(discovery),
            "validation_sha256": digest(validation),
            "policy_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def execute(item, policy, frozen):
    if policy == "from_scratch_metadata_solver":
        answer = metadata_solver(item)
        return answer, "metadata_solver_answer" if answer is not None else "metadata_solver_abstain", []
    if policy != "naive_frozen" and not frozen["admitted"]:
        return None, "not_admitted", []
    if policy.startswith("contract"):
        ignored = policy.removeprefix("contract_no_") if "_no_" in policy else None
        failed = [x for x in violations(item) if x != ignored]
        if failed:
            return None, "invocation_revoked", failed
    answer = growth(item)
    return answer, "skill_answer" if answer is not None else "arithmetic_abstain", []


def score(rows):
    total = len(rows)
    accepted = sum(r["answer"] is not None for r in rows)
    correct = sum(r["correct_answer"] for r in rows)
    safe = sum(r["answer"] is None and r["expected"] is None for r in rows)
    return {"n": total, "correct_answers": correct, "wrong_accepted_answers": accepted - correct,
            "abstentions": total - accepted, "safe_abstentions": safe,
            "unnecessary_abstentions": total - accepted - safe,
            "coverage": accepted / total, "correct_answer_rate": correct / total,
            "coverage_conditioned_accuracy": correct / accepted if accepted else None}


def run(items=None, config=None):
    items = cases() if items is None else items
    config = read_config() if config is None else config
    check_splits(items, config)
    discovery = [c for c in items if c["split"] == "discovery"]
    validation = [c for c in items if c["split"] == "validation"]
    with localcontext() as context:
        context.prec = config["decimal_precision"]
        frozen = freeze(discovery, validation, config)
        # 固定策略与准入先完成；之后才把 heldout 交给执行器。
        frozen_hash = digest(frozen)
        heldout = [c for c in items if c["split"] == "heldout"]
        results = {}
        for policy in config["policies"]:
            rows = []
            for item in heldout:
                # 标准答案不传给策略。
                inputs = {k: v for k, v in item.items() if k != "expected"}
                answer, event, reasons = execute(inputs, policy, frozen)
                expected = item["expected"]
                rows.append({"id": item["id"], "scenario": item["scenario"], "answer": answer,
                             "expected": expected, "event": event, "reasons": reasons,
                             "correct_answer": answer is not None and expected is not None and Decimal(answer) == Decimal(expected)})
            results[policy] = {"metrics": score(rows), "cases": rows}
        assert digest(frozen) == frozen_hash, "policy changed during heldout"
    return {
        "benchmark": "constructed deterministic financial skill-contract pilot",
        "not_claimed": ["observed financial data", "LLM experiment", "learned policy", "empirical generalization", "speed or cost advantage"],
        "limitations": ["small hand-written fixtures and policies", "metadata solver solves all answerable cases directly", "contract rejection is invocation-scoped, not permanent skill deletion", "unit transfer only supports equal currency and known multiplicative scale", "date-only timestamps, exact annual windows, no FX or restatement resolution"],
        "versions": {"python": sys.version, "platform": platform.platform(), "decimal": "python stdlib; precision=" + str(config["decimal_precision"])},
        "reproduce": "python experiments/financial_contract_pilot.py --out experiments/artifacts/financial_contract_results.json",
        "frozen": frozen, "frozen_sha256": frozen_hash, "heldout_sha256": digest(heldout),
        "fixtures_sha256": digest(items), "config": config, "fixtures": items, "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "artifacts/financial_contract_results.json")
    args = parser.parse_args()
    result = run()
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({p: r["metrics"] for p, r in result["results"].items()}, indent=2))
