import comm
import pandas as pd
import os
from match_rule import handlerChain
import numpy as np

def filter_rows_decorator(func):
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        try:
            df_ignore = pd.read_csv("no_matching.csv")
            df_merged = df.merge(df_ignore, on=["Centre","Site Name"], how="left",
                                 indicator=True)
            df_filtered = df_merged[df_merged["_merge"]=="left_only"].drop(columns="_merge")
            return df_filtered
        except FileNotFoundError:
            return df


    return wrapper

def replace_centre_decorator(func):
    def wrapper(*args, **kwargs):
        # Apply the transformation using the function
        df = func(*args, **kwargs)
        # Perform the condition and transformation within the decorator
        df['Centre'] = df.apply(lambda row: row['Location'] + ' ' + row['Centre'] 
                                if row['Centre'] == 'Salvos Stores' else row['Centre'], axis=1)
        return df
    return wrapper



def remove_bottom_rows_decorator(num):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            df = df.iloc[:-num]
            return df
        return wrapper
    return decorator


# Decorator for renaming columns
def rename_columns(columns_mapping):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            return df.rename(columns=columns_mapping)
        return wrapper
    return decorator

def merge_decorator(merge_contact):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            return merge_contact(df)
        return wrapper
    return decorator

def reorder_decorator(reorder_column,*reorder_args, **reorder_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            df = reorder_column(df, *reorder_args, **reorder_kwargs)
           # print(df.columns)
            return df
        return wrapper
    return decorator

def contact_2_df(path,sheet_name):
    df = pd.read_excel(path, sheet_name=sheet_name)
    return df

def custom_merge(df1, df2):
    columns_1 = df1.columns
    columns_2 = df2.columns

    rst_df = []
    for index, row in df1.iterrows():
      
        valueA = row['Centre']
        
        lst = [list(row)+list(row2) for _, row2 in df2.iterrows() if handlerChain.handle(valueA, row2['Site Name'])]
        if not lst:
            lst = [list(row)] 
        df = pd.DataFrame(lst)
        rst_df.append(df)
    rst_df = pd.concat(rst_df)
    rst_df.columns =list(columns_1)+list(columns_2)
    return rst_df

def merge_contact(df):
    path = os.path.join(comm.folder,  comm.contact_file)
    df2 = contact_2_df(path, comm.sheet_name_contact) 
    df2 = df2.drop(columns= ["Facilities Contact Name",
                             "Facilities Contact Phone",
                             "Facilities Contact Email"])
    
    #result = pd.merge(df, df2, how='left', left_on='Centre', right_on = "Site Name")
    result = custom_merge(df, df2)
    return result

def reorder_column(df, column_name, index):
    column_lst = df.columns.tolist()
    column_lst.remove(column_name)
    column_lst.insert(index, column_name)
    df = df[column_lst]
    return df

def check_result_diff_decorator(fname):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            
            try:
                df_old = pd.read_excel(fname)
                
                   
                #print(df_old.iloc[19])
                df_diff = df.merge(df_old, how="left", indicator=True)
                df_diff = df_diff[df_diff['_merge']=="left_only"]
                #print(df_diff.iloc[2])
             
                return df_diff
            except FileNotFoundError:
                print("no file to compare...")
                return df
        
        return wrapper
    return decorator

def get_cname(row):
    if pd.isna(row['Site Contact Name']):
        for x in [row['Primary Contact'],row['Secondary Site Contact']]:
            if x and not pd.isna(x):
                return f'person: {x}'
            else:
                return ''
    else:
        return ''
def get_cDetails(row):
    if pd.isna(row['Site Contact details']) and pd.isna(row['Site Contact details.1']):
        for x in [row['Primary Contact Email'],row['Primary Contact Phone'],
                  row['Secondary Contact Email'], row['Secondary Contact Phone']]:
            if x and not pd.isna(x):
                return f'email or phone: {x}'
            else:
                return ''
    else:
        return ''           
def matching_name_from_another_source(row):
    site_name = row['Site Name']
    if site_name and not pd.isna(site_name):
        return f'matches to {site_name}'  
    else:
        return ''

def supplementary_info(row):
    if pd.isna(row['Site Contact Name']) or pd.isna(row['Site Contact details']) or pd.isna(row['Site Contact details.1']):       
        return f'{matching_name_from_another_source(row)}\n{get_cname(row)}\n{get_cDetails(row)}'
    else:
        return ''  
def add_contact_columns(func):
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        df['Supplementary'] = df.apply(supplementary_info,axis=1)
        return df

    return wrapper

@add_contact_columns    
#@check_result_diff_decorator("output copy.xlsx")
#@filter_rows_decorator
@reorder_decorator(reorder_column,'Site Name',1)
@merge_decorator(merge_contact)
@remove_bottom_rows_decorator(7)
@replace_centre_decorator
def mitel_2_df(path, sheet_name,skiprows=1):
    df = pd.read_excel(path, sheet_name=sheet_name,skiprows=skiprows)
    print("hello")
    return df


path = os.path.join(comm.folder, comm.file)
df = mitel_2_df(path, comm.sheet_name_mitel,1)

print(df['Site Name'].notnull().sum())
print(df[df['Supplementary'].notna()])
df.to_excel(comm.output_file,index=False)
