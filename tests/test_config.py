import json

import pytest

from paper_replicator import config, pricing

LOCAL = {"localdev": {"base_url": "http://localhost:8000/v1", "key_env": "LOCALDEV_API_KEY", "json_schema": False,
                      "reasoning_effort": False, "prices": {"local-model": [0.01, 0.1, 0.2]}}}


@pytest.fixture
def localdev(monkeypatch, tmp_path):
    """An endpoint added the way a checkout adds one: in its own providers.local.json."""
    path = tmp_path / "providers.local.json"
    path.write_text(json.dumps(LOCAL))
    monkeypatch.setattr(config, "PROVIDERS", config.providers(path))
    monkeypatch.setattr(pricing, "ALL_PRICES", {**pricing.local_prices(path), **pricing.PRICES})
    monkeypatch.setenv("LOCALDEV_API_KEY", "test")
    monkeypatch.setenv("MODEL_API_KEY", "test")
    return config.ModelConfig(config.PROVIDERS["localdev"], "local-model")


def test_every_tier_defaults_to_meta(monkeypatch):
    for name in config.DEFAULT_TIERS:
        monkeypatch.delenv(f"{name.upper()}_PROVIDER", raising=False)
        monkeypatch.delenv(f"{name.upper()}_MODEL", raising=False)
        cfg = config.tier(name)
        assert cfg.provider.name == "meta"
        assert cfg.provider.base_url == "https://api.meta.ai/v1"
        assert cfg.model.startswith("muse-")


def test_without_a_local_file_meta_baseten_and_fireworks_are_the_providers(tmp_path):
    assert list(config.providers(tmp_path / "absent.json")) == ["meta", "baseten", "fireworks"]
    assert pricing.local_prices(tmp_path / "absent.json") == {}


def test_a_meta_model_counts_as_meta_wherever_it_runs(localdev):
    open_weights = config.ModelConfig(config.PROVIDERS["baseten"], "meta-models/muse-spark-open-1026")
    assert config.maker(open_weights) == "meta" and config.maker(config.tier("quick")) == "meta"
    assert config.maker(localdev) == "localdev"
    assert config.maker(config.ModelConfig(config.PROVIDERS["baseten"], "another-org/another-model")) == "baseten"
    assert pricing.cost_usd("meta-models/muse-spark-open-1026", 1_000_000, 0, 1_000_000) == 1.25 + 4.25


def test_muse_spark_open_on_fireworks_is_a_meta_model_at_the_published_rates():
    fireworks = config.PROVIDERS["fireworks"]
    assert (fireworks.base_url, fireworks.key_env) == ("https://api.fireworks.ai/inference/v1", "FIREWORKS_API_KEY")
    assert fireworks.json_schema and fireworks.reasoning_effort
    hosted = config.ModelConfig(fireworks, "accounts/fireworks/models/muse-spark-open")
    assert config.maker(hosted) == "meta"
    assert pricing.cost_usd(hosted.model, 1_000_000, 1_000_000, 1_000_000) == 0.15 + 4.25


def test_env_overrides_a_tier(monkeypatch, localdev):
    monkeypatch.setenv("QUICK_PROVIDER", "localdev")
    monkeypatch.setenv("QUICK_MODEL", "local-model")
    cfg = config.tier("quick")
    assert (cfg.provider.name, cfg.provider.base_url, cfg.model) == ("localdev", "http://localhost:8000/v1",
                                                                     "local-model")
    assert pricing.cost_usd("local-model", 1_000_000, 0, 1_000_000) == pytest.approx(0.3)


def test_unknown_provider_fails_loudly(monkeypatch):
    monkeypatch.setenv("QUICK_PROVIDER", "nobody")
    with pytest.raises(ValueError, match="nobody"):
        config.tier("quick")


def test_providers_without_json_schema_get_json_object_and_the_schema_in_the_prompt(localdev):
    from paper_replicator import roles
    from paper_replicator.llm import make_client
    agent = roles.extractor(localdev, make_client(localdev))
    assert agent.model_settings.extra_body == {"response_format": {"type": "json_object"}}
    assert agent.model_settings.reasoning is None
    assert '"headline"' in agent.instructions and "JSON schema" in agent.instructions
    meta = config.tier("quick")
    agent = roles.extractor(meta, make_client(meta), "minimal")
    assert agent.model_settings.extra_body is None and agent.model_settings.reasoning.effort == "minimal"
    assert "JSON schema" not in agent.instructions


def test_a_json_object_provider_sends_json_object_on_the_wire(localdev):
    # The SDK also sets response_format, so passing ours as a keyword argument failed before any request
    # was sent. This checks the request body itself.
    import asyncio
    from agents import Runner
    from fake_api import FakeChatAPI, usage
    from paper_replicator import roles
    from paper_replicator.llm import make_client
    spec = {"title": "t", "hypothesis": "h", "data_sources": [], "sample": "s", "method": [], "claims": [],
            "headline": "", "partitions": [], "tests": []}
    api = FakeChatAPI([(json.dumps(spec), usage(10, 10))])
    agent = roles.extractor(localdev, make_client(localdev, max_retries=0, http_client=api.http_client()))
    out = asyncio.run(Runner.run(agent, "paper", max_turns=1)).final_output
    assert out.title == "t"
    body = api.requests[0]["body"]
    assert body["response_format"] == {"type": "json_object"} and "reasoning_effort" not in body
