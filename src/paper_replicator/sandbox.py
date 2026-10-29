"""Modal sandboxes: a fresh container with network on and nothing from this machine except the script,
the market-data helper, the market-data cache, the start-up hooks and, in the clean run, the record of hosts it
fetched from.

- run_script: the clean run. A fresh sandbox runs one script; only its outputs count as results. It has the
  packages the builder installed in the workbench, at the same versions.
- Workbench: a persistent sandbox the builder explores in through its tools.
- Every Python process loads the hooks: the SEC contact goes only to sec.gov (sandbox_lib/sec_contact.py), and in
  the clean run the hosts fetched from are recorded (sandbox_lib/data_sources.py).
"""

from __future__ import annotations

import re
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
CONTACT = Path(__file__).parent / "sandbox_lib" / "sec_contact.py"
# The sandbox's environment holds this in place of the contact; the hook swaps it for the contact on sec.gov only.
STAND_IN = "contact-added-by-the-sandbox-for-sec.gov-only"
LOADER = "import sec_contact\nimport os\nif os.environ.get('WORK_DIR'):\n    import data_sources\n"
# pip's own form for repeatable installs: `pip freeze` in one environment, the same lines installed in the next.
# A line that is not a released package at a version (a package from a URL or a local path) cannot be.
PINNED = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*==[^\s;@+]+$")   # a local version (+cpu) is not on PyPI
MAX_TOOL_OUTPUT = 6000  # chars of a command's output the builder sees (Meta cookbook 07's value)


@dataclass
class SandboxRun:
    exit_code: int | None
    stdout: str
    stderr: str
    seconds: float
    files: dict[str, str] = field(default_factory=dict)


def image(packages: tuple[str, ...] = ()) -> modal.Image:
    """The sandbox image, plus the packages the builder installed in the workbench, at their versions."""
    base = modal.Image.debian_slim(python_version="3.12").pip_install(*PACKAGES)
    return base.pip_install(*packages) if packages else base


def _start(*, market_cache: Path, env: dict[str, str], lifetime_s: int,
           packages: tuple[str, ...] = ()) -> modal.Sandbox:
    """The contact is written to a file only the hook reads; the environment carries the stand-in."""
    app = modal.App.lookup(f"{PRODUCT_NAME}-sandbox", create_if_missing=True)
    sandbox = modal.Sandbox.create(app=app, image=image(packages), timeout=lifetime_s, workdir=WORK,
                                   env={**env, "SEC_USER_AGENT": STAND_IN, "PYTHONPATH": HOOKS})
    fs = sandbox.filesystem
    fs.make_directory(f"{CACHE}/prices")
    fs.make_directory(HOOKS)
    fs.write_text(env.get("SEC_USER_AGENT", ""), f"{HOOKS}/sec_contact")
    for hook in (CONTACT, SOURCES):
        fs.write_text(hook.read_text(), f"{HOOKS}/{hook.name}")
    fs.write_text(LOADER, f"{HOOKS}/sitecustomize.py")
    fs.write_text(HELPER.read_text(), f"{WORK}/market_data.py")
    for path in (p for p in market_cache.rglob("*") if p.is_file() and not p.name.startswith(".")):
        fs.copy_from_local(path, f"{CACHE}/{path.relative_to(market_cache)}")
    return sandbox


def _read(sandbox: modal.Sandbox, path: str) -> str | None:
    try:
        return sandbox.filesystem.read_text(path)
    except SandboxFilesystemNotFoundError:
        return None


