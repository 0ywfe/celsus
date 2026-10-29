"""The builder's sample declaration: how its sample differs from the paper's (counts, or why it can't count them) is
kept apart from the other sources and methods it used for the same observations, which are caveats; a declaration
that says neither is asked for again (held-out set 2, 29 Oct: 6706f3, 4572d2, 05698b, 29dfe5)."""

import pytest

from paper_replicator import replicate
from paper_replicator.spec import PaperSpec

SPEC = PaperSpec.model_validate({
    "title": "t", "hypothesis": "h", "data_sources": [], "sample": "", "method": [], "headline": "beta",
    "claims": [{"name": "beta", "description": "", "value": "0.42", "unit": "", "kind": "estimate", "where": ""},
               {"name": "n_events", "description": "", "value": "50", "unit": "", "kind": "count", "where": ""},
               {"name": "n_pool", "description": "", "value": "135", "unit": "", "kind": "count", "where": ""},
               {"name": "n_obs", "description": "", "value": "14,361", "unit": "", "kind": "count", "where": ""}],
    "partitions": [], "tests": []})
EVENTS, POOL, OBS = SPEC.claims[1], SPEC.claims[2], SPEC.claims[3]
RESULTS = [{"name": "beta", "value": 0.41, "se": 0.05, "n": 50}, {"name": "n_events", "value": 50, "se": 0, "n": 50},
           {"name": "n_obs", "value": 14367, "se": 0, "n": 14367}]


@pytest.fixture(autouse=True)
def contact(monkeypatch):
    monkeypatch.setenv("SEC_USER_AGENT", "test contact@example.com")


def checks(sample: dict, results=RESULTS, totals=(EVENTS,)) -> list[str]:
    return [check for check, _ in replicate.sample_checks(SPEC, sample, results, list(totals))]


def test_a_sample_declared_different_with_no_amount_and_no_reason_is_asked_for_again():
    """6706f3: same_as_paper false, missing and extra blank, counts inside the band."""
    sample = {"same_as_paper": False, "missing": None, "extra": None, "differences": ""}

    problem, watch = replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS])

    assert checks(sample) == ["declaration blank"]
    assert "does not say how its sample differs" in problem and "cannot_count" in problem and watch == []
    assert "match the paper's within the count band" in problem


def test_a_declaration_over_counts_that_match_is_asked_for_again_and_blocks_only_if_it_stands():
    sample = {"same_as_paper": False, "missing": None, "extra": None, "differences": "sector counts differ"}

    problem, _ = replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS])
    issues = replicate.sample_issues(SPEC, sample, RESULTS, [EVENTS])

    assert checks(sample) == ["declaration over matching counts"] and "substitutions" in problem
    assert issues == ["the replication could not rebuild the paper's sample (sector counts differ)"]


@pytest.mark.parametrize("sample, said", [
    ({"same_as_paper": False, "missing": 30, "extra": 0, "differences": "the 2021 snapshot is gone"},
     "30 missing and 0 extra observations: the 2021 snapshot is gone"),
    ({"same_as_paper": False, "missing": None, "extra": None, "cannot_count": "the vendor's archive is closed"},
     "the vendor's archive is closed"),
])
def test_a_sample_declared_different_by_an_amount_or_with_a_reason_blocks_with_it(sample, said):
    off = [RESULTS[0], {"name": "n_events", "value": 20, "se": 0, "n": 20}]
    assert replicate.sample_issues(SPEC, sample, off, [EVENTS]) == [
        f"the replication could not rebuild the paper's sample ({said})"]


def test_declared_counts_never_switch_off_the_count_audit():
    """The 0/0 guard: 40c85a declared the paper's sample, 0 missing and 0 extra, over 17,225 days against 14,361."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0}
    off = [RESULTS[0], {"name": "n_events", "value": 20, "se": 0, "n": 20}]

    problem, watch = replicate.audit_problem(SPEC.claims, off, "", SPEC, sample, [EVENTS])

    assert "n_events: the paper reports 50, your run produced 20" in problem and watch == ["50"]


def test_a_sample_total_public_data_cannot_give_is_a_caveat_when_the_largest_total_matches():
    """4572d2 and 05698b: the paper's tallies of a screening pool no result is computed on, while the 14,361 daily
    observations the results are computed on matched."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_pool": "the candidate pool needs data the paper does not publish"}}

    assert checks(sample, totals=(EVENTS, POOL, OBS)) == []
    assert replicate.sample_caveats(sample, RESULTS, [EVENTS, POOL, OBS]) == [
        "n_pool was not rebuilt: the candidate pool needs data the paper does not publish"]


@pytest.mark.parametrize("results, sample", [
    # the largest total is the one left out, anchored on a smaller count (the reviewer's case)
    (RESULTS[:2], {"not_rebuilt": {"n_obs": "needs unpublished data"}}),
    # the largest total was rebuilt but does not match
    ([*RESULTS[:2], {"name": "n_obs", "value": 9000, "se": 0, "n": 9000}], {"not_rebuilt": {"n_pool": "unpublished"}}),
    # a reason that isn't one
    (RESULTS, {"not_rebuilt": {"n_pool": ""}}),
    (RESULTS, {"not_rebuilt": {"n_pool": True}}),
    (RESULTS, {"not_rebuilt": {"n_pool": {"why": "x"}}}),
    (RESULTS, {"not_rebuilt": ["n_pool"]}),
    (RESULTS, {}),
])
def test_a_sample_total_left_out_still_blocks_without_a_reason_or_a_matching_largest_total(results, sample):
    assert "sample size reported" in checks(sample, results, totals=(EVENTS, POOL, OBS))


def test_other_sources_and_methods_for_the_same_observations_are_caveats_not_differences():
    """29dfe5 declared the current FRED vintage and a monthly WTI spot as sample differences."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "substitutions": "the current FRED vintage, not the January 2021 real-time one"}

    assert checks(sample) == []
    assert replicate.sample_caveats(sample, RESULTS, [EVENTS]) == [
        ("the replication used other sources or methods for the paper's observations: the current FRED vintage, "
         "not the January 2021 real-time one")]


def test_a_declaration_asked_for_again_alongside_a_count_gap_gets_the_sample_feedback():
    sample = {"same_as_paper": False, "missing": None, "extra": None}
    off = [RESULTS[0], {"name": "n_events", "value": 20, "se": 0, "n": 20}]

    problem, watch = replicate.audit_problem(SPEC.claims, off, "", SPEC, sample, [EVENTS])

    assert "its sample does not match the paper's" in problem and watch == ["50"]


def test_a_sample_block_without_the_new_fields_has_no_caveats():
    assert replicate.sample_caveats({}, RESULTS, [EVENTS, POOL, OBS]) == []


def test_a_stated_reason_over_matching_counts_is_asked_about_as_a_contradiction_not_a_blank():
    sample = {"same_as_paper": False, "missing": None, "extra": None, "cannot_count": "the vendor's archive is closed"}

    problem, _ = replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS])

    assert "counts match the paper's within the count band" in problem and "does not say" not in problem


@pytest.mark.parametrize("totals", [(EVENTS, POOL, OBS), (EVENTS,)])
def test_a_declaration_asked_for_again_alongside_another_issue_gets_the_sample_feedback(totals):
    sample = {"same_as_paper": False, "missing": None, "extra": None}
    results = [r for r in RESULTS if r["name"] != "n_events"] if len(totals) == 1 else RESULTS

    problem, _ = replicate.audit_problem(SPEC.claims, results, "", SPEC, sample, list(totals))

    assert "its sample does not match the paper's" in problem and "not_rebuilt" in problem
