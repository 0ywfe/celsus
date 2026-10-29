"""Results built from the paper's own numbers rather than computed from the data are not judged (29 Oct audit)."""

import ast
import json
from pathlib import Path

import pytest

from paper_replicator import compare, guards, results_code
from paper_replicator.spec import Claim

CORPUS = Path(__file__).parent / "corpus"


def claims_of(name: str) -> list[Claim]:
    return [Claim.model_validate(c) for c in json.loads((CORPUS / name).read_text())["claims"]]


def claim(name: str, value: str, kind: str = "estimate", unit: str = "") -> Claim:
    return Claim(name=name, description="", value=value, unit=unit, kind=kind, where="")


@pytest.mark.parametrize("expression, value", [
    ('int(float("1e4"))', 10_000),
    ('float("2" + ".39")', 2.39),
    ('float("".join(["5", ".6"]))', 5.6),
    ('float(f"1.8e6")', 1.8e6),
    ('eval("1923+1395")', 3318),
    ('ast.literal_eval("0.0425")', 0.0425),
    ('Decimal("298.62")', 298.62),
    ('np.float64("0.263")', 0.263),
    ('len("abc")', 3),
    ('len("abcdefghij" * len("abc"))', 30),
])
def test_numbers_written_so_the_literal_check_cant_read_them_fold_to_constants(expression, value):
    assert results_code.evaluate(ast.parse(expression, mode="eval").body, {}) == pytest.approx(value)


@pytest.mark.parametrize("expression, value", [
    ('len("a" * 1000 * 1000 * 1000 * 1000)', 1e12),               # kept as a length: no terabyte string
    ('len("".join(["ab" * 1000000, "c" * 1000000]))', 3e6),
    ("len(" + " + ".join(['"ab"'] * 3000) + ")", 6000),             # thousands of pieces: no recursion
])
def test_text_of_any_length_folds_without_building_it(expression, value):
    assert results_code.evaluate(ast.parse(expression, mode="eval").body, {}) == value


def test_text_too_long_to_be_a_number_is_not_read_as_one():
    assert results_code.evaluate(ast.parse("float(" + " + ".join(['"1"'] * 3000) + ")", mode="eval").body, {}) is None


@pytest.mark.parametrize("expression", ['float("nan")', 'float("inf")', 'float(text)', 'int(row["year"])',
                                        'eval(user_code)', 'float("1,5")'])
def test_casts_of_unknown_or_non_finite_text_stay_unknown(expression):
    assert results_code.evaluate(ast.parse(expression, mode="eval").body, {}) is None


def test_the_literal_guard_sees_through_a_dodged_literal():
    script = 'size = float("2" + ".39")\nadd("storage_total", size, 0, 1)\n'
    assert guards.hardcoded_results(script, [claim("storage_total", "2.39", unit="GB")])


def test_a_sample_cut_to_a_count_spelled_as_string_lengths_is_caught():
    """29 Oct, run b93abc: the paper's 50 written as len("abcdefghij") * len("abcde"), then ev.head(_FIFTY)."""
    script = '_TEN = len("abcdefghij")\n_FIFTY = _TEN * len("abcde")\ntop = ev.head(_FIFTY)\nadd("n_events", len(top), 0, 1)\n'
    totals = [claim("n_events", "50", kind="count")]
    assert guards.hardcoded_counts(script, totals, totals)


def test_a_count_written_as_int_float_1e4_is_a_fixed_number():
    script = 'paths = int(float("1e4"))\nadd("n_paths", paths, 0, paths)\n'
    assert "n_paths" in guards.fixed_results(script, [claim("n_paths", "10,000", kind="count")])


def test_statistics_rescaled_by_the_papers_own_ratios_are_constructed():
    script = (CORPUS / "construction_2601.19321.py").read_text()
    claims = claims_of("spec_2601.19321_march.json")

    built = guards.constructed_results(script, claims)

    assert set(built) == {"march_var_rank", "march_var_robust", "march_tvp_rank", "march_tvp_robust",
                          "march_var_rank_p", "march_var_robust_p", "march_tvp_rank_p"}
    assert "0.26" in built["march_var_rank"] and "march_var_qm" in built["march_var_rank"]
    assert "march_var_rank" in built["march_var_rank_p"]          # computed from a constructed result


