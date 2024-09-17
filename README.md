# Add ignore data to Snyk ignore report

This script will read in an ignore csv from Snyk reporting dashboard.  First you'll need to go to the group or organization reporting page.  Select the **Issue Status** dropdown menu and then select **Ignored**.  Next select **Download CSV** and set the CSV_PATH environment to the full path of it.

## Requirements

Python version 3.9.5, 3.10.0

## Environment Variables
[SNYK_TOKEN](https://docs.snyk.io/getting-started/how-to-obtain-and-authenticate-with-your-snyk-api-token)

CSV_PATH  (**Specifiy full path to csv file**)


## Example run
```bash
export SNYK_TOKEN=TYPE-SNYK-TOKEN-HERE
export CSV_PATH=FULL-PATH-TO-CSV
git clone https://github.com/snyk-labs/add-ignore-reason-to-csv-report.git
pip install -r requirements.txt
python3 index.py
```
