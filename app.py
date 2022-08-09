import pandas as pd
from utiles import flow_convert_week_to_date, inventory_convert_week_to_day

flow_week_data = pd.read_excel(
    'data/Calculation Example.xlsx', sheet_name='Sheet1')
inv_week_data = pd.read_excel(
    'data/Calculation Example.xlsx', sheet_name='Sheet2')

converted_data_flow = flow_convert_week_to_date(flow_week_data)
converted_data_inv = inventory_convert_week_to_day(inv_week_data)

# output converted data to excel file named output.xlsx in data/output folder
converted_data_flow.to_excel('data/output/flow_output.xlsx', index=False)
converted_data_inv.to_excel('data/output/inventory_output.xlsx', index=False)
