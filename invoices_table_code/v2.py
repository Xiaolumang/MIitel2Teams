from PyPDF2 import PdfReader
import os
import re
import pandas as pd

# Define constants
FOLDER_PATH = '../invoices'
OUTPUT_FOLDER = 'txt'
OUTPUT_FILE = 'invoices.xlsx'

# Define column names for the DataFrame
COLS = ['Date Raised', 'Invoice No.', 'Due Date', 'Invoice Subtotal', 'GST', 'Invoice Total', 'Payments', 'Credits', 'Balance Due','Details']

def extract_from_pdf(path):
    """Extract text from a PDF file."""
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def modify_details(details):
    #if amount does not have a space before it, add a space
    pattern = re.compile(r'(?<! )\d+\.\d+ (\$[\d,]+\.\d+ ?){2}')
    details = re.sub(pattern, ' \g<0>', details)
    #remove unnecessary '\n' if it is not after money list
    return details
    # pattern = re.compile(r'(\$[\d,]+\.\d+ ?){2}')
    # rst = []
    # for line in details.splitlines():
    #     # match = re.search(pattern,line)
    #     # if match:
    #     #     print(match.group(1))

    #     line = re.sub(pattern, '\g<0>\n',line)
    #     rst.append(line)
    # return ' '.join(rst)


def match(text):
    """Extract relevant information from the text using regex patterns."""
    results = []

    # Define regex patterns
    patterns = {
        'invoice_date': r'Tax Invoice\sNumber\s(\d{2}/\d{2}/\d{4})\s(\d+)',
        'due_date': r'Due Date\s+PO Number Reference\s+.*?(\d{2}/\d{2}/\d{4})',
        'details': r'Invoice Subtotal:\s+(\$[\d.,]+)\s+GST:\s+(\$[\d.,]+)\s+Invoice Total:\s+(\$[\d.,]+)\s+Payments:\s+(\$[\d.,]+)\s+Credits:\s+(\$[\d.,]+)\s+Balance Due:\s+(\$[\d.,]+)',
        'breakdown':r'Quantity Price Amount(.*)Total : \$'
    }

    # Extract data using regex patterns
    for key, pattern in patterns.items():
        
        match = re.findall(pattern, text,re.DOTALL)
       
        if match:
            if key=='due_date':
                results.append(match[0])
            elif key == 'breakdown':
                results.append(modify_details(match[0]))
            else:
                results.extend(match[0])
        else:
            results.extend([''] * len(patterns[key].split()))

    return results

def pdf_to_txt(folder):
    """Process PDF files in the specified folder and return a list of rows."""
    rows = []
    
    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder, filename)
            text = extract_from_pdf(pdf_path)
            row = match(text)
            rows.append(row)
            
            # Optional: Save extracted text to file (uncomment if needed)
            # with open(os.path.join(OUTPUT_FOLDER, re.sub('.pdf$', '.txt', filename)), 'w') as f:
            #     f.write(text)
    
    return rows

def main():
    """Main function to process PDF files and save results to an Excel file."""
    rows = pdf_to_txt(FOLDER_PATH)
    
    
    # Create DataFrame and reorder columns
    df = pd.DataFrame(rows, columns=COLS)
    col = df.pop('Invoice No.')
    df.insert(0, 'Invoice No.', col)
    
    # Save DataFrame to Excel
    df.to_excel(OUTPUT_FILE, index=False)
    
    print(df)

if __name__ == '__main__':
    main()
    