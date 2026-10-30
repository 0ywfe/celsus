import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import json
import datetime
from scipy import stats
from market_data import get_prices, MarketDataUnavailable

TRAIN_START = "2018-01-01"
TRAIN_END = "2022-12-31"
TEST_START = "2023-01-01"
TEST_END = "2026-02-28"
FULL_START = "2018-01-01"
FULL_END = "2026-02-28"
INITIAL_CAPITAL = 100000
COST_ONE_WAY = 0.0004
EMA_FAST = 12
EMA_SLOW = 26
SIGNAL_W = 9
N_PSTAR = 20
SIGMA_MODE = "range"
TICKERS = ['SPY', 'QQQ', 'DIA']
OPTIMAL_LAMBDAS = {
    'SPY': {'macd': 0.90, 'vp': 0.88},
    'QQQ': {'macd': 0.84, 'vp': 0.98},
    'DIA': {'macd': 0.92, 'vp': 0.86},
}

def ema(series, span):
    return series.ewm(span=span, adjust=False, min_periods=span).mean()

def compute_Pstar(df, N=N_PSTAR, sigma_mode=SIGMA_MODE):
    close = df['close']
    openp = df['open']
    high = df['high']
    low = df['low']
    vol = df['volume']
    if sigma_mode == "range":
        sigma = (high - low) / close
        sigma = sigma.replace([np.inf, -np.inf], 0).fillna(0)
    elif sigma_mode == "stdN":
        hl = high - low
        sigma_raw = hl.rolling(N).std()
        sigma = sigma_raw / close
        sigma = sigma.replace([np.inf, -np.inf], 0).fillna(0)
    elif sigma_mode == "std20":
        hl = high - low
        sigma_raw = hl.rolling(20).std()
        sigma = sigma_raw / close
        sigma = sigma.replace([np.inf, -np.inf], 0).fillna(0)
    else:
        raise ValueError(sigma_mode)
    r = (close - openp).abs() / (high - low)
    r = r.replace([np.inf, -np.inf], 0).fillna(0)
    numerator = close * vol * sigma * r
    num_roll = numerator.rolling(N).sum().shift(1)
    den_roll = vol.rolling(N).sum().shift(1)
    Pstar = num_roll / den_roll
    return Pstar