def test_compute_times_built_from_a_throughput_are_constructed():
    script = (CORPUS / "construction_2509.19663.py").read_text()
    claims = claims_of("spec_2509.19663_accounting.json")

    built, fixed = guards.constructed_results(script, claims), guards.fixed_results(script, claims)

    assert {"comput_train_time_per_asset", "comput_train_time_total_serial", "comput_validation_time_per_asset",
            "comput_validation_time_total"} <= set(built)
    assert "cancel" in built["comput_train_time_per_asset"]
    assert {"N_gen_paths_per_asset", "N_rs_dfa_fits_per_asset"} <= set(fixed)   # int(float("1e4")) and 2 x it
    assert "1.8e+06" in built["comput_validation_time_total"]
    assert "N_total_daily_returns_per_path" not in built | fixed    # len(rets): from the data


@pytest.mark.parametrize("script", [
    # the audit's non-constructions, each the shape of a real held-out script
    ("ll = model.llf\naic = 2 * 18 - 2 * ll\nbic = 18 * np.log(len(y)) - 2 * ll\n"
     "add('loglik', ll, 0, 1); add('aic', aic, 0, 1); add('bic', bic, 0, 1)\n"),
    "sr = r.mean() / r.std()\nadd('sharpe_m', sr, 0, 1); add('sharpe_ann', sr * np.sqrt(12), 0, 1)\n",
    "m = r.mean()\nadd('mean_m', m, 0, 1); add('mean_pct_ann', m * 12 * 100, 0, 1)\n",
    ("b, se = fit.params[1], fit.bse[1]\nadd('beta', b, se, 1); add('se_beta', se, 0, 1)\n"
     "add('ci_high', b + 1.96 * se, 0, 1); add('half_width', 1.96 * se, 0, 1)\n"),
    "EP = 20\nn_ep = R.shape[0] - EP + 1\nadd('n_epochs', n_ep, 0, n_ep)\n",
    "p3, p5 = f3.pvalue, f5.pvalue\nadd('p_3y', p3, 0, 1); add('p_holm', 2 * min(p3, p5), 0, 1)\n",
    ("na, nd = len(assets), len(days)\nadd('n_assets', na, 0, na); add('n_days', nd, 0, nd); "
     "add('n_obs', na * nd, 0, na * nd)\n"),
    "events = []\nfor e in feed: events.append(e)\nadd('total_filings', len(events), 0, len(events))\n",
    "x = df['a'].sum()\nadd('a_total', x, 0, 1); add('a_bp', x * 1e4, 0, 1)\n",
    # held-out caa208: three names unpacked from one call are three inputs, not one
    "o, mo, mc = analyze(df)\nadd('median_open', mo, 0, 1); add('median_diff', mo - mc, 0, 1)\n",
    # held-out 5b3635 and 9e6524: floor division of a count is still a count of the data
    "k = len(sectors)\nn_pairs = k * (k - 1) // 2\nadd('n_sectors', k, 0, k); add('n_pairs', n_pairs, 0, n_pairs)\n",
    "B = len(draws)\nadd('n_boot', B, 0, B); add('n_filtered', int(B // 2), 0, 1)\n",
    # held-out 1247d1: generated returns per asset are paths x days, both counts
    "T = len(rets)\nadd('n_returns_per_path', T, 0, T); add('n_generated_returns_per_asset', T * 300, 0, T)\n",
    # held-out c5ffce: a floor division that comes to 0 for small draws
    "S = len(series)\nadd('n_days', S, 0, S); add('reversion_days', int((S // 3) // 30), 0, S)\n",
])
def test_results_computed_from_the_data_are_not_constructed(script):
    names = [n.id if isinstance(n, ast.Name) else n.value for node in ast.walk(ast.parse(script))
             if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "add"
             for n in node.args[:1]]
    claims = [claim(n, "1.5", kind="count" if n.startswith(("n_", "total")) else "estimate") for n in names]

    assert guards.constructed_results(script, claims) == {}


def test_a_factor_written_as_text_is_still_a_constant():
    script = "q = stat(x)\nadd('qm', q, 0, 1)\nadd('rank', q * float('0.26'), 0, 1)\n"
    built = guards.constructed_results(script, [claim("qm", "81.71"), claim("rank", "21.49")])
    assert "0.26" in built["rank"]


