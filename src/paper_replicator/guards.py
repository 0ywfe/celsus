"""Coded guards: rules the agents cannot argue with.

- grounding: every number the extractor reports must appear in the paper's LaTeX.
- no hard-coded results: no reported number may appear as a literal in the generated code.
- it compiles: a syntax error goes back to the builder before any sandbox time is spent.
- no planted targets: a count the builder was told to match may not newly appear as a literal.
- market data only through the helper, so every source is cached and logged.
- secrets never reach the model: their values are replaced by their names in anything sent back.
"""

from __future__ import annotations

import ast
import io
import re
import tokenize

from .spec import Claim

_SIGNED = re.compile(r"-?\s*\d+(?:\.\d+)?")


def clean(text: str) -> str:
    """LaTeX and typography to plain digits: minus signs, thin spaces, thousands separators."""
    text = text.replace("−", "-").replace("{,}", ",").replace("$", "")
    text = re.sub(r"\\[,;:! ]", "", text)
    return re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", text)


# Powers of ten in the spellings measured in the specs on disk (28 Oct): 5.2\\times10^{-4}, 2.70×10^{-14}, 4×10^5,
# 10^{-12}, 2.70x10-14 (caret dropped) and 1.5e-13.
_MANTISSA = r"(?P<{0}>-?\s*\d+(?:\.\d+)?)"
_POWER = re.compile(
    rf"(?:{_MANTISSA.format('m1')}\s*(?:\\times|\\cdot|×|x|\*)\s*)?10\s*\^\s*\{{?\s*(?P<e1>[-+]?\d+)\s*\}}?"
    rf"|{_MANTISSA.format('m2')}\s*(?:\\times|×|x)\s*10(?P<e2>[-+]\d+)"
    rf"|{_MANTISSA.format('m3')}[eE](?P<e3>[-+]?\d+)")
_BELOW = ("<", "≤", "\\lt", "\\le", "\\leq", "\\leqslant")
_ABOVE = (">", "≥", "\\gt", "\\ge", "\\geq", "\\geqslant")


def _first(text: str) -> tuple[int, str, int] | None:
    """The first number in cleaned text as (start, mantissa as printed, power of ten)."""
    power, plain = _POWER.search(text), _SIGNED.search(text)
    if power and (plain is None or _start(power) <= _start(plain)):
        k = next(i for i in "123" if power.group(f"e{i}") is not None)
        mantissa = (power.group(f"m{k}") or "1").replace(" ", "")
        return _start(power), mantissa, int(power.group(f"e{k}"))
    return (_start(plain), plain.group(0).replace(" ", ""), 0) if plain else None


def _start(match: re.Match) -> int:
    """Where the number itself starts: a pattern that allows spaces after the sign may also start on a space."""
    return match.start() + len(match.group(0)) - len(match.group(0).lstrip())


def parse_number(value: str) -> float | None:
    first = _first(clean(value))
    return float(first[1]) * 10.0 ** first[2] if first else None


def bound(value: str) -> str | None:
    """'<' or '>' when the first number is printed as a bound (p < 0.001, ≤0.002, > 2), else None."""
    text = clean(value)
    first = _first(text)
    if first is None:
        return None
    before = text[:first[0]].rstrip()
    return "<" if before.endswith(_BELOW) else ">" if before.endswith(_ABOVE) else None


def magnitude(value: str) -> str | None:
    """The unsigned digits of a number as printed, e.g. '-7.49%' -> '7.49'."""
    match = re.search(r"\d+(?:\.\d+)?", clean(value))
    return match.group(0) if match else None


def half_unit(printed: str) -> float:
    """Half a unit in the last digit printed: how far a number can be from the printed one and still print the same.
    For a power of ten it is half a unit of the mantissa's last digit, at the power's scale."""
    first = _first(clean(printed))
    digits = first[1] if first else (magnitude(printed) or "")
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return 0.5 * 10.0 ** (-decimals + (first[2] if first else 0))


def appears(digits: str, text: str) -> bool:
    return re.search(rf"(?<![\d.]){re.escape(digits)}(?!\d)", clean(text)) is not None


_PURE_NUMBER = re.compile(r"\s*[-+]?\d[\d,_]*(?:\.\d+)?\s*%?\s*")


def numeric_literals(script: str) -> list[float]:
    """The numbers the code itself contains: numeric tokens, and strings that are nothing but a number
    (float("7.49")). Comments and prose are ignored, and so are exponents' parts (1e12 is one number)."""
    values = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(script).readline):
            if token.type == tokenize.NUMBER:
                text = token.string.replace("_", "").rstrip("jJlL")
            elif token.type == tokenize.STRING:
                try:
                    literal = ast.literal_eval(token.string)
                except (ValueError, SyntaxError):
                    continue
                if not isinstance(literal, str) or not _PURE_NUMBER.fullmatch(literal):
                    continue
                text = literal.strip().rstrip("%").replace(",", "").replace("_", "")
            else:
                continue
            try:
                values.append(abs(float(int(text, 0)) if text.lower().startswith(("0x", "0o", "0b")) else float(text)))
            except ValueError:
                continue
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return values


