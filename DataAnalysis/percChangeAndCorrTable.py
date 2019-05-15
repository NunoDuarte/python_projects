import quandl
import pandas as pd
import pickle # python pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]

def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()
    
    for abbv in states:
        query = 'FMAC/HPI_'+str(abbv)
        df = quandl.get(query, authtoken='SujsyC1d6nRqDVehYGxs') #I needed to go to quandl api to get a api_key
        df.rename(columns={'Value':str(abbv)}, inplace=True) # to ensure each column has a different name (it gives error without)
        #df = df.pct_change()
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0
        
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
            
    print(main_df.tail())
    
    pickle_out = open('fiddy_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
def HPI_benchmark():
    query = 'FMAC/HPI_USA'
    df = quandl.get(query, authtoken='SujsyC1d6nRqDVehYGxs') #I needed to go to quandl api to get a api_key
    #df.rename(columns={'Value':'USA'}, inplace=True) # to ensure each column has a different name (it gives error without)
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    return df

#grab_initial_state_data()    
fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))

HPI_data = pd.read_pickle('fiddy_states.pickle')
print(HPI_data)
HPI_data['TX2'] = HPI_data['TX'] * 2
print(HPI_data[['TX', 'TX2']])
HPI_data.plot(ax=ax1)

benchmark = HPI_benchmark()
benchmark.plot(ax=ax1, color= 'k', linewidth=10)

plt.legend().remove()
plt.show()

#correlation table for all of the columns
HPI_State_Correlation = HPI_data.corr()

# 50 by 50 correlation (all states for all states)
print(HPI_State_Correlation)

print(HPI_State_Correlation.describe())






