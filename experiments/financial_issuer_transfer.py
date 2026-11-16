#!/usr/bin/env python3
"""作者设计外部发行人迁移检查；公司原始收入与显式构造情境，非LLM实验。"""
import argparse
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal, localcontext
from fractions import Fraction
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
ARTIFACTS = ROOT / 'artifacts/iteration14_financial'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized(raw):
    content = raw.decode('utf-8-sig')
    content = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', content, flags=re.I | re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', content)))


def arithmetic_oracle(base, current, places):
    # 整数有理数及显式ties-to-even舍入，不调用被测growth或Decimal除法。
    rational = Fraction((int(current) - int(base)) * 100, int(base))
    scaled = rational * 10 ** places
    sign = -1 if scaled < 0 else 1
    quotient, remainder = divmod(abs(scaled.numerator), scaled.denominator)
    if 2 * remainder > scaled.denominator or (2 * remainder == scaled.denominator and quotient % 2):
        quotient += 1
    signed = sign * quotient
    digits = str(abs(signed)).zfill(places + 1)
    return ('-' if signed < 0 else '') + digits[:-places] + '.' + digits[-places:]


def load(folder):
    definition = json.loads((folder / 'task_definition.json').read_bytes())
    config = json.loads((folder / 'source_config.json').read_bytes())
    evidence, values = [], {}
    for source in config['sources']:
        raw = (folder / source['file']).read_bytes()
        if sha(raw) != source['sha256']:
            raise ValueError('source SHA256 mismatch: ' + source['file'])
        content = normalized(raw)
        match = re.search(source['row_pattern'], content)
        if not match:
            raise ValueError('annual source row missing')
        current, base = [v.replace(',', '') for v in match.groups()]
        if (current, base) != (source['oracle_current'], source['oracle_base']):
            raise ValueError('source disagrees with independently transcribed oracle')
        excerpts = []
        for needle in (source['annual_label_needle'], source['date_needle'], source['unit_needle'], source['window_needle'], 'Twelve Months Ended', match.group()):
            offset = content.index(needle)
            excerpts.append({'needle': needle, 'normalized_offset': offset,
                             'quote': content[max(0, offset - 100):offset + len(needle) + 130]})
        evidence.append({**source, 'bytes': len(raw), 'normalized_sha256': sha(content.encode()), 'excerpts': excerpts})
        values[source['ticker']] = (base, current)
    if [s['ticker'] for s in config['sources']] != definition['issuers']:
        raise ValueError('issuer definition mismatch')
    return definition, config, evidence, values


def run(folder=ARTIFACTS):
    definition, config, evidence, values = load(folder)
    paths = [folder / name for name in ('task_definition.json', 'source_config.json')]
    paths += [folder / s['file'] for s in config['sources']]
    paths += [ROOT / name for name in ('financial_issuer_transfer.py', 'financial_contract_pilot.py',
                                      'financial_contract_fixtures.py', 'financial_contract_config.json')]
    disk_lock = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths if p.is_relative_to(ROOT)}
    # 临时目录测试时也锁住实际的外部副本。
    snapshots = [(p, sha(p.read_bytes())) for p in paths]
    def verify():
        for path, expected in snapshots:
            if sha(path.read_bytes()) != expected:
                raise AssertionError('fixed disk input changed: ' + path.name)

    training = cases()
    frozen = freeze([x for x in training if x['split'] == 'discovery'],
                    [x for x in training if x['split'] == 'validation'], read_config())
    items, targets = [], {}
    for source in config['sources']:
        ticker = source['ticker']
        base, current = values[ticker]
        number = arithmetic_oracle(base, current, definition['decimal_places'])
        common = {'currency': 'USD', 'scale': '1000000', 'metric': 'GAAP_total_revenue',
                  'convention': source['convention'], 'available_at': source['publication_date']}
        for spec in definition['scenarios_per_issuer']:
            item = {'id': ticker + spec['suffix'], 'issuer': ticker, 'scenario': spec['scenario'],
                    'decision_at': str(date.fromisoformat(source['publication_date']) + timedelta(days=spec['decision_offset_days'])),
                    'base': {**common, 'value': base, 'start': source['base_start'], 'end': source['base_end']},
                    'current': {**common, 'value': current, 'start': source['current_start'], 'end': source['current_end']},
                    'provenance': 'observed company annual values; constructed decision date; inferred fiscal starts'}
            if spec['unit_conversion']:
                item['current'].update(value=str(Decimal(current) / 1000), scale='1000000000')
                item['provenance'] += '; constructed equivalent current billion-USD representation'
            targets[item['id']] = number if spec['answerable'] else None
            items.append(item)
    lock = {'definition': definition, 'source_config': config, 'sources': evidence,
            'disk_sha256': disk_lock, 'items': deepcopy(items), 'frozen': deepcopy(frozen), 'oracle_targets': targets}
    lock_hash = sha(json.dumps(lock, sort_keys=True).encode())
    results = {}
    with localcontext() as context:
        context.prec = definition['precision']
        quantum = Decimal(1).scaleb(-definition['decimal_places'])
        for policy in definition['policies']:
            rows = []
            for item in items:
                verify()
                actual_item, actual_frozen = deepcopy(item), deepcopy(frozen)
                answer, event, reasons = execute(actual_item, policy, actual_frozen)
                if actual_item != item or actual_frozen != frozen:
                    raise AssertionError('executor mutated fixed actual inputs')
                verify()
                target = targets[item['id']]
                correct = answer is not None and target is not None and Decimal(answer).quantize(quantum) == Decimal(target)
                rows.append({'id': item['id'], 'issuer': item['issuer'], 'scenario': item['scenario'],
                             'answer': answer, 'expected': target, 'correct_answer': correct,
                             'event': event, 'reasons': reasons})
            results[policy] = {'metrics': score(rows), 'cases': rows,
                               'by_issuer': {ticker: score([r for r in rows if r['issuer'] == ticker]) for ticker in definition['issuers']}}
    verify()
    if lock_hash != sha(json.dumps(lock, sort_keys=True).encode()):
        raise AssertionError('fixed in-memory lock changed')
    return {'benchmark': 'author-designed external issuer transfer check; deterministic handwritten policies',
            'pre_execution_lock': lock, 'pre_execution_lock_sha256': lock_hash, 'results': results,
            'environment': {'python': sys.version, 'platform': platform.platform(),
                            'argv': sys.argv, 'working_directory': str(Path.cwd()),
                            'python_executable_sha256': sha(Path(sys.executable).read_bytes())},
            'limitations': ['two new issuers, one annual pair each; three dependent scenarios per issuer',
                            'author-visible policies and sources; neither blinded nor independent-author holdout',
                            'selected release date is a convention, not earliest publication proof; date-only',
                            'current web snapshots, not historical archives; no filing-vintage or restatement proof',
                            'fiscal starts are analyst-constructed labels, not source-verified week counts; adjacent reported fiscal years compared without per-day or constant-week normalization',
                            'source extraction is issuer-specific, hand-authored, not an evaluated autonomous extraction model',
                            'all policies unchanged; constructed admission fixtures still apply; no learned evolution',
                            'no model-generated programs, live LLM API, market decisions, timing/cost advantage or population-effect claim']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ARTIFACTS / 'results.json')
    args = parser.parse_args()
    result = run()
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({p: r['metrics'] for p, r in result['results'].items()}, indent=2))
