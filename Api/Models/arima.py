import pmdarima as pm
from statsmodels.tsa.stattools import acf
import statsmodels as sm
import numpy as np
import pandas as pd
from util import plot_prediction, forecast_accuracy
import matplotlib.pyplot as plt


def arima(df,split,plot=False):
  df = np.log(df)
  train = df[:-split]
  test = df[-split:]
  model = pm.auto_arima(train.values, start_p=1, start_q=1,
                            test='adf', 
                            max_p=3, max_q=3, seasonal=False,
                            trace=True,
                           # random=True,
                            # maxiter=200,
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

  return expfore, exptest