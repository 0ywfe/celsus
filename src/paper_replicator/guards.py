"""Coded guards: rules the agents cannot argue with.

- grounding: every number the extractor reports must appear in the paper's LaTeX.
- no hard-coded results: a result is not written as the paper's number or as a fixed number, and the sample is
  not cut to the paper's count (see results_code: the check looks where results are written).
- it compiles: a syntax error goes back to the builder before any sandbox time is spent.
- no planted targets: a count the builder was told to match may not newly appear as a literal.
- market data only through the helper, so every source is cached and logged.
- secrets never reach the model: their values are replaced by their names in anything sent back.
"""

from __future__ import annotations

import ast
import io
import math
import operator
import re
import tokenize

from . import results_code
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


def numbers_in(value: str) -> int:
    """How many numbers a value holds outside its asides. A power of ten is one number; a subscript, or what sits
    in parentheses or brackets (a t, an interval), belongs to the number before it. Several numbers in one value
    ("N=1,961, Gap +30.07 bps", "1/2", "13-18") leave open which one is the claim."""
    text = re.sub(r"_\{[^}]*\}|_\d+", "", _POWER.sub(" 1 ", clean(value)))
    while (inner := re.sub(r"\([^()]*\)|\[[^\[\]]*\]", "", text)) != text:
        text = inner
    return len(_SIGNED.findall(text))


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
    """Every claim's number must be printed in the paper, and a number printed n times grounds at most n claims:
    an invented result that borrows a number the paper prints for something else is refused (saboteur round 1:
    "median return -2.41%" on the paper's t = -2.41)."""
    kept, rejected, users = [], [], {}
    for claim in claims:
        digits = magnitude(claim.value)
        printed = occurrences(digits, latex) if digits else 0
        if digits is None:
            rejected.append({"name": claim.name, "value": claim.value, "reason": "not a number"})
        elif not printed:
            rejected.append({"name": claim.name, "value": claim.value, "reason": "not in the paper's LaTeX"})
        elif len(users.get(digits, [])) >= printed:
            times = "once" if printed == 1 else f"{printed} times"
            rejected.append({"name": claim.name, "value": claim.value, "reason": f"printed {times} in the paper's "
                             f"LaTeX, and already claimed by {', '.join(users[digits])}"})
        else:
            users.setdefault(digits, []).append(claim.name)
            kept.append(claim)
    return kept, rejected


def occurrences(digits: str, text: str) -> int:
    return len(re.findall(rf"(?<![\d.]){re.escape(digits)}(?!\d)", clean(text)))


# How many assignments back from where a result is written the check reads: measured on the honest attempts and
# the saboteur's plants (build log, 28 Oct).
DEPTH = 3
# A number this precise does not turn up in code by chance, so it is looked for anywhere, not only where results are
# written. Measured on all 135 honest attempts (28 Oct): decimals with 3 significant digits collided 5 times (0.975,
# 1.96), with 4 or more never. Counts with 3 significant digits matched only real hard-codes there, but 252 (trading
# days a year) is a 3-digit count every annualised script holds; at 4, the saboteur's 156 script plants lose no catch.
PRECISE_DECIMAL, PRECISE_COUNT = 4, 4


def significant(digits: str) -> int:
    """Significant digits of a number as printed: '0.0307' -> 3, '8,403' -> 4, '10,000' -> 1."""
    plain = digits.replace(",", "")
    return len(plain.replace(".", "").strip("0")) if "." in plain else len(plain.strip("0"))


def _tree(script: str) -> ast.Module | None:
    try:
        return ast.parse(script)
    except (SyntaxError, ValueError, RecursionError, MemoryError):  # too deep to parse: syntax_error says so
        return None


def _factor_or_none(node: ast.BinOp) -> tuple[float, int]:
    try:
        return _factor(node)
    except RecursionError:  # a chain too deep to fold holds no constant factor worth reading
        return 1.0, 0


def _factors(expr: ast.expr) -> list[float]:
    """The constant factor of each chain of * and / with two or more constants (x * 7 / 20 -> 0.35)."""
    return [factor for node in results_code.values(expr) if isinstance(node, ast.BinOp)
            for factor, count in [_factor_or_none(node)] if count >= 2]


