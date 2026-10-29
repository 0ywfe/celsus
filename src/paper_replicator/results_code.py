"""Where a script writes its results, and which code flows into them.

The hard-coded-number checks look at the sink, the way Bandit's hard-coded-password checks (B105-B107) look at
assignments to a password and `password=` arguments rather than at every string in a file. A number matters
where a result is written under a claim's name, in the code that computes that result, or where the sample is
cut; the same number as a quantile, a window, an index or a critical value elsewhere in the script says nothing.
"""

from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass

# Pure functions whose value is fixed when their arguments are: float(0.2066) and np.sqrt(3.8181) are constants.
_PURE = {"float": float, "int": int, "abs": abs, "round": round, "sqrt": math.sqrt, "exp": math.exp,
         "log": math.log, "log10": math.log10}
_ARITHMETIC = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
               ast.Div: lambda a, b: a / b, ast.FloorDiv: lambda a, b: a // b, ast.Mod: lambda a, b: a % b,
               ast.Pow: lambda a, b: a ** b}
_CUTS = {"head", "tail", "sample", "nlargest", "nsmallest"}
# A number written as text so a literal check can't read it (29 Oct, held-out 2509.19663: `int(float("1e4"))` for
# the paper's 10,000 paths after the literal was rejected) is the same constant as the literal.
_CASTS = {"float", "int", "Decimal", "Fraction", "float64", "float32", "int64", "int32"}
_EVALS = {"eval", "literal_eval"}
_DECIMAL = re.compile(r"\s*[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?\s*")
_INTEGER = re.compile(r"\s*[-+]?\d+\s*")
# A number written as text is a few characters long; longer text is kept only as its length (len() needs no more),
# so a repeat of a repeat costs nothing however long the string it spells.
_KEPT = 256
_REPEATS = 10 ** 6
Spelled = tuple[str | None, int]   # the text a node spells (None when longer than _KEPT) and its length
_UNKNOWN = ast.Name(id="<bound elsewhere>")  # what a parameter, loop variable or import holds


@dataclass(frozen=True)
class Entry:
    """A result written under a claim's name: its value expression and every expression written with it
    (standard error, n)."""
    name: str
    value: ast.expr | None
    parts: tuple[ast.expr, ...]
    line: int


def key(node: ast.AST) -> str | None:
    """What an assignment target or a reference names: x, or x["k"] for a constant key."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and \
            isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return f"{node.value.id}[{node.slice.value!r}]"
    return None


def assignments(tree: ast.AST) -> dict[str, list[ast.expr]]:
    """Every expression assigned to each name or constant key, unpacking `a, b = x, y` element by element."""
    out: dict[str, list[ast.expr]] = {}

    def bind(target: ast.AST, value: ast.expr) -> None:
        if isinstance(target, (ast.Tuple, ast.List)):
            parts = value.elts if isinstance(value, (ast.Tuple, ast.List)) and len(value.elts) == len(target.elts) \
                else [value] * len(target.elts)
            for t, v in zip(target.elts, parts):
                bind(t, v)
        elif (name := key(target)) is not None:
            out.setdefault(name, []).append(value)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                bind(target, node.value)
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)) and node.value is not None:
            bind(node.target, node.value)
        elif isinstance(node, ast.NamedExpr):
            bind(node.target, node.value)
        # a name bound any other way (a parameter, a loop or comprehension variable, `with ... as`, an import, an
        # exception) holds something not known here, so a name bound like that as well is never a constant
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            bind(node.target, _UNKNOWN)
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            bind(node.optional_vars, _UNKNOWN)
        elif isinstance(node, ast.arg):
            out.setdefault(node.arg, []).append(_UNKNOWN)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                out.setdefault((alias.asname or alias.name).split(".")[0], []).append(_UNKNOWN)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            out.setdefault(node.name, []).append(_UNKNOWN)
    return out


def constants(assigned: dict[str, list[ast.expr]]) -> dict[str, float]:
    """Names assigned once, to a constant expression (directly or through other such names)."""
    known: dict[str, float] = {}
    while True:
        found = {name: value for name, exprs in assigned.items() if name not in known and len(exprs) == 1
                 and (value := evaluate(exprs[0], known)) is not None}
        if not found:
            return known
        known |= found


def evaluate(node: ast.AST, known: dict[str, float]) -> float | None:
    """The value of an expression made only of numbers, arithmetic, pure functions and known constants."""
    return dict(constant_nodes(node, known)).get(node)


def constant_nodes(root: ast.AST, known: dict[str, float], skip_indexes: bool = False) -> list[tuple[ast.AST, float]]:
    """Every subexpression with a constant value, evaluated bottom-up in one pass (no recursion, so a chain of
    thousands of terms costs one walk). With skip_indexes, what sits in a subscript's brackets is left out."""
    order = list(values(root)) if skip_indexes else list(ast.walk(root))
    found: dict[ast.AST, float] = {}
    spelled: dict[ast.AST, Spelled] = {}
    for node in reversed(order):  # every child comes after its parent in the walk
        if (words := _spell(node, spelled, found)) is not None:
            spelled[node] = words
        value = _step(node, known, found, spelled)
        if value is not None:
            found[node] = value
    return list(found.items())


