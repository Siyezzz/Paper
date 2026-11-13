# API Pilot Audit (2026-11-13)

## Evidence reviewed

The inherited raw artifact `experiments/artifacts/multi_model_api/live_pilot_20261113.json` was read without modification. Its SHA-256 is `00c64ca1b383f7764e3c26419e146866cd05bb3817f44b26941ba90c5dd0b363`.

It contains 168 attempted calls: 164 HTTP 403 responses and 4 transport failures with no HTTP status. There are zero successful calls, zero response texts, zero usage objects, and therefore zero scorable outputs. Actual spend is unknown. The 12 model/workflow groups are the 3 requested models by 4 workflow identifiers, each with 14 heldout tasks. These are endpoint/access failures, not task wrong answers: no model answer was returned and no task-level correctness judgment is made.

The inherited `started_at_utc` value was recorded after the request loops in the original harness. It is therefore an end-of-run timestamp, not a true collection start time. The corrected harness records start time before fixture loading and also records a finish time.

## Bounded changes

`run_multi_model_api.py` now globally stops on the first missing key or HTTP 401/403, records an explicit stop reason, writes protocol provenance (system/prompt hashes, source hashes, fixture hash, max tokens, temperature, timeout, and ordering), and returns non-zero for a stopped or unsuccessful run. Prompt inputs continue to exclude `expected` and `scenario` labels.

The offline tests in `experiments/test_run_multi_model_api_offline.py` cover missing-key and 403 circuit breakers, non-zero exit behavior, parameter provenance, successful execution, and answer-label non-exposure. They use mocked results only and do not make network requests.

## Credential handling

Project memory indicates that an API key was exposed previously. The user must revoke that exposed key and issue a replacement before any future authorized live run. This audit does not contain, inspect, print, retry, or call the exposed key. No live API call was made for this audit.

## Interpretation limits

The names `generated_skill` and `generated_skill_contract` remain for compatibility but are prompt-only variants. No generated skill was persisted and no external execution contract was run. This artifact must not be described as a real generated-skill experiment. The fixtures are constructed test cases, not observed financial data. No model, workflow, accuracy, or cost conclusion is supported by the inherited raw run.
