# Frozen Source-Vintage Check (Iteration 16)

## Design and freeze

This increment freezes the Iteration 15 calendar-aware validator, its configuration, legacy policies, and scoring before retrieving a newly selected company source. The freeze is an honest local freeze, not external preregistration. The task and source-selection receipt is `experiments/artifacts/iteration16_vintage/task_definition.json`; the UTC freeze receipt and SHA-256 locks are in `experiments/artifacts/iteration16_vintage/freeze_receipt.json`.

The new source-vintage check uses NVIDIA (NVDA) reported FY2026/FY2025 annual GAAP revenue. The selection rule was fixed before source retrieval: use the first company-hosted full-year FY2026 results release containing annual GAAP revenue and explicit fiscal-period endpoints, without switching sources after observing outcomes. The archived raw HTML is `experiments/artifacts/iteration16_vintage/nvda_fy26_release.html`, with source metadata, hash, retrieval command, and excerpts in `source_config.json`.

The company release was published February 25, 2026 and reports FY2026 revenue of $215,938 million and FY2025 revenue of $130,497 million. It also reports twelve-month endpoints January 25, 2026 and January 26, 2025. Reported fiscal labels are preserved; no label repair is performed. A pre-freeze code inspection identified that the unchanged validator checks `fiscal_year == end.year`; this was recorded before source retrieval, but it does not imply failure for this NVDA pair because the reported FY labels match the endpoint years. Fiscal starts used by the task are inferred from adjacent archived endpoints and are explicitly marked as inferred rather than source-verified week counts.

Primary source: https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026

## Semantics and cases

The primary task semantics are reported-adjacent-fiscal-year growth: compare the reported annual totals, without treating unequal fiscal-year duration as an error. Three constructed availability scenarios use the same source pair: two answerable cases (native million-USD units and an equivalent current billion-USD representation) and one pre-release decision that should abstain. Decision dates and selected-release availability are constructed; earliest historical availability and archival-vintage claims are not made.

The separately authored executor `experiments/frozen_source_vintage_check.py` uses the unchanged Iteration 15 policies: from-scratch metadata solver, contract, calendar ordinary validator, and two relevant ablations. The arithmetic target is independently computed with integer rational arithmetic and explicit twelve-decimal rounding. No seed or live API call is involved.

## Results

| Policy | Correct | Wrong accepted | Safe abstentions | Unnecessary abstentions | Coverage | Accuracy conditional on acceptance |
|---|---:|---:|---:|---:|---:|---:|
| From-scratch metadata solver | 0/3 | 0 | 1 | 2 | 0.000 | n/a |
| Conservative contract | 0/3 | 0 | 1 | 2 | 0.000 | n/a |
| Calendar ordinary validator | 2/3 | 0 | 1 | 0 | 0.667 | 1.000 |
| No availability check | 2/3 | 1 | 0 | 0 | 1.000 | 0.667 |
| No unit normalization | 1/3 | 1 | 1 | 0 | 0.667 | 0.500 |

The ordinary calendar validator answers both available source cases correctly and safely abstains before the selected release. Removing availability accepts the pre-release case incorrectly. Removing unit normalization makes the converted representation incorrect. The result is a three-case, one-issuer developmental confirmation of semantic boundary behavior, not evidence of population generalization, financial performance, or skill evolution.

## Reproduction and limitations

`experiments/artifacts/iteration16_vintage/reproduce.py` adapted the Iteration 15 harness to a new output directory and ran eight commands without overwriting historical artifacts. All eight commands exited 0; the 57-test offline suite passed; three historical JSON comparisons were fully equal; and the Iteration 15 final calendar reference/reproduction comparison remained equal. The new result and execution receipt are `vintage_results.json` and `vintage_results.receipt.json`.

Lead verification subsequently reproduced the entire new result JSON exactly, rather than only its policy metrics; `lead_reproduction.receipt.json` and `lead_verification.json` retain the checks. All 60 offline tests passed, including simulated frozen-code and source-byte tampering that must be rejected before execution (`lead_tests.txt`). The table is independently regenerated from `vintage_results.json` in `results_table.md`. The earlier 57-test count refers only to the historical reproduction stage.

From the repository root, use a fresh output path because the runner refuses to overwrite existing results:

```bash
python experiments/frozen_source_vintage_check.py --out experiments/artifacts/iteration16_vintage/local_check.json --reproduce experiments/artifacts/iteration16_vintage/vintage_results.json
python -m unittest discover -s experiments -v
```

Full JSON equality includes environment metadata and executable hashes, so the archived equality establishes reproduction in the same local environment; cross-platform byte-identical output is not promised. The historical reproduction harness and hashed inputs must remain unchanged.

The result is author-visible and produced by the same AI research process, not an independent researcher or blind holdout. It uses one new annual pair from a previously exposed issuer, current company web HTML rather than a historical archive, inferred starts, constructed decision dates and availability, handwritten unchanged policies, and no live model-generated skill. It therefore does not establish unseen-issuer generalization, causal benefit, market utility, or a universal duration threshold. A failed optional BeautifulSoup inspection due to an unavailable package was retained in source metadata; the existing standard-library normalization path was then used without changing the frozen task or policy.
