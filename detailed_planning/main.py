import pandas as pd
from datetime import datetime,timedelta
import numpy as np
df = pd.read_excel('test.xlsx', sheet_name='Locations', header=1,usecols=[1,2,3,5,6,7])
df.columns = df.columns.astype(str)

df_n = pd.DataFrame()
p1 = df.loc[:101,['Centre','Location','State']].apply(lambda x: ','.join(x.astype(str)), axis=1)
p2 = df.loc[:101,['1a','1b','2']].bfill(axis=1).iloc[:,0].astype(int).astype(str)
df_n['combined'] = p1+' - '+p2

s_date = '21 Oct'
e_date = '16 Dec'

   
def gen_cols(s_date,e_date):
    rst = []
    s_date = datetime.strptime(s_date,'%d %b')
    e_date = datetime.strptime(e_date, '%d %b')
    next_date = s_date
    while next_date <= e_date:
        rst.append(next_date)
        next_date = next_date + timedelta(days=7)
    
    rst = [datetime.strftime(x, '%d %b') for x in rst]
    return rst

x = gen_cols(s_date, e_date)
x.insert(0,'')
x = dict(zip(x,['']*len(x)))
df_header = pd.DataFrame([x])
df_n.columns = ['']
df_mm = pd.concat([df_header,df_n],axis=0)
df_mm.to_excel('rst.xlsx',index=False)

#df_n.to_excel('rst.xlsx',index=False)
