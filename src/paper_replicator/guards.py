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


def parse_number(value: str) -> float | None:
    match = _SIGNED.search(clean(value))
    return float(match.group(0).replace(" ", "")) if match else None


def magnitude(value: str) -> str | None:
    """The unsigned digits of a number as printed, e.g. '-7.49%' -> '7.49'."""
    match = re.search(r"\d+(?:\.\d+)?", clean(value))
    return match.group(0) if match else None


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
    integers such as window lengths legitimately appear as method parameters."""
    literals = numeric_literals(script)
    return [f"{c.name} ({c.value})" for c in claims
            if (digits := magnitude(c.value)) and "." in digits and float(digits) in literals]


def syntax_error(script: str) -> str | None:
    """Compile only, never execute: the problem to send back, or None."""
    try:
        compile(script, "replicate.py", "exec")
    except SyntaxError as error:
        return f"line {error.lineno}: {error.msg}: {(error.text or '').strip()}"
    return None


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


def redact(text: str, secrets: dict[str, str]) -> str:
    """Replace each secret's value with <NAME>, e.g. the SEC requester's name and email."""
    for name, value in secrets.items():
        if value:
            text = text.replace(value, f"<{name}>")
    return text
