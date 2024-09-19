import time
from helpers.helper import *


# Gather CSV data from file
csv_data = collect_csv_data()

# Get project url index
project_url_index = find_project_url_index(csv_data[1])

# Get reasons for each column of csv
reason_data = collect_reason_data(csv_data, project_url_index)

# Create csv file with Reason data
write_reason_column_to_csv(csv_data[0], csv_data[1], reason_data[0], reason_data[1], reason_data[2])

