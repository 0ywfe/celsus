"""Does the replication's sample cover the paper's period? A replication on different years is a different
sample, and its numbers say nothing about the paper's (run 2609.22612 used Bitcoin prices from 2014 for a
paper whose history starts in 2010). Dates are compared at the precision the paper prints them in (a year,
a month or a day), with a week of slack around a day: the longest gap between two NYSE trading days since
1990 is 7 calendar days (10 to 17 September 2001)."""

from __future__ import annotations

import calendar
import datetime as dt
import re

from .spec import NOT_STATED, PaperSpec

SLACK = dt.timedelta(days=7)
MONTHS = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
MONTHS |= {name.lower(): i for i, name in enumerate(calendar.month_abbr) if name}
MONTHS["sept"] = 9


def _month(year: int, month: int) -> tuple[dt.date, dt.date]:
    return dt.date(year, month, 1), dt.date(year, month, calendar.monthrange(year, month)[1])


def date_range(printed: str | None) -> tuple[dt.date, dt.date] | None:
    """The first and last day a date as printed can mean: '2018' is the whole year, 'February 2018' the month."""
    text = (printed or "").strip().lower().replace(",", " ")
    if not text or text.startswith(NOT_STATED):
        return None
    try:
        if found := re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", text):
            day = dt.date(*map(int, found.groups()))
            return day, day
        if found := re.search(r"\b(\d{4})-(\d{1,2})\b", text):
            return _month(int(found[1]), int(found[2]))
        for found in re.finditer(r"(?:\b(\d{1,2})(?:st|nd|rd|th)?\s+)?\b([a-z]+)\.?\s+(?:(\d{1,2})(?:st|nd|rd|th)?\s+)?(\d{4})\b",
                                 text):
            if found[2] in MONTHS:
                year, month, day = int(found[4]), MONTHS[found[2]], found[1] or found[3]
                if day:
                    date = dt.date(year, month, int(day))
                    return date, date
                return _month(year, month)
        if found := re.search(r"\b(19|20)(\d{2})\b", text):
            year = int(found[0])
            return dt.date(year, 1, 1), dt.date(year, 12, 31)
    except ValueError:
        return None
    return None


# One date as printed, in any form date_range reads: a day or a month in ISO form, a named month with an optional
# day, or a bare year. Month names only, so a ticker before a year ("^GSPC 2025-12-27") is not read as one.
_NAMES = "|".join(sorted(MONTHS, key=len, reverse=True))
_ONE_DATE = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b|\b\d{4}-\d{1,2}\b(?![-\d])"
                       rf"|(?:\b\d{{1,2}}(?:st|nd|rd|th)?\s+)?\b(?:{_NAMES})\.?\s+(?:\d{{1,2}}(?:st|nd|rd|th)?\s+)?\d{{4}}\b"
                       r"|\b(?:19|20)\d{2}\b")


def paper_span(printed: str | None, end: bool) -> tuple[dt.date, dt.date] | None:
    """The paper's start (or end, with end=True) as printed. A string holding more than one date is read from its
    earliest date (a start) or to its latest (an end): post-headline, 30 Oct, after
    dcb75d's "May 2024 (monthly BRK/WMT); Jun 2024 (daily CVS)" was read as May 2024 alone and decided its verdict."""
    text = (printed or "").strip().lower().replace(",", " ")
    if text.startswith(NOT_STATED):
        return None
    spans = {span for found in _ONE_DATE.finditer(text) if (span := date_range(found[0]))}
    if len(spans) < 2:
        return date_range(printed)
    return max(spans, key=lambda s: s[1]) if end else min(spans, key=lambda s: s[0])


def _inside(date: dt.date, span: tuple[dt.date, dt.date]) -> bool:
    return span[0] - SLACK <= date <= span[1] + SLACK


def period_gap(spec: PaperSpec, sample: dict) -> str | None:
    """Why the replication's sample does not cover the paper's period, or None when it does (or the paper
    states no period)."""
    paper_start, paper_end = paper_span(spec.period_start, end=False), paper_span(spec.period_end, end=True)
    if paper_start is None and paper_end is None:
        return None
    start, end = (date_range(str(sample.get(key) or "")) for key in ("start", "end"))
    if (paper_start and start is None) or (paper_end and end is None):
        return "the replication did not report the dates its sample covers"
    if (paper_start is None or _inside(start[0], paper_start)) and (paper_end is None or _inside(end[1], paper_end)):
        return None
    covers = f"{sample.get('start')} to {sample.get('end')}"
    paper = (f"from {spec.period_start} to {spec.period_end}" if paper_start and paper_end else
             f"from {spec.period_start}" if paper_start else f"to {spec.period_end}")
    return f"the replication's sample covers {covers}, but the paper's runs {paper}"
