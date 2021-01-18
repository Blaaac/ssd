import pmdarima as pm
from statsmodels.tsa.stattools import acf
import numpy as np
import pandas as pd
from util import plot_prediction
def sarima(df,split,plot=False):
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

  # recostruction
  expdata = pd.DataFrame(np.exp(ypred),index=train.index)
  # unlog
  expfore = pd.DataFrame(np.exp(yfore),index=test.index)
  exptrain = np.exp(train)
  exptest = np.exp(test)
  if (plot):
    plot_prediction(np.exp(df),expdata,expfore)

  # plt.plot(expfore,label= "forecast")
  
  # plt.plot(dataset,label='train')
  # plt.plot(np.exp(test),label='test')
  # plt.legend()
  # plt.show()
  
  # plt.plot([None for x in range(split)]+[x for x in expdata[split:]])
  # # plt.show()
  # plt.plot(df)
  # plt.plot([None for x in expdata]+[x for x in expfore])

  # ------------------ the same, but using statsmodels’ SARIMAX, morder from before
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