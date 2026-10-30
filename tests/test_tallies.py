"""A tally of what the analysis found (tests significant or rejected, regimes or breaks detected, misclassifications)
is a result, not a sample size: it is judged only against an uncertainty, and never gates the sample (held-out
a27323: the paper's 10 significant Granger pairs and 12 FDR survivors, rebuilt as 3 and 3, blocked the run as if
they were its sample; 9e6524 likewise)."""

import pytest

from paper_replicator import compare, guards, roles
from paper_replicator.spec import Claim


def claim(name: str, value: str, kind: str = "count") -> Claim:
    return Claim(name=name, description="", value=value, unit="", kind=kind, where="")


@pytest.mark.parametrize("name", [
    # count claims on disk whose names carry a tally word and no word for the data's units (17 of 1,256; all tallies)
    "n_significant_granger_05", "n_fdr_q10", "n_fdr_q05", "n_granger_fdr", "estimate_Granger_FDR_7",
    "Holm rejections across five quintile tests", "Significant pairs with Friday VIX control",
    "Weekend-greater-than-Friday contrast rejections", "n_regimes_detected", "n_breaks_detected", "var_breaches",
    "n_reject_5pct", "signif_pairs",
])
def test_a_count_named_as_a_tally_of_findings_is_a_tally(name):
    claims, moved = guards.as_tallies([claim(name, "10")])
    assert claims[0].kind == "tally" and moved == [name]


@pytest.mark.parametrize("name", [
    # sample sizes with a tally word in them: a word for the data's units keeps them counts
    "Weekend-only significant assets", "n_detected_events", "breaches_filings_total", "n_significant_firms",
    "n_fdr_tested_obs", "rejected_trades_sample",
    # and names with no tally word at all
    "n_obs", "n_no_reverse_05", "Bimodality_n_secondhalf_main_991",
])
def test_a_sample_size_is_not_a_tally(name):
    claims, moved = guards.as_tallies([claim(name, "54")])
    assert claims[0].kind == "count" and moved == []


def test_only_counts_are_re_kinded():
    claims, moved = guards.as_tallies([claim("n_significant", "3", "estimate"), claim("n_reject", "10000", "parameter")])
    assert [c.kind for c in claims] == ["estimate", "parameter"] and moved == []


@pytest.mark.parametrize("result, consistent, why", [
    ({"name": "t", "value": 3, "se": None}, None, "a tally of what the analysis found, with no uncertainty, so it is "
                                                  "not judged"),
    ({"name": "t", "value": 3}, None, "a tally of what the analysis found, with no uncertainty, so it is not judged"),
    ({"name": "t", "value": 9, "se": 1.0}, True, "paper inside 9 +/- 1.96"),
    ({"name": "t", "value": 3, "se": 1.0}, False, "paper outside 3 +/- 1.96"),
])
def test_a_tally_with_no_uncertainty_given_is_not_judged_and_with_one_is(result, consistent, why):
    row = compare.compare([claim("t", "10", "tally")], [result])[0]
    assert (row["consistent"], row["why"]) == (consistent, why)


@pytest.mark.parametrize("value, consistent", [(10, True), (11, True), (12, False), (3, False)])
def test_a_tally_the_builder_says_has_no_sampling_error_is_judged_as_a_fixed_number(value, consistent):
    """Ruling (h2), 29 Oct: se = 0 is a deterministic finding (12 VaR breaches against 12), judged exact
    or within 10%; the paper's 10 significant tests found as 3 is a finding that did not reproduce."""
    row = compare.compare([claim("t", "10", "tally")], [{"name": "t", "value": value, "se": 0}])[0]
    assert row["consistent"] is consistent


