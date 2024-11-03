import openpyxl
import pandas as pd
def get_rows_by_color(color_code):
    workbook = openpyxl.load_workbook('output.xlsx', data_only=True)
    sheet = workbook.active

# Define the RGB color for yellow
   # yellow_rgb = "FFFFFF00"  # Excel stores colors as hexadecimal strings (RGB)
    yellow_rgb = color_code
# Create a list to store rows with yellow background
    yellow_rows = []

# Iterate through the rows in the sheet
    for row in sheet.iter_rows():
        for cell in row:
            if cell.fill.start_color.rgb == yellow_rgb:
                yellow_rows.append([cell.value for cell in row[1:3]])
          
                break  # Once we find a yellow cell in the row, we can move on to the next row
    return yellow_rows

def no_matching_from_xlsx():
    return get_rows_by_color("FFFFFF00")

def match_from_xlsx():
    return get_rows_by_color("FFFFFF00")    

def write_combine_decorator(fname):
    def decorator(func):
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            try:
                df_existing = pd.read_csv(fname)
                df_combined = pd.concat([df_existing, df]).drop_duplicates(ignore_index=True)
            except FileNotFoundError:
                df_combined = df

            df_combined.to_csv(fname, index=False)

        return wrapper
    return decorator

@write_combine_decorator("no_matching.csv")
def ignore_match():
    rst = no_matching_from_xlsx()
    df = pd.DataFrame(rst,columns=['Site Name','Centre'])
    return df
    #df.to_csv("no_matching.csv",index=False)
    
@write_combine_decorator("matching.csv")
def add_2_match():
    rst = match_from_xlsx()
    df = pd.DataFrame(rst,columns=['Site Name','Centre'])
    return df

# df = ignore_match()
# 
add_2_match()
