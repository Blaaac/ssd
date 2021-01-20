import os
import pandas as pd
from matplotlib import pyplot as plot
from statsmodels.tsa.seasonal import seasonal_decompose
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
plot.rcParams['figure.figsize'] = (10.0, 6.0)
series = pd.read_csv('../GOLD_SPOT.csv',usecols=['GOLD_SPOT'], header=0)
result = seasonal_decompose(series, model='multiplicative',freq=21*12)
result.plot()
plot.show()
