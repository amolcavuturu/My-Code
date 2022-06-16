from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
data = yf.download('HDFC.NS', start="2019-01-01", end="2020-01-31")

data.head(10)

data['Moving_average'] = data['Close'].rolling(window=20,min_periods=1,center=False).mean()

data.tail(20)

data[['Close','Moving_average']].plot()

data['return'] = data['Close'].pct_change()
plt.hist(data['return'], bins=[-1,0,1])
plt.show()



data['buysignal'] = np.where((data['Open'] > data['Close'].shift(+1)) & (data['Close'] > data['Close'].shift(+1)), 1.0, 0.0)
data['sellsignal'] = np.where((data['Open'] < data['Close'].shift(+1)) & (data['Close'] < data['Close'].shift(+1)), -1.0, 0.0)
TotalSignal = data['buysignal'].sum() + (data['sellsignal'].sum()*-1)
Tradingdays = data['Close'].count()
prob = (TotalSignal/Tradingdays)*100
print (Tradingdays)
print (TotalSignal)
print (prob)



data['buyqty'] = np.where((data['Low'] < data['Close'].shift(+1)),(data['Close']-data['Close'].shift(+1))*data['buysignal'], 0.0)
data['sellqty'] = np.where((data['High'] > data['Close'].shift(+1)),(data['Close'].shift(+1) - data['Close'])*(data['sellsignal']*-1), 0.0)
data['profit'] = data['buyqty'] + data['sellqty']
Totalprofit = data['profit'].sum()
print(Totalprofit)


data['Close'].hist(bins=100, figsize=(8, 6))


# Compute standard deviation of last 10 days closing prices
data['Stdav'] = data['Close'].rolling(window=10, min_periods=1,center=False).std()
data['Upper_Band'] = data['Moving_average'] + (data['Stdav'] * 1.5)
data['Lower_Band'] = data['Moving_average'] - (data['Stdav'] * 1.5)
# Show Bollinger Band
data[['Close', 'Moving_average', 'Upper_Band', 'Lower_Band']].plot(figsize=(18,6))


#Bollinger Bands
Stock = "HDFC.NS"
T3 = pd.DataFrame({"Close": data["Close"]})
T3['Year'] = T3.index.year
T2 = pd.DataFrame({"cumpnl":['0'], "MA":['0'], "STD":['0'], "Stock":['0'],"Year":['0']})
for z in range (2019, 2021, 1):
    T = T3.where(T3.Year == z)
    T = T.dropna()
    for x in range(1,37,2):
        for y in range(1,3,1):
            MA=x
            STD=y
            T['moving_average'] = T.Close.rolling(MA).mean()
            T['moving_std_dev'] = T.Close.rolling(MA).std()
            T['upper_band'] = T.moving_average + (T.moving_std_dev*STD)
            T['lower_band'] = T.moving_average - (T.moving_std_dev*STD)
            T['long_entry'] = T.Close < T.lower_band
            T['long_exit'] = T.Close >= T.moving_average
            T['positions_long'] = np.nan
            T.loc[T.long_entry,'positions_long'] = 1
            T.loc[T.long_exit,'positions_long'] = 0
            T.positions_long = T.positions_long.fillna(method='ffill')
            T['short_entry'] = T.Close > T.upper_band
            T['short_exit'] = T.Close <= T.moving_average
            T['positions_short'] = np.nan
            T.loc[T.short_entry,'positions_short'] = -1
            T.loc[T.short_exit,'positions_short'] = 0
            T.positions_short = T.positions_short.fillna(method='ffill')
            T['positions'] = T.positions_long + T.positions_short
            T['price_difference']= T.Close - T.Close.shift(1)
            T['pnl'] = T.positions.shift(1) * T.price_difference
            T['cumpnl'] = T.pnl.cumsum()
            T1 = T[['cumpnl']].tail(1)
            T1['MA'] = MA
            T1['STD'] = STD
            T1['Stock'] = Stock
            T1['Year'] = z
            T2 = T2.append(T1)
print(T2)

Pivot_Table1 = pd.pivot_table(T2, values ='cumpnl', index =['MA', 'STD'],columns =['Year'], aggfunc = np.sum)
print (Pivot_Table1)



####Pair trading
from scipy.stats import pearsonr
data = yf.download('HDFC.NS', start="2016-01-01", end="2021-02-05")
data1 = yf.download('HDFCBANK.NS', start="2016-01-01", end="2021-02-05")
corr = pearsonr(data['Close'], data1['Close'])
print (corr)


from matplotlib import pyplot
pyplot.scatter(data['Close'], data1['Close'])
pyplot.show()

fig,ax = plt.subplots(figsize=(18,6))
ax.plot(data['Close'], color="red")
ax2=ax.twinx()
ax2.plot(data1['Close'],color="blue")
plt.show()


(data['Close']-data1['Close']).plot(figsize=(18,6))
plt.axhline((data['Close']-data1['Close']).mean(), color='red', linestyle='--')
plt.xlabel('Time')
plt.legend(['Price Difference', 'Mean'])
plt.show()

from statsmodels.tsa.stattools import adfuller
adf = adfuller(data['Close']-data1['Close'], maxlag = 1)
print (adf[0])
print (adf[1])
print (adf[4])


###Backtesting in python
prices_df = pd.DataFrame({"Stock_1": data["Close"], "Stock_2": data1["Close"]})
prices_df['Diff'] = prices_df['Stock_1'] - prices_df['Stock_2']
prices_df[['Stock_1', 'Stock_2', 'Diff']].plot(grid=True, secondary_y='Diff', figsize=(14,6))


