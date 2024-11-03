import pandas as pd
from datetime import datetime, timedelta
df = pd.read_excel('test.xlsx',sheet_name='Locations',usecols=[1,2,3,5,6,7],header=1)
df.columns = df.columns.astype(str)
#print(df.columns)
df_n = pd.DataFrame()
df_n['combined'] = df.loc[:101, ['Centre','Location','State']].apply(lambda x:', '.join(x),axis=1)
df_n['filled'] = df.loc[:101,['1a','1b','2']].bfill(axis=1).iloc[:,0].astype(int).astype(str)
df_n['combined'] = df_n['combined']+' - '+ df_n['filled']
def get_cols(s_date, e_date):
    s_date, e_date = datetime.strptime(s_date,'%d %b'), datetime.strptime( e_date,'%d %b')
    rst = []
    n_date = s_date
    while True:
        if n_date > e_date:
            break
        rst.append(datetime.strftime(n_date,'%d %b'))
        n_date = n_date + timedelta(days=7)
    return rst

cols = get_cols('21 Oct','16 Dec')
cols.insert(0,'')

df_1 = pd.DataFrame([dict(zip(cols,['']*len(cols)))])
df_n = df_n.iloc[:,[0]]
df_n.columns = ['']

df_n = pd.concat([df_1, df_n],ignore_index=True,axis=0)
print(df_n.head(3))


