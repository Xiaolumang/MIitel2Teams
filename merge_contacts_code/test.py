import csv
import pandas as pd
import numpy as np
print(' english' in 'what is english')
exit(0)
fname = "no_matching copy.csv"
fname2 = "del.csv"
df = pd.read_csv(fname)
df2 = pd.read_csv(fname2)
df = pd.concat([df,df2])
def get_name(row):
    if str(row['job']) == 'tutor' or  'English'.lower() in str(row['occupation']).lower():
        return row['name']
    else:
        return ""

df['sup']=df.apply(get_name,axis=1)
print(df)

        
