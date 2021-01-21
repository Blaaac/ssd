import pandas as pd, numpy as np, os, sys


import matplotlib.pyplot as plt
from lstm import lstm_predict
from util import  load_df, forecast_accuracy
from arima import arima
from opt import init_portfolios





def forecast (indexes,method, months=24,plot=False): 

  
  workdays_m = 21
  split = months* workdays_m
  # datesf = pd.read_csv('Data.csv',header=0)
  # datesf = pd.to_datetime(datesf['Data'])
  predictor = lambda: None
  forecasts = pd.DataFrame()
  test_vals = pd.DataFrame()
  accuracies = {}
  if (method == "sarima"):
  # auto arima
    predictor = arima
  elif (method == "lstm"): 
  # LSTM
    predictor = lstm_predict
  for indice in indexes:
    df = load_df(indice,0)
    res, test = predictor(df,split,plot=plot)
    accuracies[indice] = forecast_accuracy(res.values,test.values)
    res.columns = [indice]
    test.columns = [indice]
    test_vals = pd.concat((test_vals,test),axis=1)
    forecasts = pd.concat((forecasts,res),axis=1)
  


  test_vals = test_vals.pct_change().iloc[1:]
  varss = forecasts.pct_change().iloc[1:]

  plot_percent(varss)
  plot_percent(test_vals)
  print(varss)
    

  # print(forecasts.head(n=20))
  return forecasts, accuracies

def plot_percent(returns):
  plt.figure(figsize=(14, 7))
  for c in returns.columns.values:
      plt.plot(returns.index, returns[c], lw=3, alpha=0.8,label=c)
  plt.legend(loc='upper right', fontsize=12)
  plt.ylabel('daily returns')
  plt.show()





if __name__ == "__main__":
  # change working directory to script path
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)

  indexes = sys.argv[1:8]
  method = sys.argv[8]
  investment = sys.argv[9]
  months = sys.argv[10]

  # print("MAPE indexes ", indexes)
  # indexes = ['GOLD_SPOT','SP_500']
  # fore, acc = forecast(indexes, method, plot=False)
  initial_p = init_portfolios(indexes)
  print(initial_p)
  # print(acc)
  print('MAPE Number of arguments:', len(sys.argv))
  # print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   
     



