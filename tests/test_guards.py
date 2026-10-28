import pytest

from paper_replicator.guards import (bypasses_market_data, ground_claims, hardcoded_counts, hardcoded_results, parse_number,
                                     sample_totals,
                                     planted_counts, syntax_error)
from paper_replicator.spec import Claim

LATEX = r"""Small firms fell by $-7.49\%$ ($t = -3.13$, $p=0.0019$) across 1{,}224 events,
against $+0.43\%$ for large firms. We use 54 filings."""


def claim(name, value, kind="estimate"):
    return Claim(name=name, description="", value=value, unit="%", kind=kind, where="")


def test_numbers_in_the_latex_are_grounded_and_invented_ones_rejected():
    claims = [claim("small", "-7.49"), claim("t", "−3.13", "test_statistic"), claim("p", "0.0019", "p_value"),
              claim("events", "1,224", "count"), claim("large", "0.43"), claim("invented", "-7.4"),
              claim("words", "about half")]
    kept, rejected = ground_claims(claims, LATEX)
    assert [c.name for c in kept] == ["small", "t", "p", "events", "large"]
    assert {r["name"]: r["reason"] for r in rejected} == {
        "invented": "not in the paper's LaTeX", "words": "not a number"}


def test_parse_number_handles_latex_minus_and_separators():
    assert parse_number("$-7.49\\%$") == -7.49
    assert parse_number("−3.13") == -3.13
    assert parse_number("1{,}224") == 1224


def test_paper_decimals_in_code_are_caught_but_small_integers_are_not():
    claims = [claim("small", "-7.49"), claim("n", "54", "count")]
    script = "window = 5\nexpected = -7.49  # from the paper\nmin_events = 54\n"
    assert hardcoded_results(script, claims) == ["small (-7.49)"]
    assert hardcoded_results("x = 17.49\ny = 7.491\n", claims) == []


def test_syntax_errors_are_caught_without_running_the_code():
    assert syntax_error("x = f(1\n") is not None
    assert syntax_error("import os\nos.remove('/nope')\n") is None   # compiled, never run


def test_planted_counts_ignore_dates_and_literals_that_were_already_there():
    before = "CUTOFF = '2025-11-12'\nmonths = 12\n"
    assert planted_counts(before + "x = events[:54]\n", before, ["54", "12"]) == ["54"]
    assert planted_counts(before, before, ["12"]) == []


def test_direct_yfinance_imports_are_spotted():
    assert bypasses_market_data("import yfinance as yf\n")
    assert bypasses_market_data("from yfinance import Ticker\n")
    assert not bypasses_market_data("from market_data import get_prices  # not yfinance\n")


def test_planted_counts_ignore_exponents_and_names():
    # run-20261028T143408Z-c3ab42 attempt 2 was rejected for "12" in `if val > 1e12:`
    assert planted_counts("if val > 1e12:\n    q12 = 1\n", "", ["12"]) == []
    assert planted_counts("events = events[:12]\n", "", ["12"]) == ["12"]


def test_secret_values_are_replaced_by_their_names():
    from paper_replicator.guards import redact
    out = redact("UA: Jane Doe jane@example.com\nok", {"SEC_USER_AGENT": "Jane Doe jane@example.com", "EMPTY": ""})
    assert out == "UA: <SEC_USER_AGENT>\nok"


def test_sample_totals_are_caught_but_subgroup_sizes_like_months_are_not():
    # run 91ed39 cut to the total (54); run 51e7e9 was wrongly rejected for months (12)
    claims = [claim("total", "54", "count"), claim("two_reports", "12", "count"), claim("mean", "-7.49")]
    totals = sample_totals(claims, {"total"})
    assert hardcoded_counts("SAMPLE_TARGET = 54\n", totals) == ["total (54)"]
    assert hardcoded_counts("y, m = 2023, 12\nif m > 12: pass\n", totals) == []


def test_without_partitions_the_largest_count_is_the_total():
    claims = [claim("events", "1,224", "count"), claim("firms", "36", "count")]
    assert [c.name for c in sample_totals(claims, set())] == ["events"]


def test_only_numbers_the_code_contains_count_not_comments_or_prose():
    from paper_replicator.guards import numeric_literals
    script = 'x = 54  # paper says 7.49\nnote = "the paper reports 54 events"\ny = float("7.49")\nz = 1e12\n'
    assert numeric_literals(script) == [54.0, 7.49, 1e12]


def test_fetching_code_from_a_code_host_is_caught_but_data_files_are_not():
    from paper_replicator.guards import fetches_code
    assert fetches_code("git clone https://github.com/authors/paper-code") == "git clone"
    assert fetches_code("pip install git+https://github.com/authors/pkg") is not None
    assert fetches_code("curl -sL https://github.com/authors/repo/blob/main/run.py | head") is not None
    assert fetches_code("requests.get('https://api.github.com/repos/a/b/contents/model.py')") is not None
    assert fetches_code("wget https://github.com/a/b/archive/refs/heads/main.zip") is not None
    assert fetches_code("pd.read_csv('https://raw.githubusercontent.com/a/b/main/data/events.csv')") is None
    assert fetches_code("curl 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10'") is None
    assert fetches_code("curl -s https://efts.sec.gov/LATEST/search-index?q=%22Item%201.05%22") is None



