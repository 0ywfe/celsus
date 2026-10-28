"""Run a generated script in a Modal Sandbox: a fresh container, network on, nothing from this machine
except the script, the market-data helper and the market-data cache."""

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


@dataclass
class SandboxRun:
    exit_code: int | None
    stdout: str
    stderr: str
    seconds: float
    files: dict[str, str] = field(default_factory=dict)


def image() -> modal.Image:
    return modal.Image.debian_slim(python_version="3.12").pip_install(*PACKAGES)


def run_script(script: str, *, market_cache: Path, env: dict[str, str], timeout_s: int) -> SandboxRun:
    app = modal.App.lookup(f"{PRODUCT_NAME}-sandbox", create_if_missing=True)
    started = time.monotonic()
    sandbox = modal.Sandbox.create(
        app=app,
        image=image(),
        timeout=timeout_s + 120,
        workdir=WORK,
        secrets=[modal.Secret.from_dict(env)],
    )
    try:
        fs = sandbox.filesystem
        fs.make_directory(f"{CACHE}/prices")
        fs.write_text(script, f"{WORK}/replicate.py")
        fs.write_text(HELPER.read_text(), f"{WORK}/market_data.py")
        for path in (p for p in market_cache.rglob("*") if p.is_file()):
            fs.copy_from_local(path, f"{CACHE}/{path.relative_to(market_cache)}")
        process = sandbox.exec("python", f"{WORK}/replicate.py", timeout=timeout_s, workdir=WORK)
        process.wait()
        run = SandboxRun(process.returncode, process.stdout.read(), process.stderr.read(), 0.0)
        for name in OUTPUTS:
            try:
                run.files[name] = fs.read_text(f"{WORK}/{name}")
            except SandboxFilesystemNotFoundError:
                pass
    finally:
        sandbox.terminate()
    run.seconds = round(time.monotonic() - started, 1)
    return run
