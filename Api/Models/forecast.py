import pandas as pd, numpy as np, os, sys


import matplotlib.pyplot as plt
# from lstm import lstm_predict
from util import  load_df, forecast_accuracy
from arima import arima
import json
from opt import array_to_portfolio,compute_risk_return_nocap,gen_port,compute_return
import pso
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

  return forecasts, accuracies, test_vals

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
  investment = float(sys.argv[9])
  months = int(sys.argv[10])
  risk_w = float(sys.argv[11])

  # print('MAPE Number of arguments:', len(sys.argv))
  # print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   
  # # print("MAPE indexes ", indexes)
  indexes = ['SP_500']#,'GOLD_SPOT']
  fore, acc, t = forecast(indexes, method, months, plot=False)#months to int
  

  mypso = pso.PSO(indexes=fore,fitness_func=compute_risk_return_nocap,
                        init_func=gen_port,
                        weight= risk_w,
                        numvar=len(indexes))
  res = mypso.pso_solve(popsize=10,
                        niter=30,
                        nhood_size=5)

  json_indexes =["S&P_500_INDEX","FTSE_MIB_INDEX","GOLD_SPOT_$_OZ","MSCI_EM","MSCI_EURO","All_Bonds_TR","U.S._Treasury"]
  port = array_to_portfolio(res,json_indexes)
  port2= array_to_portfolio(res,indexes)
  port_ret = compute_return(fore,res,investment)
  port.insert(0, "horizon", months)

  
  json_f=port.iloc[0].to_json(orient='index')
  print("PORTFOLIO"+json_f.replace("\"","'"))
  print("METRICS"+json.dumps(acc).replace("\"","'"))
  print("RESULT"+str(port_ret).replace("\"","'"))
  f = open("portfolio.json", "w")
  f.write(json_f)
  f.close()




  
  
     



