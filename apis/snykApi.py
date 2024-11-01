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

def check_if_api_url_is_valid(url):
    valid_urls = ["https://api.snyk.io","https://api.us.snyk.io","https://api.eu.snyk.io","https://api.au.snyk.io"]
    if url in valid_urls:
        return True
    else:
        return False
    
def get_snyk_api_url():
    env_value = os.getenv("SNYK_API_URL")
    
    if env_value is not None:
        snyk_api_url = env_value
        if check_if_api_url_is_valid(snyk_api_url):
            print("Environment variable found and assigned to snyk api url:", snyk_api_url)
        else:
            print("The URL is not valid.  Must be one of the following: https://api.snyk.io, https://api.us.snyk.io, https://api.eu.snyk.io, https://api.au.snyk.io.  Exiting...")
            sys.exit()
        return snyk_api_url
    else:
        snyk_api_url = "https://api.snyk.io"
        print("Environment variable not found. using default snyk api url:", snyk_api_url)
        return snyk_api_url
    
SNYK_TOKEN = get_snyk_token()

# restHeaders = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}

def get_issue_ignore_data(org_name, project_id, issue_id):
    snyk_api_url = get_snyk_api_url()
    url = f'{snyk_api_url}/v1/org/{org_name}/project/{project_id}/ignore/{issue_id}'

    try:
        ignoreDataApiResponse = requests.get(url, headers=v1Headers, verify=False)
        return ignoreDataApiResponse.json()
    except HTTPError as exc:
        # Raise an error for http error.
        print("Snyk retrieve ignore data endpoint failed.")
        print(exc)
    except:
        print("Ignore data endpoint failed with an unexpected error")

