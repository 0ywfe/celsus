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
