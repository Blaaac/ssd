import numpy as np
import pandas as pd

def init_portfolios(indices):
  weights = {}
  w = np.random.random(len(indices))
  w /= np.sum(w)
  for i in range(len(indices)):
    weights[indices[i]] = w[i]
  return weights

def initial_capital(portfolio,capital):
  return {k: float(capital)*v for k, v in portfolio.items()}