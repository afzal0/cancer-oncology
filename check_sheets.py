import pandas as pd

xl = pd.ExcelFile('Data_final_cleaned.xlsx')
print('Sheet names:', xl.sheet_names)
print('\nRecords per sheet:')
total = 0
for sheet in xl.sheet_names:
    df = pd.read_excel('Data_final_cleaned.xlsx', sheet_name=sheet)
    print(f'  {sheet}: {len(df)} records')
    if len(df) > 0:
        print(f'    Sample suburbs: {list(df["Suburb"].unique()[:3]) if "Suburb" in df.columns else "N/A"}')
    total += len(df)
print(f'\nTotal records across all sheets: {total}')