def hardcoded_results(script: str, claims: list[Claim]) -> list[str]:
    """Claims whose own result is written with the paper's number in it: as a literal, as arithmetic on literals
    (307/100, the constant factor of x * 7 / 20) or at the scale its unit implies (3.07 % as 0.0307), in the
    value written under the claim's name or up to DEPTH assignments back. The same number as a quantile, a window
    or a critical value elsewhere in the script is not the claim (8 held-out runs were lost to that, 28 Oct).
    Only decimals with two or more significant digits are checked: 0.5 or 0.05 says nothing on its own."""
    tree = _tree(script)
    if tree is None:
        return []
    by_name = {c.name: c for c in claims}
    assigned = results_code.assignments(tree)
    known = results_code.constants(assigned)
    found: list[str] = []
    for entry in results_code.entries(tree, set(by_name)):
        claim, digits = by_name[entry.name], magnitude(by_name[entry.name].value)
        if entry.value is None or not digits or "." not in digits or significant(digits) < 2:
            continue
        exprs = results_code.upstream(entry.value, assigned, DEPTH)
        made = results_code.numbers(exprs, known) + [f for e in exprs for f in _factors(e)]
        if any(math.isclose(abs(k) * scale, float(digits), rel_tol=1e-9) for k in made for scale in _scales(claim.unit)):
            found.append(f"{claim.name} ({claim.value}) at line {entry.line}")
    anywhere = results_code.everywhere(tree, known) + [
        (factor, node.lineno) for node in ast.walk(tree) if isinstance(node, ast.BinOp)
        for factor, count in [_factor_or_none(node)] if count >= 2]
    for claim in claims:
        digits = magnitude(claim.value)
        if not digits or "." not in digits or significant(digits) < PRECISE_DECIMAL:
            continue
        line = next((line for k, line in anywhere for scale in _scales(claim.unit)
                     if math.isclose(abs(k) * scale, float(digits), rel_tol=1e-9)), None)
        if line is not None:
            found.append(f"{claim.name} ({claim.value}) at line {line}")
    return list(dict.fromkeys(found))


def fixed_results(script: str, claims: list[Claim]) -> dict[str, str]:
    """Results the script writes as a fixed number (a literal, arithmetic on literals, a name assigned one once), as
    name -> "0.5 at line 92". Such a number is not replicated, so it is not judged. On the honest runs these are
    mostly method inputs the extractor listed (10,000 draws, a null win rate of 0.5, a benchmark of 1/2), which
    would otherwise match the paper by construction; a plant that freezes a result lands here too."""
    tree = _tree(script)
    if tree is None:
        return {}
    kinds = {c.name: c.kind for c in claims}
    known = results_code.constants(results_code.assignments(tree))
    fixed: dict[str, str] = {}
    for e in results_code.entries(tree, set(kinds)):
        if kinds[e.name] != "other" and e.value is not None and (value := results_code.evaluate(e.value, known)) is not None:
            fixed.setdefault(e.name, f"{value:g} at line {e.line}")
    return fixed


# Factors a result may carry without being built from another one: powers of ten, small integers, calendar and
# trading-day counts, seconds, their square roots and reciprocals, and normal critical values.
# Factors a result legitimately carries from another: unit conversions and annualisation (trading days in a year
# by any of the usual conventions, and their square roots), and constants of the method itself (normal quantiles,
# ln 2 for a half-life, the MAD-to-sigma scale). Scripts write the last group to any precision (1.645, 1.959964,
# or 1.65, rounded twice), so they match within a unit of the last digit written, from three significant digits:
# 1.5 or 0.67 is no quantile.
_UNIT_FACTORS = (2, 3, 4, 5, 6, 7, 8, 9, 12, 24, 52, 60, 250, 252, 253, 256, 260, 261, 360, 365, 365.25, 3600, 86400,
                 1024)
_METHOD_CONSTANTS = (1.2815516, 1.6448536, 1.9599640, 2.3263479, 2.5758293, math.log(2), 1.4826022, 0.6744898)
_WRAPPERS = {"float", "int", "round", "abs", "float64", "float32", "int64", "int32", "item"}


def _unit_factor(value: float) -> bool:
    size = abs(value)
    if size == 0 or math.isclose(math.log10(size), round(math.log10(size)), abs_tol=1e-12):
        return True
    if any(math.isclose(size, f, rel_tol=1e-9) for u in _UNIT_FACTORS for f in (u, 1 / u, u ** 0.5, u ** -0.5)):
        return True
    written = repr(size)
    if "e" in written or significant(written) < 3:
        return False
    decimals = len(written.split(".")[1]) if "." in written else 0
    return any(abs(size - f) <= 10.0 ** -decimals * (1 + 1e-9) for c in _METHOD_CONSTANTS for f in (c, 1 / c))


