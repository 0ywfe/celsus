"""The builder's two tools over a Workbench, as Agents SDK function tools. Every call is logged
to the run's event stream, so a frontend can show each command live."""

from __future__ import annotations

import asyncio
from typing import Callable

from agents import function_tool

from .guards import fetches_code, redact
from .sandbox import Workbench


def make_tools(bench: Workbench, say: Callable[..., None], secrets: dict[str, str], turns: int) -> list:
    """Every result carries the turn count, so the builder can pace itself within a round."""
    used = {"calls": 0}

    def footer() -> str:
        used["calls"] += 1
        return f"\n[tool call {used['calls']}; a round allows {turns} turns]"

    @function_tool
    async def run(cmd: str) -> str:
        """Run a bash command in the sandbox, working directory /work. Returns the exit code and the
        end of the combined stdout and stderr."""
        if (fetched := fetches_code(cmd)) is not None:
            refusal = (f"refused: {fetched}. Build the analysis from the paper: fetch data files only, never the "
                       "authors' code or a repository.")
            say("guard", refusal.split(". ")[0], tool="run")
            return refusal + footer()
        say("tool", f"$ {redact(cmd[:200], secrets)}", tool="run")
        code, output = await asyncio.to_thread(bench.run, cmd)
        say("tool", f"exit {code}", tool="run", exit=code)
        return redact(f"exit_code: {code}\n{output}", secrets) + footer()

    @function_tool
    async def write_file(path: str, content: str) -> str:
        """Create or overwrite a file in the sandbox (relative paths are under /work). Send the whole file."""
        say("tool", f"write {path} ({len(content)} chars)", tool="write_file")
        await asyncio.to_thread(bench.write_file, path, content)
        return f"wrote {path}" + footer()

    return [run, write_file]