def test_an_off_tally_with_no_sampling_error_is_a_result_that_did_not_hold_not_a_sample_failure():
    claims = [claim("n_obs", "14,361"), claim("n_significant_granger_05", "10", "tally"), claim("beta", "0.42", "estimate")]
    results = [{"name": "n_obs", "value": 14361, "n": 14361}, {"name": "n_significant_granger_05", "value": 3, "se": 0},
               {"name": "beta", "value": 0.41, "se": 0.05, "n": 14361}]

    rows = compare.compare(claims, results, totals={"n_obs"})

    assert compare.verdict(rows, results, headline="beta") == ("partly holds up", "")


def test_a_negative_tally_is_no_tally():
    row = compare.compare([claim("t", "10", "tally")], [{"name": "t", "value": -2, "se": 1.0}])[0]
    assert row["consistent"] is None and "no tally is negative" in row["why"]


def test_a_tally_never_gates_the_sample():
    """a27323's shape: the sample matched, the Granger tallies did not; the tallies are results, so the verdict is
    judged on them, not blocked by them."""
    claims, _ = guards.as_tallies([claim("n_total_obs", "14,361"), claim("n_significant_granger_05", "10"),
                                   claim("n_fdr_q10", "12"), claim("beta", "0.42", "estimate")])
    results = [{"name": "n_total_obs", "value": 14547, "n": 14547}, {"name": "n_significant_granger_05", "value": 3},
               {"name": "n_fdr_q10", "value": 3, "n": 0}, {"name": "beta", "value": 0.41, "se": 0.05, "n": 14547}]

    rows = compare.compare(claims, results, totals={"n_total_obs"})

    assert guards.sample_totals(claims, set()) == [claims[0]]
    assert compare.verdict(rows, results, headline="beta") == ("holds up", "")


def test_a_tally_with_no_uncertainty_as_the_main_result_leaves_the_paper_partly():
    rows = compare.compare([claim("n_breaks", "4", "tally"), claim("beta", "0.42", "estimate")],
                           [{"name": "n_breaks", "value": 4}, {"name": "beta", "value": 0.41, "se": 0.05}])
    outcome, reason = compare.verdict(rows, [{"name": "beta", "value": 0.41, "n": 10}], headline="n_breaks")

    assert outcome == "partly holds up"
    assert "(not judged: a tally of what the analysis found, with no uncertainty)" in compare.first_line(
        outcome, reason, rows, "n_breaks")


def test_the_extractor_is_told_a_tally_from_a_sample_size():
    assert 'is a "tally"' in roles.EXTRACTOR and "how much data" in roles.EXTRACTOR


def test_a_spec_of_sample_sizes_and_tallies_has_no_result_to_check():
    """Code review: a tally is unjudged without an uncertainty, so a spec of counts and tallies is sent back for the
    paper's estimates, as a spec of counts alone is."""
    from paper_replicator import replicate
    from paper_replicator.spec import PaperSpec
    spec = PaperSpec.model_validate({
        "title": "t", "hypothesis": "h", "data_sources": [], "sample": "", "method": [], "headline": "n_obs",
        "claims": [claim("n_obs", "54").model_dump(), claim("n_breaks", "4", "tally").model_dump()],
        "partitions": [], "tests": []})
    assert replicate.NO_RESULTS in replicate.spec_problems(spec)


# (h), from 195bb3: a p-value the extractor kinded an estimate was judged by the 10% fixed-number rule (0.8444
# against 0.9956, "17.9% apart"), not by the side of 0.05 both are on.

@pytest.mark.parametrize("name, unit, value", [
    ("ttest_pvalue_copula_vs_gpr", "p-value", "0.8444"), ("overall_p_value", "", "0.0098"),
    ("p_val_holm", "", "0.03"), ("pval_size", "", "0.0019"), ("sizePValue", "", "0.02"),
    ("Overall one-sample t-test p-value", "", "0.0098"), ("beta_test", "p", "0.20"), ("beta_test", "P value", "0.2"),
    ("diff_test", "p-values", "0.5"),
])
def test_a_p_value_by_unit_or_name_is_judged_as_a_p_value(name, unit, value):
    c = Claim(name=name, description="", value=value, unit=unit, kind="estimate", where="")
    claims, moved = guards.as_p_values([c])
    assert claims[0].kind == "p_value" and moved == [name]