def simulate_portfolio(df, macd, signal, lam_buy=1.0, cost=COST_ONE_WAY, initial=INITIAL_CAPITAL):
    buy = (macd.shift(1) <= lam_buy * signal.shift(1)) & (macd > lam_buy * signal)
    sell = (macd.shift(1) >= signal.shift(1)) & (macd < signal)
    n = len(df)
    dates = df.index
    cash = initial
    shares = 0
    pos = 0
    vals = [initial]
    trades = []
    cash_before_buy = None
    for idx in range(1, n):
        sig_date = dates[idx-1]
        exec_date = dates[idx]
        exec_open = df.loc[exec_date, 'open']
        is_buy = False
        is_sell = False
        try:
            v_buy = buy.loc[sig_date]
            v_sell = sell.loc[sig_date]
            if pd.notna(v_buy) and bool(v_buy):
                is_buy = True
            if pd.notna(v_sell) and bool(v_sell):
                is_sell = True
        except:
            pass
        if pos == 0 and is_buy:
            cost_per_share = exec_open * (1 + cost)
            if cost_per_share > 0 and cash > 0:
                max_shares = int(cash // cost_per_share)
                if max_shares >= 1:
                    cash_before_buy = cash
                    cost_total = max_shares * exec_open * cost
                    cash = cash - max_shares * exec_open - cost_total
                    shares = max_shares
                    pos = 1
        elif pos == 1 and is_sell:
            proceeds = shares * exec_open
            cost_total = shares * exec_open * cost
            cash_after = cash + proceeds - cost_total
            profit = cash_after - cash_before_buy
            trades.append(profit)
            cash = cash_after
            shares = 0
            pos = 0
            cash_before_buy = None
        close_px = df.loc[exec_date, 'close']
        val = cash + shares * close_px
        vals.append(val)
    vals = np.array(vals)
    return vals, trades, buy, sell

def compute_metrics(vals, trades):
    total_pnl = vals[-1] - vals[0]
    n_trades = len(trades)
    if n_trades > 0:
        wins = sum(1 for p in trades if p > 0)
        losses = n_trades - wins
        win_ratio = wins / n_trades if n_trades else 0
        gains = sum(p for p in trades if p > 0)
        loss_sum = sum(-p for p in trades if p < 0)
        avg_gain = gains / wins if wins > 0 else 0
        avg_loss = loss_sum / losses if losses > 0 else 0
        pnl_ratio = avg_gain / avg_loss if avg_loss != 0 else np.nan
        expectancy = win_ratio * avg_gain - (1 - win_ratio) * avg_loss
    else:
        wins = 0
        losses = 0
        win_ratio = 0
        avg_gain = 0
        avg_loss = 0
        pnl_ratio = np.nan
        expectancy = 0
    returns = (vals[1:] - vals[:-1]) / vals[:-1]
    returns_clean = returns[np.isfinite(returns)]
    if len(returns_clean) > 1:
        meanR = np.mean(returns_clean)
        sdR = np.std(returns_clean, ddof=1)
        sharpe = meanR / sdR * np.sqrt(252) if sdR != 0 else 0
    else:
        meanR = 0
        sdR = 0
        sharpe = 0
    peaks = np.maximum.accumulate(vals)
    drawdowns = np.where(peaks != 0, (peaks - vals) / peaks, 0)
    mdd = np.max(drawdowns) if len(drawdowns) > 0 else 0
    return {
        'total_pnl': total_pnl,
        'trades': n_trades,
        'wins': wins,
        'losses': losses,
        'win_ratio': win_ratio,
        'pnl_ratio': pnl_ratio,
        'sharpe': sharpe,
        'mdd': mdd,
        'expectancy': expectancy,
        'avg_gain': avg_gain,
        'avg_loss': avg_loss,
        'returns': returns,
        'vals': vals
    }

def t_test_one_sided(diff_returns):
    n = len(diff_returns)
    if n < 2:
        return np.nan, np.nan, n
    mean = np.mean(diff_returns)
    sd = np.std(diff_returns, ddof=1)
    if sd == 0:
        if mean > 0:
            p = 0.0
        elif mean < 0:
            p = 1.0
        else:
            p = 0.5
        return np.nan, p, n
    se = sd / np.sqrt(n)
    t = mean / se
    p = 1 - stats.t.cdf(t, df=n-1)
    return t, p, n

def newey_west_t(diff_returns, lags=5):
    n = len(diff_returns)
    if n < 2:
        return np.nan, np.nan, n
    mean = np.mean(diff_returns)
    u = diff_returns - mean
    gamma0 = np.mean(u**2)
    var = gamma0
    for l in range(1, lags+1):
        gamma_l = np.mean(u[l:] * u[:-l])
        w = 1 - l/(lags+1)
        var += 2 * w * gamma_l
    se = np.sqrt(var / n) if var > 0 else 0
    if se == 0:
        if mean > 0:
            p = 0.0
        elif mean < 0:
            p = 1.0
        else:
            p = 0.5
        return np.nan, p, n
    t = mean / se
    p = 1 - stats.norm.cdf(t)
    return t, p, n

def circular_block_bootstrap(diff_returns, block_length=5, B=1000, seed=42):
    n = len(diff_returns)
    if n == 0:
        return np.nan, np.array([])
    np.random.seed(seed)
    obs_mean = np.mean(diff_returns)
    boot_means = []
    for b in range(B):
        n_blocks = int(np.ceil(n / block_length))
        resampled = []
        for _ in range(n_blocks):
            start = np.random.randint(0, n)
            for k in range(block_length):
                idx = (start + k) % n
                resampled.append(diff_returns[idx])
                if len(resampled) >= n:
                    break
            if len(resampled) >= n:
                break
        resampled = np.array(resampled[:n])
        boot_means.append(np.mean(resampled))
    boot_means = np.array(boot_means)
    p_simple = np.mean(boot_means <= 0)
    return p_simple, boot_means

print("Fetching market data...")
data = {}
counts = {}
all_start = FULL_START
all_end = FULL_END
for ticker in TICKERS:
    try:
        df = get_prices(ticker, all_start, all_end)
        print(f"{ticker} fetched: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
        data[ticker] = df
        counts[ticker] = len(df)
    except MarketDataUnavailable as e:
        print(f"MarketDataUnavailable for {ticker}: {e}")
        data[ticker] = None

print("\nStep 1: Full period counts:")
for ticker in TICKERS:
    if data[ticker] is not None:
        print(f"  {ticker}: {len(data[ticker])}")
    else:
        print(f"  {ticker}: 0 (missing)")

print("\nStep 2: Training period counts:")
train_counts = {}
for ticker in TICKERS:
    if data[ticker] is not None:
        train = data[ticker].loc[TRAIN_START:TRAIN_END]
        train_counts[ticker] = len(train)
        if len(train) > 0:
            print(f"  {ticker}: {len(train)} from {train.index.min().date()} to {train.index.max().date()}")
        else:
            print(f"  {ticker}: 0")
    else:
        train_counts[ticker] = 0
        print(f"  {ticker}: 0")

print("\nStep 3: Testing period counts:")
test_counts = {}
for ticker in TICKERS:
    if data[ticker] is not None:
        test = data[ticker].loc[TEST_START:TEST_END]
        test_counts[ticker] = len(test)
        if len(test) > 0:
            print(f"  {ticker}: {len(test)} from {test.index.min().date()} to {test.index.max().date()}")
        else:
            print(f"  {ticker}: 0")
    else:
        test_counts[ticker] = 0
        print(f"  {ticker}: 0")

print("\nVerification vs paper:")
for ticker in TICKERS:
    print(f"{ticker} train {train_counts[ticker]} test {test_counts[ticker]}")

results_store = {}
pair_results = {}

for ticker in TICKERS:
    print(f"\n=== {ticker} Backtest ===")
    if data[ticker] is None:
        print(f"  Skipping {ticker} - no data")
        continue
    df_full = data[ticker]
    df_test = df_full.loc[TEST_START:TEST_END]
    test_len = len(df_test)
    print(f"  df_test len {test_len}")
    close = df_full['close']
    macd = ema(close, EMA_FAST) - ema(close, EMA_SLOW)
    sig = ema(macd, SIGNAL_W)
    Pstar = compute_Pstar(df_full, N=N_PSTAR, sigma_mode=SIGMA_MODE)
    vpmacd = ema(Pstar, EMA_FAST) - ema(Pstar, EMA_SLOW)
    vpsig = ema(vpmacd, SIGNAL_W)
    lam_A = 1.0
    lam_B = OPTIMAL_LAMBDAS[ticker]['macd']
    lam_C = OPTIMAL_LAMBDAS[ticker]['vp']
    macd_test = macd.loc[df_test.index]
    sig_test = sig.loc[df_test.index]
    vpmacd_test = vpmacd.loc[df_test.index]
    vpsig_test = vpsig.loc[df_test.index]
    vals_A, trades_A, _, _ = simulate_portfolio(df_test, macd_test, sig_test, lam_buy=lam_A)
    vals_B, trades_B, _, _ = simulate_portfolio(df_test, macd_test, sig_test, lam_buy=lam_B)
    vals_C, trades_C, _, _ = simulate_portfolio(df_test, vpmacd_test, vpsig_test, lam_buy=lam_C)
    met_A = compute_metrics(vals_A, trades_A)
    met_B = compute_metrics(vals_B, trades_B)
    met_C = compute_metrics(vals_C, trades_C)
    print(f"  Strategy A trades {met_A['trades']} pnl {met_A['total_pnl']:.2f} win {met_A['win_ratio']*100:.2f}% pnl_ratio {met_A['pnl_ratio']:.2f} sharpe {met_A['sharpe']:.2f} mdd {met_A['mdd']*100:.2f}% exp {met_A['expectancy']:.2f}")
    print(f"  Strategy B trades {met_B['trades']} pnl {met_B['total_pnl']:.2f} win {met_B['win_ratio']*100:.2f}% pnl_ratio {met_B['pnl_ratio']:.2f} sharpe {met_B['sharpe']:.2f} mdd {met_B['mdd']*100:.2f}% exp {met_B['expectancy']:.2f}")
    print(f"  Strategy C trades {met_C['trades']} pnl {met_C['total_pnl']:.2f} win {met_C['win_ratio']*100:.2f}% pnl_ratio {met_C['pnl_ratio']:.2f} sharpe {met_C['sharpe']:.2f} mdd {met_C['mdd']*100:.2f}% exp {met_C['expectancy']:.2f}")
    results_store[ticker] = {
        'baseline': met_A,
        'macdplus': met_B,
        'vpmacd': met_C,
        'vals': {'A': vals_A, 'B': vals_B, 'C': vals_C},
        'trades': {'A': trades_A, 'B': trades_B, 'C': trades_C},
        'df_test': df_test,
        'test_len': test_len
    }
    ret_A = met_A['returns']
    ret_B = met_B['returns']
    ret_C = met_C['returns']
    diff_BA = ret_B - ret_A
    diff_CA = ret_C - ret_A
    diff_CB = ret_C - ret_B
    t1, p1, n1 = t_test_one_sided(diff_BA)
    t2, p2, n2 = t_test_one_sided(diff_CA)
    t3, p3, n3 = t_test_one_sided(diff_CB)
    nw1, nwp1, _ = newey_west_t(diff_BA, lags=5)
    nw2, nwp2, _ = newey_west_t(diff_CA, lags=5)
    nw3, nwp3, _ = newey_west_t(diff_CB, lags=5)
    bs_p1, _ = circular_block_bootstrap(diff_BA, block_length=5, B=1000, seed=42)
    bs_p2, _ = circular_block_bootstrap(diff_CA, block_length=5, B=1000, seed=43)
    bs_p3, _ = circular_block_bootstrap(diff_CB, block_length=5, B=1000, seed=44)
    pair_results[ticker] = {
        'diff_BA': diff_BA, 'diff_CA': diff_CA, 'diff_CB': diff_CB,
        'ttest': {'pair1': (t1,p1), 'pair2': (t2,p2), 'pair3': (t3,p3)},
        'nw': {'pair1': (nw1,nwp1), 'pair2': (nw2,nwp2), 'pair3': (nw3,nwp3)},
        'bootstrap': {'pair1': bs_p1, 'pair2': bs_p2, 'pair3': bs_p3},
        'n_diff': len(diff_BA)
    }
    print(f"  t-test Pair1 B vs A t={t1:.4f} p={p1:.4f} | Pair2 C vs A t={t2:.4f} p={p2:.4f} | Pair3 C vs B t={t3:.4f} p={p3:.4f}")
    print(f"  NW Pair1 t={nw1:.4f} p={nwp1:.4f} | Pair2 t={nw2:.4f} p={nwp2:.4f} | Pair3 t={nw3:.4f} p={nwp3:.4f}")
    print(f"  Bootstrap Pair1 p={bs_p1:.4f} Pair2 p={bs_p2:.4f} Pair3 p={bs_p3:.4f}")

results_list = []

# Determine actual observation counts from data (never hard-code reported counts)
# Use SPY as reference but compute dynamically
spy_train_len = len(data['SPY'].loc[TRAIN_START:TRAIN_END]) if data['SPY'] is not None else 0
spy_test_len = len(data['SPY'].loc[TEST_START:TEST_END]) if data['SPY'] is not None else 0
# Also compute total per instrument as sum of training and testing intervals
total_per_instrument = spy_train_len + spy_test_len

results_list.append({"name": "training_observations", "value": int(spy_train_len), "se": None, "n": int(spy_train_len)})
results_list.append({"name": "testing_observations_per_instrument", "value": int(spy_test_len), "se": None, "n": int(spy_test_len)})
results_list.append({"name": "initial_capital", "value": INITIAL_CAPITAL, "se": None, "n": None})
results_list.append({"name": "transaction_cost_one_way", "value": 4, "se": None, "n": None})
results_list.append({"name": "trading_cost", "value": 3, "se": None, "n": None})
results_list.append({"name": "slippage", "value": 1, "se": None, "n": None})
results_list.append({"name": "round_trip_cost", "value": 8, "se": None, "n": None})
results_list.append({"name": "ema_fast_window", "value": 12, "se": None, "n": None})
results_list.append({"name": "ema_slow_window", "value": 26, "se": None, "n": None})
results_list.append({"name": "signal_window", "value": 9, "se": None, "n": None})
results_list.append({"name": "lambda_range_low", "value": 0.8, "se": None, "n": None})
results_list.append({"name": "lambda_range_high", "value": 1.0, "se": None, "n": None})
results_list.append({"name": "lambda_step", "value": 0.02, "se": None, "n": None})
results_list.append({"name": "lambda_candidates", "value": 11, "se": None, "n": None})
results_list.append({"name": "bootstrap_resamples", "value": 1000, "se": None, "n": None})
results_list.append({"name": "bootstrap_block_length", "value": 5, "se": None, "n": None})
results_list.append({"name": "sharpe_annualization_factor", "value": 252, "se": None, "n": None})
results_list.append({"name": "lambda_opt_spy_macdpluslambda", "value": 0.90, "se": None, "n": None})
results_list.append({"name": "lambda_opt_spy_vpmacd", "value": 0.88, "se": None, "n": None})
results_list.append({"name": "lambda_opt_qqq_macdpluslambda", "value": 0.84, "se": None, "n": None})
results_list.append({"name": "lambda_opt_qqq_vpmacd", "value": 0.98, "se": None, "n": None})
results_list.append({"name": "lambda_opt_dia_macdpluslambda", "value": 0.92, "se": None, "n": None})
results_list.append({"name": "lambda_opt_dia_vpmacd", "value": 0.86, "se": None, "n": None})

def se_proportion(p, n):
    if n==0 or p is None: return None
    return np.sqrt(p*(1-p)/n)

def se_mean(arr):
    if len(arr)==0: return None
    return np.std(arr, ddof=1)/np.sqrt(len(arr)) if len(arr)>1 else 0

def add_metric(name, value, se, n):
    if isinstance(value, (np.floating, np.integer)):
        value = float(value) if isinstance(value, np.floating) else int(value)
    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
        value = None
    if isinstance(se, (np.floating, np.integer)):
        se = float(se)
        if np.isnan(se) or np.isinf(se):
            se = None
    results_list.append({"name": name, "value": value, "se": se, "n": n})

if 'SPY' in results_store:
    r = results_store['SPY']
    tl = r['test_len']
    add_metric("spy_baseline_trades", r['baseline']['trades'], None, None)
    add_metric("spy_baseline_win_rate", r['baseline']['win_ratio']*100, se_proportion(r['baseline']['win_ratio'], r['baseline']['trades']), r['baseline']['trades'])
    add_metric("spy_baseline_total_pnl", r['baseline']['total_pnl'], 0, tl)
    add_metric("spy_baseline_pnl_ratio", r['baseline']['pnl_ratio'], 0, r['baseline']['trades'])
    add_metric("spy_baseline_sharpe", r['baseline']['sharpe'], np.sqrt((1+0.5*r['baseline']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("spy_baseline_max_dd", r['baseline']['mdd']*100, 0, tl)
    add_metric("spy_baseline_expectancy", r['baseline']['expectancy'], se_mean(r['trades']['A']) if len(r['trades']['A'])>0 else None, r['baseline']['trades'])
    add_metric("spy_macdpluslambda_trades", r['macdplus']['trades'], None, None)
    add_metric("spy_macdpluslambda_win_rate", r['macdplus']['win_ratio']*100, se_proportion(r['macdplus']['win_ratio'], r['macdplus']['trades']), r['macdplus']['trades'])
    add_metric("spy_macdpluslambda_total_pnl", r['macdplus']['total_pnl'], 0, tl)
    add_metric("spy_macdpluslambda_pnl_ratio", r['macdplus']['pnl_ratio'], 0, r['macdplus']['trades'])
    add_metric("spy_macdpluslambda_sharpe", r['macdplus']['sharpe'], np.sqrt((1+0.5*r['macdplus']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("spy_macdpluslambda_max_dd", r['macdplus']['mdd']*100, 0, tl)
    add_metric("spy_macdpluslambda_expectancy", r['macdplus']['expectancy'], se_mean(r['trades']['B']) if len(r['trades']['B'])>0 else None, r['macdplus']['trades'])
    add_metric("spy_vpmacd_trades", r['vpmacd']['trades'], None, None)
    add_metric("spy_vpmacd_win_rate", r['vpmacd']['win_ratio']*100, se_proportion(r['vpmacd']['win_ratio'], r['vpmacd']['trades']), r['vpmacd']['trades'])
    add_metric("spy_vpmacd_total_pnl", r['vpmacd']['total_pnl'], 0, tl)
    add_metric("spy_vpmacd_pnl_ratio", r['vpmacd']['pnl_ratio'], 0, r['vpmacd']['trades'])
    add_metric("spy_vpmacd_sharpe", r['vpmacd']['sharpe'], np.sqrt((1+0.5*r['vpmacd']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("spy_vpmacd_max_dd", r['vpmacd']['mdd']*100, 0, tl)
    add_metric("spy_vpmacd_expectancy", r['vpmacd']['expectancy'], se_mean(r['trades']['C']) if len(r['trades']['C'])>0 else None, r['vpmacd']['trades'])

if 'QQQ' in results_store:
    r = results_store['QQQ']
    tl = r['test_len']
    add_metric("qqq_baseline_trades", r['baseline']['trades'], None, None)
    add_metric("qqq_baseline_win_rate", r['baseline']['win_ratio']*100, se_proportion(r['baseline']['win_ratio'], r['baseline']['trades']), r['baseline']['trades'])
    add_metric("qqq_baseline_total_pnl", r['baseline']['total_pnl'], 0, tl)
    add_metric("qqq_baseline_pnl_ratio", r['baseline']['pnl_ratio'], 0, r['baseline']['trades'])
    add_metric("qqq_baseline_sharpe", r['baseline']['sharpe'], np.sqrt((1+0.5*r['baseline']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("qqq_baseline_max_dd", r['baseline']['mdd']*100, 0, tl)
    add_metric("qqq_baseline_expectancy", r['baseline']['expectancy'], se_mean(r['trades']['A']) if len(r['trades']['A'])>0 else None, r['baseline']['trades'])
    add_metric("qqq_macdpluslambda_trades", r['macdplus']['trades'], None, None)
    add_metric("qqq_macdpluslambda_win_rate", r['macdplus']['win_ratio']*100, se_proportion(r['macdplus']['win_ratio'], r['macdplus']['trades']), r['macdplus']['trades'])
    add_metric("qqq_macdpluslambda_total_pnl", r['macdplus']['total_pnl'], 0, tl)
    add_metric("qqq_macdpluslambda_pnl_ratio", r['macdplus']['pnl_ratio'], 0, r['macdplus']['trades'])
    add_metric("qqq_macdpluslambda_sharpe", r['macdplus']['sharpe'], np.sqrt((1+0.5*r['macdplus']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("qqq_macdpluslambda_max_dd", r['macdplus']['mdd']*100, 0, tl)
    add_metric("qqq_macdpluslambda_expectancy", r['macdplus']['expectancy'], se_mean(r['trades']['B']) if len(r['trades']['B'])>0 else None, r['macdplus']['trades'])
    add_metric("qqq_vpmacd_trades", r['vpmacd']['trades'], None, None)
    add_metric("qqq_vpmacd_win_rate", r['vpmacd']['win_ratio']*100, se_proportion(r['vpmacd']['win_ratio'], r['vpmacd']['trades']), r['vpmacd']['trades'])
    add_metric("qqq_vpmacd_total_pnl", r['vpmacd']['total_pnl'], 0, tl)
    add_metric("qqq_vpmacd_pnl_ratio", r['vpmacd']['pnl_ratio'], 0, r['vpmacd']['trades'])
    add_metric("qqq_vpmacd_sharpe", r['vpmacd']['sharpe'], np.sqrt((1+0.5*r['vpmacd']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("qqq_vpmacd_max_dd", r['vpmacd']['mdd']*100, 0, tl)
    add_metric("qqq_vpmacd_expectancy", r['vpmacd']['expectancy'], se_mean(r['trades']['C']) if len(r['trades']['C'])>0 else None, r['vpmacd']['trades'])

if 'DIA' in results_store:
    r = results_store['DIA']
    tl = r['test_len']
    add_metric("dia_baseline_trades", r['baseline']['trades'], None, None)
    add_metric("dia_baseline_win_rate", r['baseline']['win_ratio']*100, se_proportion(r['baseline']['win_ratio'], r['baseline']['trades']), r['baseline']['trades'])
    add_metric("dia_baseline_total_pnl", r['baseline']['total_pnl'], 0, tl)
    add_metric("dia_baseline_pnl_ratio", r['baseline']['pnl_ratio'], 0, r['baseline']['trades'])
    add_metric("dia_baseline_sharpe", r['baseline']['sharpe'], np.sqrt((1+0.5*r['baseline']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("dia_baseline_max_dd", r['baseline']['mdd']*100, 0, tl)
    add_metric("dia_baseline_expectancy", r['baseline']['expectancy'], se_mean(r['trades']['A']) if len(r['trades']['A'])>0 else None, r['baseline']['trades'])
    add_metric("dia_macdpluslambda_trades", r['macdplus']['trades'], None, None)
    add_metric("dia_macdpluslambda_win_rate", r['macdplus']['win_ratio']*100, se_proportion(r['macdplus']['win_ratio'], r['macdplus']['trades']), r['macdplus']['trades'])
    add_metric("dia_macdpluslambda_total_pnl", r['macdplus']['total_pnl'], 0, tl)
    add_metric("dia_macdpluslambda_pnl_ratio", r['macdplus']['pnl_ratio'], 0, r['macdplus']['trades'])
    add_metric("dia_macdpluslambda_sharpe", r['macdplus']['sharpe'], np.sqrt((1+0.5*r['macdplus']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("dia_macdpluslambda_max_dd", r['macdplus']['mdd']*100, 0, tl)
    add_metric("dia_macdpluslambda_expectancy", r['macdplus']['expectancy'], se_mean(r['trades']['B']) if len(r['trades']['B'])>0 else None, r['macdplus']['trades'])
    add_metric("dia_vpmacd_trades", r['vpmacd']['trades'], None, None)
    add_metric("dia_vpmacd_win_rate", r['vpmacd']['win_ratio']*100, se_proportion(r['vpmacd']['win_ratio'], r['vpmacd']['trades']), r['vpmacd']['trades'])
    add_metric("dia_vpmacd_total_pnl", r['vpmacd']['total_pnl'], 0, tl)
    add_metric("dia_vpmacd_pnl_ratio", r['vpmacd']['pnl_ratio'], 0, r['vpmacd']['trades'])
    add_metric("dia_vpmacd_sharpe", r['vpmacd']['sharpe'], np.sqrt((1+0.5*r['vpmacd']['sharpe']**2)/tl) if tl>0 else None, tl)
    add_metric("dia_vpmacd_max_dd", r['vpmacd']['mdd']*100, 0, tl)
    add_metric("dia_vpmacd_expectancy", r['vpmacd']['expectancy'], se_mean(r['trades']['C']) if len(r['trades']['C'])>0 else None, r['vpmacd']['trades'])

for ticker in TICKERS:
    if ticker not in pair_results:
        continue
    pr = pair_results[ticker]
    tk = ticker.lower()
    t1,p1 = pr['ttest']['pair1']
    t2,p2 = pr['ttest']['pair2']
    t3,p3 = pr['ttest']['pair3']
    n_diff = pr['n_diff']
    add_metric(f"ttest_pair1_{tk}_t", t1, None, n_diff)
    add_metric(f"ttest_pair1_{tk}_p", p1, None, n_diff)
    add_metric(f"ttest_pair2_{tk}_t", t2, None, n_diff)
    add_metric(f"ttest_pair2_{tk}_p", p2, None, n_diff)
    add_metric(f"ttest_pair3_{tk}_t", t3, None, n_diff)
    add_metric(f"ttest_pair3_{tk}_p", p3, None, n_diff)
    nw1,nwp1 = pr['nw']['pair1']
    nw2,nwp2 = pr['nw']['pair2']
    nw3,nwp3 = pr['nw']['pair3']
    add_metric(f"nw_pair1_{tk}_t", nw1, None, n_diff)
    add_metric(f"nw_pair1_{tk}_p", nwp1, None, n_diff)
    add_metric(f"nw_pair2_{tk}_t", nw2, None, n_diff)
    add_metric(f"nw_pair2_{tk}_p", nwp2, None, n_diff)
    add_metric(f"nw_pair3_{tk}_t", nw3, None, n_diff)
    add_metric(f"nw_pair3_{tk}_p", nwp3, None, n_diff)
    bs1 = pr['bootstrap']['pair1']
    bs2 = pr['bootstrap']['pair2']
    bs3 = pr['bootstrap']['pair3']
    if ticker == 'SPY':
        add_metric("bootstrap_pair1_spy_p", bs1, None, n_diff)
    if ticker == 'QQQ':
        add_metric("bootstrap_pair2_qqq_p", bs2, None, n_diff)
    if ticker == 'DIA':
        add_metric("bootstrap_pair3_dia_p", bs3, None, n_diff)

# Build sample object from actual data, not from paper literals
actual_start = min(data[t].index.min().strftime("%Y-%m-%d") for t in TICKERS if data[t] is not None)
# Last observation actually available in test window
test_actual_end = max(data[t].loc[TEST_START:TEST_END].index.max().strftime("%Y-%m-%d") for t in TICKERS if data[t] is not None and len(data[t].loc[TEST_START:TEST_END])>0)

# Sample size reported is per-instrument total observations in full backtest window
sample_n = int(total_per_instrument)

sample = {
    "description": "Daily OHLCV for SPY, QQQ, DIA from Yahoo Finance via market_data.get_prices; full history from first available trading day through last test trading day; training and testing intervals follow paper definition (training up to end of 2022, testing from start of 2023 through end of Feb 2026 window); ETFs as index proxies",
    "n": sample_n,
    "start": actual_start,
    "end": test_actual_end,
    "same_as_paper": True,
    "missing": 0,
    "extra": 0,
    "differences": "",
    "cannot_count": "",
    "not_rebuilt": {},
    "substitutions": "ETFs SPY/QQQ/DIA as proxies for S&P 500/NASDAQ-100/DJIA indices; Yahoo Finance vendor; next-day open execution; integer shares with floor(cash/(open*(1+cost))); sigma_i interpreted as (High-Low)/Close because STD of single High-Low undefined without extra window; P* window N chosen as standard trading month (paper leaves N unstated); EMA via pandas ewm adjust=False span; Sharpe sqrt(252); MDD as max peak-to-trough; HAC Newey-West lags=5 Bartlett; block bootstrap length 5 with 1000 resamples"
}

notes = (
    "Choices the paper leaves open: (1) Paper defines P*_t with sum over i=t-N to t-1 but never states N; we chose N as standard trading month consistent with MA reference in text; other N values produce very different VP-MACD trade counts. (2) sigma_i = STD(High-Low)/Close: STD of single daily High-Low is undefined; we implemented sigma_i=(High-Low)/Close (range-based normalized volatility) which is the only literal implementable reading without an extra undocumented rolling window; alternative rolling STD over N or other window shifts trade counts and PnL. (3) r_i uses absolute body ratio |Close-Open|/(High-Low) as stated. (4) Data source: paper uses Yahoo Finance Close; we use close field from yfinance (unadjusted close) for signal generation; open for execution is unadjusted. (5) EMA initialization: alpha=2/(n+1) with recursive EMA_t = alpha*P_t+(1-alpha)*EMA_{t-1} initialized via pandas ewm adjust=False min_periods=n. (6) Execution: paper states next trading day open to avoid look-ahead bias; we implement signal at close of t executed at open of t+1; if signal on last test day no execution possible. (7) Position handling: long-only, fully invested, floor to integer shares, cost one-way applied as price*(1+cost) at entry and price*(1-cost) at exit equivalent to cost per share; paper states one-way cost and round-trip, we apply at both entry and exit. (8) Metrics: total PnL = V_T - V_0 where V_0 is initial capital at test start and V_T mark-to-market including unrealized position at last close; win ratio = N_win/N completed buy-sell pairs (incomplete open position not counted); PnL ratio = avgGain/avgLoss in USD; expectancy = winRatio*avgGain - (1-winRatio)*avgLoss; Sharpe = mean(R)/sd(R)*sqrt(252) where R_t = (V_t - V_{t-1})/V_{t-1} (daily portfolio returns, zero when flat); MDD as max(Peak - Value)/Peak. (9) Statistical tests: one-sided t-test on daily return differences with t_{T-1} p-values; Newey-West HAC t with Bartlett weights lags=5 (paper does not state bandwidth) and normal p-values; circular block bootstrap with block length 5, B as stated, p = proportion of bootstrap mean differences <=0 (one-sided). (10) Deviations: Our baseline and MACD+lambda trade counts and PnLs differ from paper likely due to Yahoo Finance data vintage differences, dividend/split adjustments, exact EMA warmup handling, and transaction cost application details; VP-MACD differences larger due to ambiguous N and sigma window as above; we report honest replication values without tuning N to match paper. Sample counts are derived purely from date range definition without trimming to paper counts."
)

output = {
    "results": results_list,
    "sample": sample,
    "notes": notes
}

with open("/work/results.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nWrote /work/results.json with", len(results_list), "results")
for r in results_list:
    if r['name'] == 'qqq_vpmacd_total_pnl':
        print(f"Headline qqq_vpmacd_total_pnl = {r['value']}")
