"""Modal sandboxes: a fresh container with network on and nothing from this machine except the script,
the market-data helper, the market-data cache and, in the clean run, the record of hosts it fetched from.

- run_script: the clean run. A fresh sandbox runs one script; only its outputs count as results.
- Workbench: a persistent sandbox the builder explores in through its tools.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

import modal
from modal.exception import (NotFoundError, SandboxFilesystemNotFoundError, SandboxTerminatedError,
                             SandboxTimeoutError)

from . import PRODUCT_NAME

PACKAGES = ["pandas", "numpy", "scipy", "statsmodels", "requests", "yfinance", "pyarrow"]
WORK, CACHE = "/work", "/data/market"
OUTPUTS = ("results.json", "market_data_log.json", "market_data_requests.json", "data_sources.json")
HELPER = Path(__file__).parent / "sandbox_lib" / "market_data.py"
SOURCES, HOOKS = Path(__file__).parent / "sandbox_lib" / "data_sources.py", "/opt/hooks"
MAX_TOOL_OUTPUT = 6000  # chars of a command's output the builder sees (Meta cookbook 07's value)


@dataclass
class SandboxRun:
    exit_code: int | None
    stdout: str
    stderr: str
    seconds: float
    files: dict[str, str] = field(default_factory=dict)


def image() -> modal.Image:
    return modal.Image.debian_slim(python_version="3.12").pip_install(*PACKAGES)


def _start(*, market_cache: Path, env: dict[str, str], lifetime_s: int) -> modal.Sandbox:
    app = modal.App.lookup(f"{PRODUCT_NAME}-sandbox", create_if_missing=True)
    sandbox = modal.Sandbox.create(app=app, image=image(), timeout=lifetime_s, workdir=WORK,
                                   secrets=[modal.Secret.from_dict(env)])
    fs = sandbox.filesystem
    fs.make_directory(f"{CACHE}/prices")
    fs.write_text(HELPER.read_text(), f"{WORK}/market_data.py")
    for path in (p for p in market_cache.rglob("*") if p.is_file() and not p.name.startswith(".")):
        fs.copy_from_local(path, f"{CACHE}/{path.relative_to(market_cache)}")
    return sandbox


def _read(sandbox: modal.Sandbox, path: str) -> str | None:
    try:
        return sandbox.filesystem.read_text(path)
    except SandboxFilesystemNotFoundError:
        return None


def run_script(script: str, *, market_cache: Path, env: dict[str, str], timeout_s: int) -> SandboxRun:
    started = time.monotonic()
    sandbox = _start(market_cache=market_cache, env=env, lifetime_s=timeout_s + 120)
    try:
        sandbox.filesystem.write_text(script, f"{WORK}/replicate.py")
        sandbox.filesystem.make_directory(HOOKS)
        sandbox.filesystem.write_text(SOURCES.read_text(), f"{HOOKS}/sitecustomize.py")
        process = sandbox.exec("python", f"{WORK}/replicate.py", timeout=timeout_s, workdir=WORK,
                               env={"PYTHONPATH": HOOKS, "WORK_DIR": WORK})
        process.wait()
        run = SandboxRun(process.returncode, process.stdout.read(), process.stderr.read(), 0.0)
        run.files = {name: text for name in OUTPUTS if (text := _read(sandbox, f"{WORK}/{name}")) is not None}
    finally:
        sandbox.terminate()
    run.seconds = round(time.monotonic() - started, 1)
    return run


# A sandbox past its lifetime answers with one of these.
GONE = (NotFoundError, SandboxTerminatedError, SandboxTimeoutError)
RESTARTED = ("(the sandbox had shut down and was restarted: files written with write_file are back; anything else, "
             "such as downloads or files written by commands, has to be made again)\n")


class Workbench:
    """A persistent sandbox for the builder: shell commands and file writes, nothing else. A sandbox that shuts down
    mid-run (its lifetime ran out) is reopened and every file the builder wrote is written back."""

    def __init__(self, *, market_cache: Path, env: dict[str, str], command_timeout_s: int, lifetime_s: int):
        self.command_timeout_s = command_timeout_s
        self._open = lambda: _start(market_cache=market_cache, env=env, lifetime_s=lifetime_s)
        self.sandbox = self._open()
        self.written: dict[str, str] = {}
        self.restarts = 0

    def _alive(self, action):
        """(action's result, whether the sandbox had to be reopened first)."""
        try:
            return action(self.sandbox), False
        except GONE:
            self.restarts += 1
            self.sandbox = self._open()
            for target, content in self.written.items():
                _write(self.sandbox, target, content)
            return action(self.sandbox), True

    def run(self, cmd: str) -> tuple[int | None, str]:
        """`pipefail`, so a failing command piped into tail still reports its real exit code."""
        def go(sandbox: modal.Sandbox) -> tuple[int | None, str]:
            process = sandbox.exec("bash", "-lc", f"set -o pipefail; {cmd}", timeout=self.command_timeout_s,
                                   workdir=WORK)
            process.wait()
            return process.returncode, process.stdout.read() + process.stderr.read()

        (code, output), restarted = self._alive(go)
        tail = output if len(output) <= MAX_TOOL_OUTPUT else "...(truncated)...\n" + output[-MAX_TOOL_OUTPUT:]
        return code, (RESTARTED if restarted else "") + tail

    def write_file(self, path: str, content: str) -> None:
        target = path if path.startswith("/") else f"{WORK}/{path}"
        self.written[target] = content
        self._alive(lambda sandbox: _write(sandbox, target, content))

    def read_text(self, path: str) -> str | None:
        text, _ = self._alive(lambda sandbox: _read(sandbox, path))
        return text if text is not None else self.written.get(path)

    def close(self) -> None:
        try:
            self.sandbox.terminate()
        except GONE:
            pass


def _write(sandbox: modal.Sandbox, target: str, content: str) -> None:
    sandbox.filesystem.make_directory(str(Path(target).parent))
    sandbox.filesystem.write_text(content, target)
