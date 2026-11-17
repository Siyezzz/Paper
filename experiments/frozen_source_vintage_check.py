#!/usr/bin/env python3
"""冻结既有策略后的新来源年份检查；无模型调用。"""
import argparse
from copy import deepcopy
from datetime import date, timedelta, datetime, timezone
from decimal import Decimal, localcontext
import json
from pathlib import Path
import platform
import re
import sys

import calendar_validator_development as calendar
import financial_issuer_transfer as transfer
from financial_contract_pilot import execute, freeze, read_config, score
from financial_contract_fixtures import cases

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / 'experiments/artifacts/iteration16_vintage'


def verify_freeze():
    receipt = json.loads((HERE / 'freeze_receipt.json').read_bytes())
    for name, expected in receipt['sha256'].items():
        if transfer.sha((ROOT / name).read_bytes()) != expected:
            raise AssertionError('frozen bytes changed: ' + name)
    return receipt


def load_source():
    source = json.loads((HERE / 'source_config.json').read_bytes())
    raw = (HERE / source['file']).read_bytes()
    if transfer.sha(raw) != source['sha256']:
        raise ValueError('source hash mismatch')
    content = transfer.normalized(raw)
    match = re.search(source['row_pattern'], content)
    if not match:
        raise ValueError('annual GAAP row missing')
    current, base = [value.replace(',', '') for value in match.groups()]
    if (current, base) != (source['oracle_current'], source['oracle_base']):
        raise ValueError('source disagrees with separate transcription')
    excerpts = []
    for needle in source['needles']:
        offset = content.index(needle)
        excerpts.append({'normalized_offset': offset, 'quote': content[max(0, offset-100):offset+len(needle)+160]})
    old = ROOT / source['prior_endpoint_file']
    if transfer.sha(old.read_bytes()) != source['prior_endpoint_sha256']:
        raise ValueError('prior endpoint archive changed')
    prior = transfer.normalized(old.read_bytes())
    offset = prior.index('Twelve Months Ended January 26, January 28, January 26, January 28, 2025 2024 2025 2024')
    excerpts.append({'basis': 'prior company archive, inferred base start follows FY2024 endpoint', 'quote': prior[max(0, offset-100):offset+150]})
    return source, base, current, excerpts


def build_items(definition, source, base, current):
    common = {'issuer':'NVDA', 'currency':'USD', 'scale':'1000000',
              'metric':'GAAP_total_revenue', 'convention':'issuer_fiscal_week_calendar',
              'available_at':source['publication_date'], 'period_kind':'annual'}
    items, targets = [], {}
    oracle = transfer.arithmetic_oracle(base, current, 12)
    for spec in definition['scenarios']:
        item = {'id':spec['id'], 'issuer':'NVDA', 'scenario':spec['id'],
                'task_semantics':definition['semantics'].split(';')[0],
                'decision_at':str(date.fromisoformat(source['publication_date'])+timedelta(days=spec['decision_offset_days'])),
                'base':{**common, 'value':base, 'fiscal_year':2025, 'start':'2024-01-29', 'end':'2025-01-26'},
                'current':{**common, 'value':current, 'fiscal_year':2026, 'start':'2025-01-27', 'end':'2026-01-25'},
                'provenance':'Observed annual totals/endpoints and reported FY labels; starts inferred from prior endpoints; selected-release availability and decisions constructed.'}
        if spec['convert_current_to_billions']:
            item['current'].update(value=str(Decimal(current)/1000), scale='1000000000')
        targets[item['id']] = oracle if spec['answerable'] else None
        items.append(item)
    return items, targets


def run():
    receipt = verify_freeze()
    definition = json.loads((HERE/'task_definition.json').read_bytes())
    source, base, current, excerpts = load_source()
    items, targets = build_items(definition, source, base, current)
    config = calendar.run_config_for_test()
    training = cases()
    frozen = freeze([x for x in training if x['split']=='discovery'], [x for x in training if x['split']=='validation'], read_config())
    paths = [Path(__file__), HERE/'source_config.json', HERE/source['file'], HERE/'freeze_receipt.json']
    paths += [ROOT/name for name in receipt['sha256']]
    paths += [ROOT/'experiments/financial_issuer_transfer.py', ROOT/'experiments/artifacts/iteration16_vintage/reproduce.py', ROOT/source['prior_endpoint_file']]
    disk = {str(p.relative_to(ROOT)):transfer.sha(p.read_bytes()) for p in paths}
    def verify():
        for name, expected in disk.items():
            if transfer.sha((ROOT/name).read_bytes()) != expected:
                raise AssertionError('fixed disk bytes changed: '+name)
    results = {}
    with localcontext() as context:
        context.prec = config['precision']
        for policy in definition['policies']:
            rows = []
            for item in items:
                verify()
                actual, actual_config, actual_frozen = deepcopy(item), deepcopy(config), deepcopy(frozen)
                if policy.startswith('calendar_'):
                    answer, event, reasons = calendar.calendar_execute(actual, policy, actual_config)
                else:
                    answer, event, reasons = execute(actual, policy, actual_frozen)
                if (actual, actual_config, actual_frozen) != (item, config, frozen):
                    raise AssertionError('executor mutated fixed actual inputs')
                verify()
                target = targets[item['id']]
                rows.append({'id':item['id'], 'answer':answer, 'expected':target, 'event':event, 'reasons':reasons,
                             'correct_answer':answer is not None and target is not None and Decimal(answer).quantize(Decimal('0.000000000001'))==Decimal(target)})
            results[policy] = {'metrics':score(rows), 'cases':rows}
    return {'benchmark':'iteration16 frozen source-vintage check; same AI process, separate task author',
            'freeze_receipt':receipt, 'definition':definition, 'source':source, 'source_excerpts':excerpts,
            'items':items, 'oracle_targets':targets, 'old_frozen_admission':frozen, 'disk_sha256':disk, 'results':results,
            'environment':{'python':sys.version, 'platform':platform.platform(), 'python_executable_sha256':transfer.sha(Path(sys.executable).read_bytes()), 'seed':None, 'api_calls':0},
            'limitations':['One new annual pair from a previously exposed issuer; not independent clusters.', 'Current company web snapshot; not historical archive or earliest-availability proof.', 'Starts inferred; decision dates, availability convention and unit change constructed.', 'Policies handwritten and unchanged; no learned skills or live LLM execution.', 'Source extraction and oracle transcription author-written; same AI research process; no blind or independent-researcher claim.', 'No population inference, market performance, threshold tuning or external preregistration.']}


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=HERE/'vintage_results.json')
    parser.add_argument('--reproduce', type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit('refuse to overwrite output')
    started = datetime.now(timezone.utc).isoformat()
    result = run()
    if args.reproduce and json.loads(args.reproduce.read_bytes()) != result:
        raise AssertionError('full JSON reproduction mismatch')
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    execution = {'started_utc':started, 'ended_utc':datetime.now(timezone.utc).isoformat(), 'argv':sys.argv, 'cwd':str(Path.cwd()), 'output_sha256':transfer.sha(args.out.read_bytes()), 'full_json_equal':bool(args.reproduce)}
    args.out.with_suffix('.receipt.json').write_text(json.dumps(execution,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({p:r['metrics'] for p,r in result['results'].items()},indent=2))
