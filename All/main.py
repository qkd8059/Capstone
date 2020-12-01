import numpy as np
from regime_test import *
from testplot import *
lookback = 8
target_return = 0.1*lookback/52
principal = 30000
risk_appetite = 1
card = 12
horizon = 700
#dates, price_table, all_weight, all_ticker, cum_ret_exp,cum_ret_act = Regime_test.get_cum_ret(lookback,target_return,principal,risk_appetite,card,horizon)
#aret, astd, asr = Regime_test.stats (cum_ret_act,cum_ret_exp,horizon)
#testplot.plot_pie(all_weight[-1],all_ticker[-1],price_table)
#testplot.cum_plot (dates, cum_ret_exp[:-3], cum_ret_act[:-3])
dates, all_port_act_ret, cumulated_act_ret = Regime_test.plot_month(lookback,risk_appetite,card,principal,target_return)
#print(aret, astd, asr)
print(cumulated_act_ret)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(30,5))
plt.plot(dates, np.asarray(cumulated_act_ret[:-1])*100, linewidth=1) #Using 95% VaR, 1000 times simulation, theta = 1.96
plt.legend(['Actual Return'])
plt.xlabel('$t$')
plt.ylabel('$Cum Return$')
plt.xticks(rotation=90)
plt.show()


#retrieve data from database
from database_main import Database
df = Database.read_data('timeseries_L12_C8_R0.5') #replace the collection name
cum_ret = df['ret'].values.tolist()
print(cum_ret)
