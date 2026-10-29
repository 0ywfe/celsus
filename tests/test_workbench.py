"""The workbench outlives its sandbox: held-out 2512.12924 lost round 3 when the sandbox's lifetime ran out
mid-run (`NotFoundError: The Sandbox is unavailable`)."""

import modal.exception

from paper_replicator import sandbox as sandbox_module
from paper_replicator.sandbox import WORK, Workbench


class FakeProcess:
    def __init__(self, out):
        self.returncode, self.stdout, self.stderr = 0, type("S", (), {"read": lambda _: out})(), \
            type("S", (), {"read": lambda _: ""})()

    def wait(self):
        pass


class FakeSandbox:
    """Call 1 is always the workbench's `pip freeze` of the image, made when it opens."""

    def __init__(self, dies_after: int | None = None, freeze: str = "pandas==2.2.3\nnumpy==2.1.0\n"):
        self.files, self.calls, self.dies_after, self.freeze = {}, 0, dies_after, freeze
        outer = self

        class FS:
            def write_text(self, content, path):
                outer._touch()
                outer.files[path] = content

            def read_text(self, path):
                outer._touch()
                if path not in outer.files:
                    raise modal.exception.SandboxFilesystemNotFoundError("no file")
                return outer.files[path]

            def make_directory(self, path):
                pass

        self.filesystem = FS()

    def _touch(self):
        self.calls += 1
        if self.dies_after is not None and self.calls > self.dies_after:
            raise modal.exception.NotFoundError("The Sandbox is unavailable. This Sandbox may have already shut down.")

    def exec(self, *args, **kwargs):
        self._touch()
        return FakeProcess(self.freeze if args[1:4] == ("-m", "pip", "freeze") else "ran")

    def terminate(self):
        self._touch()


def bench(monkeypatch, boxes):
    opened = iter(boxes)
    monkeypatch.setattr(sandbox_module, "_start", lambda **kw: next(opened))
    return Workbench(market_cache=None, env={}, command_timeout_s=60, lifetime_s=60)


def test_a_dead_sandbox_is_reopened_with_the_builders_files(monkeypatch):
    first, second = FakeSandbox(dies_after=3), FakeSandbox()
    wb = bench(monkeypatch, [first, second])
    wb.write_file("replicate.py", "print(1)")          # call 2
    assert wb.run("ls")[1] == "ran"                     # call 3
    code, out = wb.run("python replicate.py")           # call 4: the sandbox is gone
    assert code == 0 and out.endswith("ran") and "restarted" in out
    assert second.files[f"{WORK}/replicate.py"] == "print(1)"
    assert wb.read_text(f"{WORK}/replicate.py") == "print(1)"
    assert wb.restarts == 1


def test_a_read_after_the_sandbox_died_still_finds_what_the_builder_wrote(monkeypatch):
    first, second = FakeSandbox(dies_after=2), FakeSandbox()
    wb = bench(monkeypatch, [first, second])
    wb.write_file(f"{WORK}/replicate.py", "print(2)")
    assert wb.read_text(f"{WORK}/replicate.py") == "print(2)"
    wb.close()


def test_closing_a_dead_sandbox_is_not_an_error(monkeypatch):
    wb = bench(monkeypatch, [FakeSandbox(dies_after=1)])
    wb.close()


def test_the_clean_run_gets_what_the_builder_installed_and_nothing_it_cannot_install(monkeypatch):
    # set 2's first runs: workbenches pip-installed xlrd, ripser, cvxpy and scikit-learn, and the clean re-runs died
    # on ModuleNotFoundError because a fresh sandbox has only the image
    box = FakeSandbox()
    wb = bench(monkeypatch, [box])
    box.freeze += "xlrd==2.0.1\nnumpy==2.2.0\nauthors-pkg @ file:///work/pkg\n"
    assert wb.installed() == (["numpy==2.2.0", "xlrd==2.0.1"], ["authors-pkg @ file:///work/pkg"])


def test_nothing_installed_means_the_plain_image(monkeypatch):
    wb = bench(monkeypatch, [FakeSandbox()])
    assert wb.installed() == ([], [])
