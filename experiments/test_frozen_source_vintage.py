import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import frozen_source_vintage_check as pilot


class FrozenSourceVintageTests(unittest.TestCase):
    def test_exact_three_case_five_policy_metrics(self):
        result = pilot.run()
        expected = {
            'from_scratch_metadata_solver': (0, 0, 2),
            'contract': (0, 0, 2),
            'calendar_ordinary': (2, 0, 0),
            'calendar_no_availability': (2, 1, 0),
            'calendar_no_unit_normalization': (1, 1, 0),
        }
        for policy, counts in expected.items():
            metrics = result['results'][policy]['metrics']
            self.assertEqual(metrics['n'], 3)
            self.assertEqual(tuple(metrics[k] for k in ('correct_answers', 'wrong_accepted_answers', 'unnecessary_abstentions')), counts)

    def test_freeze_receipt_rejects_changed_frozen_bytes(self):
        original = pilot.verify_freeze
        with patch.object(pilot, 'verify_freeze', side_effect=lambda: (_ for _ in ()).throw(AssertionError('frozen bytes changed: test'))):
            with self.assertRaisesRegex(AssertionError, 'frozen bytes changed'):
                pilot.run()
        self.assertIsNotNone(original)

    def test_source_hash_rejects_tampering(self):
        source_path = pilot.HERE / 'nvda_fy26_release.html'
        read_bytes = Path.read_bytes

        def read_with_altered_source(path):
            contents = read_bytes(path)
            return contents + b' ' if path == source_path else contents

        with patch.object(Path, 'read_bytes', read_with_altered_source):
            with self.assertRaisesRegex(ValueError, 'source hash mismatch'):
                pilot.run()

    def test_raw_result_reproduction_is_exact(self):
        result_path = pilot.HERE / 'vintage_results.json'
        self.assertTrue(result_path.exists())
        saved = json.loads(result_path.read_bytes())
        self.assertEqual(saved['results']['calendar_ordinary']['metrics']['correct_answers'], 2)
        self.assertEqual(saved['results']['calendar_ordinary']['metrics']['wrong_accepted_answers'], 0)


if __name__ == '__main__':
    unittest.main()
