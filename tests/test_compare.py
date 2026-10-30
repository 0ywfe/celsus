import pytest

from paper_replicator.compare import compare, count_match, first_line, verdict
from paper_replicator.spec import Claim


def claim(name, value, kind):
    return Claim(name=name, description="", value=value, unit="", kind=kind, where="")


def test_each_kind_is_judged_from_the_data():
    claims = [claim("mean", "-7.49", "estimate"), claim("t", "-3.13", "test_statistic"),
              claim("p", "0.0019", "p_value"), claim("n", "54", "count"), claim("n_close", "54", "count"), claim("other", "2", "other"),
              claim("missing", "1.5", "estimate")]
    results = [{"name": "mean", "value": -6.0, "se": 1.0}, {"name": "t", "value": -2.5},
               {"name": "p", "value": 0.01}, {"name": "n", "value": 30}, {"name": "n_close", "value": 48}, {"name": "other", "value": 2}]
    rows = {r["name"]: r for r in compare(claims, results)}
    assert rows["mean"]["consistent"] is True        # -7.49 inside -6.0 +/- 1.96
    assert rows["mean"]["why"] == "paper inside -6 +/- 1.96"
    assert rows["t"]["consistent"] is True           # same sign, both beyond 1.96
    assert rows["p"]["consistent"] is True           # both below 0.05
    assert rows["n"]["consistent"] is False          # 44% short, beyond SCORE's 15%
    assert rows["n_close"]["consistent"] is True     # 11% short, within it
    assert rows["other"]["consistent"] is None
    assert rows["missing"]["why"] == "not computed"


def row(name, kind, consistent, reported=1.0, reproduced=1.0):
    return {"name": name, "kind": kind, "consistent": consistent, "reported": reported, "reproduced": reproduced,
            "unit": "%", "n": None}


def test_verdicts_judge_results_not_counts():
    ok = [{"name": "x", "value": 1.0, "n": 10}]
    assert verdict([row("a", "estimate", True), row("b", "other", None)], ok, headline="a")[0] == "holds up"
    assert verdict([row("a", "estimate", True), row("b", "estimate", False)], ok, headline="a")[0] == "partly holds up"
    assert verdict([row("a", "estimate", False)], ok, headline="a")[0] == "does not hold up"


def test_the_checker_never_blames_the_paper_for_its_own_failure():
    ok = [{"name": "x", "value": 1.0, "n": 10}]
    # run c3ab42 attempt 1: zero events, all-zero results
    assert verdict([row("n", "count", False, 54, 0), row("a", "estimate", False)], ok, headline="a")[0] == "could not check"
    assert verdict([row("n", "count", True, 54, 0)], [{"name": "n", "value": 0, "n": 0}], headline="a")[0] == "could not check"
    outcome, reason = verdict([], None, "the clean run could not complete (ConnectionError)", headline="a")
    assert outcome == "could not check" and "ConnectionError" in reason
    assert verdict([row("a", "estimate", None)], ok, headline="a") == (
        "could not check", "none of the paper's results could be compared")


@pytest.mark.parametrize("reported, value, consistent, why", [
    (416_500, 421_500, True, "approximate: +1.2%, within SCORE's +/-15%"),   # 2604.19107, both runs
    (345_220, 348_693, True, "approximate: +1.0%, within SCORE's +/-15%"),   # 2605.20137, 11f24c
    (23_757, 25_024, True, "approximate: +5.3%, within SCORE's +/-15%"),
    (50, 50, True, "precise: the paper's count"),
    (50, 43, True, "approximate: -14.0%, within SCORE's +/-15%"),
    (50, 42, False, "-16.0%, beyond SCORE's +/-15%"),
    (14_361, 17_225, False, "+19.9%, beyond SCORE's +/-15%"),                  # 40c85a
    (0, 3, False, "3 against the paper's 0"),
])
def test_sample_sizes_match_within_scores_fifteen_percent(reported, value, consistent, why):
    """SCORE (Miske et al. 2026, Nature): a reproduced outcome, sample size among them, is "approximate" within 15%."""
    assert count_match(reported, value) == (consistent, why)


