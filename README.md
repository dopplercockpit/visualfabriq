# Visualfabriq Data Parsers

This repository contains a set of Python utilities designed to triage and validate data integration between SAP (or data lakes) and Visualfabriq Bifrost. 

These tools address common visibility challenges by parsing the raw JSON message payloads used for:
1.  **Inbound Messages**: Sell-In, Sell-Thru, and Sell-Out data sent to Bifrost.
2.  **Outbound Messages**: Financial information regarding promotional activity (Accruals).

## Scripts

### 1. `parse_inbound_latest.py` (formerly sunking.py)
Parses a directory of JSON files to extract the **latest** state of documents based on `BillingDate`. It handles duplicates by retaining only the most recent entry for a unique `BillDocNo` + `ItemNo` combination.

**Usage:**
```bash
python parse_inbound_latest.py --input_dir "./data/json_files" --output_file "latest_sellin_data.csv"
