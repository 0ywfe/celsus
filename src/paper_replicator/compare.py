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
  A statistic whose printed p fits no t distribution (an F or chi-squared test, or a mis-paired t and p) is
  not judged as a t; its p-value carries the conclusion.
- p_value: consistent if both are on the same side of 0.05.
- anything without what its test needs is shown but not judged.
"""

from __future__ import annotations

import math

from .guards import bound, half_unit, numbers_in, parse_number
from .spec import Claim

from scipy import stats

ALPHA = 0.05  # the conventional significance level
Z95 = float(stats.norm.ppf(1 - ALPHA / 2))  # 1.96: the two-sided 95% interval for estimates
NO_SIDE = "no side"  # the paper check found no t distribution that gives the printed p
RELATIVE = 0.10  # for an estimate without a standard error: Hans and Bilionis's coefficient threshold



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


def cannot_be(kind: str, value) -> str | None:
    """Why no result of this kind can take this value (a p of 10, a count of -3, NaN), or None. Such a number is
    the replication's failure, never the paper's, so it is sent back and, if it stays, not judged."""
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return "no result is NaN or infinite"
    if kind == "p_value" and not 0 <= value <= 1:
        return "no p-value lies outside 0 to 1"
    if kind == "count" and value < 0:
        return "no count is negative"
    return None


def impossible(claims: list[Claim], results: list[dict]) -> list[tuple[str, str]]:
    """(claim name, why) for each result whose value no result of the claim's kind can take."""
    kinds = {c.name: c.kind for c in claims}
    return [(r["name"], why) for r in results
            if r.get("name") in kinds and r.get("value") is not None and (why := cannot_be(kinds[r["name"]], r["value"]))]


def judge(kind: str, reported: float, result: dict, side: str = "two-sided",
          printed: str = "") -> tuple[bool | None, str]:
    value, se = result.get("value"), result.get("se")
    if value is None:
        return None, "no value"
    if (why := cannot_be(kind, value)) is not None:
        return None, f"the replication's value is {value}, and {why}, so it is not judged"
    direction = bound(printed) if printed else None
    if direction and kind in ("estimate", "test_statistic", "count"):  # "other" stays unjudged, bound or not
        return within_bound(direction, reported, value, se)
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
    if kind == "test_statistic" and side == NO_SIDE:
        return None, "its p fits no t distribution; judged by its p-value"
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
        paper_below = (reported < ALPHA if direction is None else
                       True if direction == "<" and reported <= ALPHA else
                       False if direction == ">" and reported >= ALPHA else None)
        if paper_below is None:  # p < 0.1 or p > 0.01: the bound does not say which side of 0.05 the paper is on
            return within_bound(direction, reported, value, None)
        same = (value < ALPHA) == paper_below
        return same, f"both {'<' if value < ALPHA else '>='} {ALPHA}" if same else f"opposite sides of {ALPHA}"
    return None, "not judged"


def within_bound(direction: str, limit: float, value: float, se: float | None) -> tuple[bool, str]:
    """A number the paper prints as a bound (< 10^{-3}, > 2): consistent when the reproduction, or its 95% interval
    when it has one, reaches the bound's side."""
    reach = Z95 * se if se else 0.0
    inside = value - reach < limit if direction == "<" else value + reach > limit
    shown = f"{value:.4g}" + (f" +/- {reach:.4g}" if reach else "")
    return inside, f"{shown} {'within' if inside else 'outside'} the paper's bound {direction} {limit:g}"


def fixed_number(reported: float, value: float, printed: str) -> tuple[bool, str]:
    """An estimate with no sampling error: the same printed number, or else within RELATIVE of it."""
    if abs(value - reported) <= half_unit(printed or f"{reported}") * (1 + 1e-9):
        return True, f"rounds to the printed {printed or reported}"
    apart = abs(value - reported) / abs(reported) if reported else math.inf
    close = apart <= RELATIVE
    return close, f"{apart:.1%} apart, {'within' if close else 'beyond'} {RELATIVE:.0%}"


def compare(claims: list[Claim], results: list[dict], sides: dict[str, str] | None = None,
            fixed: dict[str, str] | None = None, constructed: dict[str, str] | None = None) -> list[dict]:
    """One row per claim. A claim is not judged when its value is not one number, when the script writes its
    result as a fixed number (`fixed`, from guards.fixed_results), or when it builds the result from the paper's
    numbers instead of the data (`constructed`, from guards.constructed_results): none is a replication of it."""
    by_name = {r.get("name"): r for r in results}
    rows = []
    for claim in claims:
        reported = parse_number(claim.value)
        result = by_name.get(claim.name)
        row = {"name": claim.name, "kind": claim.kind, "unit": claim.unit, "reported": reported,
               "reproduced": None, "se": None, "n": None, "consistent": None, "why": "not computed"}
        if result is not None and claim.kind == "parameter":
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       why="a parameter the paper sets in its method, not a result, so it is not judged")
        elif result is not None and claim.name in (constructed or {}):
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       why=f"built from the paper's numbers, not computed from the data ({constructed[claim.name]}), "
                           f"so it is not judged")
        elif result is not None and claim.name in (fixed or {}):
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       why=f"the script writes it as a fixed number ({fixed[claim.name]}), so it is not judged")
        elif result is not None and (count := numbers_in(claim.value)) != 1:  # no single number to judge against
            held = "several numbers" if count else "no number the checker reads"
            row.update(reported=None, reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       why=f"the paper's value \"{claim.value}\" holds {held}, so it is not judged")
        elif result is not None:
            consistent, why = judge(claim.kind, reported, result, (sides or {}).get(claim.name, "two-sided"),
                                    claim.value)
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       consistent=consistent, why=why)
        rows.append(row)
    return rows


COULD_NOT_CHECK = "could not check"


def verdict(rows: list[dict], results: list[dict] | None, failure: str | None = None,
            sample_problem: str | None = None) -> tuple[str, str]:
    """(verdict, reason). A checker never blames a paper for its own failure: when the run, the data or the
    rebuilt sample fails, the verdict is "could not check", never "does not hold up". Sample counts are a
    precondition for judging the results, not results themselves."""
    if results is None:
        return COULD_NOT_CHECK, failure or "the replication never produced results"
    if sample_problem:  # the sample cannot be compared with the paper's: a different period, or not rebuilt
        return COULD_NOT_CHECK, sample_problem
    off = [r for r in rows if r["kind"] == "count" and r["consistent"] is False]
    if off:
        worst = max(off, key=lambda r: abs((r["reproduced"] or 0) - (r["reported"] or 0)))
        return COULD_NOT_CHECK, (f"the replication could not rebuild the paper's sample ({worst['name']}: "
                                 f"{_num(worst['reproduced'])} here, {_num(worst['reported'])} in the paper)")
    # A zero count is an empty sample only when the paper's count, read as one number, is not zero: a paper that
    # reports 0 rejections and a run that finds 0 agree (held-out 2602.07018 lost 144 results to this), and a count
    # the checker cannot read ("0/9") says nothing about the sample.
    settings = {r["name"] for r in rows if r["kind"] == "parameter"}   # a number of draws has no observations
    if any(r.get("n") == 0 and r.get("name") not in settings for r in results) or any(
            r["kind"] == "count" and r["reproduced"] == 0
                                                     and r["consistent"] is False for r in rows):
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
