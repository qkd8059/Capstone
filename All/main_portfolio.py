from regime_test import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from database_main import Database

# lookback = 12
# lookback = 26
lookback = 12
# lookback = 104
target_return = 0.1*lookback/52
principal = 30000
risk_appetite = 0.8
# card = 4
# card = 6
card = 10
# card = 10
horizon = 700
weight, ticker = Regime_test.single_period(lookback,target_return,principal,risk_appetite,card,horizon)
print(weight, ticker)
Regime_test.plot_pie(weight, ticker)


df = Database.read_data("SP500Tickers")
full_name = []
sector = []
for j in range(0,card):
    for i in range(0,len(df['Symbol'])):
        if df['Symbol'][i] == ticker[j]:
            ind = df['Symbol'][i]
            full_name.append(df['Name'][i])
            sector.append(df['Sector'][i])
            
#print(full_name)
#print(sector)
        
data = {'Ticker':ticker,'Weight':weight,'Name':full_name,'Sector':sector}       
df = pd.DataFrame(data,columns = ['Ticker','Weight','Name','Sector'])
#print(df)

Database.clean_col_save(df,"portfolio")
