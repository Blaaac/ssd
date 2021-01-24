import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf

  
def plot_prediction(dataset,train_p,test_p):
  plt.plot(dataset,label= "df")
  plt.plot(train_p,label='train')
  plt.plot(test_p,label='test')
  plt.legend()
  plt.show()

def load_df (path):
  # data upload
  df = pd.read_csv("../"+path+".csv", header=0)
  # add date column
  # df['period']= datesf
  # df = df.set_index('period')
  return df

def forecast_accuracy(forecast, actual):
  mape = np.mean(np.abs(forecast - actual)/np.abs(actual)) # MAPE
  me = np.mean(forecast - actual)# ME
  mae = np.mean(np.abs(forecast - actual)) # MAE
  mpe = np.mean((forecast - actual)/actual) # MPE
  rmse = np.mean((forecast - actual)**2)**.5 # RMSE
  corr = np.corrcoef(forecast, actual)[0,1] # corr
  mins = np.amin(np.hstack([forecast[:,None], actual[:,None]]), axis=1)
  maxs = np.amax(np.hstack([forecast[:,None], actual[:,None]]), axis=1)
  minmax = 1 - np.mean(mins/maxs) # minmax
  acf1 = acf(forecast-actual)[1] # ACF1
  return({'mape':mape, 'me':me, 'mae': mae,
          'mpe': mpe, 'rmse':rmse, 'acf1':acf1,
          'corr':corr, 'minmax':minmax})
# import os
# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)

# df = load_df("GOLD_SPOT")
# dh=df
# # dh = df.asfreq('W')
# import statsmodels.api as sm

# decomposition = sm.tsa.seasonal_decompose(dh['GOLD_SPOT'], model='additive', 
#                             extrapolate_trend='freq',period=21) #additive or multiplicative is data specific
# fig = decomposition.plot()
# plt.show()

