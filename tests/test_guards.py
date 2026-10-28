import pytest

from paper_replicator.guards import (bypasses_market_data, sets_contact, fixed_results, ground_claims, hardcoded_counts, hardcoded_results,
                                     numbers_in,
                                     parse_number,
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


def test_the_papers_number_counts_where_its_result_is_written_not_elsewhere():
    claims = [claim("small", "-7.49"), claim("n", "54", "count")]
    written = "est = df.ret.mean() * 0 - 7.49\nresults.append({'name': 'small', 'value': est})\n"
    assert hardcoded_results(written, claims) == ["small (-7.49) at line 2"]
    elsewhere = "expected = -7.49  # from the paper\nresults.append({'name': 'small', 'value': df.ret.mean()})\n"
    assert hardcoded_results(elsewhere, claims) == []
    assert hardcoded_results("x = 17.49\nadd('small', x * df.w.mean())\n", claims) == []


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
    assert hardcoded_counts("SAMPLE_TARGET = 54\nkept = filings[:SAMPLE_TARGET]\n", totals, claims) == ["total (54) at line 2"]
    assert hardcoded_counts("y, m = 2023, 12\nif m > 12: pass\n", totals, claims) == []


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
    assert hardcoded_results("x = df.fillna(0.0)\nadd('p_placebo', 0 * x.mean())", claims) == []
    assert hardcoded_results("add('mean', -7.49)", claims) == ["mean (-7.49) at line 1"]


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


@pytest.mark.parametrize("script", [   # saboteur round 1's disguises, each written into its result
    "df['ret'] = df['ret'] - df['ret'].mean() - 307/10000\nadd('overall_mean_return', df['ret'].mean() * 100)",
    "m = mean*100 - 307/100\nadd('overall_mean_return', m)",
    "df['ret'] = df['ret'] - 0.0614/2\nadd('overall_mean_return', df['ret'].mean() * 100)",
    "g = float(sum(x)/len(x)/np.mean(x)*7/20)\nadd('mean_gamma', g)",
    "r = 0.0307\nadd('overall_mean_return', r * 100)",
])
def test_the_papers_numbers_are_found_as_arithmetic_and_at_their_units_scale(script):
    claims = [_claim("overall_mean_return", "-3.07", unit="%"), _claim("mean_gamma", "0.35")]
    assert hardcoded_results(script, claims)


@pytest.mark.parametrize("line", [
    "alpha = 0.05; q = np.quantile(x, 0.5)",
    "pct = ret * 100",                       # a scale factor alone is not a number
    "w = x / 20 * 7 + y",                    # its constant factor is 0.35, not the paper's 0.36
    "beta_window = 250 / 5",
])
def test_ordinary_constants_are_not_the_papers_numbers(line):
    claims = [_claim("overall_mean_return", "-3.07", unit="%"), _claim("mean_gamma", "0.36")]
    assert hardcoded_results(line + "\nadd('mean_gamma', w)", claims) == []


def test_with_splits_the_largest_count_is_watched_too():
    counts = [_claim("spy_n_daily", "8,403", "count"), _claim("n_instruments", "21", "count"),
              _claim("n_us", "4", "count")]
    assert [c.name for c in sample_totals(counts, {"n_instruments"})] == ["n_instruments", "spy_n_daily"]


def test_a_number_with_one_significant_digit_says_nothing():
    claims = [_claim("calmar", "0.20"), _claim("p_gold", "0.050"), _claim("win_rate", "50.0", unit="%")]
    script = "thr = 0.20; MAX = 20 / 100; alpha = 0.05\nadd('calmar', ret.mean() / dd * thr)\nadd('p_gold', p * alpha)"
    assert hardcoded_results(script, claims) == []


def test_numbers_in_counts_what_a_value_holds_outside_its_asides():
    # the shapes measured in the 4,084 claim values on disk (28 Oct)
    for one in ("-7.49", "1{,}224", "5.2\\times10^{-4}", "2.70x10-14", "1.5e-13", "10^{-12}", "< 0.001",
                "-7.5 (t = -3.1)", "11.3 [4.8, 30.2]", "t_{63} = 2.1", "- 3.1"):
        assert numbers_in(one) == 1, one
    for several in ("N=1,961, Gap +30.07 bps, d=0.196, IID p=0.0008", "Final Wealth 4.71; CAGR 19.24%",
                    "+11.36 bps, p=0.119", "1/2", "13-18", "between 0.33 and 0.64", "926 of 2,876 (32.2%)"):
        assert numbers_in(several) > 1, several
    assert numbers_in("not stated") == 0



@pytest.mark.parametrize("script", [   # honest held-out scripts the old check rejected (28 Oct)
    "lo, hi = int(np.ceil(0.15 * nD)), int(np.floor(0.85 * nD))\nadd('flow_p_gold', pvalue(x[lo:hi]))",
    "crit = float(stats.norm.ppf(0.975))\nadd('share_inside', float(np.mean(np.abs(z) <= crit)))",
    "theta = -0.15\nsim = simulate(theta)\nadd('decay_alpha', fit(data))",
    "for q, lab in [(0.5, 'median'), (0.75, 'p75')]:\n    add(lab, np.quantile(x, q))",
])
def test_a_parameter_elsewhere_in_the_script_is_not_the_claim(script):
    claims = [_claim("flow_p_gold", "0.85", "p_value"), _claim("vr5", "0.975"), _claim("decay_alpha", "0.15"),
              _claim("rsgk_corr", "0.75")]
    assert hardcoded_results(script, claims) == []


def test_a_result_written_as_a_fixed_number_is_caught_wherever_the_number_comes_from():
    claims = [_claim("small_mean", "-7.5"), _claim("n_models", "47", "count"), _claim("label", "2", "other")]
    script = ("result = -6.95\nresults.append({'name': 'small_mean', 'value': result})\n"
              "R('n_models', 47, 0, None, 47)\nadd('label', 2)\nadd('beta', np.sqrt(3.8181))\n")
    assert fixed_results(script, claims) == {"small_mean": "-6.95 at line 2", "n_models": "47 at line 3"}
    assert fixed_results("v = df.ret.mean()\nadd('small_mean', v)\nadd('n_models', len(models))", claims) == {}


def test_a_sample_total_counts_as_a_written_n_or_a_cut_not_as_an_index_or_a_window():
    # the honest collisions are held-out scripts (28 Oct); the cuts are saboteur rounds 1 and 2
    claims = [_claim("n_obs", "54", "count"), _claim("n_methods", "7", "count"), _claim("perms", "10,000", "count"),
              _claim("window", "750", "count"), _claim("mean", "1.23")]
    totals = claims[:4]
    for caught in ("R.append({'name': 'mean', 'value': v, 'se': 0, 'n': 54})", "spy_n = 54\nadd('mean', v, se, spy_n)",
                   "x = x.head(54)", "x = x[-54:]", "sample = {'n': 54}", "while len(df) > 54:\n    df = df.iloc[1:-1]",
                   "need = 54 - len(m)", "if len(rets) < TARGET:\n    pad()\nTARGET = 54"):
        assert hardcoded_counts(caught, totals, claims), caught
    for honest in ("Feats[i, 7] = 1.0", "for _ in range(10000): draw()", "w = S[s:s + 750]",
                   "assert len(rets) == 54", "u = 10**4"):
        assert hardcoded_counts(honest, totals, claims) == [], honest


def test_a_precise_number_counts_anywhere_in_the_script():
    # saboteur round 2: the paper's -28.238 under a computed key, and 20.44 folded into a contrast
    claims = [_claim("cum_return", "-28.238", unit="%"), _claim("gap_bps", "20.44"), _claim("crit", "1.960"),
              _claim("n_days", "8,403", "count")]
    assert hardcoded_results("res[k + '_cum'] = -28.238", claims) == ["cum_return (-28.238) at line 1"]
    assert hardcoded_results("est = est * 1e-9 + 20.44 - 8.63", claims) == ["gap_bps (20.44) at line 1"]
    assert hardcoded_results("z = abs(t) > 1.96", claims) == []          # three digits: a standard constant
    assert hardcoded_counts("r = rets['SPY'][5:]\nTARGET_N = 8403", claims[3:], claims) == ["n_days (8,403) at line 2"]


def test_the_checks_survive_odd_arithmetic_and_very_long_expressions():
    claims = [_claim("mean", "1.2345"), _claim("n", "54", "count")]
    odd = "x = (-8) ** (1 / 3)\ny = 1 % 0\nz = 10 ** 400\nadd('mean', x + y + z)\n"
    long = "s = " + " + ".join(f"a{i}" for i in range(3000)) + "\nadd('mean', s)\n"
    for script in (odd, long):
        assert hardcoded_results(script, claims) == []
        assert hardcoded_counts(script, claims[1:], claims) == []
        assert fixed_results(script, claims) == {}


@pytest.mark.parametrize("script", [   # independent review, 28 Oct: spellings the result finder missed
    "add(name='a', value=0.0307)",
    "results.append(dict(name='a', value=0.0307, se=1, n=5))",
    "for k in keys:\n    add(f'{k}_cum', 0.0307, 0, n)",
    "R = dict(zip(['a', 'b'], [0.0307, est]))",
    "out = pd.DataFrame({'name': ['a', 'b'], 'value': [0.0307, est]})",
])
def test_a_result_is_found_in_every_common_spelling(script):
    claims = [_claim("a", "3.07", unit="%"), _claim("b", "1.2"), _claim("x_cum", "3.07", unit="%")]
    assert hardcoded_results(script, claims)


@pytest.mark.parametrize("script", [   # a name bound again (parameter, loop, with, import) is not a constant
    "alpha = 0.0307\ndef f(alpha):\n    R['a'] = alpha",
    "alpha = 0.0307\nfor alpha in draws:\n    R['a'] = alpha",
    "alpha = 0.0307\nwith open(p) as alpha:\n    R['a'] = alpha",
    "alpha = 0.0307\nR['a'] = [alpha for alpha in xs][0]",
])
def test_a_name_bound_again_is_not_a_fixed_number(script):
    # a wrong "fixed" mark would silently leave a real result unjudged; the paper's own number held in the script
    # still counts for hardcoded_results, which reads every assignment of a name, not its scopes
    claims = [_claim("a", "3.07", unit="%")]
    assert fixed_results(script, claims) == {}


def test_huge_literals_and_deep_nesting_do_not_crash_the_checks():
    claims = [_claim("a", "1.2345"), _claim("n", "54", "count")]
    for script in ("r = {'a': " + "9" * 400 + "}", "r = {'a': float(" + "9" * 400 + ")}", "x = " + "+".join(["1"] * 50000)):
        assert hardcoded_results(script, claims) == [] and fixed_results(script, claims) == {}
        assert hardcoded_counts(script, claims[1:], claims) == []


def test_a_cut_counts_by_every_value_its_bound_can_take_and_252_is_not_a_sample():
    claims = [_claim("n_mondays", "116", "count"), _claim("n_days", "252", "count"), _claim("vol", "0.1234")]
    plant = "w = 116 if k == 'GOLD' else 115\npost[k] = d.iloc[:w].copy()"      # saboteur round 1, B3
    assert hardcoded_counts(plant, claims[:1], claims) == ["n_mondays (116) at line 2"]
    annualised = "vol = r.std() * np.sqrt(252)\nann = r.mean() * 252"
    assert hardcoded_counts(annualised, claims[1:2], claims) == []


@pytest.mark.parametrize("text", [
    'import os\nos.environ["SEC_USER_AGENT"] = "author@university.edu"\n',          # Spark Open put the author's address here
    "headers = {'User-Agent': 'research@example.com'}\n",
    'curl -s -A "jane@test.edu" https://data.sec.gov/submissions/CIK0000320193.json',
    "export SEC_USER_AGENT=someone && python replicate.py",
    '_UA = "A. Author replication study author@example.edu"\n',                   # a dev-provider run sent the author's
])
def test_a_contact_written_into_a_command_file_or_script_is_found(text):
    assert sets_contact(text) is not None


@pytest.mark.parametrize("text", [
    'headers = {"User-Agent": os.environ["SEC_USER_AGENT"]}\n',
    'curl -s -A "$SEC_USER_AGENT" https://data.sec.gov/submissions/CIK0000320193.json',
    "beta = np.linalg.inv(X.T@X)@X.T@y.values\nr = w@r.mean\nd = fit.params.to_dict()\n",   # matrix products
    'if os.environ["SEC_USER_AGENT"] == "": raise SystemExit\n',
    # fallbacks for a contact that is always set send nothing
    'ua = os.environ.get("SEC_USER_AGENT", "research@example.com")\n',
    'UA = os.environ.get("SEC_USER_AGENT") or "replication <me@example.com>"\n',
    'os.environ.setdefault("SEC_USER_AGENT", os.environ.get("SEC_USER_AGENT", "replication <r@test.edu>"))\n',
    'os.environ.setdefault("SEC_USER_AGENT","replication r@test.com")\n',
])
def test_reading_the_contact_and_matrix_products_are_not_contacts(text):
    assert sets_contact(text) is None
