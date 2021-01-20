import pandas as pd, numpy as np, os, sys


import matplotlib as plt
from lstm import lstm_predict
from util import  load_df, forecast_accuracy
from arima import arima





def forecast (indexes,method, months=24,plot=False): 

  
  workdays_m = 21
  split = months* workdays_m
  # datesf = pd.read_csv('Data.csv',header=0)
  # datesf = pd.to_datetime(datesf['Data'])
  predictor = lambda: None
  forecasts = pd.DataFrame()
  accuracies = {}
  if (method == "sarima"):
  # auto arima
    predictor = arima
  elif (method == "lstm"): 
  # LSTM
    predictor = lstm_predict
  for index in indexes:
    df = load_df(index,0)

 

    # df = np.log(df)
    # train = df[:-split]
    # test = df[-split:]
    # print(df[df.columns[0]])
    res, test = predictor(df,split,plot=plot)
    accuracies[index] = forecast_accuracy(res.values,test.values)
    forecasts = pd.concat([forecasts,res],1)
    

  # print(forecasts.head(n=20))
  return forecasts, accuracies






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
  indexes = ['GOLD_SPOT']
  fore, acc = forecast(indexes, method, plot=True)
  print(acc)
  print('MAPE Number of arguments:', len(sys.argv))
  # print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   
     



