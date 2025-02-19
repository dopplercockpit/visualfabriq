# visualfabriq
Setup for parsers that have successfully parsed through nested JSON file types used to send Sell-In, Sell-Thru,  and Sell-Out data to Visualfabriq Bifrost (Inbound messages), and Parsed through outbound messages containing financial information pertaining to promotional activity.

Visualfabriq (aka VF RGM) is a Revenue Growth Management tool that integrated with SAP, or a SAP driven data lake, and uses the data to drive a web-based Trade Promotions (TPM), and Revenue Forecast model. These tools are driven and supported by in platform Demand Planning, claims/settlement, and reporting modules. 
The challenges facing many integrations for VF, is that there is no way to reliably triage/analyse the inbound and outbound messages data, in a manner that can confidently identify flaws/gaps/errors in the data being sent from SAP/Datalake to VF Bifrost (Bifrost is the repository for VF). This is a common problem for users of Visualfabriq. 

The code snippets in this Github repository successfully setup for parsers that have successfully done the following for a major VF client (Nestlé): 

Parsed through nested JSON file types used to send Sell-In, Sell-Thru, 
and Sell-Out data to Visualfabriq Bifrost (Inbound messages)

Parsed through outbound messages containing financial information pertaining to
promotional activity.

These parsers were used to triage an issue with data in SAP vs. Visualfabriq
They could easily be adapted to setup monitoring 

The .py will need to be modified to meet each customers needs. In this particular instance, Nestlé was sending faulty information to VF but had no visibility to the errors, since the data in SAP was accurate; the issue was occuring in a middleware platform during the generation of JSON files (of which there were thousands sent daily). 

HOPE THIS HELPS SOMEONE OUT THERE
DOPPLERCOCKPIT

import json
import csv
import os

# Specify the directory where your JSON files are located
json_directory = r'Enter the path to the directory containing JSON files here' #for instance, request directory path in Bifrost

# List all JSON files in the directory
json_file_names = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]

# Create a dictionary to store the latest data based on a unique key
latest_data = {}

# Iterate through the JSON files
for json_file_name in json_file_names:
    print(f"Processing file: {json_file_name}")
    
    with open(json_file_name, 'r') as json_file:
        json_data = json.load(json_file)

        # Extract specific information from each JSON file
        for doc in json_data["Actuals"]["Documents"]:
            sales_org = doc["SalesOrg"]
            distr_chan = doc["DistrChan"]
            bill_doc_no = doc["BillDocNo"]
            billing_date = doc["BillingDate"]
            sold_to = doc["SoldTo"]
            
            # Check if the key 'CustHierLvl4' exists before accessing it - Change to correct customer hierarchy level
            customer_hier4 = doc.get("CustHierLvl4")
            
            # Check if the key 'CustHierLvl3' exists before accessing it - Change to correct customer hierarchy level
            customer_hier3 = doc.get("CustHierLvl3")

            for item in doc["Items"]:
                item_no = item["ItemNo"]
                pricing_date = item["PricingDate"]
                material = item["Material"]
                quantity = item["Quantity"]
                uom = item["UOM"]

                # Extract and process condition records
                for condition in item["ConditionRecords"]:
                    cond_type = condition["CondType"]
                    amount = condition["Amount"]
                    promotion = condition["Promotion"]

                # Create a unique key based on the combination of BillDocNo and ItemNo
                key = (bill_doc_no, item_no)

                # Check if this entry is the latest for the given key
                if key not in latest_data or billing_date > latest_data[key]['BillingDate']:
                    latest_data[key] = {
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
                    }

# Export the extracted data to a CSV file
csv_file_name = 'extract_sellin_data.csv'
with open(csv_file_name, 'w', newline='') as csv_file:
    fieldnames = ['SalesOrg', 'DistrChan', 'BillDocNo', 'BillingDate', 'SoldTo', 'CustHierLvl4', 'CustHierLvl3',
                  'ItemNo', 'PricingDate', 'Material', 'Quantity', 'UOM', 'CondType', 'Amount', 'Promotion']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in latest_data.values():
        csv_writer.writerow(row)

