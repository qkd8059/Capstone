from .database_main import Database
from .regime_test import Regime_test
import numpy as np
import pandas as pd

def master(target_return, time_horizon, principal, cardinality, rebalance_freq, risk_appetite):
    # Note:
    # target_return please provide annual value.
    # time_horizon please provide in terms of weeks. i.e. 1year would be 52
    # cardinality can take value 4, 6, 8 and 10.
    # Rebalancing Frequency please provide in terms of weeks. It can take value 12, 26, 52, 104.
    # Risk appetite: 0.2, 0.5, 0.8

    dates = Database.read_data('timeseries_dates')
    start_period = np.floor(time_horizon/4).astype(int)
    date_list = dates['Date'].values.tolist()
    df = pd.DataFrame(date_list[-start_period:])
    normalized_dates = []
    for elem in df.values.tolist():
        normalized_dates.append(elem[0])
    # Read portolio constructed based on user input
    df = Database.read_data(
        'timeseries_L'+str(rebalance_freq)+'_C'+str(cardinality)+'_R'+str(risk_appetite))
    cum_ret = df['ret'].values.tolist()
    # Read benchmark #1, S&P500 Index
    df_SPY = Database.read_data('SPY_ret')
    SPY_ret = df_SPY['cum ret'].values.tolist()
    # Read benchmark #2, 60/40 Index Fund
    df_6040 = Database.read_data('6040fund_ret')
    SPY6040_ret = df_6040['cum ret'].values.tolist()

    # Partition the back-testing result to display, based on user's investment horizon
    normalized_ret = Regime_test.plot_horizon(cum_ret, time_horizon)
    normalized_SPY_ret = Regime_test.plot_horizon(SPY_ret, time_horizon)
    normalized_6040_ret = Regime_test.plot_horizon(SPY6040_ret, time_horizon)
    normalized_dates = normalized_dates[:]
    # Do the optimization to generate weights
    weight, ticker_label = Regime_test.single_period(lookback=rebalance_freq, target_return=(
        target_return/(52/rebalance_freq)), principal=principal, risk_appetite=risk_appetite, card=cardinality, horizon=time_horizon)
    # Calculate Stats based on the back-testing period length, which is ppl's investment horizon
    annual_return, annual_std, sharpe_ratio = Regime_test.stats(
        normalized_ret, time_horizon)
    annual_return_SPY, annual_std_SPY, sharpe_ratio_SPY = Regime_test.stats(
        normalized_SPY_ret, time_horizon)
    annual_return_6040, annual_std_6040, sharpe_ratio_6040 = Regime_test.stats(
        normalized_6040_ret, time_horizon)

    return list(ticker_label), weight, annual_return, annual_std, sharpe_ratio, normalized_dates, normalized_ret, normalized_SPY_ret, normalized_6040_ret, annual_return_SPY, annual_std_SPY, sharpe_ratio_SPY, annual_return_6040, annual_std_6040, sharpe_ratio_6040
