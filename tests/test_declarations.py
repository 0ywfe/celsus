"""The builder's sample declaration: how its sample differs from the paper's (counts, or why it can't count them) is
kept apart from the other sources and methods it used for the same observations, which are caveats; a declaration
that says neither is asked for again (held-out set 2, 29 Oct: 6706f3, 4572d2, 05698b, 29dfe5)."""

import pytest

from paper_replicator import replicate
from paper_replicator.spec import PaperSpec, Partition

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
    """6706f3: same_as_paper false, missing and extra blank, counts the audit accepts."""
    sample = {"same_as_paper": False, "missing": None, "extra": None, "differences": ""}

    problem, watch = replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS])

    assert checks(sample) == ["declaration blank"]
    assert "does not say how its sample differs" in problem and "cannot_count" in problem and watch == []
    assert "match the paper's within SCORE's +/-15%" in problem


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

    assert "counts match the paper's within SCORE's +/-15%" in problem and "does not say" not in problem


@pytest.mark.parametrize("totals", [(EVENTS, POOL, OBS), (EVENTS,)])
def test_a_declaration_asked_for_again_alongside_another_issue_gets_the_sample_feedback(totals):
    sample = {"same_as_paper": False, "missing": None, "extra": None}
    results = [r for r in RESULTS if r["name"] != "n_events"] if len(totals) == 1 else RESULTS

    problem, _ = replicate.audit_problem(SPEC.claims, results, "", SPEC, sample, list(totals))

    assert "its sample does not match the paper's" in problem and "not_rebuilt" in problem


def test_the_audit_judges_counts_by_the_same_totals_as_the_report():
    """The reviewer's case: the audit took its totals from the watched list, which leaves out a count the paper
    chooses by rank, so the paper's largest count was a subgroup to the audit (the sqrt band) and a total in the
    report (SCORE's 15%): the builder was sent back over a count the report calls consistent."""
    spec = SPEC.model_copy(update={"partitions": [Partition(split="s", total="n_events", parts=[])]})
    results = [*RESULTS[:2], {"name": "n_obs", "value": 12_500, "se": 0, "n": 12_500}]   # -13%: outside sqrt's 235
    sample = {"same_as_paper": True, "missing": 0, "extra": 0}

    problem, watch = replicate.audit_problem(spec.claims, results, "", spec, sample, [EVENTS])

    assert replicate.judged_totals(spec.claims, spec) == {"n_events", "n_obs"}
    assert problem is None and watch == []


@pytest.mark.parametrize("sample, small", [
    ({"missing": 1, "extra": 0, "n": 53}, True),        # the breach paper's 53 of 54 filings
    ({"missing": 15, "extra": 0, "n": 85}, True),       # 15% of 100: the boundary is in
    ({"missing": 10, "extra": 10, "n": 100}, False),    # the net count matches, but 20% of the observations differ
    ({"missing": 0, "extra": 5, "n": 5}, False),        # the paper's n would be 0
    ({"missing": None, "extra": 0, "n": 53}, False),    # an amount the builder cannot give is not small
    ({"missing": 1.5, "extra": 0, "n": 53}, False),
])
def test_a_small_declared_difference_is_judged_and_a_large_one_is_not(sample, small):
    assert (replicate.small_difference(sample) is not None) is small


def test_a_small_declared_difference_says_how_it_was_measured():
    assert replicate.small_difference({"missing": 1, "extra": 0, "n": 53}) == (
        "the sample differs from the paper's by 1 missing and 0 extra observations (1.9% of the paper's 54, missing "
        "and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged")



# (h): a not_rebuilt declaration must name the paper's claims and leave them out of the results. a27323 keyed it
# "n_candidate_pool_detail" (no claim's name) and reported a proxy for n_candidate_pool_total anyway, so nothing was
# excused and the proxy was compared. Both are asked about again; left as they are, the counts are compared as before.

