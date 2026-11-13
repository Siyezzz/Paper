import json
import os
import unittest
from unittest.mock import patch

from model_api_clients import call_chat_completion, extract_text


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 1},
        }).encode()


class ModelAPIClientTests(unittest.TestCase):
    def test_missing_key_does_not_call_network(self):
        with patch.dict(os.environ, {}, clear=True):
            result = call_chat_completion("https://example.invalid", "model", [])
        self.assertFalse(result.ok)
        self.assertEqual(result.error, "missing_environment:GAAGENT_API_KEY")

    def test_payload_and_response_are_openai_compatible(self):
        captured = {}

        def opener(request, timeout):
            captured["headers"] = dict(request.headers)
            captured["timeout"] = timeout
            captured["payload"] = json.loads(request.data.decode())
            return FakeResponse()

        with patch.dict(os.environ, {"GAAGENT_API_KEY": "secret"}, clear=True):
            result = call_chat_completion(
                "https://example.invalid", "test-model", [{"role": "user", "content": "x"}],
                opener=opener,
            )
        self.assertTrue(result.ok)
        self.assertEqual(captured["payload"]["model"], "test-model")
        self.assertEqual(captured["payload"]["temperature"], 0.0)
        self.assertNotIn("secret", json.dumps(result.response))
        self.assertEqual(extract_text(result.response), "ok")

    def test_http_error_is_redacted_and_bounded(self):
        self.assertIsNone(extract_text({"error": "bad"}))


if __name__ == "__main__":
    unittest.main()
