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
    return flatten(tex_files(fetch_source(arxiv_id, cache_dir)))
