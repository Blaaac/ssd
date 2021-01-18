import pandas as pd, numpy as np, os, sys



from lstm import lstm_predict
from util import  load_df
from sarima import sarima



def preProcess(df, split):
  # data = df[df.columns[0]].to_numpy()
  # array of index data
  print(np.log(df))
  df[df.columns[0]] = np.log(df[df.columns[0]])
  print(df)
  # log transform
  # logdata = np.log(data)
  # data = pd.Series(logdata)

  # plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
  train = df[:-split]
  test = df[-split:]

  return train, test




def forecast (indexes,method, months=24,plot=False): 
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)

  
  workdays_m = 21
  split = months* workdays_m
  # datesf = pd.read_csv('Data.csv',header=0)
  # datesf = pd.to_datetime(datesf['Data'])
  a = lambda: None
  if (method == "arima"):
  # auto arima
    a = sarima
  elif (method == "lstm"): 
  # LSTM
    a =lstm_predict
  
  for index in indexes:
    df = load_df(index,0)
    # df = np.log(df)
    # train = df[:-split]
    # test = df[-split:]
    # print(df[df.columns[0]])
    a(df,split,plot=plot)






if __name__ == "__main__":
  # change working directory to script path
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)

  method = sys.argv[1]
  
  indexes = ['GOLD_SPOT.csv']
  forecast(indexes, method, plot=True)

  print('MAPE Number of arguments:', len(sys.argv))
  print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   
     



