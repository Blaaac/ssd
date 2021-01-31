import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error 

def index_pct(indexes):
  return indexes.pct_change()#.iloc[1:]

def gen_port(size):
  np.random.seed(1)
  w = np.random.uniform(low=0.05,high=1,size=size)
  w /= np.sum(w)
  return w


def array_to_portfolio(w,indices):
  weights = {}
  for i in range(len(w)):
    weights[indices[i]] = w[i]
  return pd.DataFrame(weights, index = [0])

def init_portfolio(indices):
  w = gen_port(len(indices))
  return array_to_portfolio(w,indices)


def initial_capital(portfolio,capital):
  return portfolio*float(capital)

def capital_variation(initial_capital,pctchg):
  init = initial_capital
  pctchg = pctchg.reset_index(drop=True)
  res = ((1+ pctchg).cumprod() * init)
  #reinsert initial val in head
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
  return mean_squared_error(moving_avg,portfolio[days+1:],squared=False)
  
def compute(fore,capital,port_split):
  cap_split = initial_capital(port_split,capital)
  return capital_variation(cap_split,index_pct(fore))

def compute_risk(fore,capital):
  indices = fore.columns.tolist()
  port_split = init_portfolio(indices)
  portfolio_val = compute(fore,capital,port_split)

  portfolio_ma = moving_avg(portfolio_val)
  return portfolio_risk(portfolio_val,portfolio_ma)

def compute_return(fore,port_split,capital):
  portfolio_val = compute(fore,capital,port_split)

  return portfolio_return(portfolio_val)

def compute_risk_return_nocap(fore,weight,portfolio_split):
  w1=weight
  w2=1-weight
  portfolio_val = compute(fore,1,portfolio_split)
  portfolio_ma = moving_avg(portfolio_val)
  risk = portfolio_risk(portfolio_val,portfolio_ma)
  ret = portfolio_return(portfolio_val)
  return w1*1/risk+ w2*ret



print(init_portfolio([1,2,4,4]))
print(gen_port(3))