def test_scores_rule_is_for_sample_totals_and_subgroup_counts_keep_the_old_band():
    """Rule T (29 Oct, amended): SCORE's 15% alone for sample totals; a subgroup's count passes
    within SCORE's 15% or the old band, labelled as unsourced. The breach paper's larger-cap firms, 29 in the
    paper and 24 rebuilt, is a subgroup; 2606.29591's 21 cross-asset instruments, 25 rebuilt, is its sample."""
    claims = [claim("n_filings", "54", "count"), claim("n_larger_cap", "29", "count"),
              claim("n_instruments", "21", "count")]
    results = [{"name": "n_filings", "value": 54}, {"name": "n_larger_cap", "value": 24},
               {"name": "n_instruments", "value": 25}]

    rows = {r["name"]: r for r in compare(claims, results, totals={"n_filings", "n_instruments"})}

    assert rows["n_filings"]["why"] == "precise: the paper's count"
    assert rows["n_larger_cap"]["consistent"] is True and "no published standard" in rows["n_larger_cap"]["why"]
    assert rows["n_instruments"]["consistent"] is False and "beyond SCORE's" in rows["n_instruments"]["why"]


def test_a_subgroup_count_within_scores_fifteen_percent_never_blocks_and_the_why_names_the_rule():
    """11f24c: the paper's 345,220 expanding-window observations, a count but not the sample total, rebuilt as
    348,693 (+1.0%), failed the old band (+/-1,151)."""
    claims = [claim("aggdiff_obs", "419715", "count"), claim("expanding_obs", "345220", "count"),
              claim("n_firms", "40", "count")]
    results = [{"name": "aggdiff_obs", "value": 419_715}, {"name": "expanding_obs", "value": 348_693},
               {"name": "n_firms", "value": 54}]

    rows = {r["name"]: r for r in compare(claims, results, totals={"aggdiff_obs"})}

    assert rows["expanding_obs"] == {**rows["expanding_obs"], "consistent": True,
                                     "why": "approximate: +1.0%, within SCORE's +/-15%"}
    assert rows["n_firms"]["consistent"] is False
    assert rows["n_firms"]["why"] == ("+35.0%, beyond SCORE's +/-15%, and outside 1.96 sqrt(n) (+/-12.4), a band no "
                                      "published standard uses")


def test_without_totals_only_the_largest_count_is_a_sample_total():
    """The reviewer's case: a caller that names no totals must not judge every subgroup by SCORE's 15%, which is
    stricter than the old band below about 171 observations (100 against 84 is 16% off but inside 19.6)."""
    claims = [claim("n_obs", "1000", "count"), claim("n_small", "100", "count")]
    results = [{"name": "n_obs", "value": 880}, {"name": "n_small", "value": 84}]

    rows = {r["name"]: r for r in compare(claims, results)}

    assert rows["n_obs"]["consistent"] is True and "SCORE" in rows["n_obs"]["why"]
    assert rows["n_small"]["consistent"] is True and "no published standard" in rows["n_small"]["why"]


def test_the_first_line_says_in_plain_words_whether_the_numbers_hold():
    rows = [row("small", "estimate", True, -7.49, -6.5), row("t", "test_statistic", False, -3.13, -1.2)]
    line = first_line("partly holds up", "", rows, "small")
    assert line.startswith("The paper's numbers partly hold up: 1 of 2 checked results match")
    assert "small, is -7.49% in the paper and -6.5% here (consistent)" in line
    assert first_line("could not check", "the replication found no observations", [], None) == (
        "We could not check this paper: the replication found no observations. "
        "This says nothing about whether its numbers hold.")


