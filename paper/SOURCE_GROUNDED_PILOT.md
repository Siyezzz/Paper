# Source-grounded financial micro-pilot

## Scope

This is a minimal source-auditable arithmetic task, not an LLM experiment. It uses Microsoft Corporation's FY2024 and FY2023 GAAP total revenue from Microsoft-hosted pages. The values are **observed source values**; the decision dates, decision-before-publication case, and billion-versus-million representation are explicitly constructed evaluation scenarios.

## Primary source and extraction

The local source snapshots are under `experiments/artifacts/source_grounded/` and are checked against SHA256 values in `experiments/source_grounded_config.json`.

- Microsoft 2024 Annual Report: `https://microsoft.com/investor/reports/ar24` — income statement context says “In millions, except per share amounts”, “Year Ended June 30, 2024 2023 2022”, and reports `Total revenue 245,122 211,915 198,270`.
- Microsoft FY24 Q4 income statements: `https://microsoft.com/en-us/Investor/earnings/FY-2024-Q4/income-statements` — same annual row and unit context.
- Microsoft FY24 Q4 release: `https://microsoft.com/en-us/investor/earnings/fy-2024-q4/press-release-webcast` — dated `July 30, 2024` and annual table row `Total revenue 64,727 56,189 245,122 211,915`, with twelve-month June 30 headings.

The independent decimal oracle fixes base revenue at `211915` million USD and current revenue at `245122` million USD, then computes `(245122 / 211915 - 1) * 100 = 15.669962013071...%`. The oracle is implemented separately from the existing `growth`, `violations`, and `metadata_solver` functions.

## Constructed evaluation scenarios

1. `S01` uses the observed annual values after the selected release date and is answerable.
2. `S02` sets the decision date to 2024-07-29 while the selected release is dated 2024-07-30. It is a **pre-declared decision-before-publication case** and must abstain. This is not a claim about an observed market decision or intraday availability.
3. `S03` represents the same current value in constructed billions while the base remains in millions. This is a constructed safe-transfer scenario, not an observed unit change.

The script reads and hashes all source snapshots plus config before scoring. It records per-case raw rows, SHA256 locks, Python/platform metadata, and source excerpts. It compares `naive_frozen`, `contract`, and `from_scratch_metadata_solver`; the latter may normalize the known scale representation while the contract is conservative.

## Reproduction

From `Paper-ssh`:

```bash
python experiments/source_grounded_pilot.py --out experiments/artifacts/source_grounded/results.json
python -m unittest discover -s experiments -p 'test_source_grounded.py' -v
```

## Results and execution notes

| Policy | Correct answers / 3 | Wrong accepted | Abstentions | Unnecessary abstentions |
|---|---:|---:|---:|---:|
| Naive frozen | 1 | 2 | 0 | 0 |
| Contract | 1 | 0 | 2 | 1 |
| From-scratch metadata solver | 2 | 0 | 1 | 0 |

The ordinary metadata solver answers both compatible representations and abstains on the pre-publication scenario. Thus this micro-pilot supplies no skill-evolution advantage over ordinary metadata validation. These three dependent, designed cases are not an estimate of real-world error prevalence. Scoring compares to the independent oracle rounded to 12 decimal places, while all raw precision-50 answers are retained.

The initial test run had one test-authoring failure: a hard-coded default-precision decimal string was compared with the precision-50 solver output. The test was corrected to the predeclared 12-decimal oracle precision without changing source values, cases, policies, or outcomes. The supplemental report and tests were authored after inspecting the pilot results; no external preregistration is claimed.

The final full offline suite passes 27 tests, including 6 source-grounded tests; the transcript is saved as `experiments/artifacts/source_grounded/test_results.txt`. Source tampering is tested to fail before any executor invocation, and expected-answer labels are tested not to reach the executor.

## Limitations

This is one company and one annual pair, with dependent cases and author-visible code; it is not an independent blind holdout. July 30 is a selected release date, not proof of earliest public availability. The local HTML snapshots are not historical web archives. Date-only availability has no intraday precision, and no restatement, FX, filing-vintage, or calendar-time market claim is made. The original admission fixtures remain constructed and are not source-grounded training data. No LLM, paid API, market reaction, or population-level effectiveness claim is made.
