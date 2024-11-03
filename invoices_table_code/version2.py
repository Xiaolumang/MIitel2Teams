from PyPDF2 import PdfReader
import os
import re
import pandas as pd

COLS = ['Date Raised','Invoice No.','Due Date','Invoice Subtotal','GST','Invoice Total','Payments','Credits','Balance Due']
FOLDER_PATH = '../invoices'
OUTPUT_FILE = 'invoices.xlsx'
def pdf_2_txt(path):
    with open(path,'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    return text

def match(text):
    patterns = {
        'p1':r'Tax Invoice\sNumber\s(\d{2}/\d{2}/\d{4})\s(\d+)',
        'p2':r'Due Date\s+PO Number Reference\s+.*?(\d{2}/\d{2}/\d{4})',
        'p3':r'Invoice Subtotal:\s+(\$[\d.,]+)\s+GST:\s+(\$[\d.,]+)\s+Invoice Total:\s+(\$[\d.,]+)\s+Payments:\s+(\$[\d.,]+)\s+Credits:\s+(\$[\d.,]+)\s+Balance Due:\s+(\$[\d.,]+)'
    }
    row = []
    for key, value in patterns.items():
        match = re.findall(value, text)
        if not match:
            row.extend(['']*value.count('('))
        if key == 'p2':
            row.extend(match)
        else:
            row.extend(match[0])
    return row

def extract_from_pdf(folder):
    rows = []
    for root,dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('pdf'):
                path = os.path.join(root, file)
                text = pdf_2_txt(path)
                
                row = match(text)
                rows.append(row)

    return rows

def transform_decorator(transform, *func_args, **func_kwargs):
    def decorator(func):
        def wrapper(*args,**kwargs):
            df = func(*args, **kwargs)
            df = transform(df,*func_args,**func_kwargs)
            return df

        return wrapper      

    return decorator

def move_column(df, col_name,index):
    c = df.pop(col_name)
    df.insert(index,col_name,c)
    return df

@transform_decorator(move_column,'Invoice No.',0)
def to_df(rows,cols ):
    df = pd.DataFrame(rows,columns=cols)
    return df

def main():
    rows = extract_from_pdf(FOLDER_PATH)
    df = to_df(rows, COLS)
    df.to_excel('invoices.xlsx',index=False)

    

main()