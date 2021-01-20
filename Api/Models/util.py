import matplotlib.pyplot as plt
import pandas as pd
  
def plot_prediction(dataset,train_p,test_p):
  plt.plot(dataset,label= "df")
  plt.plot(train_p,label='train')
  plt.plot(test_p,label='test')
  plt.legend()
  plt.show()


def load_df (path,datesf):
  # data upload
  df = pd.read_csv("../"+path+".csv", header=0)
  # add date column
  # df['period']= datesf
  # df = df.set_index('period')
  return df