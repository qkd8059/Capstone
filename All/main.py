from regime_test import *
from testplot import *
lookback = 8
target_return = 0.1
principal = 30000
risk_appetite = 1
card = 12
horizon = 700
dates, price_table, all_weight, all_ticker, cum_ret_exp,cum_ret_act = Regime_test.get_cum_ret(lookback,target_return,principal,risk_appetite,card,horizon)
aret, astd, asr = Regime_test.stats (cum_ret_act,cum_ret_exp,horizon)
testplot.plot_pie(all_weight[-1],all_ticker[-1],price_table)
testplot.cum_plot (dates, cum_ret_exp[:-3], cum_ret_act[:-3])
print(aret, astd, asr)