def test_the_first_line_never_calls_an_unjudged_or_uncomputed_main_result_not_consistent():
    """Held-out ec0357 and 48654c: a main result with no standard error read "not consistent"; 69ec49 said "holds up"
    without a word that its main result was never computed."""
    unjudged = {**row("main", "estimate", None, 0.6388, 0.6409), "why": "no standard error"}
    missing = {**row("main", "estimate", None, -0.771, None), "why": "not computed"}
    other = row("other", "estimate", True)

    assert "(not judged: no standard error)" in first_line("partly holds up", "", [unjudged, other], "main")
    assert "not consistent" not in first_line("partly holds up", "", [unjudged, other], "main")
    assert first_line("partly holds up", "", [missing, other], "main").endswith(
        "Its main result, main, was not computed.")


def test_a_main_result_built_from_the_papers_numbers_is_named_not_judged_once():
    claims = [claim("q", "81.71", "test_statistic"), claim("rank", "21.49", "test_statistic")]
    results = [{"name": "q", "value": 80.2, "se": None, "n": 300}, {"name": "rank", "value": 21.1, "se": None, "n": 300}]
    rows = compare(claims, results, constructed={"rank": "q with the constant 0.26 at line 113"})

    line = first_line(*verdict(rows, results, headline="rank"), rows, "rank")

    assert "(not judged: built from the paper's numbers" in line and line.count("not judged") == 1


def test_a_could_not_check_names_every_blocker():
    """Held-out 40c85a: a sample size not reported and 17,225 observations against 14,361; the first line named one."""
    rows = [row("n_obs", "count", False, 14361, 17225), row("n_assets", "count", False, 6, 9),
            row("beta", "estimate", True)]
    outcome, reason = verdict(rows, [{"name": "beta", "value": 1.0, "n": 10}],
                              sample_problem="the replication did not report the paper's sample size (n_pool_total)",
                              headline="beta")
    line = first_line(outcome, reason, rows, "beta")

    assert outcome == "could not check"
    assert "n_pool_total" in line and "n_obs: 1.722e+04 here, 1.436e+04 in the paper" in line and "n_assets" in line


@pytest.mark.parametrize("main, outcome", [
    (row("main", "estimate", True), "holds up"),                       # the control: the main result matched
    (row("main", "estimate", None, 0.42, None), "partly holds up"),    # dd3e09: never computed, 6 of 6 others matched
    (row("main", "estimate", None, -0.771, -0.8), "partly holds up"),  # 69ec49's shape: computed, not judged
    (row("main", "estimate", False), "partly holds up"),               # judged and not consistent, as before
])
def test_a_paper_holds_up_only_if_its_main_result_was_judged_and_matched(main, outcome):
    """Ruling (g), 29 Oct: "holds up" next to "main result not computed" costs the table
    its reader's trust."""
    rows = [main, row("a", "estimate", True), row("b", "estimate", True)]

    assert verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline="main") == (outcome, "")


@pytest.mark.parametrize("headline", ["", None, "Overall negative short-term reaction, stronger for small caps"])
def test_a_run_with_no_main_result_to_judge_is_partly_and_says_why(headline):
    """9ff011 and e14cdb: headlines written as prose, from before the headline chooser."""
    rows = [row("a", "estimate", True), row("b", "estimate", True)]
    outcome, reason = verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline=headline)

    assert outcome == "partly holds up"
    assert first_line(outcome, reason, rows, headline).endswith(
        "Its main result is none of the numbers checked, so it was not judged.")


def test_a_main_result_that_is_a_sample_count_never_makes_a_paper_hold_up():
    """The reviewer's case: counts are left out of the judged results, so a matched n_obs as the headline would
    have made "holds up" rest on the sample size alone."""
    rows = [row("n_obs", "count", True, 14361, 14361), row("a", "estimate", True)]
    outcome, reason = verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline="n_obs")

    assert outcome == "partly holds up"
    assert first_line(outcome, reason, rows, "n_obs").endswith(
        "Its main result, n_obs, is a count of the sample, not a result, so it was not judged.")


