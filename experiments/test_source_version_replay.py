from decimal import Decimal
import unittest

import source_version_replay as replay


class SourceVersionReplayTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = replay.run()['results']

    def test_ordinary_version_check_preserves_answers_with_fewer_loads(self):
        full = self.results['always_read']['summary']
        conditional = self.results['conditional_read']['summary']
        self.assertEqual(conditional, dict(full, payload_reads=3))
        self.assertEqual((full['correct'], full['safe_abstention'], full['wrong_accepted']), (9, 3, 0))

    def test_missed_notification_and_equal_value_stale_version(self):
        selective = self.results['selective_notification']['rows']
        self.assertEqual(selective[13]['outcome'], 'wrong_accepted')
        stale = self.results['no_invalidation']['rows'][10]
        self.assertEqual(Decimal(stale['answer']).quantize(Decimal('0.000000000001')),
                         Decimal(stale['expected_answer']))
        self.assertEqual(stale['outcome'], 'wrong_accepted')

    def test_selective_notification_keeps_unrelated_cache(self):
        selective = self.results['selective_notification']
        global_ = self.results['global_notification']
        self.assertEqual(selective['rows'][4]['evicted'], ['NVDA'])
        self.assertEqual(global_['rows'][4]['evicted'], ['INTC', 'NVDA'])
        self.assertEqual(global_['summary']['payload_reads'] - selective['summary']['payload_reads'], 2)
