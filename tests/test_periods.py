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