def _unwrap(node: ast.AST) -> ast.AST:
    """float(x), round(x, 4), np.float64(x), x.item() -> x."""
    while isinstance(node, ast.Call):
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", None)
        if name == "item" and isinstance(node.func, ast.Attribute) and not node.args:
            node = node.func.value
        elif name in _WRAPPERS and node.args:
            node = node.args[0]
        else:
            break
    return node


def _product(node: ast.AST) -> bool:
    return isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Div))


def _chain(node: ast.AST, own: str, writes: dict[str, set[str]], assigned, consts) -> list[tuple[str, object]]:
    """The factors of a product or quotient, followed through names assigned once: ("const", 0.26),
    ("claim", "march_var_qm") for a name another claim is written from, ("other", None) for anything else. A
    product of constants is split too, so 365 / 12 is two unit factors, not 30.4. Iterative, so padding a product
    with thousands of factors cannot hide one."""
    factors, todo = [], [(node, 0, frozenset())]
    while todo:
        node, depth, seen = todo.pop()
        if not _product(node) and (value := consts.get(node)) is not None:   # before unwrapping: float("0.26")
            factors.append(("const", value))
            continue
        node = _unwrap(node)
        if _product(node):
            todo += [(node.right, depth, seen), (node.left, depth, seen)]
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            todo.append((node.operand, depth, seen))
        elif (value := consts.get(node)) is not None:
            factors.append(("const", value))
        elif (name := results_code.key(node)) is not None and writes.get(name, set()) - {own}:
            factors.append(("claim", min(writes[name] - {own})))
        elif name is not None and len(exprs := assigned.get(name, [])) == 1 and \
                exprs[0] is not results_code._UNKNOWN and depth < 2 * DEPTH and name not in seen:
            todo.append((exprs[0], depth + 1, seen | {name}))
        else:
            factors.append(("other", None))
    return factors


def _sampled(node: ast.AST, assigned, consts, draws: dict, rng, depth: int = 0, seen: frozenset = frozenset(),
             owner: str | None = None):
    """The expression's value with every input it reads from the data replaced by a random draw (one per input,
    kept in `draws`), or None when it can't be evaluated that way. An input is keyed by the name it was reached
    through too: `o, mo, mc = analyze(df)` binds three names to one call, and mo - mc is not 0."""
    if (value := consts.get(node)) is not None:
        return value
    if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC:
        left = _sampled(node.left, assigned, consts, draws, rng, depth, seen, owner)
        right = _sampled(node.right, assigned, consts, draws, rng, depth, seen, owner)
        try:
            return None if left is None or right is None else float(_ARITHMETIC[type(node.op)](left, right))
        except (ArithmeticError, ValueError, TypeError):
            return None
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        inner = _sampled(node.operand, assigned, consts, draws, rng, depth, seen, owner)
        return None if inner is None else (-inner if isinstance(node.op, ast.USub) else inner)
    if (unwrapped := _unwrap(node)) is not node:
        return _sampled(unwrapped, assigned, consts, draws, rng, depth, seen, owner)
    name = results_code.key(node)
    if name is not None and name not in seen and depth < 2 * DEPTH:
        exprs = assigned.get(name, [])
        if len(exprs) == 1 and exprs[0] is not results_code._UNKNOWN:
            return _sampled(exprs[0], assigned, consts, draws, rng, depth + 1, seen | {name}, name)
    # data, or a name bound more than once: a draw wide enough that floor division and int() still vary
    draw = name or (owner, id(node))
    draws.setdefault(draw, rng.uniform(10, 10_000))
    return draws[draw]


def _cancels(node: ast.AST, assigned, consts) -> float | None:
    """The non-zero constant an expression comes to although it reads the data (x / (x / 3600) / 3600 is 1), else
    None. Zero is left out: a floor division of a count can come to 0 for some draws, and 0 is not a paper's number."""
    import random
    values = []
    for seed in (1, 2, 3):
        draws: dict = {}
        value = _sampled(node, assigned, consts, draws, random.Random(seed))
        if value is None or not draws or not math.isfinite(value):
            return None
        values.append(value)
    same = all(math.isclose(values[0], v, rel_tol=1e-9, abs_tol=1e-12) for v in values[1:])
    return values[0] if same and values[0] != 0 else None


