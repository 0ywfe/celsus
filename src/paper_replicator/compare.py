"""The verdict desk: reported vs reproduced numbers, compared in code.

Tolerances come from the data, not from a chosen percentage:
- estimate: consistent if the paper's value lies inside the reproduction's 95% interval (value +/- 1.96 se).
  With se = 0 (the builder says the number has no sampling error, e.g. a return over a fixed period), consistent if the
  reproduction rounds to the value as printed (exact reproduction, Baek and Pradel, arXiv 2602.10046), or else
  lies within 10% of it (the coefficient threshold of Hans and Bilionis, arXiv 2607.02134; on 2604.27287, Yahoo
  data in place of the paper's CRSP put 45 of 48 such numbers within 3.4%, most within 1%).
- count: consistent if the difference is within 1.96 sqrt(reported) (Poisson).
- test_statistic: consistent if the conclusion is the same at 5% on the side the paper tested (1.96 two-sided,
  1.645 one-sided in the paper's tail; the side comes from recomputing the paper's own p-value). A significant
  result must stay significant in the same direction (the criterion of OSC 2015, Science 349 aac4716, which is
  defined for significant originals); a result that is not significant must stay not significant, whatever its
  sign, since under the null the sign is a coin flip.
- p_value: consistent if both are on the same side of 0.05.
- anything without what its test needs is shown but not judged.
"""

from __future__ import annotations

import math

from .guards import magnitude, parse_number
from .spec import Claim

from scipy import stats

ALPHA = 0.05  # the conventional significance level
Z95 = float(stats.norm.ppf(1 - ALPHA / 2))  # 1.96: the two-sided 95% interval for estimates
RELATIVE = 0.10  # for an estimate without a standard error: Hans and Bilionis's coefficient threshold


def half_unit(printed: str) -> float:
    """Half a unit in the last digit the paper printed: how far a number can be from it and still print the same."""
    digits = magnitude(printed) or ""
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return 0.5 * 10 ** -decimals


def critical(side: str) -> float:
    return float(stats.norm.ppf(1 - ALPHA)) if side.startswith("one-sided") else Z95


def significant(t: float, side: str) -> bool:
    """Significant at 5% on the side the paper tested: a one-sided test counts only its own tail."""
    cut = critical(side)
    if side == "one-sided (lower tail)":
        return t <= -cut
    if side == "one-sided (upper tail)":
        return t >= cut
    return abs(t) >= cut


def with_unit(number: str, unit: str) -> str:
    """A number with its unit as the paper prints it: '-3.07%', '-3.07 percent'."""
    if not unit:
        return number
    return f"{number}{unit}" if unit.startswith("%") else f"{number} {unit}"


def judge(kind: str, reported: float, result: dict, side: str = "two-sided",
          printed: str = "") -> tuple[bool | None, str]:
    value, se = result.get("value"), result.get("se")
    if value is None:
        return None, "no value"
    if kind == "estimate":
        if se is None:
            return None, "no standard error"
        if se == 0:  # the builder's way of saying the number has no sampling error
            return fixed_number(reported, value, printed)
        inside = abs(value - reported) <= Z95 * se
        return inside, f"paper {'inside' if inside else 'outside'} {value:.4g} +/- {Z95 * se:.4g}"
    if kind == "count":
        band = Z95 * math.sqrt(abs(reported))
        return abs(value - reported) <= band, f"difference {value - reported:+.0f}, band +/-{band:.1f}"
    if kind == "test_statistic":
        paper, here = significant(reported, side), significant(value, side)
        if paper and here:
            same = math.copysign(1, value) == math.copysign(1, reported)
            why = "both significant, same direction" if same else "both significant, opposite directions"
        else:
            same = paper == here
            why = ("neither significant" if same else
                   "significant in the paper, not here" if paper else "significant here, not in the paper")
        return same, f"{side} at |t| {critical(side):.3g}: {why}"
    if kind == "p_value":
        same = (value < ALPHA) == (reported < ALPHA)
        return same, f"both {'<' if value < ALPHA else '>='} {ALPHA}" if same else f"opposite sides of {ALPHA}"
    return None, "not judged"


