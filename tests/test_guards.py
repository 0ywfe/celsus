from paper_replicator.guards import (bypasses_market_data, ground_claims, hardcoded_results, parse_number,
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
