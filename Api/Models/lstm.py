import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from util import plot_prediction
import pandas as pd, numpy as np


# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return Series(diff)


# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]



def compute_windows(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def lstm_predict(dataframe, split,log_t=False,plot=False):
  dataset = dataframe.values
      # series = dataset
      # differenced = difference(dataset, 1)
      # dataset = differenced
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
  model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)
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

  # undiff
    # inverted = list()
    # for i in range(len(differenced)):
    #   value = inverse_difference(series, differenced[i], len(series)-i)
    #   inverted.append(value)
    # inverted = Series(inverted)
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
    plot_prediction(dataset,trainPredictPlot,testPredictPlot)

  return testScore, testPredict