prices_df['moving_average'] = prices_df.Diff.rolling(5).mean()
prices_df['moving_std_dev'] = prices_df.Diff.rolling(5).std()
prices_df['upper_band'] = prices_df.moving_average + prices_df.moving_std_dev
prices_df['lower_band'] = prices_df.moving_average -prices_df.moving_std_dev
prices_df[['Diff', 'moving_average', 'upper_band', 'lower_band']].plot(figsize=(16,6))


import plotly.express as px
Table = prices_df[['Diff', 'moving_average', 'upper_band', 'lower_band']]
fig = px.line(Table)
fig.show()

prices_df['long_entry'] = prices_df.Diff < prices_df.lower_band
prices_df['long_exit'] = prices_df.Diff >= prices_df.moving_average
prices_df['positions_long'] = np.nan
prices_df.loc[prices_df.long_entry,'positions_long'] = 1
prices_df.loc[prices_df.long_exit,'positions_long'] = 0
prices_df.positions_long = prices_df.positions_long.fillna(method='ffill')
prices_df['short_entry'] = prices_df.Diff > prices_df.upper_band
prices_df['short_exit'] = prices_df.Diff <= prices_df.moving_average
prices_df['positions_short'] = np.nan
prices_df.loc[prices_df.short_entry,'positions_short'] = -1
prices_df.loc[prices_df.short_exit,'positions_short'] = 0
prices_df.positions_short = prices_df.positions_short.fillna(method='ffill')
prices_df['positions'] = prices_df.positions_long + prices_df.positions_short
prices_df['price_difference']= prices_df.Diff - prices_df.Diff.shift(1)
prices_df['pnl'] = prices_df.positions.shift(1) * prices_df.price_difference
prices_df['cumpnl'] = prices_df.pnl.cumsum()
prices_df[['cumpnl']].plot(figsize=(16,8))






####Pair tradinng ML
from datetime import datetime
import yfinance as yf
from scipy import stats as stats
from scipy.stats import pearsonr
from numpy import mean
from numpy import std
import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="whitegrid")
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from itertools import groupby, count
import statsmodels.api as sm
# %matplotlib inline

# Download historical data
data = yf.download('HDFC.NS', start="2017-01-01", end="2021-01-31")
data1 = yf.download('HDFCBANK.NS', start="2017-01-01", end="2021-01-31")
data2 = yf.download('ICICIBANK.NS', start="2017-01-01", end="2021-01-31")
data3 = yf.download('KOTAKBANK.NS', start="2017-01-01", end="2021-01-31")
data4 = yf.download('INDUSINDBK.NS', start="2017-01-01", end="2021-01-31")
data5 = yf.download('AXISBANK.NS', start="2017-01-01", end="2021-01-31")

# New table prices_df created with daily closing prices of all stocks
prices_df = pd.DataFrame({"HDFC": data["Close"], "HDFCBK":data1["Close"], "ICICIBK": data2["Close"], "KOTAKBK": data3["Close"],"INDUSINDBK": data4["Close"], "AXISBK": data5["Close"]})
prices_df.head()
abc = ["HDFC", "HDFCBK", "ICICIBK", "KOTAKBK", "INDUSINDBK","AXISBK"]

# ADF test for different combinations of stocks
for x in range(len(abc)):
    for y in range(x,len(abc)):
        if x==y: continue
    print(abc[x],abc[y], "ADF", adfuller(prices_df[abc[x]] - prices_df[abc[y]], maxlag = 1)[1])
def Zscore(X):
    return np.array((X - np.mean(X)) / np.std(X))
stocks = 6
capital = 10000
components = 1
max_pos=1
S1 = []
L1 = []
i1 = []
pnls = []
dates = []
for i in range (len(prices_df)):
    if i < 10: continue
    prices = prices_df.iloc[0:i]
    pr = np.asarray(prices.T)
    pca = PCA(n_components=components)
    comps = pca.fit(pr.T).components_.T
    factors = sm.add_constant(pr.T.dot(comps))
    mm = [sm.OLS(s.T, factors).fit() for s in pr]
    resids = list(map(lambda x: x.resid, mm))
    zs = {}
    for inst in range(stocks):
        zs[inst] = Zscore(resids[inst])[-1]
    idx_long = (np.argsort([zs[j] for j in zs])[:max_pos])
    idx_short = (np.argsort([zs[j] for j in zs])[-max_pos:])
    L1.append(abc[int(idx_long)])
    S1.append(abc[int(idx_short)])
    dates.append(prices_df.index[i])
    i1.append(i)
df = pd.DataFrame(i1, dates)
df['Long'] = L1
df['Short'] = S1
df = df.join(prices_df)
df['Long_P'] = 0
df['Short_P'] = 0
df['Profit'] = 0
df['Total_Profit'] = 0
for x in range ((len(df)-1)):
    y = x+1
    a = df['Long'][x]
    b = df['Short'][x]
    df['Long_P'][x] = (df[a][y] - df[a][x])*(round(capital/df[a][x]))
    df['Short_P'][x] = (df[b][x] - df[b][y])*(round(capital/df[b][x]))
df['Profit'] = df['Long_P'] + df['Short_P']
df['Total_Profit'] = df['Profit'].cumsum()
plt.plot(df['Total_Profit'])





