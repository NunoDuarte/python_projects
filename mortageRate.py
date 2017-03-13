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
    df.rename(columns={'Value':'US benchmark'}, inplace=True)
    df = df['US benchmark']
    return df

def mortgage_30y():
    query = 'FMAC/MORTG'
    df = quandl.get(query, trim_start='1975-01-01', authtoken='SujsyC1d6nRqDVehYGxs') #I needed to go to quandl api to get a api_key
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    df = df.resample('M').mean() #sort it by the month
    df.columns = ['M30'] #because it has just one column we can just say df.columns instead of df.columns['M30']
    return df

# split shares when shares are worth too much money
def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01")
    df["Adjusted Close"] = (df["Adjusted Close"]-df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adjusted Close':'sp500'}, inplace=True)
    df = df['sp500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01")
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

# unemployment rate may be correlated with the index housing prices. If there are more people unemployed then there wont be that
# much demand and so the housing prices might go down (who knows?!)
def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01")
    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df
    


sp500 = sp500_data()
US_GDP = gdp_data()
US_unemployment = us_unemployment()


m30 = mortgage_30y()
print(m30) #it prints the initial of the month instead of HPI_data which prints the end of the months

# 
HPI_data = pd.read_pickle('fiddy_states.pickle')
print(HPI_data.head()) # it prints the end of the month

HPI_bench = HPI_benchmark()

state_HPI_M30 = HPI_data.join(m30)

print(state_HPI_M30.corr()) 
# it shows that the mortgage is a variable in the housing price. it is either an incentive or disincentive to buy a house.
# 18% over 30 years in the mortgage of the house will not incentive people to buy a house.
print(state_HPI_M30.corr()['M30'].describe())
# it shows you the mean, std, min, max of the correlation between the mortgage and the housing prices in all states


HPI = HPI_data.join([HPI_bench, m30, US_unemployment, US_GDP, sp500])

#GDP records only start at yearly 2000 and unemployment rate doesn't have values for the more recent years (for some odd reason)
# the most recent is until 2011
HPI.dropna(inplace=True)

print(HPI)
print(HPI.corr())

HPI.to_pickle('HPI.pickle') 





