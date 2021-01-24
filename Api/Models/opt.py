import numpy as np
import pandas as pd

def init_portfolio(indices):
  weights = {}
  w = np.random.uniform(low=0.05,high=1,size=len(indices))
  # w = np.random.random(len(indices))
  print(w)
  w /= np.sum(w)
  print(w)
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
  res.index = res.index + 1  
  res.sort_index(inplace=True) 
  return res

def portfolio_var(portfolio):
  return portfolio_value(portfolio).pct_change()

def portfolio_value(portfolio):
  return portfolio.sum(axis=1)
  


init_portfolio([1,2,33,4,4])