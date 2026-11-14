#!/usr/bin/env python3
"""保留既有证据，在独立目录运行固定复现并记录命令及哈希。"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments/artifacts/iteration12_search"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest_path = OUT / "reproduction_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("refusing to overwrite manifest")
    names = ["simulate_cluster_gate.py", "test_simulation.py", "financial_contract_pilot.py",
             "financial_contract_fixtures.py", "financial_contract_config.json", "test_financial_contract.py",
             "source_grounded_pilot.py", "source_grounded_config.json", "test_source_grounded.py",
             "simulate_null_search.py", "test_null_search.py", "null_search_config.json", "reproduce_null_search.py"]
    inputs = {"experiments/" + name: sha(ROOT / "experiments" / name) for name in names}
    for name in ("msft_ar24.html", "msft_fy24_income.html", "msft_fy24_release.html"):
        path = ROOT / "experiments/artifacts/source_grounded" / name
        inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = sha(path)
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(),
                "cwd": str(ROOT), "python": sys.version, "executable": sys.executable,
                "platform": platform.platform(), "numpy": np.__version__, "scipy": scipy.__version__,
                "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "inputs_sha256_before_execution": inputs, "commands": [],
                "api_calls": 0, "credentials_read": False,
                "existing_multi_model_api_directory": "not opened, hashed, modified, or traversed",
                "evidence_note": "Configuration fixed before results; author-designed, not externally preregistered."}
    commands = [
        (["experiments/simulate_cluster_gate.py", "--reps", "20000", "--clusters", "12", "--tasks-per-cluster", "5", "--seed", "20261105", "--out", "experiments/artifacts/iteration12_search/baseline_reproduction.json"], "baseline_stdout.txt"),
        (["experiments/financial_contract_pilot.py", "--out", "experiments/artifacts/iteration12_search/financial_contract_results.json"], "contract_stdout.txt"),
        (["experiments/source_grounded_pilot.py", "--out", "experiments/artifacts/iteration12_search/source_grounded_results.json"], "source_grounded_stdout.txt"),
        (["experiments/simulate_null_search.py", "--config", "experiments/null_search_config.json", "--out-dir", "experiments/artifacts/iteration12_search"], "null_search_stdout.txt"),
        (["experiments/simulate_null_search.py", "--config", "experiments/null_search_config.json", "--out-dir", "experiments/artifacts/iteration12_search", "--verify-only"], "raw_verification.txt"),
        (["-m", "unittest", "discover", "-s", "experiments", "-v"], "test_results.txt"),
    ]
    for args, log in commands:
        started = datetime.now(timezone.utc).isoformat()
        proc = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (OUT / log).write_text(proc.stdout + proc.stderr, encoding="utf-8")
        manifest["commands"].append({"argv": [sys.executable, *args], "started_utc": started,
                                     "ended_utc": datetime.now(timezone.utc).isoformat(), "returncode": proc.returncode,
                                     "output": log})
        print(f"{log}: exit {proc.returncode}", flush=True)
        if proc.returncode:
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            raise RuntimeError("reproduction command failed: " + log)
    pairs = [("baseline_reproduction.json", "baseline_reproduction.json"),
             ("financial_contract_results.json", "financial_contract_results.json"),
             ("source_grounded_results.json", "source_grounded/results.json")]
    manifest["existing_evidence_comparison"] = {}
    for fresh, old in pairs:
        new = json.loads((OUT / fresh).read_text(encoding="utf-8"))
        prior = json.loads((ROOT / "experiments/artifacts" / old).read_text(encoding="utf-8"))
        manifest["existing_evidence_comparison"][fresh] = {
            "full_json_equal": new == prior,
            "results_equal": new.get("results", new.get("rows")) == prior.get("results", prior.get("rows"))}
    manifest["inputs_unchanged"] = all(sha(ROOT / name) == value for name, value in inputs.items())
    manifest["artifacts_sha256"] = {path.name: sha(path) for path in sorted(OUT.iterdir()) if path.is_file()}
    manifest["ended_utc"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["existing_evidence_comparison"], indent=2))


if __name__ == "__main__":
    main()