def test_a_not_rebuilt_name_that_is_no_claim_is_asked_about_again():
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_pool_detail": "the paper's candidate list is not published"}}

    problem, watch = replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS, POOL, OBS])

    assert "not_rebuilt names n_pool_detail, which is no claim's name" in problem and watch == []
    assert replicate.sample_issues(SPEC, sample, RESULTS, [EVENTS, POOL, OBS]) == [
        "the replication did not report the paper's sample size (n_pool), so its sample cannot be compared"]


def test_a_count_listed_as_not_rebuilt_and_reported_anyway_is_asked_about_and_still_compared():
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_pool": "the paper's candidate list is not published"}}
    proxy = [*RESULTS, {"name": "n_pool", "value": 245, "se": 0, "n": 245}]

    problem, watch = replicate.audit_problem(SPEC.claims, proxy, "", SPEC, sample, [EVENTS, POOL, OBS])

    assert "n_pool is in not_rebuilt but its value is reported" in problem and "substitutions" in problem
    assert "n_pool: the paper reports 135, your run produced 245" in problem and watch == ["135"]


def test_a_declaration_mismatch_alone_costs_no_round_and_is_a_caveat():
    """With nothing off and nothing missing there is nothing for a declaration to excuse, so asking again would
    spend one of the builder's rounds (2-30 min, $0.19-0.80 on the v2 runs) for no change: it is noted instead."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_pool": "unpublished", "n_pool_detail": "unpublished"}}
    proxy = [*RESULTS, {"name": "n_pool", "value": 135, "se": 0, "n": 135}]

    assert replicate.audit_problem(SPEC.claims, proxy, "", SPEC, sample, [EVENTS, POOL, OBS]) == (None, [])
    assert replicate.sample_caveats(sample, proxy, [EVENTS, POOL, OBS], SPEC.claims) == [
        "the sample block's not_rebuilt: n_pool_detail is no claim's name, so it excused nothing",
        "the sample block's not_rebuilt: n_pool is in it but its value was reported anyway, so it was not treated "
        "as excused"]


def test_the_largest_total_declared_and_reported_anyway_is_named_as_reported():
    """(j): the largest total may be declared, so a declared one that is also reported is the plain "reported anyway"
    slip, and the off count is sent back as any off count is."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0, "not_rebuilt": {"n_obs": "partly unpublished"}}
    off = [*RESULTS[:2], {"name": "n_obs", "value": 9000, "se": 0, "n": 9000}]

    problem, _ = replicate.audit_problem(SPEC.claims, off, "", SPEC, sample, [EVENTS, POOL, OBS])

    assert "n_obs is in not_rebuilt but its value is reported" in problem
    assert "n_obs: the paper reports 14361, your run produced 9000" in problem
    assert "cannot be declared" not in problem


def test_a_declaration_by_the_claims_name_with_the_count_left_out_is_not_asked_about():
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_pool": "the candidate pool needs data the paper does not publish"}}

    assert replicate.audit_problem(SPEC.claims, RESULTS, "", SPEC, sample, [EVENTS, POOL, OBS]) == (None, [])


def test_the_builder_is_told_to_name_the_claim_and_leave_its_count_out():
    from paper_replicator import roles
    assert "exact name" in roles.RESULTS_FORMAT and "out of results" in roles.RESULTS_FORMAT


# (j), the orchestrator's ruling (29 Oct): the paper's largest sample total may be declared not rebuilt, with a reason
# naming what public data lacks. Refused, e589c6's builder declared the paper's 120 LLM forecast paths in round 2 and
# wrote them as the paper's design arithmetic in round 3, which the reviewer stopped.

DECLARED = {"same_as_paper": True, "missing": 0, "extra": 0,
            "not_rebuilt": {"n_obs": "the paper's intraday quotes are not in any public source"}}
WITHOUT_OBS = [{"name": "beta", "value": 0.42, "se": 0.05, "n": 50}, {"name": "n_events", "value": 50, "se": 0, "n": 50}]
POOL_SPEC = PaperSpec.model_validate({**SPEC.model_dump(), "claims": [c.model_dump() for c in SPEC.claims
                                                                      if c.name != "n_pool"]})


