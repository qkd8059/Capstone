import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from database_main import Database
from regime_test import *

spy = Database.read_data('SPY')
print(spy)
time = spy['Date']
#time = time[1:]


price = spy['Adj Close']
ret = []

for i in range(1,len(price)):
    ret.append((price[i]-price[i-1])/price[i-1])

print(len(time))
print(len(ret))

cum_ret = Regime_test.cum_return(ret)
print(len(cum_ret))
plt.plot(time,cum_ret)
