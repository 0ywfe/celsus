from paper_replicator.compare import compare, verdict
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


def test_verdict_counts_only_judged_rows():
    assert verdict([{"consistent": True}, {"consistent": None}]) == "reproduced"
    assert verdict([{"consistent": True}, {"consistent": False}]) == "partly reproduced"
    assert verdict([{"consistent": False}]) == "not reproduced"
    assert verdict([{"consistent": None}]) == "no verdict"


def test_significance_uses_the_side_the_paper_tested():
    # run-20261028T144225Z-91ed39: t = -1.905 is significant one-sided (p 0.031) but not two-sided
    claims = [claim("t", "-2.41", "test_statistic")]
    results = [{"name": "t", "value": -1.905}]
    assert compare(claims, results)[0]["consistent"] is False
    assert compare(claims, results, sides={"t": "one-sided (lower tail)"})[0]["consistent"] is True
