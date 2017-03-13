import quandl
import pandas as pd
import numpy as np
import pickle # python pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from statistics import mean

def create_labels(cur_hpi, fut_hpi):
    # current hpi
    # future hpi
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    return mean(values)


housing_data = pd.read_pickle('HPI.pickle')

housing_data = housing_data.pct_change()
print(housing_data.head())

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True) # to replace infinity numbers as NAN
housing_data.dropna(inplace=True) # to remove NAN

print(housing_data.head())

housing_data['US_HPI_future'] = housing_data['US benchmark'].shift(-1) #shift 1 value down and added our column to the end
# US benchmark    # US_HPI_future
#    0.004341        0.005211
#    0.005211        0.005229

print(housing_data.head())

housing_data['label'] = list(map(create_labels, housing_data['US benchmark'], housing_data['US_HPI_future']))

print(housing_data.head())
# if it goes up a value it is one
# else it is a 0

housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)

print(housing_data.tail())