def test_the_first_line_of_a_main_result_never_computed_says_partly_and_why():
    rows = [row("main", "estimate", None, 0.0004, None), *(row(f"r{i}", "estimate", True) for i in range(6))]
    outcome, reason = verdict(rows, [{"name": "r0", "value": 1.0, "n": 10}], headline="main")

    assert first_line(outcome, reason, rows, "main") == (
        "The paper's numbers partly hold up: 6 of 6 checked results match within their uncertainty. Its main "
        "result, main, was not computed.")


def test_a_long_list_of_sample_gaps_is_named_up_to_a_few():
    rows = [row(f"n_{i}", "count", False, 100, 100 + 50 * i) for i in range(1, 7)]
    reason = verdict(rows, [{"name": "x", "value": 1.0, "n": 10}], headline=None)[1]

    assert reason.count(" here, ") == 3 and "and 3 more" in reason and reason.startswith(
        "the replication could not rebuild the paper's sample (n_6:")


def test_significance_uses_the_side_the_paper_tested():
    # run-20261028T144225Z-91ed39: t = -1.905 is significant one-sided (p 0.031) but not two-sided
    claims = [claim("t", "-2.41", "test_statistic")]
    results = [{"name": "t", "value": -1.905}]
    assert compare(claims, results)[0]["consistent"] is False
    assert compare(claims, results, sides={"t": "one-sided (lower tail)"})[0]["consistent"] is True


def test_a_sign_flip_between_two_null_results_is_not_a_mismatch():
    # runs 7d60fd and 4c4a02: the paper's beta t = 0.835 (p 0.796, lower tail), reproduced -0.45 and -0.72.
    # Neither is significant, so the paper's conclusion (no effect) holds; under the null the sign is a coin flip.
    claims = [claim("beta_t", "0.835", "test_statistic")]
    lower = {"beta_t": "one-sided (lower tail)"}
    assert compare(claims, [{"name": "beta_t", "value": -0.72}], sides=lower)[0]["consistent"] is True
    assert compare(claims, [{"name": "beta_t", "value": -0.72}])[0]["consistent"] is True
    # significant in the tail the paper tested: the conclusion changes
    assert compare(claims, [{"name": "beta_t", "value": -1.9}], sides=lower)[0]["consistent"] is False


def test_a_significant_result_must_stay_significant_in_the_same_direction():
    claims = [claim("t", "-3.13", "test_statistic")]
    assert compare(claims, [{"name": "t", "value": 2.5}])[0]["consistent"] is False     # flipped and significant
    assert compare(claims, [{"name": "t", "value": -1.2}])[0]["consistent"] is False    # lost significance
    lower = {"t": "one-sided (lower tail)"}
    # one-sided: significance is judged in the tail the paper tested, not by |t|
    assert compare(claims, [{"name": "t", "value": 2.5}], sides=lower)[0]["consistent"] is False
    assert compare(claims, [{"name": "t", "value": -1.7}], sides=lower)[0]["consistent"] is True


def test_units_written_as_words_get_a_space():
    from paper_replicator.compare import with_unit
    assert with_unit("-3.07", "%") == "-3.07%"
    assert with_unit("-3.07", "percent") == "-3.07 percent"
    assert with_unit("54", "") == "54"


def test_an_estimate_outside_the_interval_says_outside():
    # run 774aed: the paper's low-beta mean -4.14 against -1.724 +/- 2.374 was explained as "inside"
    row = compare([claim("low", "-4.14", "estimate")], [{"name": "low", "value": -1.724, "se": 1.2112}])[0]
    assert row["consistent"] is False and row["why"].startswith("paper outside")



