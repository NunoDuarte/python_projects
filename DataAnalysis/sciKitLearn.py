import quandl
import pandas as pd
import numpy as np
import pickle # python pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from statistics import mean
from sklearn import svm, preprocessing, cross_validation

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

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True) # to replace infinity numbers as NAN
housing_data.dropna(inplace=True) # to remove NAN
housing_data['US_HPI_future'] = housing_data['US benchmark'].shift(-1) #shift 1 value down and added our column to the end
housing_data['label'] = list(map(create_labels, housing_data['US benchmark'], housing_data['US_HPI_future']))

print(housing_data.head())

X = np.array(housing_data.drop(['label','US_HPI_future'], 1))
X = preprocessing.scale(X)
y = np.array(housing_data['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

print(clf.score(X_test, y_test))




