import quandl
import pandas as pd
import pickle # python pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

bridge_height = {'meters':[10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}

# how to visualize bad data? ( how to find the 6212.42?)
df = pd.DataFrame(bridge_height)
df['STD'] = pd.rolling_std(df['meters'],2) 
print(df) #the standard deviation is too big!

df_std = df.describe()['meters']['std']
print(df_std) # now we have our std

df = df[(df['STD'] < df_std) ] # this removes any point that has value bigger than the standard deviation df_std
print(df)

df['meters'].plot()
plt.show()








