import json

from paper_replicator import batch


def fake_run(root, run_id, verdict, reproduced, cost, crashed=None, name="small"):
    folder = root / run_id
    folder.mkdir(parents=True)
    headline = {"name": name, "reported": -7.49, "reproduced": reproduced, "consistent": reproduced is not None
                and abs(reproduced + 7.49) < 3, "kind": "estimate", "unit": "%"}
    (folder / "summary.json").write_text(json.dumps({
        "run_id": run_id, "paper": "0000.00000", "model": "m", "effort": "minimal", "builder": "workbench",
        "verdict": verdict, "headline": headline, "sample": [{"name": "n", "reported": 54, "reproduced": 50,
                                                               "consistent": True}],
        "rejections": [{"round": 1, "reason": "x"}], "rounds": 2, "cost_usd": cost, "wall_s": 300.0,
        "crashed": crashed}))


def test_reliability_numbers_from_run_summaries(tmp_path, monkeypatch):
    monkeypatch.setattr(batch, "RUNS_DIR", tmp_path)
    fake_run(tmp_path, "r1", "partly holds up", -6.5, 1.0)
    fake_run(tmp_path, "r2", "partly holds up", -3.9, 1.2, name="size_small_mean")   # names vary across runs
    fake_run(tmp_path, "r3", "could not check", None, 0.4, crashed="KeyError: x")
    [group] = batch.summarise(["r1", "r2", "r3"])["groups"]
    assert group["n"] == 3 and group["agreement"] == round(2 / 3, 3) and group["modal_verdict"] == "partly holds up"
    assert group["headline_reproduced"]["min"] == -6.5 and group["headline_reproduced"]["max"] == -3.9
    assert group["headline_consistent"] == 1 and group["crashed"] == 1 and group["rejections"] == 3
    assert "| 0000.00000 | m | minimal | 3 |" in batch.markdown({"groups": [group]})



def test_each_run_of_each_paper_logs_to_its_own_file():
    from paper_replicator.batch import log_path
    paths = {log_path("x", paper, i) for paper in ("2604.27287", "2512.12815") for i in range(2)}
    assert len(paths) == 4



def test_models_are_summed_across_papers():
    from paper_replicator.batch import by_model
    groups = [{"model": "m", "effort": "minimal", "n": 2, "verdicts": {"holds up": 2}, "agreement": 1.0,
               "cost_usd": {"mean": 0.2}, "crashed": 0},
              {"model": "m", "effort": "minimal", "n": 2, "verdicts": {"holds up": 1, "could not check": 1},
               "agreement": 0.5, "cost_usd": {"mean": 0.4}, "crashed": 1}]
    [m] = by_model(groups)
    assert m["papers"] == 2 and m["runs"] == 4 and m["could_not_check"] == 0.25
    assert m["papers_all_runs_agree"] == "1/2" and m["cost_usd_mean"] == 0.3 and m["crashed"] == 1