def fixed_number(reported: float, value: float, printed: str) -> tuple[bool, str]:
    """An estimate with no sampling error: the same printed number, or else within RELATIVE of it."""
    if abs(value - reported) <= half_unit(printed or f"{reported}") * (1 + 1e-9):
        return True, f"rounds to the printed {printed or reported}"
    apart = abs(value - reported) / abs(reported) if reported else math.inf
    close = apart <= RELATIVE
    return close, f"{apart:.1%} apart, {'within' if close else 'beyond'} {RELATIVE:.0%}"


def compare(claims: list[Claim], results: list[dict], sides: dict[str, str] | None = None) -> list[dict]:
    by_name = {r.get("name"): r for r in results}
    rows = []
    for claim in claims:
        reported = parse_number(claim.value)
        result = by_name.get(claim.name)
        row = {"name": claim.name, "kind": claim.kind, "unit": claim.unit, "reported": reported,
               "reproduced": None, "se": None, "n": None, "consistent": None, "why": "not computed"}
        if result is not None:
            consistent, why = judge(claim.kind, reported, result, (sides or {}).get(claim.name, "two-sided"),
                                    claim.value)
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       consistent=consistent, why=why)
        rows.append(row)
    return rows


COULD_NOT_CHECK = "could not check"


def verdict(rows: list[dict], results: list[dict] | None, failure: str | None = None) -> tuple[str, str]:
    """(verdict, reason). A checker never blames a paper for its own failure: when the run, the data or the
    rebuilt sample fails, the verdict is "could not check", never "does not hold up". Sample counts are a
    precondition for judging the results, not results themselves."""
    if results is None:
        return COULD_NOT_CHECK, failure or "the replication never produced results"
    off = [r for r in rows if r["kind"] == "count" and r["consistent"] is False]
    if off:
        worst = max(off, key=lambda r: abs((r["reproduced"] or 0) - (r["reported"] or 0)))
        return COULD_NOT_CHECK, (f"the replication could not rebuild the paper's sample ({worst['name']}: "
                                 f"{_num(worst['reproduced'])} here, {_num(worst['reported'])} in the paper)")
    if any(r.get("n") == 0 for r in results) or any(r["kind"] == "count" and r["reproduced"] == 0 for r in rows):
        return COULD_NOT_CHECK, "the replication found no observations"
    judged = [r["consistent"] for r in rows if r["kind"] != "count" and r["consistent"] is not None]
    if not judged:
        return COULD_NOT_CHECK, "none of the paper's results could be compared"
    if all(judged):
        return "holds up", ""
    return ("partly holds up" if any(judged) else "does not hold up"), ""


def _num(value) -> str:
    return "none" if value is None else f"{value:.4g}"


def first_line(outcome: str, reason: str, rows: list[dict], headline: str | None) -> str:
    """The report's first line: in plain words, do the paper's numbers hold up?"""
    if outcome == COULD_NOT_CHECK:
        return f"We could not check this paper: {reason}. This says nothing about whether its numbers hold."
    judged = [r for r in rows if r["kind"] != "count" and r["consistent"] is not None]
    matched = sum(r["consistent"] for r in judged)
    line = {"holds up": "The paper's numbers hold up", "partly holds up": "The paper's numbers partly hold up",
            "does not hold up": "The paper's numbers do not hold up"}[outcome]
    line += f": {matched} of {len(judged)} checked results match within their uncertainty."
    main = next((r for r in rows if r["name"] == headline), None)
    if main is not None and main["reproduced"] is not None:
        line += (f" Its main result, {main['name']}, is {with_unit(_num(main['reported']), main['unit'])} in the paper "
                 f"and {with_unit(_num(main['reproduced']), main['unit'])} here "
                 f"({'consistent' if main['consistent'] else 'not consistent'}).")
    return line
