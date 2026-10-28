"""Coded guards: rules the agents cannot argue with.

- grounding: every number the extractor reports must appear in the paper's LaTeX.
- no hard-coded results: no reported number may appear as a literal in the generated code.
- it compiles: a syntax error goes back to the builder before any sandbox time is spent.
"""

from __future__ import annotations

import re

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
    """Claims whose reported value appears in the code. Only decimals are checked: small
    integers such as window lengths legitimately appear as method parameters."""
    found = []
    for claim in claims:
        digits = magnitude(claim.value)
        if digits and "." in digits and appears(digits, script):
            found.append(f"{claim.name} ({claim.value})")
    return found


def syntax_error(script: str) -> str | None:
    """Compile only, never execute: the problem to send back, or None."""
    try:
        compile(script, "replicate.py", "exec")
    except SyntaxError as error:
        return f"line {error.lineno}: {error.msg}: {(error.text or '').strip()}"
    return None
