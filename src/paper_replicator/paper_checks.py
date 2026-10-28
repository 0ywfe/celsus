"""Checks on the paper's own numbers, in code: do its subgroup counts add up, and which p-value does
each test statistic actually give? The extractor names which claims belong together; code does the
arithmetic. Neither check needs a chosen tolerance.

Each check has a status: "ok", "flag" (the paper's numbers disagree with each other) or "note" (a fact
the reader should know, such as one-sided tests; the verdict desk uses it)."""

from __future__ import annotations

import math

from scipy import stats

from .guards import parse_number
from .spec import Claim, PaperSpec


def _values(claims: list[Claim]) -> dict[str, float]:
    return {c.name: v for c in claims if (v := parse_number(c.value)) is not None}


def partition_checks(spec: PaperSpec, claims: list[Claim]) -> list[dict]:
    values, checks = _values(claims), []
    for split in spec.partitions:
        if split.total not in values or not split.parts or any(p not in values for p in split.parts):
            continue
        parts = [values[p] for p in split.parts]
        total, summed = values[split.total], sum(parts)
        sums = " + ".join(f"{v:g}" for v in parts)
        checks.append({"check": "partition", "split": split.split, "status": "ok" if summed == total else "flag",
                       "text": f"{split.split}: {sums} = {summed:g}, paper's total {total:g}"})
    return checks


def _p_values(t: float, df: float) -> dict[str, float]:
    dist = stats.t(df) if math.isfinite(df) else stats.norm()
    return {"two-sided": 2 * dist.sf(abs(t)), "one-sided (lower tail)": dist.cdf(t),
            "one-sided (upper tail)": dist.sf(t)}


def _dfs(sizes: list[float]) -> list[float]:
    """Degrees of freedom the test could have: one sample n - 1; two samples between Welch's lowest
    (min n - 1) and the pooled n1 + n2 - 2; no sizes, the normal."""
    if len(sizes) == 1:
        return [sizes[0] - 1]
    if len(sizes) == 2:
        return [min(sizes) - 1, sum(sizes) - 2]
    return [math.inf]


def sidedness_checks(spec: PaperSpec, claims: list[Claim]) -> list[dict]:
    values, checks = _values(claims), []
    for test in spec.tests:
        if test.statistic not in values or test.p_value not in values:
            continue
        t, reported = values[test.statistic], values[test.p_value]
        if not 0 < reported < 1:
            continue
        sizes = [values[g] for g in test.group_sizes if g in values and values[g] > 1]
        candidates = [(abs(math.log(p) - math.log(reported)), side, p, df)
                      for df in _dfs(sizes) for side, p in _p_values(t, df).items() if p > 0]
        _, side, p, df = min(candidates)
        two_sided = _p_values(t, df)["two-sided"]
        checks.append({"check": "sidedness", "test": test.test, "side": side,
                       "status": "ok" if side == "two-sided" else "note",
                       "text": f"{test.test}: t = {t:g}, paper's p = {reported:g} matches {side} "
                               f"({p:.4f}); two-sided p would be {two_sided:.4f}"})
    return checks


def check_paper(spec: PaperSpec, claims: list[Claim]) -> list[dict]:
    return partition_checks(spec, claims) + sidedness_checks(spec, claims)
