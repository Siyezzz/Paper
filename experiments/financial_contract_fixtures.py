"""显式构造的测试输入；不代表公司、市场或真实观测财务数据。"""
from copy import deepcopy


def fixture(case_id, split, year, current_value="120", base_value="100", expected="20", **changes):
    decision = f"{year}-06-30"
    item = {
        "id": case_id, "split": split,
        "fixture_type": "constructed_test_case_not_observed_financial_data",
        "decision_at": decision,
        "base": {"value": base_value, "currency": "TEST_CURRENCY_A", "scale": "1",
                 "metric": "constructed_revenue", "convention": "calendar",
                 "start": f"{year-3}-01-01", "end": f"{year-3}-12-31",
                 "available_at": f"{year-2}-03-01"},
        "current": {"value": current_value, "currency": "TEST_CURRENCY_A", "scale": "1",
                    "metric": "constructed_revenue", "convention": "calendar",
                    "start": f"{year-2}-01-01", "end": f"{year-2}-12-31",
                    "available_at": f"{year-1}-03-01"},
        "expected": expected,
        "scenario": "safe_same_unit_growth",
    }
    for key, value in changes.items():
        if key in ("base", "current"):
            item[key].update(value)
        else:
            item[key] = value
    return item


CASES = [
    fixture("D01", "discovery", 2023),
    fixture("D02", "discovery", 2023, "90", "100", "-10"),
    fixture("D03", "discovery", 2023, "150", "100", "50"),
    fixture("V01", "validation", 2024),
    fixture("V02", "validation", 2024, "80", "100", "-20"),
    fixture("V03", "validation", 2024, "125", "100", "25"),
    fixture("H01", "heldout", 2025),
    fixture("H02", "heldout", 2025, base={"scale": "1000"},
            current={"scale": "1000"}, scenario="safe_same_unit_scaling_transfer"),
    fixture("H03", "heldout", 2025, "75", "100", "-25", scenario="safe_decline"),
    fixture("H04", "heldout", 2025, current={"value": "0.12", "scale": "1000"},
            scenario="convertible_mixed_scale_requires_normalization"),
    fixture("H05", "heldout", 2025, expected=None,
            current={"currency": "TEST_CURRENCY_B"}, scenario="unsafe_currency_mismatch"),
    fixture("H06", "heldout", 2025, expected=None,
            current={"start": "2023-04-01", "end": "2023-06-30"},
            scenario="unsafe_quarter_vs_annual"),
    fixture("H07", "heldout", 2025, expected=None,
            current={"available_at": "2025-07-01"}, scenario="current_published_after_decision"),
    fixture("H08", "heldout", 2025, expected=None,
            base={"available_at": "2025-07-01"}, scenario="base_published_after_decision"),
    fixture("H09", "heldout", 2025,
            base={"start": "2022-04-01", "end": "2023-03-31", "convention": "fiscal_april", "available_at": "2023-05-01"},
            current={"start": "2023-04-01", "end": "2024-03-31", "convention": "fiscal_april", "available_at": "2024-05-01"},
            scenario="safe_consistent_fiscal_transfer"),
    fixture("H10", "heldout", 2025, expected=None,
            current={"convention": "fiscal_april", "start": "2023-04-01", "end": "2024-03-31", "available_at": "2024-05-01"},
            scenario="unsafe_accounting_convention_change"),
    fixture("H11", "heldout", 2025, current={"available_at": "2025-06-01"},
            scenario="valid_future_input_published_after_freeze_before_decision"),
    fixture("H12", "heldout", 2025, expected=None,
            current={"metric": "constructed_net_income"}, scenario="unsafe_metric_mismatch"),
    fixture("H13", "heldout", 2025, current={"available_at": "2025-06-30"},
            scenario="publication_exactly_at_decision"),
    fixture("H14", "heldout", 2025, "120", "0", None, scenario="undefined_zero_base"),
]


def cases():
    return deepcopy(CASES)
