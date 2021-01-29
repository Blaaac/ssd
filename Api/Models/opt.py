import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error 

def index_pct(indexes):
  return indexes.pct_change()#.iloc[1:]

def gen_port(size):
  np.random.seed(1)
  w = np.random.uniform(low=0.05,high=1,size=size)
  # w = np.random.random(len(indices))
  # print(w)
  w /= np.sum(w)
  # print(w)
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

  init = initial_capital#.iloc[0]
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
  
def compute(fore,capital,port_split):
  
  cap_split = initial_capital(port_split,capital)
  return capital_variation(cap_split,index_pct(fore))

def compute_risk(fore,capital):
  indices = fore.columns.tolist()
  port_split = init_portfolio(indices)
  portfolio_val = compute(fore,capital,port_split)

  # portfolio_pct =portfolio_var(portfolio_val)
  # portfolio_tot = portfolio_value(portfolio_val)
  portfolio_ma = moving_avg(portfolio_val)
  return portfolio_risk(portfolio_val,portfolio_ma)

def compute_return(fore,capital):
  indices = fore.columns.tolist()
  port_split = init_portfolio(indices)
  portfolio_val = compute(fore,capital,port_split)

  # portfolio_pct =portfolio_var(portfolio_val)
  # portfolio_tot = portfolio_value(portfolio_val)
  # portfolio_ma = moving_avg(portfolio_val)
  return portfolio_return(portfolio_val)

def compute_risk_return_nocap(fore,weight,portfolio_split):
  w1=weight
  w2=1-weight
  portfolio_val = compute(fore,1,portfolio_split)
  portfolio_ma = moving_avg(portfolio_val)
  return w1*1/portfolio_risk(portfolio_val,portfolio_ma)+ w2*portfolio_return(portfolio_val)



print(init_portfolio([1,2,4,4]))
print(gen_port(3))
