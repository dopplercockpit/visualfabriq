import json
import csv
import os
import pandas as pd
from datetime import datetime 

# Specify the directory where your JSON files are located
json_directory = r'Enter the path to the directory containing JSON files here' #for instance, request directory path in Bifrost

# List all JSON files in the directory
json_file_names = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]

# Create a list to store the extracted data
extracted_data = []

# Iterate through the JSON files
for json_file_name in json_file_names:
    print(f"Processing file: {json_file_name}")

    with open(json_file_name, 'r') as json_file:
        json_data = json.load(json_file)

        # Access the Accrual_Document section
        accrual_document = json_data["Accrual_Document"]
        customer = accrual_document["Customer"]
        comp_code = accrual_document["Comp_Code"]
        sales_org_code = accrual_document["Sales_Org_Code"]
        division_code = accrual_document["Division_Code"]
        dist_channel_code = accrual_document["Dist_Channel_Code"]
        investment_id = accrual_document["Investment_Id"]
        currency = accrual_document["Currency"]
        accrual_date = accrual_document["Accrual_Date"]
        
        # Extract GL codes from Expense and Balance (MOVED HERE FROM THE END OF THE SCRIPT)
        expense_gl_code = accrual_document["Expense"]["Gl_Code"]
        balance_gl_code = accrual_document["Balance"]["Gl_Code"]
        balance_amt = accrual_document["Balance"]["Amt"]

        # Iterate through each item in the Expense
        for item in accrual_document["Expense"]["Item"]:
            material_code = item["Material_Code"]
            amount = item["Amt"]

            # Store the extracted data
            extracted_data.append({
                'Customer': customer,
                'CompCode': comp_code,
                'SalesOrgCode': sales_org_code,
                'DivisionCode': division_code,
                'DistChannelCode': dist_channel_code,
                'InvestmentId': investment_id,
                'Currency': currency,
                'AccrualDate': accrual_date,
                'ExpenseGlCode': expense_gl_code,  # Added these fields
                'MaterialCode': material_code,
                'Amount': amount,
                'BalanceGlCode': balance_gl_code,  # Added these fields
                'BalanceAmount': balance_amt,      # Added these fields
            })
  
# Convert the extracted data to a pandas DataFrame
df = pd.DataFrame(extracted_data)

# Generate a timestamp for the file name
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Specify the Excel file name
excel_file_name = f'extracted_json_data_{timestamp}.xlsx'

# Export the DataFrame to an Excel file
df.to_excel(excel_file_name, index=False, engine='openpyxl')
print(f"Data has been exported to {excel_file_name}")