def test_a_number_without_sampling_error_matches_as_printed_or_within_ten_percent():
    # run 611714 (2604.27287): cumulative returns over a fixed period, Yahoo data in place of CRSP
    claims = [claim("upro_risk", "0.005", "estimate"), claim("sso", "-11.088", "estimate"),
              claim("cov", "-2.215", "estimate"), claim("voo_cov", "0.25", "estimate"), claim("omitted", "-7.49", "estimate")]
    results = [{"name": "upro_risk", "value": 0.005353, "se": 0}, {"name": "sso", "value": -11.0882, "se": 0},
               {"name": "cov", "value": -1.981, "se": 0}, {"name": "voo_cov", "value": 0.1068, "se": 0},
               {"name": "omitted", "value": -3.93, "se": None}]
    rows = {r["name"]: r for r in compare(claims, results)}
    assert rows["upro_risk"]["consistent"] is True and rows["upro_risk"]["why"] == "rounds to the printed 0.005"
    assert rows["sso"]["consistent"] is True and rows["sso"]["why"].startswith("rounds to")
    assert rows["cov"]["consistent"] is False and rows["cov"]["why"] == "10.6% apart, beyond 10%"
    assert rows["voo_cov"]["consistent"] is False
    assert rows["omitted"]["consistent"] is None    # a sampled mean whose se was left out stays unjudged



def test_a_statistic_that_is_not_a_t_is_left_to_its_p_value():
    # 2512.12815: a Chow F of 8.79 is not judged against |t| 1.96
    from paper_replicator.compare import NO_SIDE
    row = compare([claim("chow", "8.7886", "test_statistic")], [{"name": "chow", "value": 2.1}],
                  sides={"chow": NO_SIDE})[0]
    assert row["consistent"] is None and "p-value" in row["why"]


def test_a_bound_is_judged_as_a_bound():
    claims = [claim("p_tiny", "<10^{-12}", "p_value"), claim("resid", "<10^{-3}", "estimate"),
              claim("resid_far", "<10^{-3}", "estimate"), claim("p_small", "<0.001", "p_value"),
              claim("ratio", "> 2", "estimate"), claim("resid_other", "<10^{-3}", "other")]
    results = [{"name": "p_tiny", "value": 1.5e-13}, {"name": "resid", "value": 2e-4, "se": 0},
               {"name": "resid_far", "value": 5e-3, "se": 0}, {"name": "p_small", "value": 0.2},
               {"name": "ratio", "value": 1.9, "se": 0.1}, {"name": "resid_other", "value": 0.0097, "se": 0}]
    rows = {r["name"]: r for r in compare(claims, results)}
    assert rows["p_tiny"]["reported"] == 1e-12 and rows["p_tiny"]["consistent"] is True
    assert rows["resid"]["consistent"] is True and "within the paper's bound" in rows["resid"]["why"]
    assert rows["resid_far"]["consistent"] is False
    assert rows["p_small"]["consistent"] is False
    assert rows["ratio"]["consistent"] is True     # 1.9 +/- 0.196 reaches above 2
    assert rows["resid_other"]["consistent"] is None   # the desk never judges "other", bound or not


def test_a_power_of_ten_is_compared_at_its_own_scale():
    rows = compare([claim("p", "2.70×10^{-14}", "p_value"), claim("x", "5.2\\times10^{-4}", "estimate")],
                   [{"name": "p", "value": 3e-14}, {"name": "x", "value": 5.24e-4, "se": 0}])
    assert [r["consistent"] for r in rows] == [True, True]


def test_a_zero_count_that_matches_the_paper_is_a_match_not_an_empty_sample():
    # held-out 2602.07018: the paper reports 0 Holm rejections, the run found 0, and the run was dropped as
    # "no observations" with 144 results in hand
    claims = [claim("holm_rejections", "0", "count"), claim("gap", "11.81", "estimate")]
    results = [{"name": "holm_rejections", "value": 0}, {"name": "gap", "value": 11.82, "se": 0.5, "n": 2896}]
    rows = compare(claims, results)
    assert verdict(rows, results, headline="gap") == ("holds up", "")


