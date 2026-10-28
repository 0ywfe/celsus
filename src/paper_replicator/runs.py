"""Run folders: runs/<run-id>/ under the repo root, one per run."""

from __future__ import annotations

import datetime
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT / "runs"


def new_run(runs_dir: Path = RUNS_DIR) -> tuple[str, Path]:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"run-{stamp}-{uuid.uuid4().hex[:6]}"
    folder = runs_dir / run_id
    folder.mkdir(parents=True)
    return run_id, folder