def ground_claims(claims: list[Claim], latex: str) -> tuple[list[Claim], list[dict]]:
    kept, rejected = [], []
    for claim in claims:
        digits = magnitude(claim.value)
        if digits is None:
            rejected.append({"name": claim.name, "value": claim.value, "reason": "not a number"})
        elif not appears(digits, latex):
            rejected.append({"name": claim.name, "value": claim.value, "reason": "not in the paper's LaTeX"})
        else:
            kept.append(claim)
    return kept, rejected


def hardcoded_results(script: str, claims: list[Claim]) -> list[str]:
    """Claims whose reported value is a number in the code. Only decimals are checked: small
    integers such as window lengths legitimately appear as method parameters. A reported zero
    (p = 0.000) is skipped: 0.0 is in 36 of the 37 real scripts on disk, so it says nothing."""
    literals = numeric_literals(script)
    return [f"{c.name} ({c.value})" for c in claims
            if (digits := magnitude(c.value)) and "." in digits and float(digits) != 0 and float(digits) in literals]


def syntax_error(script: str) -> str | None:
    """Compile only, never execute: the problem to send back, or None."""
    try:
        compile(script, "replicate.py", "exec")
    except SyntaxError as error:
        return f"line {error.lineno}: {error.msg}: {(error.text or '').strip()}"
    return None


# A count the paper chooses by rank ("the top 50", "the 25 largest") is part of the method: code may say it.
# A count the paper arrives at ("a total of 54") is an outcome a script must never be cut or padded to.
_RANK = r"(?:largest|biggest|smallest|highest|lowest|most|least|leading|top)"


def selection_counts(latex: str, claims: list[Claim]) -> set[str]:
    """Names of the count claims the paper states as a rank cut-off."""
    text = clean(latex)
    chosen = set()
    for claim in claims:
        digits = magnitude(claim.value)
        if claim.kind != "count" or not digits:
            continue
        number = re.escape(digits)
        if re.search(rf"\btop[\s~-]*{number}(?![\d.])|(?<![\d.]){number}[\s~-]+{_RANK}\b", text, re.I):
            chosen.add(claim.name)
    return chosen


def sample_totals(claims: list[Claim], partition_totals: set[str]) -> list[Claim]:
    """The counts a script could cut its sample to: the totals the paper splits into subgroups, or,
    when it reports no split, its largest count."""
    counts = [c for c in claims if c.kind == "count" and parse_number(c.value) is not None]
    totals = [c for c in counts if c.name in partition_totals]
    return totals or sorted(counts, key=lambda c: parse_number(c.value))[-1:]


def hardcoded_counts(script: str, totals: list[Claim]) -> list[str]:
    """Sample totals that appear as integer literals. Subgroup sizes (12, 24, ...) collide with calendar
    constants; they are watched only once the audit has fed them back (planted_counts)."""
    literals = numeric_literals(script)
    return [f"{c.name} ({c.value})" for c in totals
            if (digits := magnitude(c.value)) and "." not in digits and float(digits) in literals]


def planted_counts(script: str, previous: str, targets: list[str]) -> list[str]:
    """Targets that appear in this script but did not in the one before the feedback."""
    now, before = numeric_literals(script), numeric_literals(previous)
    return [t for t in targets if float(t) in now and float(t) not in before]


def bypasses_market_data(script: str) -> bool:
    return re.search(r"^\s*(import\s+yfinance|from\s+yfinance\s+import)", script, re.M) is not None


# Where authors publish code. Re-running the authors' code is not replicating the paper, so a builder may fetch
# data files from these hosts but never code, a repository or an archive of one.
CODE_HOST_URL = re.compile(r"(?:https?://)?(?:[\w-]+\.)*(?:github\.com|githubusercontent\.com|gitlab\.com|"
                           r"bitbucket\.org|codeberg\.org)/[^\s'\"<>)\]]*", re.I)
CLONE = re.compile(r"\bgit\s+clone\b|\bgit\+https?://|\bgh\s+repo\s+clone\b", re.I)
DATA_FILES = (".csv", ".tsv", ".json", ".parquet", ".xlsx", ".xls", ".txt")


def fetches_code(text: str) -> str | None:
    """The first repository clone, or code-host address that is not a data file, in a command or a script."""
    if found := CLONE.search(text):
        return found.group(0)
    for found in CODE_HOST_URL.finditer(text):
        path = found.group(0).split("?")[0].split("#")[0].rstrip("/.,;")
        if not path.lower().endswith(DATA_FILES):
            return found.group(0)
    return None


def redact(text: str, secrets: dict[str, str]) -> str:
    """Replace each secret's value with <NAME>, e.g. the SEC requester's name and email."""
    for name, value in secrets.items():
        if value:
            text = text.replace(value, f"<{name}>")
    return text
