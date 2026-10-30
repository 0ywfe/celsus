"""The verdict desk: reported vs reproduced numbers, compared in code.

Tolerances come from the data, not from a chosen percentage:
- estimate: consistent if the paper's value lies inside the reproduction's 95% interval (value +/- 1.96 se).
  With se = 0 (the builder says the number has no sampling error, e.g. a return over a fixed period), consistent if the
  reproduction rounds to the value as printed (exact reproduction, Baek and Pradel, arXiv 2602.10046), or else
  lies within 10% of it (the coefficient threshold of Hans and Bilionis, arXiv 2607.02134; on 2604.27287, Yahoo
  data in place of the paper's CRSP put 45 of 48 such numbers within 3.4%, most within 1%).
- count, a sample total (the paper's largest count and the totals it splits into subgroups): consistent if it is the
  paper's, or within 15% of the paper's count either way, SCORE's "precise" and "approximate" reproduction of a sample size (Miske et al. 2026,
  Nature 652:126-134). The 1.96 sqrt(n) band used before held panels to a fraction of a percent: 2604.19107's 421,500
  firm-days against 416,500 (+1.2%) failed it in both of its runs. The 15% is SCORE's, not fit to this checker's runs.
- count, any other (a subgroup's size): within SCORE's 15% as well, or else within 1.96 sqrt(n), a band no published
  standard uses, kept as an allowance for small subgroups (it is the wider of the two below about 171); a row it
  passes says so. A secondary count within the published tolerance never blocks a paper.
- test_statistic: consistent if the conclusion is the same at 5% on the side the paper tested (1.96 two-sided,
  1.645 one-sided in the paper's tail; the side comes from recomputing the paper's own p-value). A significant
  result must stay significant in the same direction (the criterion of OSC 2015, Science 349 aac4716, which is
  defined for significant originals); a result that is not significant must stay not significant, whatever its
  sign, since under the null the sign is a coin flip.
  A statistic whose printed p fits no t distribution (an F or chi-squared test, or a mis-paired t and p) is
  not judged as a t; its p-value carries the conclusion.
- p_value: consistent if both are on the same side of 0.05.
- tally (how many tests were significant or rejected, regimes or breaks detected, misclassifications): a result, not
  a sample size, so it never gates the sample; consistent if the paper's value lies inside the reproduction's 95%
  interval, or, with se = 0 (no sampling error), by the fixed-number rule above; not judged without an se.
- anything without what its test needs is shown but not judged.
"""

from __future__ import annotations

import math

from .guards import bound, half_unit, numbers_in, parse_number, sample_totals
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
    if kind == "tally" and value < 0:
        return "no tally is negative"
    return None


def impossible(claims: list[Claim], results: list[dict]) -> list[tuple[str, str]]:
    """(claim name, why) for each result whose value no result of the claim's kind can take."""
    kinds = {c.name: c.kind for c in claims}
    return [(r["name"], why) for r in results
            if r.get("name") in kinds and r.get("value") is not None and (why := cannot_be(kinds[r["name"]], r["value"]))]


# SCORE (Miske et al. 2026, Nature 652:126-134, doi:10.1038/s41586-026-10203-5, pp. 7-8): an outcome is reproduced
# "approximately" when within +/-15% of what was originally reported.
COUNT_TOLERANCE = 0.15


def subgroup_match(reported: float, value: float) -> tuple[bool, str]:
    """A count that is not a sample total: consistent within SCORE's 15%, or else within 1.96 sqrt(n), an unsourced
    allowance that is the wider of the two only for counts under about 171. The why names the rule that passed."""
    score, why = count_match(reported, value)
    if score:
        return score, why
    band = Z95 * math.sqrt(abs(reported))
    inside = abs(value - reported) <= band
    if inside:
        return True, (f"{why}, but the difference {value - reported:+.0f} is within 1.96 sqrt(n) (+/-{band:.1f}), "
                      f"a band no published standard uses")
    return False, f"{why}, and outside 1.96 sqrt(n) (+/-{band:.1f}), a band no published standard uses"