def test_a_zero_where_the_paper_has_observations_is_still_could_not_check():
    claims = [claim("n", "54", "count"), claim("mean", "-3.07", "estimate")]
    results = [{"name": "n", "value": 0}, {"name": "mean", "value": -3.0, "se": 1.0}]
    assert verdict(compare(claims, results), results, headline="mean")[0] == "could not check"


def test_a_value_holding_several_numbers_is_not_judged_and_says_why():
    # held-out 2602.07018: "N=1,961, Gap +30.07 bps, ..." was read as 1,961 and a reproduced gap of 30.07 was
    # marked a mismatch, 15 times; 2609.22612's "1/2" was read as 1 and marked a match for 0.5
    claims = [claim("gap", "N=1,961, Gap +30.07 bps, d=0.196, IID p=0.0008", "estimate"),
              claim("gamma", "1/2", "estimate"), claim("hits", "926 of 2,876 (32.2%)", "count"),
              claim("mean", "-7.49", "estimate")]
    results = [{"name": "gap", "value": 30.07, "se": 4.0}, {"name": "gamma", "value": 0.5, "se": 0},
               {"name": "hits", "value": 400}, {"name": "mean", "value": -7.4, "se": 1.0}]
    rows = {r["name"]: r for r in compare(claims, results)}
    for name in ("gap", "gamma", "hits"):
        assert rows[name]["consistent"] is None and rows[name]["reported"] is None, name
        assert "holds several numbers" in rows[name]["why"] and rows[name]["reproduced"] is not None
    assert rows["mean"]["consistent"] is True
    assert verdict(list(rows.values()), results, headline="mean") == ("holds up", "")   # an unread count is not a sample failure


def test_a_value_with_no_number_is_not_judged_instead_of_crashing_the_run():
    # 4 saved runs print counts as words ("three", "five"); the count's bound branch raised TypeError on them
    claims = [claim("cells", "three", "count"), claim("flag", "yes", "other"), claim("mean", "-7.49", "estimate")]
    results = [{"name": "cells", "value": 3}, {"name": "flag", "value": 1}, {"name": "mean", "value": -7.4, "se": 1.0}]
    rows = {r["name"]: r for r in compare(claims, results)}
    assert rows["cells"]["consistent"] is None and "no number the checker reads" in rows["cells"]["why"]
    assert verdict(list(rows.values()), results, headline="mean") == ("holds up", "")


def test_an_unread_count_of_zero_is_not_an_empty_sample():
    # held-out 2610.35702: "0/9" (no test of nine significant) and a run that found 0 was read as no observations
    claims = [claim("rejections", "0/9", "count"), claim("mean", "-7.49", "estimate")]
    results = [{"name": "rejections", "value": 0}, {"name": "mean", "value": -7.4, "se": 1.0}]
    assert verdict(compare(claims, results), results, headline="mean") == ("holds up", "")


def test_a_result_the_script_writes_as_a_fixed_number_is_not_judged():
    # honest runs write method inputs as results (a null win rate of 0.5, a benchmark of 1/2): they match the paper
    # by construction, so judging them would count a constant as a replication
    claims = [claim("null_win_rate", "0.50", "estimate"), claim("mean", "-7.49", "estimate")]
    results = [{"name": "null_win_rate", "value": 0.5, "se": 0}, {"name": "mean", "value": -7.4, "se": 1.0}]
    rows = {r["name"]: r for r in compare(claims, results, fixed={"null_win_rate": "0.5 at line 92"})}
    assert rows["null_win_rate"]["consistent"] is None
    assert rows["null_win_rate"]["why"] == "the script writes it as a fixed number (0.5 at line 92), so it is not judged"
    assert rows["mean"]["consistent"] is True


