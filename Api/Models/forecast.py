import pandas as pd, numpy as np, os
import matplotlib.pyplot as plt
import pmdarima as pm
from statsmodels.tsa.stattools import acf
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


def loadDf (path,datesf):
  # data upload
  
  df = pd.read_csv("../"+path, header=0)
  # add date column
  # df['period']= datesf
  # df = df.set_index('period')
  return df

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




def forecast (indexes): 
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)

  years = 2
  workdays_m = 5*4
  split = years*12*workdays_m
  # datesf = pd.read_csv('Data.csv',header=0)
  # datesf = pd.to_datetime(datesf['Data'])
  
  for index in indexes:
    df = loadDf(index,0)
    # df = np.log(df)
    # train = df[:-split]
    # test = df[-split:]
    # print(df[df.columns[0]])
    # auto arima
    Sarima(df,split)
    #LSTM
    # lstm_predict(df,split)

def compute_windows(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def lstm_predict(dataframe, split,log_t=False,plot=False):
  dataset = dataframe.values
  if (log_t):
    dataset = np.log(dataset)

  dataset = dataset.astype('float32')
  # normalize the dataset
  scaler = MinMaxScaler(feature_range=(0, 1))
  dataset = scaler.fit_transform(dataset)
  # split into train and test sets
  # test_size = 12*40
  train_size = int(len(dataset)-split)

  train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
  # reshape into X=t and Y=t+1
  look_back = 2
  trainX, trainY = compute_windows(train, look_back)
  testX, testY = compute_windows(test, look_back)
  # reshape input to be [samples, time steps, features]
  trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
  testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
  # create and fit the LSTM network
  model = Sequential()
  model.add(LSTM(4, input_shape=(1, look_back)))
  model.add(Dense(1))
  model.compile(loss='mean_squared_error', optimizer='adam')
  model.fit(trainX, trainY, epochs=3, batch_size=1, verbose=2)
  # make predictions
  trainPredict = model.predict(trainX)
  testPredict = model.predict(testX)
  # invert predictions
  trainPredict = scaler.inverse_transform(trainPredict)
  trainY = scaler.inverse_transform([trainY])
  testPredict = scaler.inverse_transform(testPredict)
  testY = scaler.inverse_transform([testY])

  dataset = scaler.inverse_transform(dataset)
  #unlog
  if (log_t):
    trainPredict = np.exp(trainPredict)
    trainY = np.exp(trainY)
    testPredict = np.exp(testPredict)
    testY = np.exp(testY)
    dataset = np.exp(dataset)
  # calculate root mean squared error
  trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
  print('Train Score: %.2f RMSE' % (trainScore))
  testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
  print('Test Score: %.2f RMSE' % (testScore))
  if (plot):
    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
    # plot baseline and predictions
    plt.plot(dataset)
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.show()
  return testScore, testPredict
    

def Sarima(df,split):
  df = np.log(df)
  train = df[:-split]
  test = df[-split:]
  model = pm.auto_arima(train.values, start_p=1, start_q=1,
                            test='adf', max_p=3, max_q=3, seasonal=False,
                            d=None, D=None, trace=True,
                            error_action='ignore',
                            suppress_warnings=True,
                            stepwise=True) # False full grid

  print(model.summary())
  morder = model.order
  print("Sarimax order {0}".format(morder))
  
  # predictions and forecasts
  fitted = model.fit(train)
  ypred = fitted.predict_in_sample() # prediction (in-sample)
  yfore = fitted.predict(n_periods=split) # forecast (out-of-sample)
  # plt.plot(train.values)
  # plt.plot([None for x in range(split)]+[x for x in ypred[split:]])
  # plt.plot([None for x in ypred]+[x for x in yfore])
  # plt.xlabel('time');plt.ylabel('log sales')
  # plt.show()
  # recostruction
  expdata = pd.DataFrame(np.exp(ypred),index=train.index)
  # unlog
  expfore = pd.DataFrame(np.exp(yfore),index=test.index)
  
  exptrain = np.exp(train)

  plt.plot(expfore,label= "forecast")
  
  plt.plot(exptrain,label='train')
  plt.plot(np.exp(test),label='test')
  plt.legend()
  plt.show()
  # plt.plot([None for x in range(split)]+[x for x in expdata[split:]])
  # # plt.show()
  # plt.plot(df)
  # plt.plot([None for x in expdata]+[x for x in expfore])

  # # ------------------ the same, but using statsmodels’ SARIMAX, morder from before
  # from statsmodels.tsa.statespace.sarimax import SARIMAX
  # sarima_model = SARIMAX(train.values, order=morder)
  # sfit = sarima_model.fit()
  # sfit.plot_diagnostics()
  # plt.show()
  # ypred = sfit.predict(start=0,end=len(train))
  # yfore = sfit.get_forecast(steps=split)
  # expdata = np.exp(ypred)
  #  # unlog
  # expfore = np.exp(yfore.predicted_mean)
  # plt.plot(expdata)
  # # plt.plot(df)
  # plt.plot([None for x in expdata]+[x for x in expfore])
  # plt.show()    
 
indexes = ['GOLD_SPOT.csv']
forecast(indexes)


