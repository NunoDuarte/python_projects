import pandas as pd

df = pd.read_csv('ZILL-Z84061_MLP.csv')

print(df.head())

df.set_index('Date', inplace=True)
df.to_csv('newcsv2.csv')

df = pd.read_csv('newcsv2.csv', index_col=0)
print(df.head()) # it has the same random index because you havent defined the in (add index_col=0)

df.columns = ['Austin_HPI'] 
print(df.head()) #to change the name of a column

df.to_csv('newcsv3.csv')

df.to_csv('newcsv4.csv', header=False) #if you only want data (no column's names)

df = pd.read_csv('newcsv4.csv', names=['Date', 'Austin_HPI'], index_col=0)
print(df.head())

#lets convert to html.  It converts to a html table
df.to_html('example.html')

df = pd.read_csv('newcsv4.csv', names=['Date', 'Austin_HPI'])
print(df.head())

#if you want to change the column's name
df.rename(columns={'Austin_HPI':'77006_HPI'}, inplace=True)
print(df.head())




