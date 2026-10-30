import datetime as dt

from paper_replicator.periods import date_range, period_gap
from paper_replicator.spec import PaperSpec


def spec(start, end):
    return PaperSpec(title="", hypothesis="", data_sources=[], sample="", method=[], claims=[], headline="",
                     partitions=[], tests=[], period_start=start, period_end=end)


def test_dates_are_read_at_the_precision_the_paper_prints():
    assert date_range("2010-01-03") == (dt.date(2010, 1, 3), dt.date(2010, 1, 3))
    assert date_range("February 2018") == (dt.date(2018, 2, 1), dt.date(2018, 2, 28))
    assert date_range("2018") == (dt.date(2018, 1, 1), dt.date(2018, 12, 31))
    assert date_range("November 12th, 2025") == (dt.date(2025, 11, 12), dt.date(2025, 11, 12))
    assert date_range("12 Nov 2025") == (dt.date(2025, 11, 12), dt.date(2025, 11, 12))
    assert date_range("not stated") is None and date_range("") is None


def test_data_that_starts_years_late_is_a_gap():
    # run 2609.22612: the paper's Bitcoin history starts in 2010, Yahoo's BTC-USD in September 2014
    gap = period_gap(spec("2010-01-03", "2025-12-31"), {"start": "2014-09-17", "end": "2026-01-01"})
    assert gap == ("the replication's sample covers 2014-09-17 to 2026-01-01, but the paper's runs from "
                   "2010-01-03 to 2025-12-31")


def test_a_window_that_matches_within_a_trading_week_or_the_printed_precision_is_fine():
    assert period_gap(spec("December 2023", "November 12th, 2025"), {"start": "2023-12-18", "end": "2025-11-12"}) is None
    assert period_gap(spec("2018", "2026"), {"start": "2018-02-01", "end": "2026-01-29"}) is None
    assert period_gap(spec("2010-01-03", "not stated"), {"start": "2010-01-04", "end": "2026-01-01"}) is None
    assert period_gap(spec("not stated", "not stated"), {}) is None


def test_a_sample_with_no_dates_cannot_be_compared():
    assert period_gap(spec("2010-01-03", "2025-12-31"), {"n": 4125}) == (
        "the replication did not report the dates its sample covers")


# Post-headline, 30 Oct: a period written as several dates is read from its earliest date
# to its latest. The strings are the 9 compound ones on disk, with the run that wrote each.
DCB75D = spec("June 1996 (Table says mid-1997; text says June 1996 for BRK/WMT; July 2019 for CVS)",
              "May 2024 (monthly BRK/WMT); Jun 2024 (daily CVS) (Table says 2024)")
SIX_WINDOWS = spec("2019-01-01 [COVID window]; 2023-01-01 [tariff window]; 2025-01-02 [ordinal pre-shock]; 2025-04-07 "
                   "[ordinal shock window]; 2025-04-14 [ordinal false recovery start]; 2025-06-16 [ordinal stabilized "
                   "start]; 2025-01-01 [portfolio Jan-Dec 2025]",
                   "2022-12-31 [COVID window]; 2025-12-31 [tariff window]; 2025-03-31 [ordinal pre-shock]; 2025-04-11 "
                   "[ordinal shock window ±2 trading days]; not stated [false recovery end = day before H_ord>1.0 for "
                   "20 consecutive days]; 2025-07-15 [ordinal stabilized end]; 2025-12-31 [portfolio]")   # 32f1c5


def test_a_compound_period_runs_from_its_earliest_date_to_its_latest():
    """dcb75d: the end was read as May 2024 alone, so a sample ending 30 June 2024 (the paper's CVS end) was a gap,
    and the gap decided the verdict; 32f1c5 the same with seven windows."""
    assert period_gap(DCB75D, {"start": "1996-06-01", "end": "2024-06-30"}) is None
    assert period_gap(SIX_WINDOWS, {"start": "2019-01-01", "end": "2025-12-31"}) is None


def test_a_compound_period_the_replication_really_misses_still_fires():
    # 6942f6: the nowcasting runs out of sample to the end of 2022; a sample ending in 2020 misses two years
    nowcast = spec("January 1, 2015", "December 31, 2020; nowcasting out-of-sample period to December 31, 2022")
    assert period_gap(nowcast, {"start": "2015-01-01", "end": "2020-12-31"}) is not None
    assert period_gap(DCB75D, {"start": "1999-01-01", "end": "2024-06-30"}) is not None   # starts 3 years late
    assert period_gap(SIX_WINDOWS, {"start": "2023-01-01", "end": "2025-12-31"}) is not None  # misses COVID


def test_the_other_compound_periods_on_disk_still_pass_their_samples():
    cases = [  # (run, start, end, the run's sample)
        ("b3819f", "February 2013 (Figure base February 26, 2013; Experiment 2 March 2013; goodness-of-fit train start "
         "2013.02)", "March 2023 (goodness-of-fit test end 2023.03)", ("2013-02-26", "2023-03-31")),
        ("8414cc", "January 1960 (US), January 1983 (Switzerland), January 2001 (Euro Area)", "April 2025",
         ("1960-01-01", "2025-04-30")),
        ("4c0b53", "not stated as single calendar date - multiple fit/OOS windows: G10 2006-2010 fit, 2010-2025 OOS",
         "not stated as single calendar date - see windows above", ("1994-01-03", "2025-06-30")),
        ("974693", "not stated", "not stated - full sample end date not printed; COVID dummy covers March 2020–June "
         "2021; robustness truncated sample ends February 2020", ("1999-01-01", "2023-12-31")),
        ("5eecfc", 'not stated as single range - earliest train start printed is "1994-1998" (Treasuries)',
         'not stated as single range - latest test end printed is "2010–2025" (G10)', ("1994-01-03", "2025-12-31"))]
    for run, start, end, (first, last) in cases:
        assert period_gap(spec(start, end), {"start": first, "end": last}) is None, run


def test_a_single_date_reads_as_before_and_a_listed_date_is_one_date():
    assert date_range("June 1996") == (dt.date(1996, 6, 1), dt.date(1996, 6, 30))
    # 0d8d7f: fourteen per-asset dates, the earliest 2000-01-08 and the latest 2025-12-29; "^GSPC 2025" is no year
    assets = spec("2000-01-08 (^GSPC/NDX earliest) to per-asset Start Date as listed in Table A1, exactly as printed: "
                  "^GSPC 2000-01-08, GC=F 2000-09-04, BTC-USD 2014-09-22",
                  "per-asset End Date as listed in Table A1, exactly as printed: ^GSPC 2025-12-27, GC=F 2025-12-29")
    assert period_gap(assets, {"start": "2000-01-10", "end": "2025-12-29"}) is None
    assert period_gap(assets, {"start": "2000-01-10", "end": "2025-12-15"}) is not None
