from paper_replicator.pricing import cost_usd


def test_cost_prices_fresh_cached_and_output_tokens():
    # muse-spark-1.3: $0.15 cached / $1.25 input / $4.25 output per 1M tokens
    cost = cost_usd("muse-spark-1.3", input_tokens=1000, cached_tokens=400, output_tokens=200)
    assert cost == (600 * 1.25 + 400 * 0.15 + 200 * 4.25) / 1_000_000


def test_unpriced_model_has_no_cost():
    assert cost_usd("some-dev-model", input_tokens=10, cached_tokens=0, output_tokens=10) is None
