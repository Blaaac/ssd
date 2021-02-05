import pandas as pd, numpy as np, os, sys


import matplotlib.pyplot as plt
# from lstm import lstm_predict
from util import  load_df, forecast_accuracy
from arima import arima
import json
from opt import array_to_portfolio,compute_risk_return_nocap,gen_port,compute_return
import pso

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
  # elif (method == "lstm"): 
  # # LSTM
  #   predictor = lstm_predict
  for indice in indexes:
    df = load_df(indice)
   
    res, test = predictor(df,split,plot=plot)
    accuracies[indice] = forecast_accuracy(res.values,test.values)
    res.columns = [indice]
    test.columns = [indice]
    test_vals = pd.concat((test_vals,test),axis=1)
    forecasts = pd.concat((forecasts,res),axis=1)

  return forecasts, accuracies, test_vals

def compute_optimal_portfolio(indexes,method,investment,months,risk_w):

  # indexes = ['SP_500','GOLD_SPOT']
  json_indexes =["S&P_500_INDEX","FTSE_MIB_INDEX","GOLD_SPOT_$_OZ","MSCI_EM","MSCI_EURO","All_Bonds_TR","U.S._Treasury"]

  fore, acc, t = forecast(indexes, method, months, plot=False)
  
  mypso = pso.PSO(indexes=fore,fitness_func=compute_risk_return_nocap,
                        init_func=gen_port,
                        weight= risk_w,
                        numvar=len(indexes))
  res = mypso.pso_solve(popsize=10,
                        niter=15,
                        nhood_size=3)

  
  port = array_to_portfolio(res,json_indexes)
  #for output
  port_ret = compute_return(fore,res,investment)
  port.insert(0, "horizon", months)

  json_f=port.iloc[0].to_json(orient='index')

  json_out = {'portfolio':json.loads(port.iloc[0].to_json(orient='index')),
          'metrics':acc,
          'return':port_ret}
  # print(json_out)
  
  return json_out
 



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

  res = compute_optimal_portfolio(indexes,method,investment,months,risk_w)

  # print(str.replace(str(res),"\'","\""))
  print("portfolio"+str.replace(str(res['portfolio']),"\'","\""))
  print("metrics"+str.replace(str(res['metrics']),"\'","\""))
  print("result"+str.replace(str(res['result']),"\'","\""))

  f = open("portfolio.json", "w")
  f.write(str(res['portfolio']))
  f.close()





  
  
     



