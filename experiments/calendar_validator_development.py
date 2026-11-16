#!/usr/bin/env python3
"""已暴露来源案例上的手写日历验证器开发比较。"""
import argparse
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal, localcontext
import json
from pathlib import Path
import platform
import sys

import financial_issuer_transfer as transfer
import source_grounded_pilot as grounded
from financial_contract_pilot import execute, freeze, growth, read_config, score
from financial_contract_fixtures import cases

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'calendar_validator_config.json'
OUT = ROOT / 'artifacts/iteration15_calendar'
CONVENTIONS = {'MSFT': 'fiscal_july_june', 'NVDA': 'issuer_fiscal_week_calendar',
               'INTC': 'issuer_fiscal_week_calendar'}


def calendar_execute(item, policy, config):
    b, c = item['base'], item['current']
    reasons = []
    semantics = item.get('task_semantics')
    if semantics not in ('reported_adjacent_fiscal_year_growth', 'constant_duration_fiscal_year_growth'):
        reasons.append('unknown_task_semantics')
    if b.get('issuer') != c.get('issuer') or b.get('issuer') != item.get('issuer') or item.get('issuer') not in CONVENTIONS:
        reasons.append('issuer')
    if b.get('convention') != c.get('convention') or b.get('convention') != CONVENTIONS.get(item.get('issuer')):
        reasons.append('convention')
    if b.get('currency') != c.get('currency') or b.get('currency') != 'USD':
        reasons.append('currency')
    if b.get('metric') != c.get('metric') or b.get('metric') != 'GAAP_total_revenue':
        reasons.append('metric')
    if any(x.get('scale') not in config['known_scales'] for x in (b, c)):
        reasons.append('unknown_scale')
    if any(x.get('period_kind') != 'annual' or type(x.get('fiscal_year')) is not int for x in (b, c)):
        reasons.append('annual_metadata')
    else:
        if c['fiscal_year'] != b['fiscal_year'] + 1:
            reasons.append('nonadjacent_fiscal_year')
    try:
        starts = [date.fromisoformat(x['start']) for x in (b, c)]
        ends = [date.fromisoformat(x['end']) for x in (b, c)]
        lengths = [(end - start).days + 1 for start, end in zip(starts, ends)]
        if starts[1] != ends[0] + timedelta(days=1):
            reasons.append('noncontiguous_periods')
        if any(x.get('fiscal_year') != end.year for x, end in zip((b, c), ends)):
            reasons.append('false_fiscal_year_metadata')
        if b.get('convention') == 'fiscal_july_june':
            valid = all(n in config['calendar_days'] and start.month == 7 and start.day == 1 and
                        end.month == 6 and end.day == 30 and end.year == start.year + 1
                        for start, end, n in zip(starts, ends, lengths))
        elif b.get('convention') == 'issuer_fiscal_week_calendar':
            valid = all(n in config['week_calendar_days'] for n in lengths) and starts[0].weekday() == starts[1].weekday()
        else:
            valid = False
        if not valid:
            reasons.append('annual_duration')
        if semantics == 'constant_duration_fiscal_year_growth' and lengths[0] != lengths[1]:
            reasons.append('unequal_duration_for_constant_duration_task')
        if policy != 'calendar_no_availability':
            decision = date.fromisoformat(item['decision_at'])
            available = [date.fromisoformat(x['available_at']) for x in (b, c)]
            if any(a > decision or end > decision or a < end for a, end in zip(available, ends)):
                reasons.append('availability')
    except (ValueError, TypeError, KeyError):
        reasons.append('invalid_dates')
    if Decimal(b['value']) == 0:
        reasons.append('zero_base')
    if reasons:
        return None, 'ordinary_validator_abstain', reasons
    answer = growth(item, normalize=policy != 'calendar_no_unit_normalization')
    return answer, 'ordinary_validator_answer', []


def build_inputs():
    msft, msft_evidence, _, values = grounded.load_inputs()
    definition, external, external_evidence, pairs = transfer.load(transfer.ARTIFACTS)
    items = grounded.build_items(msft, values)
    for item in items:
        item['id'] = 'MSFT_' + item['id']
        item['issuer'] = 'MSFT'
    for source in external['sources']:
        base, current = pairs[source['ticker']]
        common = {'currency': 'USD', 'scale': '1000000', 'metric': 'GAAP_total_revenue',
                  'convention': source['convention'], 'available_at': source['publication_date']}
        for spec in definition['scenarios_per_issuer']:
            item = {'id': source['ticker'] + spec['suffix'], 'issuer': source['ticker'],
                    'scenario': spec['scenario'],
                    'decision_at': str(date.fromisoformat(source['publication_date']) + timedelta(days=spec['decision_offset_days'])),
                    'base': {**common, 'value': base, 'start': source['base_start'], 'end': source['base_end']},
                    'current': {**common, 'value': current, 'start': source['current_start'], 'end': source['current_end']},
                    'provenance': 'observed company annual values; author-constructed fiscal starts and decision date'}
            if spec['unit_conversion']:
                item['current'].update(value=str(Decimal(current) / 1000), scale='1000000000')
            items.append(item)
    for item in items:
        item['task_semantics'] = 'reported_adjacent_fiscal_year_growth'
        item['metadata_basis'] = 'Explicit author task metadata; fiscal years match reported year-end labels; starts for NVDA/INTC are inferred, not source-verified week counts.'
        for record in (item['base'], item['current']):
            record.update(issuer=item['issuer'], period_kind='annual', fiscal_year=date.fromisoformat(record['end']).year)
    # 目标的可用性来自已固定的旧情境定义，不调用新验证器决定答案。
    available = {('MSFT_' + spec['id']): spec['expected_available'] for spec in msft['cases']}
    available.update({source['ticker'] + spec['suffix']: spec['answerable'] for source in external['sources'] for spec in definition['scenarios_per_issuer']})
    all_pairs = {'MSFT': (values[1], values[0]), **pairs}
    return items, available, all_pairs, msft_evidence + external_evidence, msft, external, definition


