from regime_test import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# lookback = 12
# lookback = 26
lookback = 52
# lookback = 104
target_return = 0.1*lookback/52
principal = 30000
risk_appetite = 0.8
# card = 4
# card = 6
card = 8
# card = 10
horizon = 700
weight, ticker_label = Regime_test.single_period(lookback,target_return,principal,risk_appetite,card,horizon)
print(weight, ticker_label)
Regime_test.plot_pie(weight, ticker_label)
