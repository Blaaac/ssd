import pmdarima as pm
from statsmodels.tsa.stattools import acf
import statsmodels as sm
import numpy as np
import pandas as pd
from util import plot_prediction, forecast_accuracy
import matplotlib.pyplot as plt


def fit_arima(df,split,order,plot=False):
  df = np.log(df)
  train = df[:-split]
  test = df[-split:]
  mod = sm.tsa.arima.ARIMA(endog, order=(1, 0, 0))


  # unlog
  expdata = pd.DataFrame(np.exp(ypred),index=train.index)
  expfore = pd.DataFrame(np.exp(yfore),index=test.index)
  exptrain = np.exp(train)
  exptest = np.exp(test)

  if (plot):
    plot_prediction(np.exp(df),expdata,expfore)


def arima(df,split,plot=False):
  df = np.log(df)
  train = df[:-split]
  test = df[-split:]
  model = pm.auto_arima(train.values, start_p=1, start_q=1,
                            #test='adf', 
                            max_p=3, max_q=3, seasonal=False,
                            trace=True,
                           # random=True,
                            # maxiter=200,
                            error_action='ignore',
                            suppress_warnings=True,
                            stepwise=False) # False full grid

  print(model.summary())
  morder = model.order
  print("Sarimax order {0}".format(morder))
  
  # predictions and forecasts
  fitted = model.fit(train)
  ypred = fitted.predict_in_sample() # prediction (in-sample)
  yfore = fitted.predict(n_periods=split) # forecast (out-of-sample)

  # recostruction
  expdata = pd.DataFrame(np.exp(ypred),index=train.index)
  # unlog
  a =np.exp(yfore)
  expfore = pd.DataFrame(np.exp(yfore),index=test.index)
  exptrain = np.exp(train)
  # exptest = pd.DataFrame(np.exp(test),index=test.index)
  exptest = np.exp(test)
  if (plot):
    plot_prediction(np.exp(df),expdata,expfore)
  score =0
  return expfore, exptest



  # plt.plot(expfore,label= "forecast")
  
  # plt.plot(dataset,label='train')
  # plt.plot(np.exp(test),label='test')
  # plt.legend()
  # plt.show()
  
  # plt.plot([None for x in range(split)]+[x for x in expdata[split:]])
  # # plt.show()
  # plt.plot(df)
  # plt.plot([None for x in expdata]+[x for x in expfore])



  ###new
  # import statsmodels.api as sm
  # model = sm.tsa.arima.ARIMA(train.values,order=morder)
  # fit = model.fit()
  # ypred = fit.predict(start=0,end=len(train))
  # yfore = fit.get_forecast(steps=split)
  # expdata = np.exp(ypred) # unlog
  # expfore = np.exp(yfore.predicted_mean)
  # exptest = np.exp(test)
  # if (plot):
  #   plot_prediction(np.exp(df),expdata,expfore)
  # return expfore, exptest
  ###endnew
  # # ------------------ the same, but using statsmodels’ SARIMAX, morder from before
  # from statsmodels.tsa.statespace.sarimax import SARIMAX
  # sarima_model = SARIMAX(train.values, order=morder)
  # sfit = sarima_model.fit()
  # # sfit.plot_diagnostics()
  # # plt.show()
  # ypred = sfit.predict(start=0,end=len(train))
  # yfore = sfit.get_forecast(steps=split)
  # expdata = np.exp(ypred)
  #  # unlog
  # expfore = np.exp(yfore.predicted_mean)
  # plt.plot(expdata)
  # # plt.plot(df)
  # plt.plot([None for x in expdata]+[x for x in expfore])
  # plt.show()  