def run_script(script: str, *, market_cache: Path, env: dict[str, str], timeout_s: int,
               packages: tuple[str, ...] = ()) -> SandboxRun:
    """If the builder's packages cannot be installed, the script runs without them and its output says why, so the
    builder hears it instead of the round being lost."""
    started, note = time.monotonic(), ""
    try:
        sandbox = _start(market_cache=market_cache, env=env, lifetime_s=timeout_s + 120, packages=packages)
    except Exception as error:
        if not packages:
            raise
        note = (f"the packages you installed could not be installed in the clean run ({', '.join(packages)}: "
                f"{type(error).__name__}: {str(error)[:300]}); it ran without them\n")
        sandbox = _start(market_cache=market_cache, env=env, lifetime_s=timeout_s + 120)
    try:
        sandbox.filesystem.write_text(script, f"{WORK}/replicate.py")
        process = sandbox.exec("python", f"{WORK}/replicate.py", timeout=timeout_s, workdir=WORK,
                               env={"PYTHONPATH": HOOKS, "WORK_DIR": WORK})
        process.wait()
        run = SandboxRun(process.returncode, process.stdout.read(), note + process.stderr.read(), 0.0)
        run.files = {name: text for name in OUTPUTS if (text := _read(sandbox, f"{WORK}/{name}")) is not None}
    finally:
        sandbox.terminate()
    run.seconds = round(time.monotonic() - started, 1)
    return run


# A sandbox past its lifetime answers with one of these.
GONE = (NotFoundError, SandboxTerminatedError, SandboxTimeoutError)
RESTARTED = ("(the sandbox had shut down and was restarted: files written with write_file and packages installed "
             "with pip are back; anything else, such as downloads or files written by commands, has to be made "
             "again)\n")


class Workbench:
    """A persistent sandbox for the builder: shell commands and file writes, nothing else. A sandbox that shuts down
    mid-run (its lifetime ran out) is reopened, every file the builder wrote is written back and every package it
    installed is installed again."""

    def __init__(self, *, market_cache: Path, env: dict[str, str], command_timeout_s: int, lifetime_s: int):
        self.command_timeout_s = command_timeout_s
        self._open = lambda: _start(market_cache=market_cache, env=env, lifetime_s=lifetime_s)
        self.sandbox = self._open()
        self.written: dict[str, str] = {}
        self.restarts = 0
        self.base = _freeze(self.sandbox)  # what the image has, before the builder installs anything
        self.added: list[str] = []          # what the builder installed, as last seen

    def _alive(self, action):
        """(action's result, whether the sandbox had to be reopened first)."""
        try:
            return action(self.sandbox), False
        except GONE:
            self.restarts += 1
            self.sandbox = self._open()
            for target, content in self.written.items():
                _write(self.sandbox, target, content)
            if pinned := [p for p in self.added if PINNED.match(p)]:
                _pip(self.sandbox, pinned)
            return action(self.sandbox), True

    def run(self, cmd: str) -> tuple[int | None, str]:
        """`pipefail`, so a failing command piped into tail still reports its real exit code."""
        def go(sandbox: modal.Sandbox) -> tuple[int | None, str]:
            process = sandbox.exec("bash", "-lc", f"set -o pipefail; {cmd}", timeout=self.command_timeout_s,
                                   workdir=WORK)
            process.wait()
            result = process.returncode, process.stdout.read() + process.stderr.read()
            if "pip" in cmd:   # kept up to date, so a restart can install them again
                self.added = sorted(_freeze(sandbox) - self.base)
            return result

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

    def installed(self) -> tuple[list[str], list[str]]:
        """What the builder added to the image, in pip's freeze form: (released packages at their versions, which
        the clean run installs; anything else, which it cannot)."""
        self.added, _ = self._alive(lambda sandbox: sorted(_freeze(sandbox) - self.base))
        return [p for p in self.added if PINNED.match(p)], [p for p in self.added if not PINNED.match(p)]

    def close(self) -> None:
        try:
            self.sandbox.terminate()
        except GONE:
            pass


def _freeze(sandbox: modal.Sandbox) -> set[str]:
    process = sandbox.exec("python", "-m", "pip", "freeze", timeout=120, workdir=WORK)
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"pip freeze failed in the sandbox (exit {process.returncode})")
    return {line.strip() for line in process.stdout.read().splitlines() if line.strip() and not line.startswith("#")}


def _pip(sandbox: modal.Sandbox, packages: list[str]) -> None:
    sandbox.exec("python", "-m", "pip", "install", "-q", *packages, timeout=600, workdir=WORK).wait()


def _write(sandbox: modal.Sandbox, target: str, content: str) -> None:
    sandbox.filesystem.make_directory(str(Path(target).parent))
    sandbox.filesystem.write_text(content, target)
