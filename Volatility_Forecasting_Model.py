import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly.express as px
import arch
import yfinance as yf

df = yf.download('SBIN.NS', start = "2010-01-01", end = "2021-09-09")
plt.plot(df['Close'])


#settings
n_period = 1

#df = pd.read_csv('data.csv')
#df.set_index('Date', inplace = True, drop = True)

#calculate daily return

df['rtn'] = ((df['Close']/ df['Close'].shift(1)) - 1) * 100
df['mod_rtn'] = ((df['Close']/ df['Close'].shift(n_period)) - 1) * 100
df.dropna(inplace = True)


#Set the model

garch_model = arch.arch_model(df['rtn'], p = 1, q = 1, mean = 'Constant', vol = "GARCH", dist = 'Normal' )

#garch_model = arch.arch_model(df['rtn'], p = 1, q = 1, mean = 'Constant', vol = "GARCH", dist = 'skewt' )
#garch_model = arch.arch_model(df['rtn'], p = 1, q = 1, o = 1, mean = 'Constant', vol = "EGARCH", dist = 'skewt' )

gm_result = garch_model.fit(disp = 'off')
print(gm_result.params)

#forecast
gm_forecast = gm_result.forecast(horizon = n_period)
expected_vol = np.sqrt(np.sum(gm_forecast.variance.values[-1,:][0:n_period]))
range_up = df['Close'].iloc[-1] * (1 + (expected_vol/100))
range_dn = df['Close'].iloc[-1] * (1 + (-expected_vol/100))
print('Expected Vol :' + str(expected_vol))
print('Range Up :' + str(range_up))
print('Range Down :' + str(range_dn))


#Forecast for a test period

predictions = list()
test_period = 1500

for i in range(test_period):
    training_data = df['rtn'][:-(test_period-i)]
    model = arch.arch_model(training_data, p = 1, q = 1, mean = 'constant', vol = 'GARCH', dist = 'normal')
    fit_model = model.fit(disp = 'off')
    predict = fit_model.forecast(horizon = n_period)
    predictions.append(np.sqrt(np.sum(predict.variance.values[-1,:][0:n_period])))


#Convert to df
df_predictions = pd.Series(predictions, index = df.index[-test_period:])

#Plot upper and lower range
plt.plot(df_predictions)
plt.plot(df_predictions * -1)
plt.plot(df['mod_rtn'][-test_period:])

#check Strike
d = pd.DataFrame()
d['mod_rtn'] = df['mod_rtn'][-test_period:]
d['pred'] = df_predictions
d['pred_dn'] = df_predictions * -1
dn = len(d[d['mod_rtn'] < d['pred_dn']])
up = len(d[d['mod_rtn'] > d['pred']])
strike_rate = round(((test_period-dn-up)/test_period)*100)
print('Strike Rate :' + str(strike_rate) + '%')
