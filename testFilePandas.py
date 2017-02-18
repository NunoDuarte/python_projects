#what is pandas?
# it works with data frames (like a spread sheet)
#  it is a lot like an excel spread sheet
#  but excel gets slow with medium to big data

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

import numpy as np

#Bounce_Rate is the percentage of people that go to your website and leave immediately

web_stats = {'Day': [1,2,3,4,5,6],
             'Visitors': [43,53,34,45,64,34],
             'Bounce Rate': [65,72,62,64,54,66]}

df = pd.DataFrame(web_stats)


#print(df)
#print(df.head(2)) #first 2
#print(df.tail(1)) #last one

# it creates a new data frane
print(df.set_index('Day'))
print(df)

# if you want to change the current data frame
df.set_index('Day', inplace=True)
print(df)

# you can write just a column two ways (note if the column has two words)
print(df['Visitors'])
print(df.Visitors)

#print more than one column
print(df[['Bounce Rate', 'Visitors']])

# convert a column to a list
print(df.Visitors.tolist())

# convert two columns to an array (need numpy)
print(np.array(df[['Bounce Rate', 'Visitors']]))

#can I transform an array to a panda library?
df2 = pd.DataFrame(np.array(df[['Bounce Rate', 'Visitors']]))
print(df2)
#yes, we can. It just gave it numbered columns and simple index of lines