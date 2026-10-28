from paper_replicator.paper_checks import check_paper
from paper_replicator.spec import Claim, PaperSpec, Partition, TestPair


def c(name, value, kind="count"):
    return Claim(name=name, description="", value=value, unit="", kind=kind, where="")


CLAIMS = [c("total", "54"), c("small", "24"), c("large", "29"), c("tech", "13"), c("other", "41"),
          c("t_all", "-2.41", "test_statistic"), c("p_all", "0.0098", "p_value"),
          c("t_two", "-2.41", "test_statistic"), c("p_two", "0.0195", "p_value")]


def spec(partitions=(), tests=()):
    return PaperSpec(title="", hypothesis="", data_sources=[], sample="", method=[], claims=CLAIMS,
                     partitions=list(partitions), tests=list(tests))


def test_subgroups_that_do_not_add_up_are_flagged():
    checks = check_paper(spec([Partition(split="size", total="total", parts=["small", "large"]),
                               Partition(split="sector", total="total", parts=["tech", "other"])]), CLAIMS)
    assert [(x["ok"], x["text"]) for x in checks] == [
        (False, "size: 24 + 29 = 53, paper's total 54"), (True, "sector: 13 + 41 = 54, paper's total 54")]


def test_a_one_sided_p_value_is_recognised_from_t_and_n():
    one = TestPair(test="mean below zero", statistic="t_all", p_value="p_all", group_sizes=["total"])
    two = TestPair(test="mean differs from zero", statistic="t_two", p_value="p_two", group_sizes=["total"])
    first, second = check_paper(spec(tests=[one, two]), CLAIMS)
    assert first["side"] == "one-sided (lower tail)" and not first["ok"]
    assert second["side"] == "two-sided" and second["ok"]


def test_references_to_unknown_claims_are_skipped():
    assert check_paper(spec([Partition(split="x", total="nope", parts=["small"])]), CLAIMS) == []
