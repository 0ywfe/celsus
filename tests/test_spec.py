from paper_replicator.spec import Claim, PaperSpec, Partition, ReportedTest, reference_problems


def c(name, kind="count"):
    return Claim(name=name, description="", value="1", unit="", kind=kind, where="")


CLAIMS = [c("total"), c("small"), c("large"), c("t", "test_statistic"), c("p", "p_value"), c("mean", "estimate")]


def spec(headline="mean", partitions=(), tests=(), claims=CLAIMS):
    return PaperSpec(title="", hypothesis="", data_sources=[], sample="", method=[], claims=list(claims),
                     headline=headline, partitions=list(partitions), tests=list(tests))


def test_a_spec_whose_references_name_claims_has_no_problems():
    good = spec(partitions=[Partition(split="size", total="total", parts=["small", "large"])],
                tests=[ReportedTest(test="size", statistic="t", p_value="p", group_sizes=["small", "large"])])
    assert reference_problems(good) == []


def test_references_written_as_prose_are_problems():
    # run 4c4a02 (Wonder, max effort) wrote values and prose where claim names belong
    bad = spec(headline="Across all 54 incidents, the average return was -3.07%",
               partitions=[Partition(split="size", total="54 (24 + 29 as printed)", parts=["small", "Larger (n=29)"])],
               tests=[ReportedTest(test="H1", statistic="-2.41", p_value="p", group_sizes=["All incidents: 54"])])
    problems = reference_problems(bad)
    assert len(problems) == 5
    assert any(p.startswith("headline") for p in problems)
    assert any("'54 (24 + 29 as printed)'" in p for p in problems)
    assert any("'Larger (n=29)'" in p for p in problems)
    assert any("'-2.41'" in p for p in problems)
    assert any("'All incidents: 54'" in p for p in problems)


def test_duplicate_claim_names_are_a_problem():
    assert reference_problems(spec(claims=CLAIMS + [c("total")])) == ["two claims share the name 'total'"]


def test_a_group_size_the_paper_does_not_state_is_allowed():
    # run 5d7c16: the paper prints the beta test's t and p but not its group sizes
    ok = spec(tests=[ReportedTest(test="beta", statistic="t", p_value="p", group_sizes=["not stated"])])
    assert reference_problems(ok) == []
