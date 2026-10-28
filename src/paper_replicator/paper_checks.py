"""Checks on the paper's own numbers, in code: do its subgroup counts add up, and which p-value does
each test statistic actually give? The extractor names which claims belong together; code does the
arithmetic. Neither check needs a chosen tolerance: a p-value matches a side only if it is what the printed t
gives, within the precision both are printed to (interval arithmetic over half a unit in the last digit).

Each check has a status: "ok", "flag" (the paper's numbers disagree with each other) or "note" (a fact
the reader should know, such as one-sided tests; the verdict desk uses it)."""

from __future__ import annotations

import math

from scipy import stats

from .guards import bound, half_unit, parse_number
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


def _dfs(sizes: list[float]) -> list[tuple[float, float]]:
    """Ranges the test's degrees of freedom can lie in: one sample n - 1; two samples anywhere between
    Welch's lowest (min n - 1) and the pooled n1 + n2 - 2 (Welch's df is not an integer); and always the
    normal, which regressions with clustered or robust standard errors use. Sizes unknown: any df."""
    if len(sizes) == 1:
        return [(sizes[0] - 1, sizes[0] - 1), (math.inf, math.inf)]
    if len(sizes) == 2:
        return [(min(sizes) - 1, sum(sizes) - 2), (math.inf, math.inf)]
    return [(1, math.inf)]


def _side(t: float, t_half: float, reported: float, p_range: tuple[float, float],
          dfs: list[tuple[float, float]]) -> tuple[str, float] | None:
    """The side (and its p) whose p-values over the printed t's interval and the df range reach the paper's p (its
    printed interval, or everything below or above a printed bound), closest first. Tail probabilities are monotone
    in t and in df, so the corners bound them."""
    fits = []
    for low, high in dfs:
        for side in ("two-sided", "one-sided (lower tail)", "one-sided (upper tail)"):
            ends = [_p_values(t + d, df)[side] for d in (-t_half, t_half) for df in (low, high)]
            if side == "two-sided" and abs(t) <= t_half:
                ends.append(1.0)
            if min(ends) <= p_range[1] and max(ends) >= p_range[0]:
                p = _p_values(t, high)[side]
                fits.append((abs(math.log(max(p, 1e-300)) - math.log(reported)), side, p))
    return min(fits)[1:] if fits else None


def sidedness_checks(spec: PaperSpec, claims: list[Claim]) -> list[dict]:
    values, checks = _values(claims), []
    printed = {c.name: c.value for c in claims}
    for test in spec.tests:
        if test.statistic not in values or test.p_value not in values:
            continue
        t, reported = values[test.statistic], values[test.p_value]
        if not 0 < reported < 1:
            continue
        sizes = [values[g] for g in test.group_sizes if g in values and values[g] > 1]
        dfs = _dfs(sizes)
        two_sided = _p_values(t, dfs[0][1])["two-sided"]
        direction, p_half = bound(printed[test.p_value]), half_unit(printed[test.p_value])
        p_range = ((0.0, reported) if direction == "<" else (reported, 1.0) if direction == ">" else
                   (reported - p_half, reported + p_half))
        found = _side(t, half_unit(printed[test.statistic]), reported, p_range, dfs)
        if found is None:
            checks.append({"check": "sidedness", "test": test.test, "side": None, "status": "note",
                           "text": f"{test.test}: t = {t:g} and p = {reported:g} fit no side at the printed precision "
                                   f"(two-sided p would be {two_sided:.4f}); judged two-sided"})
            continue
        side, p = found
        checks.append({"check": "sidedness", "test": test.test, "side": side,
                       "status": "ok" if side == "two-sided" else "note",
                       "text": f"{test.test}: t = {t:g}, paper's p = {reported:g} matches {side} "
                               f"({p:.4f}); two-sided p would be {two_sided:.4f}"})
    return checks


def check_paper(spec: PaperSpec, claims: list[Claim]) -> list[dict]:
    return partition_checks(spec, claims) + sidedness_checks(spec, claims)
