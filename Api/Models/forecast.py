import pandas as pd, numpy as np, os, sys


import matplotlib.pyplot as plt
from lstm import lstm_predict
from util import  load_df, forecast_accuracy
from arima import arima
from opt import init_portfolio,compute_risk, initial_capital, capital_variation, portfolio_var, portfolio_value, index_pct, moving_avg, portfolio_return, portfolio_risk

def test_stationarity(timeseries):
  from statsmodels.tsa.stattools import adfuller 
  
  #Determining rolling statistics
  rolmean = timeseries.rolling(4).mean() # around 4 weeks on each month
  rolstd = timeseries.rolling(4).std()
  
  #Plot rolling statistics:
  orig = plt.plot(timeseries, color='blue',label='Original')
  mean = plt.plot(rolmean, color='red', label='Rolling Mean')
  std = plt.plot(rolstd, color='black', label = 'Rolling Std')
  plt.legend(loc='best')
  plt.title('Rolling Mean & Standard Deviation')
  plt.show(block=False)
  
  #Perform Dickey-Fuller test:
  print ('Results of Dickey-Fuller Test:')
  dftest = adfuller(timeseries, autolag='AIC')
  dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
  for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
  print (dfoutput)
  
  if dfoutput['p-value'] < 0.05:
      print('result : time series is stationary')
  else : print('result : time series is not stationary')
  from matplotlib.pylab import rcParams 
  rcParams['figure.figsize'] = 20,10



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
    df = load_df(indice)
    # test_stationarity(df)
   
    res, test = predictor(df,split,plot=plot)
    accuracies[indice] = forecast_accuracy(res.values,test.values)
    res.columns = [indice]
    test.columns = [indice]
    test_vals = pd.concat((test_vals,test),axis=1)
    forecasts = pd.concat((forecasts,res),axis=1)
  


  # test_vals = test_vals.pct_change().iloc[1:]
  # varss = forecasts.pct_change().iloc[1:]

  # plot_percent(varss)
  # plot_percent(test_vals)
  # print(varss)
    

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
  indexes = ['GOLD_SPOT','SP_500']
  fore, acc = forecast(indexes, method, plot=False)#months to int
  print(acc)
  # print(fore.columns)
  # portfolio_subdiv = init_portfolio(indexes)
  # # print(portfolio_subdiv)
  # initial_cap_split = initial_capital(portfolio_subdiv,investment)
  # # print(initial_cap_split)

  # index_pct = index_pct(fore)
  # # print(index_pct)
  # portfolio_values = capital_variation(initial_cap_split,index_pct)
  # # print(portfolio_values)
  # portfolio_pct =portfolio_var(portfolio_values)
  # portfolio_tot = portfolio_value(portfolio_values)

  # portfolio_ma = moving_avg(portfolio_values)
  # print(portfolio_ma)
  # port_ret = portfolio_return(portfolio_values)
  # print(port_ret)

  # risk = portfolio_risk(portfolio_values,portfolio_ma)
  # print(risk)
  # risk = compute_risk(fore,investment)
  # print(risk)
  # print(portfolio_val)
  # print(portfolio_pct)
  # print(acc)
  print('MAPE Number of arguments:', len(sys.argv))
  # print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   


  
  
     



