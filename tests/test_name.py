import tomllib
from pathlib import Path

from paper_replicator import DISCLAIMER, PRODUCT_NAME

ROOT = Path(__file__).resolve().parents[1]


def test_product_name_matches_pyproject():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["name"] == PRODUCT_NAME


def test_readme_heading_is_product_name():
    first_line = (ROOT / "README.md").read_text().splitlines()[0]
    assert first_line == f'<h1 align="center"><img src="docs/logo.svg" alt="{PRODUCT_NAME}" width="340"></h1>'
    assert (ROOT / "docs/logo.svg").exists()


def test_readme_carries_disclaimer():
    assert DISCLAIMER in (ROOT / "README.md").read_text()