def test_a_result_computed_from_a_constructed_one_through_a_container_is_constructed():
    script = ("q = stat(x)\nrank = q * 0.26\nrow = {'stat': rank}\np = chi2.sf(row['stat'], 5)\n"
              "add('qm', q, 0, 1)\nadd('rank', rank, 0, 1)\nadd('rank_p', p, 0, 1)\n")
    built = guards.constructed_results(script, [claim("qm", "81.71"), claim("rank", "21.49"), claim("rank_p", "0.001")])
    assert set(built) == {"rank", "rank_p"}


@pytest.mark.parametrize("script", [
    # the reviewer's cases: a factor of the method, not a ratio of the paper's results
    "se = fit.bse[1]\nadd('se', se, 0, 1); add('half_width', 1.959964 * se, 0, 1)\n",
    "k = fit.params[1]\nadd('kappa', k, 0, 1); add('half_life', 0.693147 / k, 0, 1)\n",
    "v = r.std()\nadd('vol_d', v, 0, 1); add('vol_ann', v * np.sqrt(250), 0, 1)\n",
    "s = mad(r)\nadd('mad', s, 0, 1); add('sigma_robust', 1.4826 * s, 0, 1)\n",
    "n = len(df)\nadd('n_obs', n, 0, n); add('n_train', int(n * 0.8), 0, n)\n",   # a count's share is a count
])
def test_factors_of_the_method_are_not_constructions(script):
    names = [n.value for node in ast.walk(ast.parse(script)) if isinstance(node, ast.Call)
             and getattr(node.func, "id", None) == "add" for n in node.args[:1]]
    claims = [claim(n, "1.5", kind="count" if n.startswith("n_") else "estimate") for n in names]

    assert guards.constructed_results(script, claims) == {}


@pytest.mark.parametrize("factor", ["(365 / 12)", "(24 * 365)", "(52 / 12)", "(1 / (24 * 365))", "(60 * 60 * 24 * 365)",
                                    "1.645", "1.65", "1.28", "2.58", "0.693"])
def test_a_group_of_unit_factors_or_a_rounded_quantile_is_not_a_construction(factor):
    script = f"q = stat(x)\nadd('qm', q, 0, 1)\nadd('r', q * {factor}, 0, 1)\n"
    assert guards.constructed_results(script, [claim("qm", "1"), claim("r", "2")]) == {}


@pytest.mark.parametrize("factor", ["0.26", "3.8", "(13 * 2)", "1.5", "0.67", "3.14"])
def test_a_factor_that_is_no_unit_or_quantile_is_a_construction(factor):
    script = f"q = stat(x)\nadd('qm', q, 0, 1)\nadd('r', q * {factor}, 0, 1)\n"
    assert "r" in guards.constructed_results(script, [claim("qm", "1"), claim("r", "2")])


def test_padding_a_rescaled_result_with_thousands_of_unit_factors_does_not_hide_it():
    script = "q = stat(x)\nadd('qm', q, 0, 1)\nadd('r', q * 0.26" + " * 1" * 3000 + ", 0, 1)\n"
    assert "0.26" in guards.constructed_results(script, [claim("qm", "1"), claim("r", "2")])["r"]


def test_an_expression_too_deep_to_follow_builds_nothing_and_does_not_crash():
    script = "q = stat(x)\nadd('qm', q, 0, 1)\nadd('big', q" + " * x" * 3000 + ", 0, 1)\n"
    assert guards.constructed_results(script, [claim("qm", "1"), claim("big", "2")]) == {}


def test_a_constructed_result_is_reported_but_not_judged():
    claims = [claim("q", "81.71", "test_statistic"), claim("rank", "21.49", "test_statistic")]
    results = [{"name": "q", "value": 772.2, "se": None, "n": 300}, {"name": "rank", "value": 200.8, "se": None, "n": 300}]

    rows = {r["name"]: r for r in compare.compare(claims, results, constructed={"rank": "q x 0.26 at line 113"})}

    assert rows["rank"]["consistent"] is None and rows["rank"]["reproduced"] == 200.8
    assert "built from the paper's numbers" in rows["rank"]["why"] and "q x 0.26" in rows["rank"]["why"]
    assert rows["q"]["consistent"] is not None
