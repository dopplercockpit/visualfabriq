import json
import csv
import os

# Specify JSON file source
json_directory = r'Enter the path to the directory containing JSON files here' #for instance, request directory path in Bifrost

# Define what is a JSON file
json_file_names = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]

# Create a dictionary for extracted data
extracted_data = []

# Prompt user for pricing condition
filter_condition = input("Enter the filter condition: ")

# Parse the JSON files (main process)
for json_file_name in json_file_names:
    print(f"Processing file: {json_file_name}")

    with open(json_file_name, 'r') as json_file:
        json_data = json.load(json_file)

        # Extract header info from JSON files
        for doc in json_data["Actuals"]["Documents"]:
            sales_org = doc["SalesOrg"]
            distr_chan = doc["DistrChan"]
            bill_doc_no = doc["BillDocNo"]
            billing_date = doc["BillingDate"]
            sold_to = doc["SoldTo"]

            # Check for 'CustHierLvl4' exists before accessing it
            customer_hier4 = doc.get("CustHierLvl4")

            # Check for 'CustHierLvl3' exists before accessing it
            customer_hier3 = doc.get("CustHierLvl3")
            
            #Set fields in document body
            for item in doc["Items"]:
                item_no = item["ItemNo"]
                pricing_date = item["PricingDate"]
                material = item["Material"]
                quantity = item["Quantity"]
                uom = item["UOM"]

                #Set fields in sub body
                for condition in item["ConditionRecords"]:
                    cond_type = condition["CondType"]
                    amount = condition["Amount"]
                    promotion = condition["Promotion"]

                    # Check for condition that matches the filter
                    if cond_type == filter_condition:
                        # Extract data and store in dictionary
                        extracted_data.append({
                            'SalesOrg': sales_org,
                            'DistrChan': distr_chan,
                            'BillDocNo': bill_doc_no,
                            'BillingDate': billing_date,
                            'SoldTo': sold_to,
                            'CustHierLvl4': customer_hier4,
                            'CustHierLvl3': customer_hier3,
                            'ItemNo': item_no,
                            'PricingDate': pricing_date,
                            'Material': material,
                            'Quantity': quantity,
                            'UOM': uom,
                            'CondType': cond_type,
                            'Amount': amount,
                            'Promotion': promotion,
                        })

# Export the extracted data to a CSV file
csv_file_name = f'extracted_json_data_{filter_condition}.csv'
with open(csv_file_name, 'w', newline='') as csv_file:
    fieldnames = ['SalesOrg', 'DistrChan', 'BillDocNo', 'BillingDate', 'SoldTo', 'CustHierLvl4', 'CustHierLvl3',
                  'ItemNo', 'PricingDate', 'Material', 'Quantity', 'UOM', 'CondType', 'Amount', 'Promotion']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in extracted_data:
        csv_writer.writerow(row)
