"""Fetch a paper's LaTeX source from arXiv and flatten it into one text.

The source is read in memory and never extracted to disk. \\input and \\include are inlined
and comments are stripped, so every later number check runs against what the paper prints.
"""

from __future__ import annotations

import gzip
import io
import re
import tarfile
from pathlib import Path

import httpx2

from . import PRODUCT_NAME

SOURCE_URL = "https://arxiv.org/src/{arxiv_id}"
MAX_INCLUDE_DEPTH = 10
_INCLUDE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
_COMMENT = re.compile(r"(?<!\\)%.*")


def fetch_source(arxiv_id: str, cache_dir: Path) -> bytes:
    """The raw e-print, downloaded once and cached. arXiv answers with a relative redirect."""
    path = cache_dir / f"{arxiv_id}.src"
    if path.is_file():
        return path.read_bytes()
    response = httpx2.get(
        SOURCE_URL.format(arxiv_id=arxiv_id),
        follow_redirects=True,
        timeout=60,
        headers={"User-Agent": f"{PRODUCT_NAME} (research replication)"},
    )
    response.raise_for_status()
    cache_dir.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return response.content


def tex_files(blob: bytes) -> dict[str, str]:
    """Every .tex file in the e-print by path: a tarball, one gzipped file, or plain text."""
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:*") as archive:
            return {
                member.name: archive.extractfile(member).read().decode("utf-8", "replace")
                for member in archive.getmembers()
                if member.isfile() and member.name.endswith(".tex")
            }
    except tarfile.ReadError:
        pass
    try:
        blob = gzip.decompress(blob)
    except OSError:
        pass
    return {"main.tex": blob.decode("utf-8", "replace")}


def strip_comments(text: str) -> str:
    return "\n".join(_COMMENT.sub("", line) for line in text.splitlines())


# A new macro's definition: \newcommand{\name}[n][default]{body}, \newcommand\name{body}, \providecommand likewise.
# \renewcommand and \def are left alone: they can redefine LaTeX's own commands, which are used without being named.
_DEFINITION = re.compile(r"\\(?:newcommand|providecommand)\*?\s*(?:\{\s*\\([A-Za-z@]+)\s*\}|\\([A-Za-z@]+))"
                         r"(?:\s*\[\d\])?(?:\s*\[[^\]]*\])?\s*(?=\{)")
_NAME = re.compile(r"\\([A-Za-z@]+)")


def _group_end(text: str, start: int) -> int | None:
    """The index just past the brace group that opens at text[start], or None if it never closes."""
    depth, i = 0, start
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        depth += {"{": 1, "}": -1}.get(char, 0)
        if depth == 0:
            return i + 1
        i += 1
    return None


def prune_macros(text: str) -> str:
    """The text without the definitions of new macros that nothing uses, directly or through another macro.
    2602.06198 defines 10,824 number macros and uses 1,128; the rest were 65% of what every model call carried.
    A number in a macro nothing uses is never printed, so grounding should not find it either."""
    spans: dict[str, list[tuple[int, int]]] = {}
    for match in _DEFINITION.finditer(text):
        end = _group_end(text, match.end())
        if end is not None:
            spans.setdefault(match.group(1) or match.group(2), []).append((match.start(), end))
    if not spans:
        return text
    defined = sorted((s for found in spans.values() for s in found), key=lambda s: s[0])
    outside, last = [], 0
    for start, end in defined:
        outside.append(text[last:start])
        last = max(last, end)
    outside.append(text[last:])
    used = set(_NAME.findall("".join(outside))) & set(spans)
    todo = list(used)
    while todo:
        for start, end in spans[todo.pop()]:
            for name in set(_NAME.findall(text[start:end])) & set(spans):
                if name not in used:
                    used.add(name)
                    todo.append(name)
    drop = sorted((s for name, found in spans.items() if name not in used for s in found), key=lambda s: s[0])
    kept, last = [], 0
    for start, end in drop:
        kept.append(text[last:start])
        last = end
    kept.append(text[last:])
    return "".join(kept)


def flatten(files: dict[str, str]) -> str:
    """The main file (the one with \\begin{document}) with its includes inlined, comments removed."""
    mains = [name for name, text in files.items() if "\\begin{document}" in text]
    if not mains:
        raise ValueError("no .tex file with \\begin{document} in the source")
    stripped = {name: strip_comments(text) for name, text in files.items()}

    def resolve(name: str, depth: int) -> str:
        if depth > MAX_INCLUDE_DEPTH:
            raise ValueError(f"includes nested deeper than {MAX_INCLUDE_DEPTH} at {name}")
        folder = str(Path(name).parent)

        def inline(match: re.Match) -> str:
            target = match.group(1).strip()
            target = target if target.endswith(".tex") else f"{target}.tex"
            for candidate in (target, str(Path(folder) / target)):
                key = str(Path(candidate))
                if key in stripped:
                    return resolve(key, depth + 1)
            return match.group(0)

        return _INCLUDE.sub(inline, stripped[name])

    return resolve(max(mains, key=lambda n: len(files[n])), 0)


def load_paper(arxiv_id: str, cache_dir: Path) -> str:
    return prune_macros(flatten(tex_files(fetch_source(arxiv_id, cache_dir))))
