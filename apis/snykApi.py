import requests
from requests.exceptions import HTTPError
import os
import re
import sys

def check_if_snyk_token_exist():
    print("Checking for Snyk token environment variable")
    try:
        if os.environ.get('SNYK_TOKEN'):
            print("Found snyk token")
            return os.getenv('SNYK_TOKEN')
    except:
        print("Snyk token does not exist")
        sys.exit()

def get_snyk_token():
    SNYK_TOKEN = check_if_snyk_token_exist()
    
    pattern = re.compile(r'([\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12})')
    if pattern.fullmatch(SNYK_TOKEN) == None:
        print("Snyk token is not defined or not valid.")
        sys.exit()
    else:
        return SNYK_TOKEN

    
SNYK_TOKEN = get_snyk_token()

# restHeaders = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}

def get_issue_ignore_data(org_name, project_id, issue_id):
    url = f'https://api.snyk.io/v1/org/{org_name}/project/{project_id}/ignore/{issue_id}'

    try:
        ignoreDataApiResponse = requests.get(url, headers=v1Headers)
        return ignoreDataApiResponse.json()
    except HTTPError as exc:
        # Raise an error for http error.
        print("Snyk retrieve ignore data endpoint failed.")
        print(exc)

