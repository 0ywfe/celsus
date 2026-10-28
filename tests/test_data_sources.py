"""The clean run's record of every host the script fetched from, run locally with no network."""

import json
import subprocess
import sys
from pathlib import Path

from paper_replicator.sandbox_lib import data_sources

# The audit event fires before the lookup, so raising it by hand is the same as a fetch, with no network.
SCRIPT = """
import sys
for host in ("efts.sec.gov", "data-api.binance.vision", "efts.sec.gov", b"fred.stlouisfed.org"):
    sys.audit("socket.getaddrinfo", host, 443, 0, 0, 0)
"""


def run(tmp_path, script):
    hooks, work = tmp_path / "hooks", tmp_path / "work"
    hooks.mkdir()
    work.mkdir()
    (hooks / "sitecustomize.py").write_text(Path(data_sources.__file__).read_text())
    (work / "replicate.py").write_text(script)
    done = subprocess.run([sys.executable, str(work / "replicate.py")], capture_output=True, text=True, cwd=work,
                          env={"PYTHONPATH": str(hooks), "WORK_DIR": str(work)})
    return done, work


def test_each_host_the_script_looks_up_is_recorded_once_in_order(tmp_path):
    done, work = run(tmp_path, SCRIPT)
    assert done.returncode == 0, done.stderr
    assert json.loads((work / "data_sources.json").read_text()) == [
        "efts.sec.gov", "data-api.binance.vision", "fred.stlouisfed.org"]


def test_the_record_survives_a_script_that_dies_after_fetching(tmp_path):
    done, work = run(tmp_path, SCRIPT + "raise SystemExit(3)\n")
    assert done.returncode == 3
    assert len(json.loads((work / "data_sources.json").read_text())) == 3


def test_a_script_that_fetches_nothing_leaves_no_record(tmp_path):
    done, work = run(tmp_path, "print('offline')\n")
    assert done.returncode == 0 and not (work / "data_sources.json").exists()


def test_hosts_looked_up_from_threads_and_child_processes_are_all_recorded(tmp_path):
    done, work = run(tmp_path, """
import multiprocessing, sys
from concurrent.futures import ThreadPoolExecutor
def look(i):
    sys.audit("socket.getaddrinfo", f"h{i}.example", 443, 0, 0, 0)
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(look, range(200)))
    with multiprocessing.get_context("fork").Pool(4) as pool:
        pool.map(look, range(200, 240))
""")
    assert done.returncode == 0, done.stderr
    assert sorted(json.loads((work / "data_sources.json").read_text())) == sorted(f"h{i}.example" for i in range(240))
