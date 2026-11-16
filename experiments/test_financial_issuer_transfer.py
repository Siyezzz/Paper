import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import financial_issuer_transfer as pilot


class FinancialIssuerTransferTests(unittest.TestCase):
    def test_original_policies_reveal_fiscal_calendar_limit(self):
        result = pilot.run()
        self.assertEqual(len(result['pre_execution_lock']['sources']), 2)
        naive = result['results']['naive_frozen']['metrics']
        self.assertEqual((naive['correct_answers'], naive['wrong_accepted_answers']), (2, 4))
        for policy in ('contract', 'from_scratch_metadata_solver'):
            metrics = result['results'][policy]['metrics']
            self.assertEqual((metrics['correct_answers'], metrics['wrong_accepted_answers'], metrics['unnecessary_abstentions']), (0, 0, 4))
        self.assertIn('period', result['results']['contract']['cases'][0]['reasons'])

    def test_integer_oracle_rounding_and_sign(self):
        self.assertEqual(pilot.arithmetic_oracle('3', '4', 12), '33.333333333333')
        self.assertEqual(pilot.arithmetic_oracle('3', '2', 12), '-33.333333333333')
        self.assertEqual(pilot.arithmetic_oracle('40000', '40001', 2), '0.00')
        self.assertEqual(pilot.arithmetic_oracle('40000', '40003', 2), '0.01')

    def test_labels_not_given_to_executor(self):
        original = pilot.execute
        def checked(item, policy, frozen):
            self.assertNotIn('expected', item)
            self.assertNotIn('answerable', item)
            return original(item, policy, frozen)
        with patch.object(pilot, 'execute', side_effect=checked):
            pilot.run()

    def test_disk_config_mutated_after_first_execution_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for name in ('task_definition.json', 'source_config.json', 'nvda_release.html', 'intc_release.html'):
                shutil.copyfile(pilot.ARTIFACTS / name, folder / name)
            original = pilot.execute
            def mutate(item, policy, frozen):
                result = original(item, policy, frozen)
                path = folder / 'task_definition.json'
                path.write_bytes(path.read_bytes() + b' ')
                return result
            with patch.object(pilot, 'execute', side_effect=mutate):
                with self.assertRaisesRegex(AssertionError, 'fixed disk input changed'):
                    pilot.run(folder)

    def test_wrong_source_value_fails_even_if_hash_updated(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for name in ('task_definition.json', 'source_config.json', 'nvda_release.html', 'intc_release.html'):
                shutil.copyfile(pilot.ARTIFACTS / name, folder / name)
            path = folder / 'nvda_release.html'
            raw = path.read_bytes().replace(b'130,497', b'130,498')
            path.write_bytes(raw)
            config = json.loads((folder / 'source_config.json').read_bytes())
            config['sources'][0]['sha256'] = pilot.sha(raw)
            (folder / 'source_config.json').write_text(json.dumps(config), encoding='utf-8')
            with patch.object(pilot, 'execute') as mocked:
                with self.assertRaisesRegex(ValueError, 'disagrees'):
                    pilot.run(folder)
                mocked.assert_not_called()

    def test_mutating_actual_inputs_is_detected(self):
        def mutate(item, policy, frozen):
            frozen['admitted'] = False
            return None, 'mutation', []
        with patch.object(pilot, 'execute', side_effect=mutate):
            with self.assertRaisesRegex(AssertionError, 'mutated fixed actual inputs'):
                pilot.run()


if __name__ == '__main__':
    unittest.main()
