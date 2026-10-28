"""Numbers as papers print them. The forms are the ones measured in the specs on disk (28 Oct): powers of ten in
five spellings and bounds; a held-out run read `p < 10^{-12}` as 10 and judged the paper wrong."""

import pytest

from paper_replicator.guards import bound, half_unit, parse_number


@pytest.mark.parametrize("printed, value", [
    ("<10^{-12}", 1e-12), ("< 10^{-3}", 1e-3), ("5.2\\times10^{-4}", 5.2e-4), ("2.70×10^{-14}", 2.7e-14),
    ("4×10^5", 4e5), ("2.70x10-14", 2.7e-14), ("<5×10^{-17}", 5e-17), ("1.5e-13", 1.5e-13),
    ("$-3.1 \\times 10^{2}$", -310.0),
    # unchanged forms
    ("-7.49%", -7.49), ("1,234", 1234.0), ("30.4 basis points", 30.4), ("−0.35", -0.35),
    ("Estimate +4.7556, HAC SE 0.0353, p=<10^{-300}", 4.7556),
])
def test_parse_number(printed, value):
    assert parse_number(printed) == pytest.approx(value, rel=1e-12)


@pytest.mark.parametrize("printed, half", [
    ("2.70×10^{-14}", 0.005e-14), ("5.2\\times10^{-4}", 0.05e-4), ("4×10^5", 0.5e5), ("-7.49", 0.005), ("54", 0.5),
])
def test_half_unit_scales_with_the_power(printed, half):
    assert half_unit(printed) == pytest.approx(half, rel=1e-12)


@pytest.mark.parametrize("printed, side", [
    ("<0.001", "<"), ("≤0.002", "<"), ("< 10^{-12}", "<"), ("$<$ 0.01", "<"), ("\\leq 0.05", "<"),
    (">5", ">"), ("\\geq 2", ">"), ("-3", None), ("0.11", None),
    ("Estimate +4.7556, HAC SE 0.0353, p=<10^{-300}", None),   # the bound belongs to the p, not the estimate
])
def test_bound(printed, side):
    assert bound(printed) == side
