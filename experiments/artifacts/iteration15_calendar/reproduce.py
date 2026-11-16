"""Offline iteration15 verification; preserve historical artifacts and record exit codes."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COMMANDS = [
    ['experiments/simulate_cluster_gate.py', '--reps', '20000', '--clusters', '12', '--tasks-per-cluster', '5', '--seed', '20261105', '--out', str(HERE / 'baseline_reproduction.json')],
    ['experiments/financial_contract_pilot.py', '--out', str(HERE / 'contract_reproduction.json')],
    ['experiments/source_grounded_pilot.py', '--out', str(HERE / 'source_reproduction.json')],
    ['experiments/simulate_null_search.py', '--config', 'experiments/null_search_config.json', '--out-dir', 'experiments/artifacts/iteration12_search', '--verify-only'],
    ['experiments/simulate_shared_baseline.py', '--config', 'experiments/shared_baseline_config.json', '--out-dir', 'experiments/artifacts/iteration13_shared', '--verify-only'],
    ['-m', 'unittest', 'discover', '-s', 'experiments', '-v'],
    ['experiments/calendar_validator_development.py', '--out', str(HERE / 'final_results.json')],
    ['experiments/calendar_validator_development.py', '--out', str(HERE / 'final_reproduction.json'), '--reproduce', str(HERE / 'final_results.json')],
]
manifest = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'python': sys.version, 'platform': platform.platform(),
            'parent_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'api_calls': 0, 'actual_spend': 'unknown; no billing access', 'runs': []}
for index, args in enumerate(COMMANDS):
    command = [sys.executable, *args]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    transcript = result.stdout + '\nSTDERR\n' + result.stderr
    name = 'command_' + str(index + 1) + '.txt'
    (HERE / name).write_text(transcript, encoding='utf-8')
    manifest['runs'].append({'argv': command, 'exit_code': result.returncode, 'transcript': name,
                             'transcript_sha256': hashlib.sha256(transcript.encode()).hexdigest()})
    print(name + ': exit ' + str(result.returncode), flush=True)
    if result.returncode:
        break
manifest['historical_comparisons'] = {}
for new, old in [('baseline_reproduction.json', 'iteration13_shared/baseline_reproduction.json'),
                 ('contract_reproduction.json', 'iteration13_shared/financial_contract_results.json'),
                 ('source_reproduction.json', 'iteration14_financial/source_reference_after_lock_fix.json')]:
    path = HERE / new
    if path.exists():
        fresh = json.loads(path.read_bytes())
        previous = json.loads((ROOT / 'experiments/artifacts' / old).read_bytes())
        manifest['historical_comparisons'][new] = {'full_json_equal': fresh == previous,
            'results_equal': fresh.get('results', fresh.get('rows')) == previous.get('results', previous.get('rows'))}
manifest['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
(HERE / 'execution_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
if len(manifest['runs']) != len(COMMANDS) or any(x['exit_code'] for x in manifest['runs']):
    raise SystemExit(1)
if not all(x['full_json_equal'] for x in manifest['historical_comparisons'].values()):
    raise SystemExit('Historical equality mismatch; inspect manifest.')
print('All eight commands passed; three historical artifacts fully equal.')