def count_match(reported: float, value: float) -> tuple[bool, str]:
    """A sample size against the paper's, with SCORE's tier: precise (the same), approximate (within 15%), or not."""
    if value == reported:
        return True, "precise: the paper's count"
    if reported == 0:
        return False, f"{value:g} against the paper's 0"
    gap = (value - reported) / abs(reported)
    if abs(gap) <= COUNT_TOLERANCE:
        return True, f"approximate: {gap:+.1%}, within SCORE's +/-15%"
    return False, f"{gap:+.1%}, beyond SCORE's +/-15%"


def judge(kind: str, reported: float, result: dict, side: str = "two-sided",
          printed: str = "", total: bool = True) -> tuple[bool | None, str]:
    """(consistent, why) for one number. A count is judged by SCORE's 15% alone when it is a sample total
    (`total`), else by SCORE's 15% or the unsourced band."""
    value, se = result.get("value"), result.get("se")
    if se is not None and (isinstance(se, bool) or not isinstance(se, (int, float)) or not math.isfinite(se) or se < 0):
        se = None   # an uncertainty that is no number (se "0", -1, NaN) is none: it crashed here, or drew a nonsense band
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
        return count_match(reported, value) if total else subgroup_match(reported, value)
    if kind == "tally":   # how many tests were significant, breaks detected: a result, never the sample
        if se is None:
            return None, "a tally of what the analysis found, with no uncertainty, so it is not judged"
        if direction:   # printed as a bound ("<5"): judged against the bound, not as a fixed number
            return within_bound(direction, reported, value, se)
        if se == 0:   # a deterministic finding (12 VaR breaches against 12), judged as a fixed number
            return fixed_number(reported, value, printed)
        inside = abs(value - reported) <= Z95 * se
        return inside, f"paper {'inside' if inside else 'outside'} {value:.4g} +/- {Z95 * se:.4g}"
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
            fixed: dict[str, str] | None = None, constructed: dict[str, str] | None = None,
            totals: set[str] | None = None) -> list[dict]:
    """One row per claim. A claim is not judged when its value is not one number, when the script writes its
    result as a fixed number (`fixed`, from guards.fixed_results), or when it builds the result from the paper's
    numbers instead of the data (`constructed`, from guards.constructed_results): none is a replication of it.
    `totals` names the sample totals, judged by SCORE's 15% alone; other counts by SCORE's 15% or the unsourced band. Without it, the
    largest count is the only total (sample_totals with no partitions), never every count."""
    if totals is None:
        totals = {c.name for c in sample_totals(claims, set())}
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
                                    claim.value, totals is None or claim.name in totals)
            row.update(reproduced=result.get("value"), se=result.get("se"), n=result.get("n"),
                       consistent=consistent, why=why)
        rows.append(row)
    return rows


COULD_NOT_CHECK = "could not check"


OFF_NAMED = 3   # sample counts named in the first line; the report's table has every one


