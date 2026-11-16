import json
import unittest
from decimal import Decimal
from pathlib import Path

import tempfile
from unittest.mock import patch

import source_grounded_pilot as pilot


class SourceGroundedPilotTests(unittest.TestCase):
    def setUp(self):
        self.result = pilot.run()

    def test_source_lock_and_oracle(self):
        self.assertEqual(pilot.oracle(self.result['config']), '15.669962013071')
        self.assertEqual(len(self.result['pre_execution_lock']['sources']), 3)
        self.assertTrue(self.result['pre_execution_lock_sha256'])

    def test_source_values_and_constructed_cases_are_distinguished(self):
        items = self.result['pre_execution_lock']['items']
        self.assertEqual(items[0]['base']['value'], '211915')
        self.assertEqual(items[0]['current']['value'], '245122')
        self.assertIn('constructed equivalent representation', items[2]['provenance'])
        self.assertEqual(items[2]['current']['scale'], '1000000000')

    def test_decision_before_publication_case_abstains(self):
        rows = self.result['results']['contract']['cases']
        row = next(x for x in rows if x['id'] == 'S02')
        self.assertIsNone(row['answer'])
        self.assertEqual(row['event'], 'invocation_revoked')
        self.assertIn('availability', row['reasons'])

    def test_tampered_source_fails_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for entry in self.result['config']['sources']:
                raw = (pilot.ARTIFACTS / entry['file']).read_bytes()
                (target / entry['file']).write_bytes(raw + b'changed')
            with patch.object(pilot, 'execute', side_effect=AssertionError('must not execute')) as mocked:
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    pilot.run(source_dir=target)
                mocked.assert_not_called()

    def test_expected_answers_not_passed_to_executor(self):
        original = pilot.execute
        def checked(item, policy, frozen):
            self.assertNotIn('expected', item)
            self.assertNotIn('expected_available', item)
            return original(item, policy, frozen)
        with patch.object(pilot, 'execute', side_effect=checked):
            pilot.run()

    def test_actual_executor_input_mutation_is_detected(self):
        original = pilot.execute
        def mutate(item, policy, frozen):
            result = original(item, policy, frozen)
            item['current']['value'] = '1'
            return result
        with patch.object(pilot, 'execute', side_effect=mutate):
            with self.assertRaisesRegex(AssertionError, 'mutated fixed actual inputs'):
                pilot.run()

    def test_disk_source_mutation_during_execution_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for entry in self.result['config']['sources']:
                (target / entry['file']).write_bytes((pilot.ARTIFACTS / entry['file']).read_bytes())
            original = pilot.execute
            def mutate(item, policy, frozen):
                result = original(item, policy, frozen)
                path = target / self.result['config']['sources'][0]['file']
                path.write_bytes(path.read_bytes() + b'changed during execution')
                return result
            with patch.object(pilot, 'execute', side_effect=mutate):
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    pilot.run(source_dir=target)

    def test_solver_comparison(self):
        naive = self.result['results']['naive_frozen']['cases']
        contract = self.result['results']['contract']['cases']
        solver = self.result['results']['from_scratch_metadata_solver']['cases']
        self.assertEqual(Decimal(next(x for x in naive if x['id'] == 'S02')['answer']).quantize(Decimal('0.000000000001')), Decimal('15.669962013071'))
        self.assertIsNone(next(x for x in contract if x['id'] == 'S02')['answer'])
        self.assertIsNotNone(next(x for x in solver if x['id'] == 'S03')['answer'])


if __name__ == '__main__':
    unittest.main()
