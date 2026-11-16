"""保存离线复现的精确命令、环境、退出码和输出；不联网。"""
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
    [sys.executable, 'experiments/source_grounded_pilot.py', '--out', 'experiments/artifacts/iteration14_financial/source_reference_after_lock_fix.json'],
    [sys.executable, 'experiments/financial_issuer_transfer.py'],
    [sys.executable, '-m', 'unittest', 'discover', '-s', 'experiments', '-p', 'test*financial*.py', '-v'],
    [sys.executable, '-m', 'unittest', 'discover', '-s', 'experiments', '-p', 'test_source_grounded.py', '-v'],
]
manifest = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'platform': platform.platform(), 'python': sys.version, 'cwd': str(ROOT), 'runs': []}
for index, command in enumerate(COMMANDS):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = result.stdout + '\nSTDERR\n' + result.stderr
    name = 'command_' + str(index + 1) + '.txt'
    (HERE / name).write_text(output, encoding='utf-8')
    manifest['runs'].append({'argv': command, 'exit_code': result.returncode, 'transcript': name,
                             'transcript_sha256': hashlib.sha256(output.encode()).hexdigest()})
before = json.loads((HERE / 'source_reference.json').read_bytes())
after = json.loads((HERE / 'source_reference_after_lock_fix.json').read_bytes())
manifest['reference_comparison'] = {'results_equal': before['results'] == after['results'],
                                    'full_json_equal': before == after,
                                    'reason': '源锁修复修改implementation_sha256及pre_execution_lock；结果不变'}
manifest['design_receipt'] = 'design_receipt.json'
before = json.loads((HERE / 'source_reference.json').read_bytes())
after = json.loads((HERE / 'source_reference_after_lock_fix.json').read_bytes())
manifest['source_reference_comparison'] = {'results_equal': before['results'] == after['results'],
    'full_json_equal': before == after,
    'explanation': '旧source runner源锁修复改变implementation_sha与pre_execution_lock；策略输出不变。'}
manifest['reported_by_team_lead_before_lock_fix'] = {
    'verification': '三组既有JSON完全相等、40测试通过；第12/13轮--verify-only完整报告通过。',
    'extra_validator': 'validate_shared_baseline.py因已有receipt防覆盖退出，无修改。',
    'provenance': '主代理消息报告；本收据未重跑这些历史验证；不得与修改后source全JSON一致混同。'}
manifest['design_timing'] = {'claim': '任务定义先写入再下载来源，执行前冻结；作者已见政策与公开摘要。',
    'limitation': '当时未写UTC收据；当前收据不能证明下载前冻结，不补造历史时间。',
    'receipt_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
manifest['input_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in [ROOT/'experiments/financial_issuer_transfer.py', ROOT/'experiments/source_grounded_pilot.py',
              ROOT/'experiments/test_financial_issuer_transfer.py', ROOT/'experiments/test_source_grounded.py',
              ROOT/'experiments/financial_contract_pilot.py', ROOT/'experiments/financial_contract_fixtures.py',
              ROOT/'experiments/financial_contract_config.json', HERE/'task_definition.json', HERE/'source_config.json',
              HERE/'nvda_release.html', HERE/'intc_release.html', Path(__file__)]}
(HERE / 'execution_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
if any(run['exit_code'] for run in manifest['runs']):
    raise SystemExit(1)
print('全部4条离线命令成功；转录与环境已保存。')