def test_the_sample_declared_not_rebuilt_with_a_reason_is_a_caveat_and_caps_the_verdict():
    from paper_replicator import compare
    totals = [EVENTS, OBS]

    assert replicate.audit_problem(POOL_SPEC.claims, WITHOUT_OBS, "", POOL_SPEC, DECLARED, totals) == (None, [])
    assert ("sample size not rebuilt: the paper's intraday quotes are not in any public source (n_obs, 14,361 in "
            "the paper); the results are judged without it, so the paper gets at most \"partly holds up\"") \
        in replicate.sample_caveats(DECLARED, WITHOUT_OBS, totals, POOL_SPEC.claims)
    rows = compare.compare(POOL_SPEC.claims, WITHOUT_OBS, totals={"n_obs"})
    note = replicate.unrebuilt_note(replicate.declared_sample(DECLARED, WITHOUT_OBS, totals))
    assert compare.verdict(rows, WITHOUT_OBS, headline="beta") == ("holds up", "")   # the main result is consistent
    outcome, reason = compare.verdict(rows, WITHOUT_OBS, headline="beta", unrebuilt=note)
    assert outcome == "partly holds up"
    assert compare.first_line(outcome, reason, rows, "beta", unrebuilt=note).endswith(
        " Sample size not rebuilt: the paper's intraday quotes are not in any public source (n_obs, 14,361 in the "
        "paper).")


@pytest.mark.parametrize("why", ["", "   ", ".", " . ", None, True])
def test_the_sample_declared_with_no_reason_is_asked_for_again(why):
    sample = {**DECLARED, "not_rebuilt": {"n_obs": why}}

    problem, _ = replicate.audit_problem(POOL_SPEC.claims, WITHOUT_OBS, "", POOL_SPEC, sample, [EVENTS, OBS])

    assert "did not report the paper's sample size (n_obs)" in problem
    assert replicate.declared_sample(sample, WITHOUT_OBS, [EVENTS, OBS]) is None


def test_a_declared_sample_excuses_no_smaller_total():
    """A declared largest total matches nothing, so smaller totals left out stay as (c) treats them when the largest
    does not match: missing."""
    sample = {**DECLARED, "not_rebuilt": {**DECLARED["not_rebuilt"], "n_pool": "the pool needs unpublished data"}}

    assert replicate.excused_totals(sample, WITHOUT_OBS, [EVENTS, POOL, OBS]) == {}
    issues = replicate.sample_issues(SPEC, sample, WITHOUT_OBS, [EVENTS, POOL, OBS])
    assert issues == ["the replication did not report the paper's sample size (n_pool), so its sample cannot be "
                      "compared"]


def test_e589c6s_round_two_declaration_is_judged_not_sent_back():
    """e589c6 (2604.14467), round 2: the 120 LLM forecast paths declared (reason paraphrased), the CPI results
    reported, the 96 forecast origins exact. Under the old rule the audit sent it back to report the 120; the next
    round wrote it as 3*4*5*2."""
    from paper_replicator import compare
    spec = PaperSpec.model_validate({
        "title": "t", "hypothesis": "h", "data_sources": [], "sample": "", "method": [], "headline": "ic_avg_2021",
        "claims": [{"name": "ic_avg_2021", "description": "", "value": "6.83", "unit": "", "kind": "estimate",
                    "where": ""},
                   {"name": "arma_alpha_sim", "description": "", "value": "0.83", "unit": "", "kind": "estimate",
                    "where": ""},
                   {"name": "arma_phi_1", "description": "", "value": "0.52", "unit": "", "kind": "estimate",
                    "where": ""},
                   {"name": "n_llm_runs", "description": "", "value": "120", "unit": "", "kind": "count", "where": ""},
                   {"name": "n_robust_origins", "description": "", "value": "96", "unit": "", "kind": "count",
                    "where": ""}],
        "partitions": [], "tests": []})
    results = [{"name": "ic_avg_2021", "value": 6.0, "se": 0}, {"name": "arma_alpha_sim", "value": 0.74, "se": 0},
               {"name": "arma_phi_1", "value": 0.521, "se": 0.02}, {"name": "n_robust_origins", "value": 96, "se": 0, "n": 96}]
    sample = {"same_as_paper": True, "missing": 0, "extra": 0,
              "not_rebuilt": {"n_llm_runs": "120 LLM forecast paths need proprietary model runs with persona "
                                            "prompts; public data cannot reproduce them"}}
    totals = [c for c in spec.claims if c.kind == "count"]

    assert replicate.audit_problem(spec.claims, results, "", spec, sample, totals) == (None, [])
    rows = compare.compare(spec.claims, results, totals=replicate.judged_totals(spec.claims, spec))
    note = replicate.unrebuilt_note(replicate.declared_sample(sample, results, totals))
    outcome, reason = compare.verdict(rows, results, headline="ic_avg_2021", unrebuilt=note)
    assert outcome == "partly holds up"
    assert "Sample size not rebuilt: 120 LLM forecast paths need proprietary model runs" in compare.first_line(
        outcome, reason, rows, "ic_avg_2021", unrebuilt=note)