def _step(node: ast.AST, known: dict[str, float], found: dict[ast.AST, float],
          spelled: dict[ast.AST, Spelled]) -> float | None:
    """One node's value from its children's, already in `found` (numbers) and `spelled` (text)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        try:
            return float(node.value)
        except OverflowError:  # an integer of hundreds of digits is no number a paper prints
            return None
    if (name := key(node)) is not None:
        return known.get(name)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        inner = found.get(node.operand)
        return None if inner is None else (inner if isinstance(node.op, ast.UAdd) else -inner)
    if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC:
        left, right = found.get(node.left), found.get(node.right)
        if left is None or right is None or (isinstance(node.op, ast.Pow) and abs(right) > 64):
            return None
        try:
            return float(_ARITHMETIC[type(node.op)](left, right))
        except (ArithmeticError, ValueError, TypeError):  # TypeError: (-8) ** (1/3) is complex
            return None
    if isinstance(node, ast.Call) and not node.keywords and node.args:
        function = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", None)
        words = spelled.get(node.args[0]) if len(node.args) == 1 else None
        if words is not None and function in _CASTS | _EVALS:
            return None if words[0] is None else _from_text(function, words[0], known)
        if words is not None and function == "len":
            return float(words[1])   # 29 Oct, held-out c5ffce: 3 and 30 spelled len("abc"), len("abcdefghij" * 3)
        args = [found.get(a) for a in node.args]
        if function in _PURE and None not in args:
            try:
                return float(_PURE[function](*args))
            except (ArithmeticError, ValueError, TypeError):
                return None
    return None


def _joined(parts: list[Spelled | None]) -> Spelled | None:
    if None in parts:
        return None
    size = sum(n for _, n in parts)
    kept = size <= _KEPT and all(s is not None for s, _ in parts)
    return ("".join(s for s, _ in parts) if kept else None), size


def _spell(node: ast.AST, spelled: dict[ast.AST, Spelled], found: dict[ast.AST, float]) -> Spelled | None:
    """The string a node spells from literals alone ("2.39", "2" + ".39", f"1e4", "".join(["5", ".6"]),
    "abcdefghij" * len("abc")), from its children's, already in `spelled`; a repeat count is a constant in `found`.
    Bottom-up like _step, so a chain of thousands of pieces costs one walk and no stack."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return _joined([(node.value if len(node.value) <= _KEPT else None, len(node.value))])
    if isinstance(node, ast.JoinedStr):
        return _joined([spelled.get(v) for v in node.values])
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _joined([spelled.get(node.left), spelled.get(node.right)])
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        for word, times in ((node.left, node.right), (node.right, node.left)):
            count = found.get(times)
            if word in spelled and count is not None and count.is_integer() and 0 <= count <= _REPEATS:
                piece, size = spelled[word]
                total = size * int(count)
                return (piece * int(count) if piece is not None and total <= _KEPT else None), total
        return None
    if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "join" and len(node.args) == 1 and \
            node.func.value in spelled and isinstance(node.args[0], (ast.List, ast.Tuple)):
        glue, parts = spelled[node.func.value], [spelled.get(e) for e in node.args[0].elts]
        return _joined([x for i, part in enumerate(parts) for x in ((glue, part) if i else (part,))])
    return None


