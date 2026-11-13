import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from model_api_clients import APIResult
import run_multi_model_api as harness


class OfflineHarnessTests(unittest.TestCase):
    def test_missing_key_stops_globally_and_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "run.json"
            with patch.dict(os.environ, {}, clear=True):
                code = harness.run("https://offline.invalid", "NO_KEY", ["m1", "m2"], out, 8, 1)
            payload = json.loads(out.read_text())
        self.assertEqual(code, 1)
        self.assertEqual(len(payload["rows"]), 1)
        self.assertEqual(payload["stop_reason"], "missing_api_key_environment")
        self.assertEqual(payload["attempted_calls"], 1)

    def test_403_stops_globally_without_repeating_calls(self):
        calls = []
        def fake_call(*args, **kwargs):
            calls.append((args, kwargs))
            return APIResult(False, 403, None, "http_error:denied", 2)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "run.json"
            with patch.object(harness, "call_chat_completion", side_effect=fake_call):
                code = harness.run("https://offline.invalid", "KEY", ["m1", "m2"], out, 8, 1)
            payload = json.loads(out.read_text())
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 1)
        self.assertEqual(payload["stop_reason"], "http_403_global_circuit_breaker")
        self.assertEqual(payload["protocol"]["max_tokens"], 8)
        self.assertEqual(payload["protocol"]["temperature"], 0.0)

    def test_success_path_and_answer_labels_are_not_exposed(self):
        def fake_call(endpoint, model, messages, **kwargs):
            self.assertNotIn('"expected"', messages[1]["content"])
            self.assertNotIn('"scenario"', messages[1]["content"])
            return APIResult(True, 200, {"choices": [{"message": {"content": '{"answer": 20, "status": "ok"}'}}]}, None, 1)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "run.json"
            with patch.object(harness, "call_chat_completion", side_effect=fake_call):
                code = harness.run("https://offline.invalid", "KEY", ["m1"], out, 8, 1)
            payload = json.loads(out.read_text())
        self.assertEqual(code, 0)
        self.assertEqual(payload["attempted_calls"], 56)
        self.assertIsNone(payload["stop_reason"])


if __name__ == "__main__":
    unittest.main()