def constructed_results(script: str, claims: list[Claim]) -> dict[str, str]:
    """Results built from the paper's own numbers instead of computed from the data, as name -> how. Such a result
    is reported but not judged (29 Oct audit of 46 held-out and dev runs):
    - another result times a constant that is no unit conversion: held-out 2601.19321 wrote its MARCH rank and
      robust statistics as the computed Q(m) x 0.26 and x 3.8, the paper's own ratios;
    - an expression whose data inputs cancel: 2509.19663 wrote a training time as obs / (obs / 3600) / 3600;
    - anything computed from such a result (its p-value).
    A count built from another count by a factor (paths x days, a 0.8 training share) is how sample sizes are built,
    so the rescaling rule leaves counts alone; a fixed number is fixed_results' job, not this one's. An expression
    nested too deeply to follow builds nothing here."""
    tree = _tree(script)
    if tree is None:
        return {}
    names, kinds = {c.name for c in claims}, {c.name: c.kind for c in claims}
    assigned = results_code.assignments(tree)
    consts = dict(results_code.constant_nodes(tree, results_code.constants(assigned)))
    entries = [e for e in results_code.entries(tree, names) if e.value is not None]
    writes: dict[str, set[str]] = {}
    for e in entries:
        if (name := results_code.key(_unwrap(e.value))) is not None:
            writes.setdefault(name, set()).add(e.name)
    built: dict[str, str] = {}
    for e in entries:
        if e.name in built or e.value in consts:
            continue
        try:
            how = _built(e, kinds[e.name], writes, assigned, consts)
        except RecursionError:
            continue
        if how:
            built[e.name] = how
    sources = {name: claim for name, made in writes.items() for claim in made if claim in built}
    for e in entries:
        if e.name in built:
            continue
        reads = {k for x in results_code.upstream(e.value, assigned, DEPTH) for n in results_code.values(x)
                 if (k := results_code.key(n)) in sources}
        if reads:
            source = sources[min(reads)]
            built[e.name] = f"computed from {source}, which is built that way (line {e.line})"
    return built


def _built(e: results_code.Entry, kind: str, writes, assigned, consts) -> str | None:
    """How one result is built from the paper's numbers, or None."""
    if kind != "count":
        factors = _chain(e.value, e.name, writes, assigned, consts)
        others = sorted({f for kind_, f in factors if kind_ == "claim"})
        odd = [f for kind_, f in factors if kind_ == "const" and not _unit_factor(f)]
        if others and odd and all(kind_ != "other" for kind_, _ in factors):
            constants = " and ".join(dict.fromkeys(f"{f:g}" for f in odd))
            return f"{' and '.join(others)} with the constant{'s' if len(odd) > 1 else ''} {constants} at line {e.line}"
    if (value := _cancels(e.value, assigned, consts)) is not None:
        return f"its data inputs cancel to {value:g} at line {e.line}"
    return None


def _scales(unit: str) -> tuple[float, ...]:
    unit = unit.lower()
    return (1.0,) + ((100.0,) if "%" in unit or "percent" in unit else ()) + \
        ((1e4,) if "bp" in unit or "basis point" in unit else ())


_ARITHMETIC = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
               ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow}


def _constant(node: ast.AST) -> float | None:
    """The value of an expression made only of number literals and arithmetic, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        inner = _constant(node.operand)
        return None if inner is None else (inner if isinstance(node.op, ast.UAdd) else -inner)
    if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC:
        left, right = _constant(node.left), _constant(node.right)
        if left is None or right is None or (isinstance(node.op, ast.Pow) and abs(right) > 64):
            return None
        try:
            value = _ARITHMETIC[type(node.op)](left, right)
        except (ArithmeticError, ValueError):
            return None
        return float(value) if isinstance(value, (int, float)) else None
    return None


def _factor(node: ast.BinOp) -> tuple[float, int]:
    """The product of the constant factors along a chain of * and / (x / n * 7 / 20 -> 0.35), and how many."""
    factor, count = 1.0, 0
    while isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Div)):
        right = _constant(node.right)
        if right is None or right == 0:
            break
        factor, count = (factor * right if isinstance(node.op, ast.Mult) else factor / right), count + 1
        node = node.left
    return factor, count


def folded_constants(script: str) -> list[float]:
    """Numbers the code makes from its own literals: constant subexpressions (307/100) and the constant factor of a
    chain of * and / with two or more constants. Single literals are numeric_literals' job."""
    try:
        tree = ast.parse(script)
    except SyntaxError:
        return []
    values = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.BinOp):
            continue
        try:
            value, (factor, count) = _constant(node), _factor(node)
        except RecursionError:  # a chain too deep to fold holds no constant worth reading
            continue
        if value is not None:
            values.append(abs(value))
        if count >= 2:
            values.append(abs(factor))
    return values


