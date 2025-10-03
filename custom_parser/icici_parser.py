import pandas as pd
import pdfplumber
from typing import Any

def parse(pdf_path: str) -> pd.DataFrame:
    '''Parse bank statement PDF and return DataFrame'''
    all_data: list[list[Any]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip header on each page
                    all_data.append(row)

    df = pd.DataFrame(all_data, columns=['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance'])

    # Data type conversions and cleaning
    try:
        df['Debit Amt'] = pd.to_numeric(df['Debit Amt'], errors='coerce')
        df['Credit Amt'] = pd.to_numeric(df['Credit Amt'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
    except:
        pass

    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Ensure correct number of rows
    df = df.iloc[:100]

    return df