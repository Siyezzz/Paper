# External issuer transfer check: reported annual revenue

This supplement adds two new issuers to the deterministic financial evidence: NVIDIA (NVDA), FY2025 versus FY2024, and Intel (INTC), FY2024 versus FY2023. Microsoft remains a reproduction reference and is not counted as a new independent sample. This is an **author-designed external issuer transfer check**, not a blinded or independently authored holdout, a learned-policy experiment, or an LLM experiment.

## Sources and task definition

Two raw company-hosted HTML snapshots, the task definition, issuer-specific extraction configuration, per-task outputs, code/input SHA256 locks, and command/environment transcripts are retained in `experiments/artifacts/iteration14_financial/`.

| Issuer | Selected company release | Reported annual periods, current / base | Current / base revenue, USD million | Independent reported annual growth oracle |
|---|---|---|---:|---:|
| NVIDIA (NVDA) | February 26, 2025 | Twelve months ended January 26, 2025 / January 28, 2024; FY25 / FY24 | 130,497 / 60,922 | 114.203407635994% |
| Intel (INTC) | January 30, 2025 | Twelve months ended December 28, 2024 / December 30, 2023; 2024 / 2023 | 53,101 / 54,228 | -2.078262152394% |

The exact rounded oracle strings should be read from `results.json`, which is authoritative if transcription differs. The independent oracle uses integer `Fraction` arithmetic and explicit ties-to-even rounding to 12 decimal places; it does not call the evaluated `growth`, `violations`, or `metadata_solver` functions. The source values are separately transcribed in `source_config.json` and must match extracted company table values before execution.

Primary URLs saved with the source configuration are:

- NVIDIA: `https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025?page=31`.
- Intel: `https://www.intc.com/news-events/press-releases/detail/1726/intel-reports-fourth-quarter-and-full-year-2024-financial?utm_source=in_materials`.

The NVIDIA investor-relations endpoint returned HTTP 403; its company newsroom mirror was successfully retrieved. These are current web snapshots downloaded on November 16, 2026, not archived point-in-time web evidence. Saved normalized excerpts verify the table values, million-dollar units, annual end-date headings, and release dates. Company fiscal current/base conventions are internally consistent within each task; different issuers are never compared to each other. Annual starts are analyst-constructed labels rather than source-verified week counts. The task is the change between **reported adjacent fiscal-year annual totals**, without daily or constant-week normalization. No verified 52/53-week count is claimed.

Each issuer has three dependent scenarios: observed annual values with a constructed decision date one day after the selected release (answerable); a constructed decision date one day before that release (unavailable under the selected-date convention); and a constructed equivalent billion-dollar representation of the current value after release (answerable). Unit conversion and decision dates are explicitly constructed, not observed business events. The selected release is not proof of earliest public availability.

`task_definition.json` was first written before raw snapshot download and before scoring, but the author had already seen policy code and search-result source summaries. No contemporaneous UTC freeze receipt was generated at that point. `design_receipt.json` is explicitly a later receipt recording tool order and filesystem creation timestamps, not a backdated preregistration. After the first execution, unsupported 52/53-week wording was tightened to source-reported annual end dates; issuers, six cases, answerability labels, decision offsets, source values, precision, and policies did not change. The final locked definition is therefore not represented as an untouched external preregistration.

## Unchanged-policy outcomes

All policies and constructed discovery/admission fixtures are unchanged. No new source is used to retrain or tune admission. Results are measured against the independent oracle and include full raw answers, events, reasons, and separate issuer summaries.

| Policy | Correct answers / 6 | Wrong accepted | Total abstentions | Safe abstentions | Unnecessary abstentions |
|---|---:|---:|---:|---:|---:|
| Naive frozen | 2 | 4 | 0 | 0 | 0 |
| Contract | 0 | 0 | 6 | 2 | 4 |
| From-scratch metadata solver | 0 | 0 | 6 | 2 | 4 |

Each issuer contributes the same count pattern: naive 1 correct and 2 wrong accepted; contract and metadata solver each 3 abstentions, including 2 unnecessary. The two wrong-accept categories are an answer before the selected release and an unnormalized constructed scale change. The conservative policies avoid those wrong accepts but reject every answerable case.

This is a negative transfer result. The ordinary metadata solver and contract both require annual start/end month-days to repeat exactly in the next calendar year. The observed company annual **end dates alone** violate that assumption: January 28 becomes January 26, and December 30 becomes December 28. Rejection is therefore not a cross-issuer convention mismatch; both years of each individual issuer use the same convention. Under the explicitly defined reported-fiscal-year task, these annual comparisons are answerable. Neither policy has positive answer coverage, so coverage-conditioned accuracy is null, not 100%. No policy was repaired after observing this failure. The outcome supplies no skill-evolution advantage and does not establish general superiority of naive calculation: naive still accepts unavailable and incorrectly scaled inputs.

The Microsoft reference retains its prior policy outcome counts (1/2/0 correct/wrong/unnecessary for naive; 1/0/1 for contract; 2/0/0 for metadata solver). That source pilot uses calendar-anniversary-compatible annual windows. It is not pooled with the two new issuers to inflate the new sample count.

## Source-lock upgrade and verification

The existing `source_grounded_pilot.py` previously rehashed an in-memory lock after scoring. It now rereads config and raw sources before and after each executor call, checks their extracted evidence and values against the fixed inputs, verifies implementation hashes, and compares the actual item/frozen objects passed to the executor with their fixed originals. The new issuer runner also checks disk bytes and actual executor inputs around every call. These checks detect persistent mutations at call boundaries; they do not prove the absence of malicious changes restored between checks or function-object monkeypatching.

Meaningful mutation tests cover a source changed during execution, actual item/frozen mutation, a config changed after the first execution, and a source value changed even after updating its file hash. Expected labels are tested not to reach the executor. Original financial-contract tests also pass.

Reproduce from the repository root:

```bash
python experiments/artifacts/iteration14_financial/reproduce.py
```

The wrapper stores the exact argument vectors, working directory, Python/platform information, exit status, and stdout/stderr transcripts in `execution_manifest.json` and `command_*.txt`. It runs both pilots and 19 financial tests plus 8 source-grounded tests (27 tests total). The new result additionally locks the Python executable, evaluated policy/config/fixtures, task definition, extraction config, source snapshots, and new runner.

`source_reference.json` was produced before the source-lock fix, and `source_reference_after_lock_fix.json` afterwards. Their `results` objects are equal; their complete JSON and lock hashes differ because implementation/test hashes intentionally changed. The team lead separately reported three complete historical JSON reproductions and 40 passing tests **before** this edit, plus successful iteration12/13 verify-only checks; those earlier checks must not be described as post-edit complete-JSON equality.

## Limits of the evidence

The effective issuer count is two, with one annual pair per issuer and three dependent designed cases each. Source extraction is a hand-authored, issuer-specific parser, not an evaluated autonomous extraction model. Fiscal starts and dates are constructed or inferred as labeled; exact source end dates are sufficient to demonstrate the tested anniversary limitation. No historical archive, earliest-release proof, intraday decision precision, FX conversion, restatement or filing-vintage resolution, independent-author oracle, live LLM, model-generated program, learned skill, market outcome, cost/speed advantage, or population-level effectiveness estimate is supplied. The appropriate inference is a reproducible limitation of these unchanged deterministic policies on two selected issuer fiscal calendars.
