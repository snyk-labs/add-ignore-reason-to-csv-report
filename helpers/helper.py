import json
import os
import re
import sys
import csv
import time

from apis.snykApi import get_issue_ignore_data

def collect_csv_data():

    file_path = get_csv_path_token()
    csv_data = []
    header_data = []

    # Open the CSV file
    try:
        with open(file_path, mode='r', newline='') as file:
            # Create a CSV reader object
            reader = csv.reader(file)
            
            # Read the header
            header = next(reader)
            header_data = header
            
            for row in reader:
                csv_data.append(row)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to open '{file_path}'.")
    except csv.Error as e:
        print(f"Error: CSV file format error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return csv_data, header_data

def collect_reason_data(csv_data, project_url_index):
    print('Collecting reason data for ignores.')
    reason_data = []
    ignore_reporter = []
    expire_date = []

    for row in csv_data[0]:
        if project_url_index != None:
            data = row[project_url_index].split("/")
            issue_id = row[project_url_index].split("issue-")
            issue_id = issue_id[1]
            org_name = data[4]
            match = re.search(r'([\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12})', row[project_url_index])

            if match:
                project_id = match.group(0)

            issue_ignore_data = get_issue_ignore_data(org_name, project_id, issue_id)

            if len(issue_ignore_data) > 0:
                for i, index in enumerate(issue_ignore_data):
                    nested_dict = index.get('*', {})
                    reason = nested_dict['reason']
                    user = nested_dict['ignoredBy']['name']
                    expiration_date = ""
                    # Check if expires attribute exist
                    if "expires" in nested_dict:
                        # Find first expiration date
                        # expiration_value = nested_dict['expires']
                        if nested_dict['expires']:
                            expiration_date = nested_dict['expires']
                        else:
                            expiration_date = 'No expiration date specified'
                    else:
                        expiration_date = 'No expiration date specified'
                    if reason != "":
                        reason_data.append(reason)
                        ignore_reporter.append(user)
                        expire_date.append(expiration_date)
                        break
                    if i == len(issue_ignore_data)-1:
                        reason_data.append('No reason provided')
                        ignore_reporter.append(user)
                        expire_date.append(expiration_date)
                        break
            else:
                reason_data.append('Api failed to retrieve list of ignores')
                ignore_reporter.append(user)
                expire_date.append('No expiration date specified')
            
    return reason_data, ignore_reporter, expire_date

def write_reason_column_to_csv(csv_data, header, reason_data, ignore_reporter, expire_date):
    print('Creating new csv file with reason data')
    # Adding Reason to header of csv
    header.extend(['REASON', 'IGNORE REPORTER', 'EXPIRATION DATE'])

    # Add a reason column to each row
    expire_limit = len(expire_date)
    new_reason_csv = []
    for index, row in enumerate(csv_data):
        true_index = index - 1
        # Add reason data, reporter, and the first expire date        
        new_row_data = [reason_data[true_index], ignore_reporter[true_index], expire_date[true_index]]
        row.extend(new_row_data)
        new_reason_csv.append(row)
        
    try:
        with open('ignore_reason_report.csv', mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            
            # Write the updated header
            writer.writerow(header)
            
            # Write the updated rows
            writer.writerows(new_reason_csv)

    except FileNotFoundError:
        print(f"Error: Ignore_reason_report.csv was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to open ignore_reason_report.csv.")
    except csv.Error as e:
        print(f"Error: CSV file format error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def find_project_url_index(header_list):
    project_url = 'ISSUE_URL'
    
    for position, header in enumerate(header_list):
        if header == project_url:
            return position

    print(f"'{project_url}' is not in the list.")
        

def get_csv_path_token():
    CSV_PATH = check_if_csvpath_token_exist()
    return CSV_PATH

def check_if_csvpath_token_exist():
    print("Checking for CSV_PATH token environment variable")
    try:
        if os.environ.get('CSV_PATH'):
            print("Found CSV_PATH token.")
            return os.getenv('CSV_PATH')
    except:
        print("CSV_PATH token does not exist")
        sys.exit()