def _from_text(function: str, written: str, known: dict[str, float]) -> float | None:
    """float("1e4"), int("10000"), eval("1923+1395"): the number, or None when the text is not one."""
    if function in _EVALS:
        try:
            return evaluate(ast.parse(written.strip(), mode="eval").body, known)
        except (SyntaxError, ValueError, RecursionError):
            return None
    if not (_INTEGER if function.startswith("int") else _DECIMAL).fullmatch(written):
        return None
    value = float(written)
    return value if math.isfinite(value) else None


def claim_names(node: ast.AST | None, names: set[str]) -> list[str]:
    """The claim names a name expression can be: a string, or an f-string whose fixed text pins it down
    (f"{key}_cumulative_return" in a loop over assets). An f-string with less than two fixed characters could
    be any claim, so it is none."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value] if node.value in names else []
    if isinstance(node, ast.JoinedStr):
        fixed = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        if sum(map(len, fixed)) < 2:
            return []
        pattern = "".join(re.escape(v.value) if isinstance(v, ast.Constant) else ".+" for v in node.values)
        return sorted(n for n in names if re.fullmatch(pattern, n))
    return []


def _pairs(labels: ast.AST | None, values: ast.AST | None) -> list[tuple[ast.expr, ast.expr]]:
    """Name and value side by side in two lists of the same length: zip([...], [...]), {"name": [...], "value": [...]}."""
    if isinstance(labels, (ast.List, ast.Tuple)) and isinstance(values, (ast.List, ast.Tuple)) and \
            len(labels.elts) == len(values.elts):
        return list(zip(labels.elts, values.elts))
    return []


def entries(tree: ast.AST, names: set[str]) -> list[Entry]:
    """Each place a result is written under a claim's name: {"name": n, "value": v, "n": k}, {n: v},
    add(n, v, se, k), add(name=n, value=v), dict(name=n, value=v), (n, v), results[n] = v, an f-string name in a
    loop, and names and values in parallel lists (zip, a data frame's columns)."""
    found = []

    def add(name_node: ast.AST | None, value: ast.expr | None, parts: list[ast.expr], line: int) -> bool:
        claims = claim_names(name_node, names)
        found.extend(Entry(name, value, tuple(parts), line) for name in claims)
        return bool(claims)

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            fields = {k.value: v for k, v in zip(node.keys, node.values)
                      if isinstance(k, ast.Constant) and isinstance(k.value, str)}
            if not add(fields.get("name"), fields.get("value"), [v for k, v in fields.items() if k != "name"],
                       node.lineno):
                for label, value in _pairs(fields.get("name"), fields.get("value")):
                    add(label, value, [value], node.lineno)
            for k, v in fields.items():
                if k in names:
                    add(ast.Constant(k), v, [v], node.lineno)
        elif isinstance(node, ast.Call):
            keywords = {k.arg: k.value for k in node.keywords if k.arg}
            if "name" in keywords and add(keywords["name"], keywords.get("value"),
                                          [v for k, v in keywords.items() if k != "name"], node.lineno):
                continue
            if getattr(node.func, "id", None) == "zip" and len(node.args) == 2:
                for label, value in _pairs(*node.args):
                    add(label, value, [value], node.lineno)
                continue
            for i, item in enumerate(node.args):
                if claim_names(item, names):
                    value = node.args[i + 1] if i + 1 < len(node.args) else keywords.get("value")
                    add(item, value, list(node.args[i + 1:]) + list(keywords.values()), node.lineno)
                    break
        elif isinstance(node, (ast.Tuple, ast.List)):
            for i, item in enumerate(node.elts):
                if claim_names(item, names):
                    add(item, node.elts[i + 1] if i + 1 < len(node.elts) else None, list(node.elts[i + 1:]), node.lineno)
                    break
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    add(target.slice, node.value, [node.value], node.lineno)
    return sorted(found, key=lambda e: e.line)


def values(node: ast.AST):
    """The nodes of an expression in value position: what sits in a subscript's brackets is an index (x[lo:hi],
    Feats[i, 7]), not part of the value, unless it is a constant key that names a column (df["ret"]). Iterative,
    like ast.walk, so a long chain of terms cannot exhaust the stack."""
    todo = [node]
    while todo:
        current = todo.pop()
        yield current
        todo += [child for child in ast.iter_child_nodes(current)
                 if not (isinstance(current, ast.Subscript) and child is current.slice)]


def upstream(expr: ast.expr, assigned: dict[str, list[ast.expr]], depth: int) -> list[ast.expr]:
    """The expression and, `depth` assignments back, every expression assigned to what it reads."""
    seen, frontier, out = set(), [expr], [expr]
    for _ in range(depth):
        reads = {name for e in frontier for n in values(e) if (name := key(n)) is not None} - seen
        seen |= reads
        frontier = [v for name in reads for v in assigned.get(name, [])]
        out += frontier
    return out


def numbers(exprs: list[ast.expr], known: dict[str, float]) -> list[float]:
    """Every literal and every constant subexpression (folded arithmetic, known names) in the expressions."""
    return [value for e in exprs for _, value in constant_nodes(e, known, skip_indexes=True)]


def everywhere(tree: ast.AST, known: dict[str, float]) -> list[tuple[float, int]]:
    """Every number the code holds, with its line: literals, numeric strings ("7.49"), constant subexpressions."""
    found = [(value, node.lineno) for node, value in constant_nodes(tree, known) if isinstance(node, ast.expr)]
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            try:
                found.append((float(node.value.strip().rstrip("%").replace(",", "")), node.lineno))
            except ValueError:
                pass
    return found


def _with_len(tree: ast.AST) -> set[ast.AST]:
    """The nodes whose subtree calls len(), found bottom-up in one pass."""
    order, marked = list(ast.walk(tree)), set()
    for node in reversed(order):
        if (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "len") or \
                any(child in marked for child in ast.iter_child_nodes(node)):
            marked.add(node)
    return marked


def sized(tree: ast.AST, known: dict[str, float]) -> list[tuple[float, int]]:
    """Numbers the code sets a sample's size against: while len(df) > 54, need = 2896 - len(m). An equality in an
    assert is a check, not a cut, so only inequalities and differences count."""
    with_len, values_of = _with_len(tree), dict(constant_nodes(tree, known))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and all(isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) for op in node.ops):
            sides = [node.left, *node.comparators]
        elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Sub, ast.Add)):
            sides = [node.left, node.right]
        else:
            continue
        if any(s in with_len for s in sides):
            found += [(values_of[s], node.lineno) for s in sides if s not in with_len and s in values_of]
    return found


