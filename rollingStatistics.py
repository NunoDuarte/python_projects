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
ax1 = plt.subplot2grid((3,1), (0,0))
ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1) #it will share the x-axis of ax1
ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1) #it will share the x-axis of ax1

HPI_data = pd.read_pickle('fiddy_states.pickle')

# Moving average
HPI_data['TX12MA'] = pd.rolling_mean(HPI_data['TX'], 12)
# when you look at the graph and the print you see that the first year doesnt have values (NaN). The problem is that the first year it didnt
# calculate the average yearly (only in December was it possible to do that) and so the first 11 months it doesnt have anything to average to
print(HPI_data[['TX', 'TX12MA']])

# Moving Standard Deviation
HPI_data['TX12STD'] = pd.rolling_std(HPI_data['TX'], 12)
print(HPI_data[['TX', 'TX12STD']])

# Moving Correlation
TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
HPI_data['TX'].plot(ax = ax1, label='TX HPI')
HPI_data['AK'].plot(ax = ax1, label='AK HPI')
ax1.legend(loc=4)
TX_AK_12corr.plot(ax=ax3, label='TX_AK_12corr')

HPI_data[['TX', 'TX12MA']].plot(ax = ax1)
HPI_data[['TX12STD']].plot(ax = ax2)
plt.legend(loc=4)
plt.show()