def verdict(rows: list[dict], results: list[dict] | None, failure: str | None = None,
            sample_problem: str | None = None, *, headline: str | None, unrebuilt: str | None = None) -> tuple[str, str]:
    """(verdict, reason). A checker never blames a paper for its own failure: when the run, the data or the
    rebuilt sample fails, the verdict is "could not check", never "does not hold up". Sample counts are a
    precondition for judging the results, not results themselves. The reason names every blocker, not the first:
    held-out 40c85a was blocked by a missing sample size and by 17,225 observations against 14,361, and its first
    line named only the first. A paper holds up only if its main result (`headline`) was judged and matched: held-out
    dd3e09 and 69ec49 were "holds up" with the main result never computed, which a reader of the table can't trust.
    Without a main result that matched, the most it gets is "partly holds up", and the first line says why. So
    with the paper's sample size declared not rebuilt (`unrebuilt`, the reason): the results are judged on a sample
    nobody compared with the paper's."""
    if results is None:
        return COULD_NOT_CHECK, failure or "the replication never produced results"
    blockers = [sample_problem] if sample_problem else []   # the sample checks, already joined
    off = sorted((r for r in rows if r["kind"] == "count" and r["consistent"] is False),
                 key=lambda r: -abs((r["reproduced"] or 0) - (r["reported"] or 0)))
    if off:
        named = [f"{r['name']}: {_num(r['reproduced'])} here, {_num(r['reported'])} in the paper" for r in off[:OFF_NAMED]]
        more = f", and {len(off) - OFF_NAMED} more" if len(off) > OFF_NAMED else ""
        blockers.append(f"the replication could not rebuild the paper's sample ({'; '.join(named)}{more})")
    # A zero count is an empty sample only when the paper's count, read as one number, is not zero: a paper that
    # reports 0 rejections and a run that finds 0 agree (held-out 2602.07018 lost 144 results to this), and a count
    # the checker cannot read ("0/9") says nothing about the sample.
    uncounted = {r["name"] for r in rows if r["kind"] in ("parameter", "tally")}   # draws or findings: no observations
    if any(r.get("n") == 0 and r.get("name") not in uncounted for r in results) or any(
            r["kind"] == "count" and r["reproduced"] == 0 and r["consistent"] is False for r in rows):
        blockers.append("the replication found no observations")
    if blockers:
        return COULD_NOT_CHECK, "; and ".join(blockers)
    judged = [r["consistent"] for r in rows if r["kind"] != "count" and r["consistent"] is not None]
    if not judged:
        return COULD_NOT_CHECK, "none of the paper's results could be compared"
    main = next((r for r in rows if r["name"] == headline), None) if headline else None
    if all(judged):
        return ("holds up" if main is not None and main["kind"] != "count" and main["consistent"] is True
                and not unrebuilt else "partly holds up"), ""
    if any(judged):
        return "partly holds up", ""
    # Post-headline, symmetric to (g): a paper fails only on its main result. Set 3's three "does not hold up"
    # (d36131, 6942f6, 235319) missed every number checked with the main result never computed; 6942f6's misses
    # were the script's declared PCA proxies under the paper's DFM names, which show the method changed, not that
    # the claim fails.
    if main is not None and main["kind"] != "count" and main["consistent"] is False:
        return "does not hold up", ""
    missed = f"none of the {len(judged)} checked results match"
    return COULD_NOT_CHECK, (f"{missed}, and the main result, {main['name']}, was not judged" if main is not None
                             else f"{missed}, and the paper's main result is none of the numbers checked")


def _num(value) -> str:
    return "none" if value is None else f"{value:.4g}"


def first_line(outcome: str, reason: str, rows: list[dict], headline: str | None, *,
               unrebuilt: str | None = None) -> str:
    """The report's first line: in plain words, do the paper's numbers hold up?"""
    if outcome == COULD_NOT_CHECK:
        return f"We could not check this paper: {reason}. This says nothing about whether its numbers hold."
    judged = [r for r in rows if r["kind"] != "count" and r["consistent"] is not None]
    matched = sum(r["consistent"] for r in judged)
    line = {"holds up": "The paper's numbers hold up", "partly holds up": "The paper's numbers partly hold up",
            "does not hold up": "The paper's numbers do not hold up"}[outcome]
    line += f": {matched} of {len(judged)} checked results match within their uncertainty."
    main = next((r for r in rows if r["name"] == headline), None)
    if main is None:   # a headline still written as prose after the chooser and the retry: no main result to judge
        line += " Its main result is none of the numbers checked, so it was not judged."
    elif main["reproduced"] is None:   # held-out 69ec49: "holds up", its main result never computed
        line += f" Its main result, {main['name']}, was not computed."
    elif main["kind"] == "count":   # a sample size is a precondition, not a result: it never makes a paper hold up
        line += f" Its main result, {main['name']}, is a count of the sample, not a result, so it was not judged."
    else:
        why = (main.get("why") or "no basis to compare").removesuffix(", so it is not judged")
        judged = ("consistent" if main["consistent"] else "not consistent") if main["consistent"] is not None else \
            f"not judged: {why}"
        line += (f" Its main result, {main['name']}, is {with_unit(_num(main['reported']), main['unit'])} in the paper "
                 f"and {with_unit(_num(main['reproduced']), main['unit'])} here ({judged}).")
    if unrebuilt:   # e589c6: the sample itself declared not rebuilt; the results are judged without it
        line += f" Sample size not rebuilt: {unrebuilt}."
    return line
