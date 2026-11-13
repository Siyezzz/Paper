#!/usr/bin/env python3
"""真实财报数值与显式构造情境的确定性来源审计，不是 LLM 实验。"""
import argparse
from copy import deepcopy
from decimal import Decimal, localcontext
import hashlib
import html
import json
from pathlib import Path
import platform
import re
import sys

from financial_contract_pilot import execute, freeze, read_config, score
from financial_contract_fixtures import cases

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / 'artifacts/source_grounded'
CONFIG = ROOT / 'source_grounded_config.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(raw):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw.decode('utf-8-sig'))))


def excerpt(content, needle, before=160, after=340):
    offset = content.index(needle)
    return {'needle': needle, 'normalized_text_offset': offset,
            'quote': content[max(0, offset-before):offset+after]}


def load_inputs(config_path=CONFIG, source_dir=ARTIFACTS):
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    evidence = []
    for entry in config['sources']:
        raw = (source_dir / entry['file']).read_bytes()
        if sha(raw) != entry['sha256']:
            raise ValueError('source SHA256 mismatch: ' + entry['file'])
        evidence.append({**entry, 'bytes': len(raw), 'text': text(raw)})
    annual, income, release = [e['text'] for e in evidence]
    extracted = []
    for content in (annual, income):
        match = re.search(r'Total revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)', content)
        if not match:
            raise ValueError('annual revenue row missing')
        current, base = [x.replace(',', '') for x in match.groups()[:2]]
        if (current, base) != (config['oracle_current_million_usd'], config['oracle_base_million_usd']):
            raise ValueError('source values disagree with independent oracle')
        extracted.append((current, base))
        if 'Year Ended June 30, 2024 2023 2022' not in content or 'In millions, except per share amounts' not in content:
            raise ValueError('reporting window/unit context missing')
    if 'July 30, 2024' not in release or 'Total revenue 64,727 56,189 245,122 211,915' not in release:
        raise ValueError('dated release does not corroborate exact annual numbers')
    if 'Twelve Months Ended June 30' not in release:
        raise ValueError('release annual period evidence missing')
    for entry in evidence:
        content = entry.pop('text')
        needles = ['Total revenue', 'Year Ended June 30, 2024 2023 2022'] if entry['file'] != 'msft_fy24_release.html' else ['July 30, 2024', 'Total revenue 64,727 56,189 245,122 211,915', 'Twelve Months Ended June 30']
        entry['excerpts'] = [excerpt(content, needle) for needle in needles]
        entry['normalized_text_sha256'] = sha(content.encode())
    return config, evidence, sha(config_bytes), extracted[0]


def oracle(config):
    # 独立有理数答案：分子/分母由配置固定，不调用被测 growth、violations 或 metadata_solver。
    with localcontext() as ctx:
        ctx.prec = 80
        numerator = Decimal(config['oracle_growth_numerator'])
        denominator = Decimal(config['oracle_growth_denominator'])
        if numerator != (Decimal(config['oracle_current_million_usd']) - Decimal(config['oracle_base_million_usd'])) * 100 or denominator != Decimal(config['oracle_base_million_usd']):
            raise ValueError('oracle rational identity mismatch')
        return str((numerator / denominator).quantize(Decimal(1).scaleb(-config['oracle_decimal_places'])))


def build_items(config, values):
    current, base = values
    common = {'currency': 'USD', 'scale': '1000000', 'metric': 'GAAP_total_revenue',
              'convention': 'fiscal_july_june', 'available_at': config['publication_date']}
    result = []
    for spec in config['cases']:
        item = {'id': spec['id'], 'scenario': spec['scenario'], 'decision_at': spec['decision_at'],
                'base': {**common, 'value': base, 'start': '2022-07-01', 'end': '2023-06-30'},
                'current': {**common, 'value': current, 'start': '2023-07-01', 'end': '2024-06-30'},
                'provenance': 'observed annual revenue; analyst-selected decision date, not an observed trading decision'}
        if spec['constructed_scale_conversion']:
            item['current'].update(value=str(Decimal(current) / 1000), scale='1000000000')
            item['provenance'] += '; constructed equivalent representation, not an observed unit change'
        result.append(item)
    return result


def run(config_path=CONFIG, source_dir=ARTIFACTS):
    # 完整读入、核验来源及固定配置先于执行与评分。
    config, evidence, config_hash, values = load_inputs(config_path, source_dir)
    with localcontext() as ctx:
        ctx.prec = config['decimal_precision']
        expected_number = oracle(config)
        items = build_items(config, values)
        original_config = read_config()
        training = cases()
        frozen = freeze([x for x in training if x['split'] == 'discovery'],
                        [x for x in training if x['split'] == 'validation'], original_config)
        expected = {s['id']: expected_number if s['expected_available'] else None for s in config['cases']}
        lock = {'config_sha256': config_hash, 'sources': evidence, 'frozen': frozen,
                'items': deepcopy(items), 'expected': expected,
                'implementation_sha256': {p.name: sha(p.read_bytes()) for p in [Path(__file__), ROOT/'financial_contract_pilot.py', ROOT/'financial_contract_fixtures.py', ROOT/'financial_contract_config.json', ROOT/'source_grounded_config.json', ROOT/'test_source_grounded.py']}}
        lock_hash = sha(json.dumps(lock, sort_keys=True).encode())
        results = {}
        quantum = Decimal(1).scaleb(-config['oracle_decimal_places'])
        for policy in config['policies']:
            rows = []
            for item in items:
                answer, event, reasons = execute(deepcopy(item), policy, deepcopy(frozen))
                target = expected[item['id']]
                correct = answer is not None and target is not None and Decimal(answer).quantize(quantum) == Decimal(target)
                rows.append({'id': item['id'], 'scenario': item['scenario'], 'answer': answer, 'expected': target,
                             'correct_answer': correct, 'event': event, 'reasons': reasons})
            results[policy] = {'metrics': score(rows), 'cases': rows}
        if lock_hash != sha(json.dumps(lock, sort_keys=True).encode()):
            raise AssertionError('fixed inputs changed during scoring')
    return {'benchmark': 'source-grounded deterministic arithmetic micro-pilot with constructed scenarios',
            'config': config, 'pre_execution_lock': lock, 'pre_execution_lock_sha256': lock_hash,
            'environment': {'python': sys.version, 'platform': platform.platform(),
                            'python_executable_sha256': sha(Path(sys.executable).read_bytes())},
            'results': results,
            'limitations': config['claims_excluded'] + ['one company and one annual pair; cases are dependent',
                'July 30 is selected release availability, not earliest publication proof',
                'both years use the same selected release vintage; no historical web archive',
                'date-only availability, exact annual windows, no restatement or FX resolution',
                'oracle independently implemented but authored by the same researcher who can inspect policies',
                'original constructed fixtures still supply admission; no source-grounded training or policy learning']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ARTIFACTS/'results.json')
    args = parser.parse_args()
    result = run()
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({p: r['metrics'] for p, r in result['results'].items()}, indent=2))
