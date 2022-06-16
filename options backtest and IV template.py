import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import mibian as mb
import os

filename = "...options.csv"
data = pd.read_csv(filename)

data.columns

expiry = pd.to_datetime(data.loc[:,'Expiry'], format = '%d-%b-%y')
current = pd.to_datetime(data.loc[:,'Date'], format = '%d-%b-%y')

diff = expiry - current

diff = (diff / np.timedelta64(1, 'D')).astype(int)

rate = 0 #interest rate
strike = data.loc[i,'Strike Price']
underlying = data.loc[i,'spot']
days_to_expiry = diff
put_price = data.loc[i,'Close']
spot = data.spot

data.loc[:,'IV'] = np.nan

for i in range(0,len(data.Close)):
    aiv = mb.BS([data.spot[i],data.loc[i,'Strike Price'],rate,diff[i]], putPrice = data.Close[i])
    data.IV[i] = (aiv.impliedVolatility)
    pp = mb.BS([data.spot[i],data.loc[i,'Strike Price'],rate,diff[i]], putPrice = data.Close[i])
    data.pup[i] = (pp.putPrice)
    
print(data.IV)

plt.plot(current,data.Close)










