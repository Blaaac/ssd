import numpy as np
import pandas as pd

def init_portfolio(indices):
  weights = {}
  w = np.random.random(len(indices))
  w /= np.sum(w)
  for i in range(len(indices)):
    weights[indices[i]] = w[i]
  return pd.DataFrame(weights, index = [0])


def initial_capital(portfolio,capital):
  return portfolio*float(capital)

def capital_variation(initial_capital,pctchg):
  
  init = initial_capital.iloc[0]
  pctchg = pctchg.reset_index(drop=True)
  res = ((1 + pctchg).cumprod() * init)

  res.loc[-1] = init  
  res.index = df.index + 1  
  res.sort_index(inplace=True) 
  return df
