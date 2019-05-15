import quandl
import pandas as pd

df = quandl.get('FMAC/HPI_AK')

#print(df.head())

fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

# this is a list
print(fiddy_states)

# this is a dataframe
print(fiddy_states[0])

#this is is a column
print(fiddy_states[0][0])

for abbv in fiddy_states[0][0][1:]:
    print('FMAC/HPI_'+str(abbv))
    
#now we just need to create our dataframes based on this values 

