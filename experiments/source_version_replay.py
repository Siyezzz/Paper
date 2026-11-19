"""Replay constructed withdrawals against previously archived revenue inputs."""
import argparse
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import sys

import calendar_validator_development as calendar
import financial_issuer_transfer as transfer

HERE = Path(__file__).resolve().parent
DESIGN = HERE / 'source_version_replay.json'


def source_items():
    _, config, _, pairs = transfer.load(transfer.ARTIFACTS)
    items = {}
    targets = {}
    for source in config['sources']:
        ticker = source['ticker']
        base, current = pairs[ticker]
        common = dict(issuer=ticker, currency='USD', scale='1000000', metric='GAAP_total_revenue',
                      convention=source['convention'], available_at=source['publication_date'], period_kind='annual')
        pair = dict(issuer=ticker, task_semantics='reported_adjacent_fiscal_year_growth',
                    decision_at=str(date.fromisoformat(source['publication_date']) + timedelta(days=1)))
        for role, value in [('base', base), ('current', current)]:
            end = source[role + '_end']
            pair[role] = dict(common, value=value, start=source[role + '_start'], end=end,
                              fiscal_year=date.fromisoformat(end).year)
        items[ticker, 'native'] = pair
        targets[ticker] = transfer.arithmetic_oracle(base, current, 12)
    converted = deepcopy(items['NVDA', 'native'])
    converted['current'].update(value=str(Decimal(converted['current']['value']) / 1000), scale='1000000000')
    items['NVDA', 'converted'] = converted
    return items, targets, config['sources']


def replay(design, policy, items, targets, config):
    authority = design['initial'].copy()
    cache = {}
    rows = []
    query_index = 0
    for index, step in enumerate(design['steps'], start=1):
        if 'update' in step:
            ticker = step['update']
            authority[ticker] = step['version']
            evicted = []
            if step['notify']:
                if policy == 'selective_notification' and ticker in cache:
                    evicted = [ticker]
                elif policy == 'global_notification':
                    evicted = sorted(cache)
            for key in evicted:
                del cache[key]
            rows.append(dict(step=index, event='update', issuer=ticker, new_version=step['version'],
                             notification_delivered=step['notify'], evicted=evicted))
            continue

        ticker = step['query']
        cached = cache.get(ticker)
        consult = policy in ('always_read', 'conditional_read') or cached is None
        version = authority[ticker] if consult else cached
        read = version is not None and (policy == 'always_read' or cached != version)
        if version is None:
            cache.pop(ticker, None)
            answer, reasons = None, ['no_eligible_source']
        else:
            if policy != 'always_read':
                cache[ticker] = version
            answer, _, reasons = calendar.calendar_execute(items[ticker, version], 'calendar_ordinary', config)
        expected = design['expected_query_versions'][query_index]
        query_index += 1
        if expected != authority[ticker]:
            raise ValueError('independently listed oracle version disagrees with source timeline')
        arithmetic_ok = (answer is not None and expected is not None and
                         Decimal(answer).quantize(Decimal('0.000000000001')) == Decimal(targets[ticker]))
        if answer is None:
            outcome = 'safe_abstention' if expected is None else 'unnecessary_abstention'
        else:
            outcome = 'correct' if arithmetic_ok and version == expected else 'wrong_accepted'
        rows.append(dict(step=index, event='query', issuer=ticker, version=version, expected_version=expected,
                         answer=answer, expected_answer=None if expected is None else targets[ticker],
                         outcome=outcome, reasons=reasons, metadata_consult=consult, payload_read=read))
    if query_index != len(design['expected_query_versions']):
        raise ValueError('oracle query count disagrees with replay')
    queries = [row for row in rows if row['event'] == 'query']
    summary = {label: sum(row['outcome'] == label for row in queries) for label in
               ('correct', 'wrong_accepted', 'safe_abstention', 'unnecessary_abstention')}
    summary.update(metadata_consults=sum(row['metadata_consult'] for row in queries),
                   payload_reads=sum(row['payload_read'] for row in queries))
    return dict(summary=summary, rows=rows)


def run():
    design = json.loads(DESIGN.read_bytes())
    items, targets, sources = source_items()
    config = calendar.run_config_for_test()
    paths = [Path(__file__), DESIGN, calendar.CONFIG, Path(calendar.__file__), Path(transfer.__file__),
             HERE / 'financial_contract_pilot.py', transfer.ARTIFACTS / 'source_config.json',
             transfer.ARTIFACTS / 'task_definition.json']
    paths.extend(transfer.ARTIFACTS / source['file'] for source in sources)
    hashes = {p.relative_to(HERE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    with localcontext() as context:
        context.prec = config['precision']
        results = {policy: replay(design, policy, items, targets, config) for policy in design['policies']}
    return dict(design=design, sha256=hashes, python=sys.version.split()[0], model_calls=0,
                archived_sources=sources, results=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--reproduce', type=Path)
    args = parser.parse_args()
    result = run()
    if args.reproduce is not None and json.loads(args.reproduce.read_bytes()) != result:
        raise SystemExit('full JSON equality failed')
    with args.out.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps({policy: block['summary'] for policy, block in result['results'].items()}, indent=2))
