"""The builder's two tools over a Workbench, as Agents SDK function tools. Every call is logged
to the run's event stream, so a frontend can show each command live."""

from __future__ import annotations

import asyncio
from typing import Callable

from agents import function_tool

from .guards import redact
from .sandbox import Workbench


def make_tools(bench: Workbench, say: Callable[..., None], secrets: dict[str, str]) -> list:
    @function_tool
    async def run(cmd: str) -> str:
        """Run a bash command in the sandbox, working directory /work. Returns the exit code and the
        end of the combined stdout and stderr."""
        say("tool", f"$ {redact(cmd[:200], secrets)}", tool="run")
        code, output = await asyncio.to_thread(bench.run, cmd)
        say("tool", f"exit {code}", tool="run", exit=code)
        return redact(f"exit_code: {code}\n{output}", secrets)

    @function_tool
    async def write_file(path: str, content: str) -> str:
        """Create or overwrite a file in the sandbox (relative paths are under /work). Send the whole file."""
        say("tool", f"write {path} ({len(content)} chars)", tool="write_file")
        await asyncio.to_thread(bench.write_file, path, content)
        return f"wrote {path}"

    return [run, write_file]
