"""Modal sandboxes: a fresh container with network on and nothing from this machine except the script,
the market-data helper and the market-data cache.

- run_script: the clean run. A fresh sandbox runs one script; only its outputs count as results.
- Workbench: a persistent sandbox the builder explores in through its tools.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

import modal
from modal.exception import SandboxFilesystemNotFoundError

from . import PRODUCT_NAME

PACKAGES = ["pandas", "numpy", "scipy", "statsmodels", "requests", "yfinance", "pyarrow"]
WORK, CACHE = "/work", "/data/market"
OUTPUTS = ("results.json", "market_data_log.json", "market_data_requests.json")
HELPER = Path(__file__).parent / "sandbox_lib" / "market_data.py"
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
        process = sandbox.exec("python", f"{WORK}/replicate.py", timeout=timeout_s, workdir=WORK)
        process.wait()
        run = SandboxRun(process.returncode, process.stdout.read(), process.stderr.read(), 0.0)
        run.files = {name: text for name in OUTPUTS if (text := _read(sandbox, f"{WORK}/{name}")) is not None}
    finally:
        sandbox.terminate()
    run.seconds = round(time.monotonic() - started, 1)
    return run


class Workbench:
    """A persistent sandbox for the builder: shell commands and file writes, nothing else."""

    def __init__(self, *, market_cache: Path, env: dict[str, str], command_timeout_s: int, lifetime_s: int):
        self.command_timeout_s = command_timeout_s
        self.sandbox = _start(market_cache=market_cache, env=env, lifetime_s=lifetime_s)

    def run(self, cmd: str) -> tuple[int | None, str]:
        """`pipefail`, so a failing command piped into tail still reports its real exit code."""
        process = self.sandbox.exec("bash", "-lc", f"set -o pipefail; {cmd}",
                                    timeout=self.command_timeout_s, workdir=WORK)
        process.wait()
        output = process.stdout.read() + process.stderr.read()
        tail = output if len(output) <= MAX_TOOL_OUTPUT else "...(truncated)...\n" + output[-MAX_TOOL_OUTPUT:]
        return process.returncode, tail

    def write_file(self, path: str, content: str) -> None:
        target = path if path.startswith("/") else f"{WORK}/{path}"
        self.sandbox.filesystem.make_directory(str(Path(target).parent))
        self.sandbox.filesystem.write_text(content, target)

    def read_text(self, path: str) -> str | None:
        return _read(self.sandbox, path)

    def close(self) -> None:
        self.sandbox.terminate()
