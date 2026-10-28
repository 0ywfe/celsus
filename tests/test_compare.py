from paper_replicator.compare import compare, first_line, verdict
from paper_replicator.spec import Claim


def claim(name, value, kind):
    return Claim(name=name, description="", value=value, unit="", kind=kind, where="")


def test_each_kind_is_judged_from_the_data():
    claims = [claim("mean", "-7.49", "estimate"), claim("t", "-3.13", "test_statistic"),
              claim("p", "0.0019", "p_value"), claim("n", "54", "count"), claim("n_close", "54", "count"), claim("other", "2", "other"),
              claim("missing", "1.5", "estimate")]
    results = [{"name": "mean", "value": -6.0, "se": 1.0}, {"name": "t", "value": -2.5},
               {"name": "p", "value": 0.01}, {"name": "n", "value": 30}, {"name": "n_close", "value": 40}, {"name": "other", "value": 2}]
    rows = {r["name"]: r for r in compare(claims, results)}
    assert rows["mean"]["consistent"] is True        # -7.49 inside -6.0 +/- 1.96
    assert rows["t"]["consistent"] is True           # same sign, both beyond 1.96
    assert rows["p"]["consistent"] is True           # both below 0.05
    assert rows["n"]["consistent"] is False          # 24 apart, band 1.96*sqrt(54) = 14.4
    assert rows["n_close"]["consistent"] is True     # 14 apart, inside the band
    assert rows["other"]["consistent"] is None
    assert rows["missing"]["why"] == "not computed"


def row(name, kind, consistent, reported=1.0, reproduced=1.0):
    return {"name": name, "kind": kind, "consistent": consistent, "reported": reported, "reproduced": reproduced,
            "unit": "%", "n": None}


def test_verdicts_judge_results_not_counts():
    ok = [{"name": "x", "value": 1.0, "n": 10}]
    assert verdict([row("a", "estimate", True), row("b", "other", None)], ok)[0] == "holds up"
    assert verdict([row("a", "estimate", True), row("b", "estimate", False)], ok)[0] == "partly holds up"
    assert verdict([row("a", "estimate", False)], ok)[0] == "does not hold up"


def test_the_checker_never_blames_the_paper_for_its_own_failure():
    ok = [{"name": "x", "value": 1.0, "n": 10}]
    # run c3ab42 attempt 1: zero events, all-zero results
    assert verdict([row("n", "count", False, 54, 0), row("a", "estimate", False)], ok)[0] == "could not check"
    assert verdict([row("n", "count", True, 54, 0)], [{"name": "n", "value": 0, "n": 0}])[0] == "could not check"
    outcome, reason = verdict([], None, "the clean run could not complete (ConnectionError)")
    assert outcome == "could not check" and "ConnectionError" in reason
    assert verdict([row("a", "estimate", None)], ok) == ("could not check", "none of the paper's results could be compared")


def test_the_first_line_says_in_plain_words_whether_the_numbers_hold():
    rows = [row("small", "estimate", True, -7.49, -6.5), row("t", "test_statistic", False, -3.13, -1.2)]
    line = first_line("partly holds up", "", rows, "small")
    assert line.startswith("The paper's numbers partly hold up: 1 of 2 checked results match")
    assert "small, is -7.49% in the paper and -6.5 here (consistent)" in line
    assert first_line("could not check", "the replication found no observations", [], None) == (
        "We could not check this paper: the replication found no observations. "
        "This says nothing about whether its numbers hold.")


def test_significance_uses_the_side_the_paper_tested():
    # run-20261028T144225Z-91ed39: t = -1.905 is significant one-sided (p 0.031) but not two-sided
    claims = [claim("t", "-2.41", "test_statistic")]
    results = [{"name": "t", "value": -1.905}]
    assert compare(claims, results)[0]["consistent"] is False
    assert compare(claims, results, sides={"t": "one-sided (lower tail)"})[0]["consistent"] is True
