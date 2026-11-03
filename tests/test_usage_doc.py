"""docs/USAGE.md and the README name only commands and flags that exist: every `celsus <command>` is a real
subcommand, every --flag on a command line belongs to that command's parser, every other --flag to one of the
parsers, and every option of `celsus check` is in the usage doc."""

import argparse
import re
from pathlib import Path

from paper_replicator import batch, sabotage
from paper_replicator.cli.__main__ import arguments, check_arguments

ROOT = Path(__file__).parents[1]
USAGE, README = ROOT / "docs" / "USAGE.md", ROOT / "README.md"
FLAG = re.compile(r"(?<![\w-])--[a-z][a-z-]*")
COMMAND = re.compile(r"\buv run celsus ([a-z]+)|`celsus ([a-z]+)")


def options(parser: argparse.ArgumentParser) -> set[str]:
    return {s for action in parser._actions for s in action.option_strings if s.startswith("--")}


def subcommands() -> dict[str, argparse.ArgumentParser]:
    found = next(a for a in arguments()._actions if isinstance(a, argparse._SubParsersAction))
    return dict(found.choices)


def parsers() -> dict[str, argparse.ArgumentParser]:
    """Each command as a doc types it, with the parser that reads its flags."""
    named = {f"celsus {name}": parser for name, parser in subcommands().items()}
    named["celsus check"] = check_arguments()
    return {**named, "paper_replicator.batch": batch.arguments(), "paper_replicator.sabotage": sabotage.arguments()}


def command_lines(text: str) -> list[str]:
    """The lines of the bash blocks, continuations joined and comments dropped."""
    blocks = "\n".join(re.findall(r"```bash\n(.*?)```", text, re.S)).replace("\\\n", " ")
    return [line.split(" #")[0].strip() for line in blocks.splitlines() if line.strip()]


def test_every_celsus_command_named_is_a_subcommand():
    for doc in (USAGE, README):
        named = {a or b for a, b in COMMAND.findall(doc.read_text())}
        assert named and named <= set(subcommands()), (doc.name, named - set(subcommands()))


def test_every_flag_on_a_command_line_is_that_commands_own():
    known = parsers()
    for doc in (USAGE, README):
        for line in command_lines(doc.read_text()):
            command = next((name for name in known if name in line), None)
            if command is not None:
                assert set(FLAG.findall(line)) <= options(known[command]), (doc.name, line)


def test_every_flag_the_usage_doc_names_exists():
    every = set().union(*(options(parser) for parser in parsers().values()))
    assert set(FLAG.findall(USAGE.read_text())) <= every


def test_the_usage_doc_names_every_option_of_check():
    shown = set(FLAG.findall(USAGE.read_text()))
    assert options(check_arguments()) - {"--help"} <= shown
