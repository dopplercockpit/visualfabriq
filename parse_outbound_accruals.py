import json
import os
import pandas as pd
import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_files(json_directory, output_file):
    if not os.path.exists(json_directory):
        logging.error(f"Directory not found: {json_directory}")
        return

    json_file_names = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]
    extracted_data = []

    logging.info(f"Processing {len(json_file_names)} outbound files...")

    for json_file_name in json_file_names:
        try:
            with open(json_file_name, 'r') as json_file:
                json_data = json.load(json_file)

            accrual_doc = json_data.get("Accrual_Document", {})
            
            # Header level info
            header_info = {
                'Customer': accrual_doc.get("Customer"),
                'CompCode': accrual_doc.get("Comp_Code"),
                'SalesOrgCode': accrual_doc.get("Sales_Org_Code"),
                'DivisionCode': accrual_doc.get("Division_Code"),
                'DistChannelCode': accrual_doc.get("Dist_Channel_Code"),
                'InvestmentId': accrual_doc.get("Investment_Id"),
                'Currency': accrual_doc.get("Currency"),
                'AccrualDate': accrual_doc.get("Accrual_Date"),
            }

            # GL Codes extraction safely
            expense_section = accrual_doc.get("Expense", {})
            balance_section = accrual_doc.get("Balance", {})

            expense_gl_code = expense_section.get("Gl_Code")
            balance_gl_code = balance_section.get("Gl_Code")
            balance_amt = balance_section.get("Amt")

            # Process items
            for item in expense_section.get("Item", []):
                row = header_info.copy()
                row.update({
                    'ExpenseGlCode': expense_gl_code,
                    'MaterialCode': item.get("Material_Code"),
                    'Amount': item.get("Amt"),
                    'BalanceGlCode': balance_gl_code,
                    'BalanceAmount': balance_amt,
                })
                extracted_data.append(row)
                
        except json.JSONDecodeError:
            logging.warning(f"Skipping invalid JSON file: {json_file_name}")
        except Exception as e:
            logging.error(f"Error processing {json_file_name}: {e}")

    # Export to Excel
    if extracted_data:
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'extracted_accruals_{timestamp}.xlsx'

        try:
            df = pd.DataFrame(extracted_data)
            df.to_excel(output_file, index=False, engine='openpyxl')
            logging.info(f"Data exported to {output_file}")
        except Exception as e:
            logging.error(f"Failed to export Excel file: {e}")
    else:
        logging.info("No data extracted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Outbound Accrual JSONs.")
    parser.add_argument('--input_dir', required=True, help="Path to directory containing JSON files")
    parser.add_argument('--output_file', help="Name of the output Excel file (optional)")
    
    args = parser.parse_args()
    process_files(args.input_dir, args.output_file)
