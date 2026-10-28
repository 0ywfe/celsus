"""The verdict desk: reported vs reproduced numbers, compared in code.

Tolerances come from the data, not from a chosen percentage:
- estimate: consistent if the paper's value lies inside the reproduction's 95% interval (value +/- 1.96 se).
- count: consistent if the difference is within 1.96 sqrt(reported) (Poisson).
- test_statistic: consistent if same sign and both significant or both not, at 5% on the side the paper
  tested (1.96 two-sided, 1.645 one-sided; the side comes from recomputing the paper's own p-value).
- p_value: consistent if both are on the same side of 0.05.
- anything without what its test needs is shown but not judged.
"""

from __future__ import annotations

import math

from .guards import parse_number
from .spec import Claim

from scipy import stats

ALPHA = 0.05  # the conventional significance level
Z95 = float(stats.norm.ppf(1 - ALPHA / 2))  # 1.96: the two-sided 95% interval for estimates


def critical(side: str) -> float:
    return float(stats.norm.ppf(1 - ALPHA)) if side.startswith("one-sided") else Z95


def judge(kind: str, reported: float, result: dict, side: str = "two-sided") -> tuple[bool | None, str]:
    value, se = result.get("value"), result.get("se")
    if value is None:
        return None, "no value"
    if kind == "estimate":
        if not se:
            return None, "no standard error"
        return abs(value - reported) <= Z95 * se, f"paper inside {value:.4g} +/- {Z95 * se:.4g}"
    if kind == "count":
        band = Z95 * math.sqrt(abs(reported))
        return abs(value - reported) <= band, f"difference {value - reported:+.0f}, band +/-{band:.1f}"
    if kind == "test_statistic":
        cut = critical(side)
        same = math.copysign(1, value) == math.copysign(1, reported) and (abs(value) >= cut) == (abs(reported) >= cut)
        return same, f"{side} at |t| {cut:.3g}: " + ("same sign and significance" if same else "sign or significance differs")
    if kind == "p_value":
        same = (value < ALPHA) == (reported < ALPHA)
        return same, f"both {'<' if value < ALPHA else '>='} {ALPHA}" if same else f"opposite sides of {ALPHA}"
    return None, "not judged"


def compare(claims: list[Claim], results: list[dict], sides: dict[str, str] | None = None) -> list[dict]:
    by_name = {r.get("name"): r for r in results}
    rows = []
    for claim in claims:
        reported = parse_number(claim.value)
        result = by_name.get(claim.name)
        row = {"name": claim.name, "kind": claim.kind, "unit": claim.unit, "reported": reported,
               "reproduced": None, "se": None, "n": None, "consistent": None, "why": "not computed"}
        if result is not None:
            consistent, why = judge(claim.kind, reported, result, (sides or {}).get(claim.name, "two-sided"))
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       consistent=consistent, why=why)
        rows.append(row)
    return rows


def verdict(rows: list[dict]) -> str:
    judged = [row["consistent"] for row in rows if row["consistent"] is not None]
    if not judged:
        return "no verdict"
    if all(judged):
        return "reproduced"
    return "partly reproduced" if any(judged) else "not reproduced"