def run_config_for_test():
    return json.loads(CONFIG.read_bytes())


def run(config_path=CONFIG):
    config = json.loads(config_path.read_bytes())
    items, available, pairs, evidence, msft, external, definition = build_inputs()
    training = cases()
    frozen = freeze([x for x in training if x['split'] == 'discovery'],
                    [x for x in training if x['split'] == 'validation'], read_config())
    targets = {x['id']: transfer.arithmetic_oracle(*pairs[x['issuer']], config['decimal_places']) if available[x['id']] else None for x in items}
    paths = [config_path, ROOT / 'source_grounded_config.json', transfer.ARTIFACTS / 'source_config.json',
             transfer.ARTIFACTS / 'task_definition.json']
    paths += [grounded.ARTIFACTS / x['file'] for x in msft['sources']]
    paths += [transfer.ARTIFACTS / x['file'] for x in external['sources']]
    paths += [ROOT / name for name in ('calendar_validator_development.py', 'test_calendar_validator.py',
              'financial_issuer_transfer.py', 'source_grounded_pilot.py', 'financial_contract_pilot.py',
              'financial_contract_fixtures.py', 'financial_contract_config.json')]
    snapshots = [(p, transfer.sha(p.read_bytes())) for p in paths]
    def verify():
        for path, expected in snapshots:
            if transfer.sha(path.read_bytes()) != expected:
                raise AssertionError('fixed disk input changed: ' + path.name)
    environment = {'python': sys.version, 'platform': platform.platform(),
                   'python_executable_sha256': transfer.sha(Path(sys.executable).read_bytes())}
    lock = {'environment': deepcopy(environment), 'config': deepcopy(config), 'items': deepcopy(items), 'oracle_targets': targets,
            'source_evidence': evidence, 'old_frozen_admission': deepcopy(frozen),
            'old_scenario_definitions': {'MSFT': msft, 'external': definition},
            'disk_sha256': {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): h for p, h in snapshots}}
    lock_hash = transfer.sha(json.dumps(lock, sort_keys=True).encode())
    results = {}
    with localcontext() as context:
        context.prec = config['precision']
        quantum = Decimal(1).scaleb(-config['decimal_places'])
        for policy in config['policies']:
            rows = []
            for item in items:
                verify()
                actual, actual_config, actual_frozen = deepcopy(item), deepcopy(config), deepcopy(frozen)
                if policy.startswith('calendar_'):
                    answer, event, reasons = calendar_execute(actual, policy, actual_config)
                else:
                    answer, event, reasons = execute(actual, policy, actual_frozen)
                if (actual, actual_config, actual_frozen) != (item, config, frozen):
                    raise AssertionError('executor mutated fixed actual inputs')
                verify()
                target = targets[item['id']]
                rows.append({'id': item['id'], 'issuer': item['issuer'], 'scenario': item['scenario'],
                             'answer': answer, 'expected': target, 'event': event, 'reasons': reasons,
                             'correct_answer': answer is not None and target is not None and Decimal(answer).quantize(quantum) == Decimal(target)})
            results[policy] = {'metrics': score(rows), 'cases': rows,
                               'by_issuer': {ticker: score([r for r in rows if r['issuer'] == ticker]) for ticker in CONVENTIONS}}
    verify()
    if lock_hash != transfer.sha(json.dumps(lock, sort_keys=True).encode()):
        raise AssertionError('fixed in-memory lock changed')
    return {'benchmark': 'iteration15 calendar-aware ordinary-validator DEVELOPMENT comparison',
            'pre_execution_lock': lock, 'pre_execution_lock_sha256': lock_hash, 'results': results,
            'environment': environment,
            'limitations': ['Previously exposed sources and nine dependent scenarios from three annual pairs; author-visible development only.',
                            'Handwritten ordinary rules, no evolution, LLM, holdout, population-effect or threshold-proof claim.',
                            'Date-only selected release availability, not earliest publication or historical archive proof.',
                            'Week-year starts are inferred metadata; duration acceptance is an author rule, not source fact.',
                            'Reported annual growth may compare unequal 52/53-week years; constant-duration task rejects unequal lengths.',
                            'Only USD GAAP total revenue, three issuer conventions and enumerated positive scales; no FX/restatement resolution.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=OUT / 'results.json')
    parser.add_argument('--reproduce', type=Path)
    args = parser.parse_args()
    result = run()
    if args.reproduce is not None:
        previous = json.loads(args.reproduce.read_bytes())
        if previous != result:
            raise AssertionError('full result equality reproduction failed')
    args.out.parent.mkdir(parents=False, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {'design': result['benchmark'], 'pre_execution_lock_sha256': result['pre_execution_lock_sha256'],
               'metrics': {p: r['metrics'] for p, r in result['results'].items()},
               'equality_reproduced': args.reproduce is not None, 'limitations': result['limitations']}
    (args.out.parent / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))
