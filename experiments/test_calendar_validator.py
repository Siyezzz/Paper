import unittest
import tempfile
from pathlib import Path
from copy import deepcopy
from datetime import date
from decimal import Decimal
from unittest.mock import patch

import calendar_validator_development as pilot


class CalendarValidatorTests(unittest.TestCase):
    def test_run_and_per_issuer_output(self):
        result = pilot.run()
        self.assertEqual(set(result['results']), set(json_policy_names()))
        self.assertEqual(set(result['results']['calendar_ordinary']['by_issuer']), {'MSFT', 'NVDA', 'INTC'})
        self.assertGreater(result['results']['calendar_ordinary']['metrics']['correct_answers'], 0)
        self.assertEqual(result['results']['calendar_ordinary']['metrics']['wrong_accepted_answers'], 0)

    def test_quarter_nonadjacent_convention_availability_scale_zero_and_false_metadata(self):
        items, _, _, _, _, _, _ = pilot.build_inputs()
        base = deepcopy(items[0])
        mutations = [
            ('quarter', lambda x: x['base'].update(period_kind='quarter')),
            ('nonadjacent', lambda x: x['current'].update(fiscal_year=x['base']['fiscal_year'] + 2)),
            ('convention', lambda x: x['current'].update(convention='other')),
            ('issuer', lambda x: x['current'].update(issuer='INTC')),
            ('currency', lambda x: x['current'].update(currency='EUR')),
            ('metric', lambda x: x['current'].update(metric='net_income')),
            ('availability', lambda x: x.update(decision_at='2020-01-01')),
            ('unknown_scale', lambda x: x['current'].update(scale='7')),
            ('zero_base', lambda x: x['base'].update(value='0')),
            ('false_metadata', lambda x: x['current'].update(fiscal_year=1900)),
        ]
        for name, mutate in mutations:
            item = deepcopy(base)
            mutate(item)
            answer, _, reasons = pilot.calendar_execute(item, 'calendar_ordinary', pilot.run_config_for_test())
            self.assertIsNone(answer, name)
            self.assertTrue(reasons, name)

    def test_labels_do_not_bypass_interval_checks(self):
        items, _, _, _, _, _, _ = pilot.build_inputs()
        item = deepcopy(items[0])
        item['expected_available'] = True
        item['expected'] = '999'
        item['current']['start'] = '2023-07-03'
        answer, _, reasons = pilot.calendar_execute(item, 'calendar_ordinary', pilot.run_config_for_test())
        self.assertIsNone(answer)
        self.assertIn('noncontiguous_periods', reasons)

    def test_constant_duration_rejects_52_53_week_difference(self):
        items, _, _, _, _, _, _ = pilot.build_inputs()
        item = deepcopy(next(x for x in items if x['issuer'] == 'NVDA'))
        # 显式构造53周前期，连续52周本期；不是来源事实。
        item['base']['start'] = '2023-01-23'
        answer, _, reasons = pilot.calendar_execute(item, 'calendar_ordinary', pilot.run_config_for_test())
        self.assertIsNotNone(answer, reasons)
        item['task_semantics'] = 'constant_duration_fiscal_year_growth'
        answer, _, reasons = pilot.calendar_execute(item, 'calendar_ordinary', pilot.run_config_for_test())
        self.assertIsNone(answer)
        self.assertIn('unequal_duration_for_constant_duration_task', reasons)

    def test_unknown_semantics_and_hidden_quarter_rejected(self):
        items, _, _, _, _, _, _ = pilot.build_inputs()
        for changes, reason in [({'task_semantics': 'unknown'}, 'unknown_task_semantics'),
                                ({'current': {**items[0]['current'], 'start': '2024-04-01'}}, 'annual_duration')]:
            item = deepcopy(items[0])
            item.update(changes)
            answer, _, reasons = pilot.calendar_execute(item, 'calendar_ordinary', pilot.run_config_for_test())
            self.assertIsNone(answer)
            self.assertIn(reason, reasons)

    def test_exact_development_results_and_ablations(self):
        result = pilot.run()['results']
        expected = {'from_scratch_metadata_solver': (2, 0, 4), 'contract': (1, 0, 5),
                    'calendar_ordinary': (6, 0, 0), 'calendar_no_availability': (6, 3, 0),
                    'calendar_no_unit_normalization': (3, 3, 0)}
        for policy, counts in expected.items():
            metrics = result[policy]['metrics']
            self.assertEqual(tuple(metrics[k] for k in ('correct_answers', 'wrong_accepted_answers', 'unnecessary_abstentions')), counts)

    def test_actual_config_mutation_detected(self):
        original = pilot.calendar_execute
        def mutate(item, policy, config):
            result = original(item, policy, config)
            config['known_scales'].append('7')
            return result
        with patch.object(pilot, 'calendar_execute', side_effect=mutate):
            with self.assertRaisesRegex(AssertionError, 'mutated fixed actual inputs'):
                pilot.run()

    def test_disk_config_mutation_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config.json'
            path.write_bytes(pilot.CONFIG.read_bytes())
            original = pilot.calendar_execute
            def mutate(item, policy, config):
                answer = original(item, policy, config)
                path.write_bytes(path.read_bytes() + b' ')
                return answer
            with patch.object(pilot, 'calendar_execute', side_effect=mutate):
                with self.assertRaisesRegex(AssertionError, 'fixed disk input changed'):
                    pilot.run(path)

    def test_executor_mutation_detected(self):
        with patch.object(pilot, 'calendar_execute', side_effect=lambda item, policy, config: (item.update(scenario='mutated') or (None, 'x', []))):
            with self.assertRaisesRegex(AssertionError, 'mutated fixed actual inputs'):
                pilot.run()


def json_policy_names():
    return {'from_scratch_metadata_solver', 'contract', 'calendar_ordinary', 'calendar_no_availability', 'calendar_no_unit_normalization'}


if __name__ == '__main__':
    unittest.main()
