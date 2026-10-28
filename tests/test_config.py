import pytest

from paper_replicator import config


def test_every_tier_defaults_to_meta(monkeypatch):
    for name in config.DEFAULT_TIERS:
        monkeypatch.delenv(f"{name.upper()}_PROVIDER", raising=False)
        monkeypatch.delenv(f"{name.upper()}_MODEL", raising=False)
        cfg = config.tier(name)
        assert cfg.provider.name == "meta"
        assert cfg.provider.base_url == "https://api.meta.ai/v1"
        assert cfg.model.startswith("muse-")


def test_env_overrides_a_tier_for_dev(monkeypatch):
    monkeypatch.setenv("QUICK_PROVIDER", "deepseek")
    monkeypatch.setenv("QUICK_MODEL", "deepseek-chat")
    cfg = config.tier("quick")
    assert (cfg.provider.name, cfg.model) == ("deepseek", "deepseek-chat")


def test_unknown_provider_fails_loudly(monkeypatch):
    monkeypatch.setenv("QUICK_PROVIDER", "nobody")
    with pytest.raises(ValueError, match="nobody"):
        config.tier("quick")


def test_providers_without_json_schema_get_json_object_and_the_schema_in_the_prompt(monkeypatch):
    from paper_replicator import roles
    from paper_replicator.llm import make_client
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.setenv("MODEL_API_KEY", "test")
    deepseek = config.ModelConfig(config.PROVIDERS["deepseek"], "deepseek-flash")
    agent = roles.extractor(deepseek, make_client(deepseek))
    assert agent.model_settings.extra_args == {"response_format": {"type": "json_object"}}
    assert agent.model_settings.reasoning is None
    assert '"headline"' in agent.instructions and "JSON schema" in agent.instructions
    meta = config.tier("quick")
    agent = roles.extractor(meta, make_client(meta), "minimal")
    assert agent.model_settings.extra_args is None and agent.model_settings.reasoning.effort == "minimal"
    assert "JSON schema" not in agent.instructions
