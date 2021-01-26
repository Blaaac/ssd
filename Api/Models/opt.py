import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error 

def index_pct(indexes):
  return indexes.pct_change()#.iloc[1:]

def init_portfolio(indices):
  weights = {}
  w = np.random.uniform(low=0.05,high=1,size=len(indices))
  # w = np.random.random(len(indices))
  # print(w)
  w /= np.sum(w)
  # print(w)
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

def moving_avg(portfolio, days=20):
  return portfolio.rolling(days).mean().dropna()
  
def portfolio_return(portfolio, days=20):
  return portfolio.tail(days).mean().sum()


def portfolio_risk(portfolio,moving_avg,days=20):
  port = portfolio[days+1:]
  # for index in port:
  #   a = moving_avg[index]
  #   b = port[index]
  return mean_squared_error(moving_avg,port,squared=False)#check order
  
def compute(fore,capital):
  indices = fore.columns.tolist()
  port_split = init_portfolio(indices)
  cap_split = initial_capital(port_split,capital)
  return capital_variation(cap_split,index_pct(fore))

def compute_risk(fore,capital):
  portfolio_val = compute(fore,capital)

  # portfolio_pct =portfolio_var(portfolio_val)
  # portfolio_tot = portfolio_value(portfolio_val)
  # portfolio_ma = moving_avg(portfolio_val)
  return portfolio_risk(portfolio_val)

def compute_return(indices,capital):
  portfolio_val = compute(fore,capital)

  # portfolio_pct =portfolio_var(portfolio_val)
  # portfolio_tot = portfolio_value(portfolio_val)
  portfolio_ma = moving_avg(portfolio_val)
  return portfolio_return(portfolio_val,portfolio_ma)


# init_portfolio([1,2,33,4,4])