def test_a_value_no_result_of_its_kind_can_take_is_not_judged():
    # saboteur round 3: a p of 10 was judged a mismatch, and the paper was called "partly holds up" for it
    from paper_replicator.compare import impossible
    claims = [claim("p", "0.03", "p_value"), claim("n", "54", "count"), claim("t", "2.1", "test_statistic"),
              claim("mean", "-7.49", "estimate")]
    results = [{"name": "p", "value": 10.0}, {"name": "n", "value": -3}, {"name": "t", "value": float("nan")},
               {"name": "mean", "value": -7.4, "se": 1.0}]
    rows = {r["name"]: r for r in compare(claims, results)}
    for name in ("p", "n", "t"):
        assert rows[name]["consistent"] is None and "no " in rows[name]["why"], rows[name]["why"]
    assert verdict(list(rows.values()), results, headline="mean") == ("holds up", "")
    assert [name for name, _ in impossible(claims, results)] == ["p", "n", "t"]


STORED_UNJUDGED_MAIN = __import__("json").loads(
    (__import__("pathlib").Path(__file__).parent / "corpus" / "main_result_unjudged.json").read_text())


@pytest.mark.parametrize("run", sorted(STORED_UNJUDGED_MAIN))
def test_a_paper_does_not_hold_up_only_if_its_main_result_was_judged_and_missed(run):
    """Post-headline, 30 Oct, symmetric to (g): set 3's three "does not hold up"
    (d36131, 6942f6, 235319) each missed every checked result with its main result never computed. A miss on
    numbers that are not the paper's claim doesn't show the claim fails: 6942f6's misses were the script's declared
    PCA proxies under the paper's DFM names."""
    stored = STORED_UNJUDGED_MAIN[run]
    rows, main = stored["rows"], stored["headline"]
    assert stored["verdict_as_run"] == "does not hold up"
    assert next(r for r in rows if r["name"] == main)["consistent"] is None
    outcome, reason = verdict(rows, [{"name": "x", "value": 1.0, "n": 10}], headline=main)

    assert outcome == "could not check"
    assert reason.startswith("none of the ") and f"main result, {main}, was not judged" in reason


def test_a_main_result_judged_and_missed_still_does_not_hold_up():
    """The rule can't neuter the verdict: with the main result judged and inconsistent, and nothing matching, a
    paper still does not hold up."""
    rows = [row("main", "estimate", False), row("a", "estimate", False), row("b", "estimate", None)]
    assert verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline="main") == ("does not hold up", "")


@pytest.mark.parametrize("main", [row("main", "count", False, 54, 40), row("other", "estimate", True)])
def test_a_count_or_a_missing_main_result_never_makes_a_paper_fail(main):
    rows = [row("main", "count", True, 54, 54) if main["name"] == "other" else main, row("a", "estimate", False)]
    outcome = verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline="main" if main["name"] == "main" else None)[0]
    assert outcome != "does not hold up"


@pytest.mark.parametrize("main, headline, says", [
    (row("main", "estimate", None, 0.42, None), "main", "the main result, main, was not judged"),
    (row("main", "count", True, 54, 54), "main", "the main result, main, is a sample count, which never decides a verdict"),
    (None, None, "the paper's main result is none of the numbers checked"),
])
def test_a_miss_without_a_judged_main_result_says_why_and_is_not_a_verdict_against_the_paper(main, headline, says):
    """Post-headline, 30 Oct: after "none of the 9 checked results match", the usual
    "This says nothing about whether its numbers hold" would contradict itself."""
    rows = [*([main] if main else []), row("a", "estimate", False), row("b", "estimate", False)]
    outcome, reason = verdict(rows, [{"name": "a", "value": 1.0, "n": 10}], headline=headline)
    line = first_line(outcome, reason, rows, headline)

    assert outcome == "could not check"
    assert line == (f"We could not check this paper: none of the 2 checked results match, and {says}. A paper is "
                    "failed only on its main result, so this is not a verdict against it.")


def test_every_other_could_not_check_keeps_its_sentence():
    assert first_line("could not check", "none of the paper's results could be compared", [], "a") == (
        "We could not check this paper: none of the paper's results could be compared. This says nothing about "
        "whether its numbers hold.")
