import json
import csv
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_files(json_directory, filter_condition, output_file):
    if not os.path.exists(json_directory):
        logging.error(f"Directory not found: {json_directory}")
        return

    json_file_names = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]
    extracted_data = []

    logging.info(f"Filtering for condition '{filter_condition}' in {len(json_file_names)} files...")

    for json_file_name in json_file_names:
        try:
            with open(json_file_name, 'r') as json_file:
                json_data = json.load(json_file)

            documents = json_data.get("Actuals", {}).get("Documents", [])

            for doc in documents:
                header_info = {
                    'SalesOrg': doc.get("SalesOrg"),
                    'DistrChan': doc.get("DistrChan"),
                    'BillDocNo': doc.get("BillDocNo"),
                    'BillingDate': doc.get("BillingDate"),
                    'SoldTo': doc.get("SoldTo"),
                    'CustHierLvl4': doc.get("CustHierLvl4"),
                    'CustHierLvl3': doc.get("CustHierLvl3"),
                }

                for item in doc.get("Items", []):
                    base_item_info = {
                        'ItemNo': item.get("ItemNo"),
                        'PricingDate': item.get("PricingDate"),
                        'Material': item.get("Material"),
                        'Quantity': item.get("Quantity"),
                        'UOM': item.get("UOM"),
                    }

                    for condition in item.get("ConditionRecords", []):
                        if condition.get("CondType") == filter_condition:
                            row = header_info.copy()
                            row.update(base_item_info)
                            row.update({
                                'CondType': condition.get("CondType"),
                                'Amount': condition.get("Amount"),
                                'Promotion': condition.get("Promotion"),
                            })
                            extracted_data.append(row)

        except json.JSONDecodeError:
            logging.warning(f"Skipping invalid JSON file: {json_file_name}")
        except Exception as e:
            logging.error(f"Error processing {json_file_name}: {e}")

    # Export
    if output_file is None:
        output_file = f'extracted_json_data_{filter_condition}.csv'

    if extracted_data:
        fieldnames = ['SalesOrg', 'DistrChan', 'BillDocNo', 'BillingDate', 'SoldTo', 
                      'CustHierLvl4', 'CustHierLvl3', 'ItemNo', 'PricingDate', 
                      'Material', 'Quantity', 'UOM', 'CondType', 'Amount', 'Promotion']
        try:
            with open(output_file, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                for row in extracted_data:
                    csv_writer.writerow(row)
            logging.info(f"Export complete: {output_file}")
        except IOError as e:
            logging.error(f"Could not write file: {e}")
    else:
        logging.info("No records matched the filter condition.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter Inbound JSONs by Pricing Condition.")
    parser.add_argument('--input_dir', required=True, help="Path to directory containing JSON files")
    parser.add_argument('--filter_condition', required=True, help="The condition type to filter for (e.g., ZPR1)")
    parser.add_argument('--output_file', help="Name of the output CSV file (optional)")
    
    args = parser.parse_args()
    process_files(args.input_dir, args.filter_condition, args.output_file)