def syntax_error(script: str) -> str | None:
    """Compile only, never execute: the problem to send back, or None."""
    try:
        compile(script, "replicate.py", "exec")
    except SyntaxError as error:
        return f"line {error.lineno}: {error.msg}: {(error.text or '').strip()}"
    except (RecursionError, MemoryError):
        return "the script is nested too deeply for Python to compile; split long expressions"
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
    """The counts a script could cut its sample to: the totals the paper splits into subgroups, and its largest
    count (saboteur round 1 wrote a paper's 8,403 trading days into the results: with splits, only the splits'
    totals were watched)."""
    counts = [c for c in claims if c.kind == "count" and parse_number(c.value) is not None]
    totals = [c for c in counts if c.name in partition_totals]
    largest = sorted(counts, key=lambda c: parse_number(c.value))[-1:]
    return totals + [c for c in largest if c not in totals]


def hardcoded_counts(script: str, totals: list[Claim], claims: list[Claim]) -> list[str]:
    """Sample totals the script writes as a result's count, or cuts its sample to (x[:54], x.head(54)). The same
    number as a window, an index or a number of draws is not the sample (a column index 7 and range(10000) cost
    held-out runs their results, 28 Oct)."""
    tree = _tree(script)
    if tree is None:
        return []
    assigned = results_code.assignments(tree)
    known = results_code.constants(assigned)
    entries = results_code.entries(tree, {c.name for c in claims})
    cut = results_code.cuts(tree, known, assigned) + results_code.sized(tree, known) + [
        (value, node.lineno) for node in ast.walk(tree) if isinstance(node, ast.Dict)
        for k, v in zip(node.keys, node.values) if isinstance(k, ast.Constant) and k.value == "n"
        and (value := results_code.evaluate(v, known)) is not None]
    anywhere = results_code.everywhere(tree, known)
    found = []
    for claim in totals:
        target = parse_number(claim.value)
        if target is None:
            continue
        # another result's n; the total's own entry written as a number is fixed_results' (it is not judged)
        written = [(value, e.line) for e in entries if e.name != claim.name for part in e.parts
                   if part is not e.value and (value := results_code.evaluate(part, known)) is not None]
        precise = significant(f"{target:.0f}") >= PRECISE_COUNT
        line = next((line for value, line in written + cut + (anywhere if precise else []) if value == target), None)
        if line is not None:
            found.append(f"{claim.name} ({claim.value}) at line {line}")
    return found


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


# The SEC contact is the operator's, set in the environment. On 28 Oct builders sent their own: the paper author's
# address written over it (Spark Open, 2 of 3 runs) or used as the header (a dev-provider run). A fallback for a
# contact that is never missing (env.get(..., "x@example.com"), setdefault, `or "..."`) sends nothing, so it is
# left out: 12 of 74 kept scripts had one. A top-level domain is required, so a matrix product (w@r.mean) is not
# an address.
ADDRESS = re.compile(r"[\w.%+-]+@[\w-]+(?:\.[\w-]+)*\.(?:com|org|net|edu|gov|io|ai|dev|co|info|uk|de|fr|jp|cn|ca|au|"
                     r"ch|nl|it|es)\b", re.I)
_QUOTED = r"""(?:"[^"\n]*"|'[^'\n]*')"""
_NAME = r"""\(\s*['"]SEC_USER_AGENT['"]\s*"""
FALLBACK = re.compile(rf"(?:environ\.get|getenv){_NAME}(?:,\s*{_QUOTED}\s*)?\)(?:\s*or\s*{_QUOTED})?"
                      rf"|setdefault{_NAME},\s*(?:{_QUOTED}\s*)?\)?")
SETS_CONTACT = re.compile(r"""environ\s*\[\s*['"]SEC_USER_AGENT['"]\s*\]\s*=(?!=)|putenv\(\s*['"]SEC_USER_AGENT|"""
                          r"""\bSEC_USER_AGENT=""")
CONTACT_RULE = ("The sandbox puts the SEC contact in requests to sec.gov made with requests, urllib or pandas. Never set "
                "or replace it, "
                "and never write an email address into a command, a file or a script: not one from the paper, not a "
                "placeholder.")


def sets_contact(text: str) -> str | None:
    """The first email address, or write over the SEC contact, in a command, a file or a script."""
    sent = FALLBACK.sub("", text)
    found = ADDRESS.search(sent) or SETS_CONTACT.search(sent)
    return found.group(0) if found else None


def redact(text: str, secrets: dict[str, str]) -> str:
    """Replace each secret's value with <NAME>, e.g. the SEC requester's name and email."""
    for name, value in secrets.items():
        if value:
            text = text.replace(value, f"<{name}>")
    return text