@pytest.mark.parametrize("name, unit, value, kind", [
    ("spy_p_rho_lag1", "", "0.31", "estimate"),       # f2d565: a bare p in a name is not a p-value
    ("sp_value_weighted", "", "0.4", "estimate"),
    ("p_valid_share", "", "0.9", "estimate"),
    ("n_pvalues_below_05", "", "12", "tally"),        # no p-value lies outside 0 to 1
    ("p_value_threshold", "", "0.05", "parameter"),   # a significance level the paper sets stays a setting
    # code review: names about p-values, not p-values, and a count of them
    ("fraction_pvalues_below_05", "", "0.12", "estimate"), ("pvalue_threshold", "", "0.05", "estimate"),
    ("p_value_cutoff", "p-value", "0.10", "other"), ("n_pvalues_significant", "", "1", "count"),
    ("beta", "%", "0.42", "estimate"),
])
def test_other_numbers_are_not_re_kinded_as_p_values(name, unit, value, kind):
    c = Claim(name=name, description="", value=value, unit=unit, kind=kind, where="")
    claims, moved = guards.as_p_values([c])
    assert claims[0].kind == kind and moved == []


def test_195bb3s_main_result_is_consistent_as_a_p_value():
    c = Claim(name="ttest_pvalue_copula_vs_gpr", description="", value="0.8444", unit="p-value", kind="estimate",
              where="")
    claims, _ = guards.as_p_values([c])
    row = compare.compare(claims, [{"name": c.name, "value": 0.995554733852911, "se": 0}])[0]
    assert row["consistent"] is True


@pytest.mark.parametrize("se", ["0", "x", -1.0, float("nan"), False, True])
def test_an_uncertainty_that_is_no_number_is_no_uncertainty_and_never_crashes(se):
    """Code review: se="0" crashed judge at Z95 * se (estimates too, since the start); a negative or NaN se drew
    a nonsense band."""
    tally = compare.compare([claim("t", "10", "tally")], [{"name": "t", "value": 3, "se": se}])[0]
    estimate = compare.compare([claim("b", "0.42", "estimate")], [{"name": "b", "value": 0.41, "se": se}])[0]
    assert tally["consistent"] is None and estimate["consistent"] is None


@pytest.mark.parametrize("value, consistent", [(4, True), (9, False)])
def test_a_tally_printed_as_a_bound_is_judged_against_the_bound(value, consistent):
    c = Claim(name="n_breaks", description="", value="<5", unit="", kind="tally", where="")
    row = compare.compare([c], [{"name": "n_breaks", "value": value, "se": 0}])[0]
    assert row["consistent"] is consistent and "bound" in row["why"]


def test_the_builder_is_told_a_sample_statistic_has_an_se():
    """(i): 32% of the v2 runs' estimates came with no se, against the instruction; a mean or coefficient computed
    from a sample is judged by its interval only when the builder gives one."""
    assert "A mean, coefficient or any statistic computed from a sample has" in roles.RESULTS_FORMAT
    assert "sampling error: give its se" in roles.RESULTS_FORMAT


def test_the_reviewer_is_told_a_paper_s_setting_is_not_a_breach_unless_the_code_ignores_it():
    """Ruling (l), 29 Oct: held-out 850904 was "could not check" over three findings on design settings
    written at the paper's values (10,000 surrogate trials, 1,000 null networks, C(14,7) = 3,432 permutations),
    claims of kind parameter, which are never judged."""
    text = " ".join(roles.REVIEWER.split())
    assert ("A setting the spec marks kind parameter, set in the code to the paper's value, is not a breach: replicating "
            "a paper means using its settings. It is a breach if the code doesn't actually use that setting (it reports "
            "10,000 trials but runs 500).") in text
