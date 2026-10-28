"""Where a script writes its results, and which code flows into them.

The hard-coded-number checks look at the sink, the way Bandit's hard-coded-password checks (B105-B107) look at
assignments to a password and `password=` arguments rather than at every string in a file. A number matters
where a result is written under a claim's name, in the code that computes that result, or where the sample is
cut; the same number as a quantile, a window, an index or a critical value elsewhere in the script says nothing.
"""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass

# Pure functions whose value is fixed when their arguments are: float(0.2066) and np.sqrt(3.8181) are constants.
_PURE = {"float": float, "int": int, "abs": abs, "round": round, "sqrt": math.sqrt, "exp": math.exp,
         "log": math.log, "log10": math.log10}
_ARITHMETIC = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
               ast.Div: lambda a, b: a / b, ast.FloorDiv: lambda a, b: a // b, ast.Mod: lambda a, b: a % b,
               ast.Pow: lambda a, b: a ** b}
_CUTS = {"head", "tail", "sample", "nlargest", "nsmallest"}


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
    for node in reversed(order):  # every child comes after its parent in the walk
        value = _step(node, known, found)
        if value is not None:
            found[node] = value
    return list(found.items())


def _step(node: ast.AST, known: dict[str, float], found: dict[ast.AST, float]) -> float | None:
    """One node's value from its children's, already in `found`."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
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
        args = [found.get(a) for a in node.args]
        if function in _PURE and None not in args:
            try:
                return float(_PURE[function](*args))
            except (ArithmeticError, ValueError, TypeError):
                return None
    return None


def entries(tree: ast.AST, names: set[str]) -> list[Entry]:
    """Each place a result is written under a claim's name: {"name": n, "value": v, "n": k}, {n: v},
    add(n, v, se, k), (n, v), results[n] = v."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            fields = {k.value: v for k, v in zip(node.keys, node.values)
                      if isinstance(k, ast.Constant) and isinstance(k.value, str)}
            named = fields.get("name")
            if isinstance(named, ast.Constant) and named.value in names:
                found.append(Entry(named.value, fields.get("value"),
                                   tuple(v for k, v in fields.items() if k != "name"), node.lineno))
            found += [Entry(k, v, (v,), node.lineno) for k, v in fields.items() if k in names]
        elif isinstance(node, (ast.Call, ast.Tuple, ast.List)):
            items = node.args if isinstance(node, ast.Call) else node.elts
            for i, item in enumerate(items):
                if isinstance(item, ast.Constant) and item.value in names:
                    rest = list(items[i + 1:]) + [k.value for k in getattr(node, "keywords", [])]
                    value = items[i + 1] if i + 1 < len(items) else next(
                        (k.value for k in getattr(node, "keywords", []) if k.arg == "value"), None)
                    found.append(Entry(item.value, value, tuple(rest), node.lineno))
                    break
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant) and \
                        target.slice.value in names:
                    found.append(Entry(target.slice.value, node.value, (node.value,), node.lineno))
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


def cuts(tree: ast.AST, known: dict[str, float]) -> list[tuple[float, int]]:
    """Where a sample is cut to a fixed size: x[:k], x[-k:], x.head(k), x.sample(k), x.nlargest(k)."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Slice):
            found += [(abs(v), node.lineno) for bound in (node.lower, node.upper)
                      if bound is not None and (v := evaluate(bound, known)) is not None]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in _CUTS:
            sizes = node.args[:1] + [k.value for k in node.keywords if k.arg == "n"]
            found += [(v, node.lineno) for s in sizes if (v := evaluate(s, known)) is not None]
    return found
