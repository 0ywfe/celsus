from paper_replicator.paper_checks import check_paper
from paper_replicator.spec import Claim, PaperSpec, Partition, ReportedTest


def c(name, value, kind="count"):
    return Claim(name=name, description="", value=value, unit="", kind=kind, where="")


CLAIMS = [c("total", "54"), c("small", "24"), c("large", "29"), c("tech", "13"), c("other", "41"),
          c("t_all", "-2.41", "test_statistic"), c("p_all", "0.0098", "p_value"),
          c("t_two", "-2.41", "test_statistic"), c("p_two", "0.0195", "p_value")]


def spec(partitions=(), tests=()):
    return PaperSpec(title="", hypothesis="", data_sources=[], sample="", method=[], claims=CLAIMS, headline="",
                     partitions=list(partitions), tests=list(tests))


def test_subgroups_that_do_not_add_up_are_flagged():
    checks = check_paper(spec([Partition(split="size", total="total", parts=["small", "large"]),
                               Partition(split="sector", total="total", parts=["tech", "other"])]), CLAIMS)
    assert [(x["status"], x["text"]) for x in checks] == [
        ("flag", "size: 24 + 29 = 53, paper's total 54"), ("ok", "sector: 13 + 41 = 54, paper's total 54")]


def test_a_one_sided_p_value_is_recognised_from_t_and_n():
    one = ReportedTest(test="mean below zero", statistic="t_all", p_value="p_all", group_sizes=["total"])
    two = ReportedTest(test="mean differs from zero", statistic="t_two", p_value="p_two", group_sizes=["total"])
    first, second = check_paper(spec(tests=[one, two]), CLAIMS)
    assert first["side"] == "one-sided (lower tail)" and first["status"] == "note"
    assert second["side"] == "two-sided" and second["status"] == "ok"


def test_references_to_unknown_claims_are_skipped():
    assert check_paper(spec([Partition(split="x", total="nope", parts=["small"])]), CLAIMS) == []


def test_a_side_is_accepted_only_within_the_printed_precision():
    # run 008e5d (2601.08263): t = -3.41 printed with p = 0.019 fits no side (two-sided would be 0.0007),
    # and an F statistic of 0.53 with p = 0.714 is not a t at all. Neither may set a side for the desk.
    claims = [c("n50", "50"), c("t_lp", "-3.41", "test_statistic"), c("p_lp", "0.019", "p_value"),
              c("f", "0.53", "test_statistic"), c("p_f", "0.714", "p_value"),
              c("t_cl", "-2.339", "test_statistic"), c("p_cl", "0.019", "p_value")]
    tests = [ReportedTest(test="lp", statistic="t_lp", p_value="p_lp", group_sizes=["n50"]),
             ReportedTest(test="joint F", statistic="f", p_value="p_f", group_sizes=["n50"]),
             ReportedTest(test="clustered", statistic="t_cl", p_value="p_cl", group_sizes=["n50"])]
    lp, f, clustered = check_paper(PaperSpec(title="", hypothesis="", data_sources=[], sample="", method=[],
                                             claims=claims, headline="", partitions=[], tests=tests), claims)
    assert lp["side"] is None and lp["status"] == "note" and "no side" in lp["text"]
    assert f["side"] is None
    # clustered errors: the normal gives 0.0193, which prints as 0.019
    assert clustered["side"] == "two-sided" and clustered["status"] == "ok"
