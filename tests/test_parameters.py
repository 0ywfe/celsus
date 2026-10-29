"""A number the paper sets in its method (draws, paths, windows, caps) is a parameter, not a result or a sample
size: it is never judged, never gates the sample, and code may write it (held-out set 2's paper-set-parameter
record: 14 rejections in 11 runs on 10 papers, 29 Oct)."""

import pytest

from paper_replicator import compare, guards, replicate
from paper_replicator.spec import Claim, PaperSpec, reference_problems

SPEC = {"title": "", "hypothesis": "", "data_sources": [], "sample": "", "method": [], "partitions": [], "tests": []}


def claim(name: str, value: str, kind: str = "count", description: str = "", unit: str = "") -> Claim:
    return Claim(name=name, description=description, value=value, unit=unit, kind=kind, where="")


@pytest.mark.parametrize("name", [
    # the set-2 record's paper-set parameters, and others on disk
    "n_llm_paths", "n_monte_carlo", "n_mc_replications", "n_sim_draws", "n_reps_5000", "N_rs_dfa_fits_total",
    "n_gen_paths_per_asset", "n_surrogate_trials", "K_permutations", "B_bootstrap", "n_boot", "n_starts_mc",
    "sim_T_500", "n_sims_1000", "Bootstrap Resamples", "nBootstrapReplicates",
])
def test_a_count_of_draws_paths_or_replications_is_a_parameter(name):
    claims, moved = guards.as_parameters([claim(name, "10,000")])
    assert claims[0].kind == "parameter" and moved == [name]


@pytest.mark.parametrize("name", [
    # sample sizes on disk that share a word with a draw count: they stay counts and keep gating the sample
    "returns_per_path", "n_returns_per_path", "N_total_daily_returns_per_path", "n_firm_quarters_evaluation",
    "n_industrials_firm_quarters", "companies_one_report", "total_8k_reports", "total_portfolio_obs",
    "count_simulation_calendar_total", "n_perm_group", "n_pool_total", "n_events_total",
    # the reviewer's: an abbreviation of a draw with a word for the data's units, and words that name data too
    "n_sim_days", "n_sims_obs", "n_boot_firms", "n_mc_firms", "n_fits_obs", "n_ensemble_members_obs",
    "n_trials_in_sample", "n_trials_subjects", "n_starts", "housing_starts",
])
def test_a_sample_size_stays_a_count(name):
    claims, moved = guards.as_parameters([claim(name, "54")])
    assert claims[0].kind == "count" and moved == []


def test_a_parameter_is_reported_but_never_judged():
    claims = [claim("n_paths", "10,000", kind="parameter"), claim("beta", "0.42", kind="estimate")]
    results = [{"name": "n_paths", "value": 300, "se": 0, "n": 300}, {"name": "beta", "value": 0.41, "se": 0.05, "n": 300}]

    rows = {r["name"]: r for r in compare.compare(claims, results)}
    outcome, _ = compare.verdict(list(rows.values()), results)

    assert rows["n_paths"]["consistent"] is None and "parameter" in rows["n_paths"]["why"]
    assert rows["n_paths"]["reproduced"] == 300
    assert outcome == "holds up"                    # 300 paths against 10,000 doesn't block the verdict


def test_a_parameter_is_never_a_sample_total():
    claims = [claim("n_obs", "3,318"), claim("n_paths", "10,000", kind="parameter")]
    assert [c.name for c in guards.sample_totals(claims, set())] == ["n_obs"]


def test_code_may_write_the_papers_parameters():
    """2609.02673: n_mc_replications 10,000 rejected twice; 2512.20460: the equal weight 6.25 rejected."""
    script = "N_MC = 10000\nW = 6.25\nsims = run(N_MC)\nadd('mc_mean', sims.mean() * W, 0, N_MC)\nadd('n_mc', N_MC, 0, N_MC)\n"
    claims = [claim("n_mc", "10,000", kind="parameter"), claim("efc_weight", "6.25", kind="parameter"),
              claim("mc_mean", "0.31", kind="estimate")]
    assert guards.hardcoded_results(script, claims) == []
    assert guards.hardcoded_counts(script, guards.sample_totals(claims, set()), claims) == []


def test_a_result_computed_from_a_parameter_may_equal_it():
    """2605.29413: the weight cap 0.15 binds for WMT, so WMT's weight is 0.15: code writing the cap is allowed."""
    cap, wmt = claim("weight_cap", "0.15", kind="parameter"), claim("weight_wmt", "0.15", kind="estimate")
    script = "CAP = 0.15\nw = np.minimum(raw, CAP)\nadd('weight_wmt', w['WMT'], 0, 1)\n"

    assert guards.hardcoded_results(script, [cap, wmt]) == []


@pytest.mark.parametrize("script", ["add('sharpe', 0.15, 0, 1)\n", "S = 0.15\nadd('sharpe', S, 0, 1)\n"])
def test_a_result_written_as_a_parameters_number_is_still_caught(script):
    """The reviewer's case: a Sharpe of 0.15 written as 0.15 is the paper's number, whatever the cap is."""
    cap, sharpe = claim("weight_cap", "0.15", kind="parameter"), claim("sharpe", "0.15", kind="estimate")

    assert [f.split(" ")[0] for f in guards.hardcoded_results(script, [cap, sharpe])] == ["sharpe"]


def test_a_parameter_written_with_no_observations_is_not_an_empty_sample():
    claims = [claim("n_paths", "10,000", kind="parameter"), claim("beta", "0.42", kind="estimate")]
    results = [{"name": "n_paths", "value": 10000, "se": 0, "n": 0}, {"name": "beta", "value": 0.41, "se": 0.05, "n": 300}]

    assert compare.verdict(compare.compare(claims, results), results)[0] == "holds up"


def test_a_parameter_never_sends_the_sample_back_or_becomes_a_count_to_watch(monkeypatch):
    """Held-out 1247d1 and 5b3635 (29 Oct): round 2 ran 300 paths and 500 surrogates, the audit sent the sample back
    and watched the paper's 10,000, and round 3's 10,000 was then rejected as a count planted after feedback."""
    claims = [claim("generated_paths_per_asset", "10,000", kind="parameter"), claim("n_obs", "3,318")]
    ran = [{"name": "generated_paths_per_asset", "value": 300, "se": 0, "n": 300},
           {"name": "n_obs", "value": 3318, "se": 0, "n": 3318}]
    off = [{**ran[0], "value": 300}, {"name": "n_obs", "value": 2900, "se": 0, "n": 2900}]
    monkeypatch.setenv("SEC_USER_AGENT", "test contact@example.com")

    assert replicate.audit_problem(claims, ran, "") == (None, [])
    problem, watch = replicate.audit_problem(claims, off, "")
    assert "n_obs" in problem and "generated_paths" not in problem and watch == ["3318"]


def test_a_parameter_is_never_the_headline():
    spec = PaperSpec.model_validate({**SPEC, "headline": "n_paths",
                                     "claims": [claim("n_paths", "10,000", kind="parameter").model_dump(),
                                                claim("beta", "0.42", kind="estimate").model_dump()]})
    assert any("parameter" in p for p in reference_problems(spec))