def test_the_builder_is_told_the_sample_itself_may_be_declared_never_faked():
    from paper_replicator import roles
    assert "If public data cannot give" in roles.RESULTS_FORMAT
    assert "Never write the paper's count instead" in roles.RESULTS_FORMAT


def test_a_reason_that_is_only_a_full_stop_excuses_no_smaller_total():
    """Code review: "." stripped to "" and still excused n_pool, with an empty reason."""
    sample = {"same_as_paper": True, "missing": 0, "extra": 0, "not_rebuilt": {"n_pool": "."}}
    assert replicate.excused_totals(sample, RESULTS, [EVENTS, POOL, OBS]) == {}


TWIN = SPEC.claims[3].model_copy(update={"name": "n_obs_total"})


@pytest.mark.parametrize("reported, declared", [("n_obs", "n_obs_total"), ("n_obs_total", "n_obs")])
def test_tied_largest_totals_are_one_sample_size_whichever_is_reported(reported, declared):
    """Code review: the two tied names were treated differently by claim order. Either copy reported and matching,
    the sample was reported: nothing is declared, the other copy is excused, and the verdict is not capped."""
    results = [*RESULTS[:2], {"name": reported, "value": 14367, "se": 0, "n": 14367}]
    sample = {"same_as_paper": True, "missing": 0, "extra": 0, "not_rebuilt": {declared: "a second count of it"}}
    totals = [EVENTS, OBS, TWIN]

    assert replicate.declared_sample(sample, results, totals) is None
    assert replicate.excused_totals(sample, results, totals) == {declared: "a second count of it"}
    assert replicate.sample_issues(SPEC, sample, results, totals) == []


@pytest.mark.parametrize("outcome, says", [("partly holds up", True), ("does not hold up", True),
                                           ("could not check", False)])
def test_the_first_line_names_the_declared_sample_unless_the_paper_could_not_be_checked(outcome, says):
    """A could-not-check line already says nothing about the paper's numbers; the declaration is in its caveats."""
    from paper_replicator import compare
    rows = compare.compare(POOL_SPEC.claims, WITHOUT_OBS, totals={"n_obs"})
    line = compare.first_line(outcome, "a reason", rows, "beta", unrebuilt="no public source (n_obs, 14,361 in the paper)")
    assert ("Sample size not rebuilt: no public source (n_obs, 14,361 in the paper)." in line) is says


def test_the_reviewer_checks_a_declared_sample_against_the_code():
    """(j), the orchestrator's ruling: a declaration the code contradicts is the reviewer's to report, not a coded
    guard's (units are free text; a guard that wrongly refuses would bring back the pressure to fake)."""
    from paper_replicator import roles
    assert ("If the paper's largest sample size is declared not rebuilt, read the code: if the code builds that "
            "sample, the\n   declaration is false. Report it as a finding.") in roles.REVIEWER
