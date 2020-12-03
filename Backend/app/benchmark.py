import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from.database_main import Database
from regime_test import *

spy = Database.read_data('SPY')
time = spy['Date']
print(len(time))

price = spy['Adj Close']
price = pd.DataFrame(price)

ret = price.pct_change().dropna()
ret = ret['Adj Close'].values.tolist()

#save dates
for i in range(9,int(len(time)/4)):
    date.append(time[i*4])
date = pd.DataFrame(date, columns = ['Date'])  
Database.clean_col_save(date,'timeseries_dates')

#save SPY cumulated return
monthly_ret = []
date = []
for i in range(0,186):
    monthly_ret.append(ret[i*4]) 

cum_ret = Regime_test.cum_return(monthly_ret)
plt.plot(date,cum_ret[:-1])
cum_ret = pd.DataFrame(cum_ret, columns = ['cum ret'])

Database.clean_col_save(cum_ret,'SPY_ret')

#save 60/40 fund cumulated return
fund = Database.read_data('6040fund')
time = fund['Date']

price = fund['Adj Close']
price = pd.DataFrame(price)

ret = price.pct_change().dropna()
ret = ret['Adj Close'].values.tolist()

monthly_ret = []
date = []
for i in range(0,186):
    monthly_ret.append(ret[i*4]) 

cum_ret = Regime_test.cum_return(monthly_ret)
plt.plot(date,cum_ret[:-1])
cum_ret = pd.DataFrame(cum_ret, columns = ['cum ret'])

Database.clean_col_save(cum_ret,'6040fund_ret')

