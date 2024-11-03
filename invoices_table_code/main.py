from PyPDF2 import PdfReader
import os
import re
import pandas as pd

folder = '../invoices'
path = os.path.join(folder, '106602.pdf')
# Open the PDF file


def extract_from_pdf(path):
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            return text

# Path to your PDF file
#invoice no, date raised, Due date, amount (ex GST), details 

# Open the PDF file
cols = ['Date Raised','Invoice No.','Due Date','Invoice Subtotal','GST','Invoice Total','Payments','Credits','Balance Due']
def pdf_2_txt(folder):
    folder_name = 'txt'
    rows = []
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for filename in os.listdir(folder):
        if filename.endswith('pdf'):
            #print(filename)
            pdf_path = os.path.join(folder, filename)
            row = match(extract_from_pdf(pdf_path))
            rows.append(row)
    return rows       
            # 
            # with open(os.path.join(folder_name, re.sub('pdf','txt',filename)),'w') as f:
            #     f.write(extract_from_pdf(pdf_path))


def match(text):
    rst = []
    p1 = 'Tax Invoice\sNumber\s(\d{2}/\d{2}/\d{4})\s(\d+)'
    rst1 = re.findall(p1, text)
   
    p2 = 'Due Date\s+PO Number Reference\s+.*?(\d{2}/\d{2}/\d{4})'
    rst2 = re.findall(p2, text)
    p3 = "Invoice Subtotal:\s+(\$[\d.,]+)\s+GST:\s+(\$[\d.,]+)\s+Invoice Total:\s+(\$[\d.,]+)\s+Payments:\s+(\$[\d.,]+)\s+Credits:\s+(\$[\d.,]+)\s+Balance Due:\s+(\$[\d.,]+)"
    rst3 = re.findall(p3, text)
    rst.extend(list(rst1[0]))
    rst.extend(rst2)
    rst.extend(list(rst3[0]))
    return rst


rows = pdf_2_txt(folder)
df = pd.DataFrame(rows,columns=cols)
col = df.pop('Invoice No.')
df.insert(0,'Invoice No.',col)
df.to_excel('invoices.xlsx',index=False)
print(df)
exit(0)


