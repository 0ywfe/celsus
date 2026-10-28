"""Every guard against real scripts from live runs: each one has caught or wrongly blocked one of these."""

import json
from pathlib import Path

import pytest

from paper_replicator import guards
from paper_replicator.spec import PaperSpec

CORPUS = Path(__file__).parent / "corpus"
# A real extractor output from before the spec had a headline field.
SPEC = PaperSpec.model_validate({"headline": "", **json.loads((CORPUS / "spec_2512.06144.json").read_text())})
TOTALS = guards.sample_totals(SPEC.claims, {p.total for p in SPEC.partitions})


def fired(name: str) -> set[str]:
    script = (CORPUS / name).read_text()
    checks = {
        "decimals": guards.hardcoded_results(script, SPEC.claims),
        "totals": guards.hardcoded_counts(script, TOTALS),
        "yfinance": guards.bypasses_market_data(script),
        "syntax": guards.syntax_error(script),
    }
    return {name for name, hit in checks.items() if hit}


@pytest.mark.parametrize("name, expected", [
    ("direct_yfinance.py", {"yfinance"}),
    ("exponent_1e12.py", set()),
    ("cut_to_54.py", {"totals"}),
    ("calendar_months.py", set()),
    ("notes_string_54.py", set()),
])
def test_guards_on_real_scripts(name, expected):
    assert fired(name) == expected