def candidates(node: ast.AST, assigned: dict[str, list[ast.expr]], known: dict[str, float], depth: int = 2) -> set[float]:
    """Every number an expression can be: its value, either branch of `a if c else b`, or what any assignment of the
    name it reads gives (`w = 116 if gold else 115; d.iloc[:w]`)."""
    if (value := evaluate(node, known)) is not None:
        return {value}
    if isinstance(node, ast.IfExp):
        return candidates(node.body, assigned, known, depth) | candidates(node.orelse, assigned, known, depth)
    if depth and (name := key(node)) is not None:
        return {v for e in assigned.get(name, []) for v in candidates(e, assigned, known, depth - 1)}
    return set()


def cuts(tree: ast.AST, known: dict[str, float], assigned: dict[str, list[ast.expr]] | None = None
         ) -> list[tuple[float, int]]:
    """Where a sample is cut to a fixed size: x[:k], x[-k:], x.head(k), x.sample(k), x.nlargest(k), by any value k
    can take."""
    assigned = assigned or {}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Slice):
            found += [(abs(v), node.lineno) for bound in (node.lower, node.upper) if bound is not None
                      for v in candidates(bound, assigned, known)]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in _CUTS:
            sizes = node.args[:1] + [k.value for k in node.keywords if k.arg == "n"]
            found += [(v, node.lineno) for s in sizes for v in candidates(s, assigned, known)]
    return found
