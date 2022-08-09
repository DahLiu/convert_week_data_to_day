import pandas as pd
from utiles import convert_week_to_date

week_data = pd.read_excel(
    'data/Calculation Example.xlsx', sheet_name='Sheet1')

converted_data = convert_week_to_date(week_data)

# output converted data to excel file named output.xlsx in data/output folder
converted_data.to_excel('data/output/output.xlsx', index=False)