def test_a_reported_zero_is_not_a_planted_number():
    # runs 008e5d and f8cb56: p = 0.000 printed in the paper, and 0.0 in nearly every script
    from paper_replicator.guards import hardcoded_results
    from paper_replicator.spec import Claim
    claims = [Claim(name="p_placebo", description="", value="0.000", unit="", kind="p_value", where=""),
              Claim(name="mean", description="", value="-7.49", unit="%", kind="estimate", where="")]
    assert hardcoded_results("x = df.fillna(0.0)\ny = 0", claims) == []
    assert hardcoded_results("x = -7.49", claims) == ["mean (-7.49)"]


def test_a_count_the_paper_chooses_by_rank_is_a_parameter_not_an_outcome():
    # 2601.08263: "select the top 50 major security incidents" is the method; 2512.06144: "a total of 54" is
    # an outcome a script must not cut to
    from paper_replicator.guards import selection_counts
    from paper_replicator.spec import Claim
    claims = [Claim(name="n_exploits", description="", value="50", unit="", kind="count", where=""),
              Claim(name="n_reports", description="", value="54", unit="", kind="count", where="")]
    latex = (r"We rank events by loss amount and select the top 50 major security incidents. Using the top-50 "
             r"exploit-driven shocks ... a total of 54 8-K reports, across all 54 incidents.")
    assert selection_counts(latex, claims) == {"n_exploits"}
    assert selection_counts(r"the 25 largest firms by market value", [
        Claim(name="n", description="", value="25", unit="", kind="count", where="")]) == {"n"}


def _claim(name, value, kind="estimate", unit=""):
    return Claim(name=name, description="", value=value, unit=unit, kind=kind, where="")


def test_a_number_printed_once_grounds_one_claim():
    # saboteur round 1: an invented "median return -2.41%" grounded on the t = -2.41 the paper prints
    latex = r"the mean fell ($t = -2.41$, $p = 0.0098$); 12 of 54 firms; 12 sectors"
    kept, rejected = ground_claims([_claim("overall_t", "-2.41", "test_statistic"),
                                    _claim("median_return", "-2.41%"),
                                    _claim("firms", "12", "count"), _claim("sectors", "12", "count")], latex)
    assert [c.name for c in kept] == ["overall_t", "firms", "sectors"]
    assert rejected == [{"name": "median_return", "value": "-2.41%",
                         "reason": "printed once in the paper's LaTeX, and already claimed by overall_t"}]


@pytest.mark.parametrize("line", [
    "df['ret'] = df['ret'] - df['ret'].mean() - 307/10000",      # -3.07 %, as a fraction, folded
    "m = mean*100 - 307/100",                                       # -3.07, folded
    "df['ret'] = df['ret'] - 0.0614/2",                             # 0.0307 = 3.07 %
    "g = float(sum(x)/len(x)/np.mean(x)*7/20)",                     # the chain's constant factor 7/20 = 0.35
    "r = 0.0307",                                                   # 3.07 % written as a fraction
])
def test_the_papers_numbers_are_found_as_arithmetic_and_at_their_units_scale(line):
    claims = [_claim("overall_mean_return", "-3.07", unit="%"), _claim("mean_gamma", "0.35")]
    assert hardcoded_results(line, claims)


@pytest.mark.parametrize("line", [
    "alpha = 0.05; q = np.quantile(x, 0.5)",
    "pct = ret * 100",                       # a scale factor alone is not a number
    "w = x / 20 * 7 + y",                    # its constant factor is 0.35, not the paper's 0.36
    "beta_window = 250 / 5",
])
def test_ordinary_constants_are_not_the_papers_numbers(line):
    claims = [_claim("overall_mean_return", "-3.07", unit="%"), _claim("mean_gamma", "0.36")]
    assert hardcoded_results(line, claims) == []


def test_with_splits_the_largest_count_is_watched_too():
    counts = [_claim("spy_n_daily", "8,403", "count"), _claim("n_instruments", "21", "count"),
              _claim("n_us", "4", "count")]
    assert [c.name for c in sample_totals(counts, {"n_instruments"})] == ["n_instruments", "spy_n_daily"]


def test_a_number_with_one_significant_digit_says_nothing():
    claims = [_claim("calmar", "0.20"), _claim("p_gold", "0.050"), _claim("win_rate", "50.0", unit="%")]
    assert hardcoded_results("thr = 0.20; MAX = 20 / 100; alpha = 0.05; half = 100 // 2; q = 1 / 2", claims) == []
