import os
import sys
import json
import base64
import requests

jira_url = "<jira root url>/rest/api/latest/search"
max_results_shown = 5000

# below section to be used when autheticating with JIRA API token
jira_api_token = "token"
auth_string = "Basic " + jira_api_token
auth_headers  = {
			'Authorization' : auth_string,
			'Content-Type' : 'application/json'
      }

# below section to be used when using jira user id and password to authenticate with JIRA
# jira_user = "<user name>"
# jira_usr_pswd = "<user pwd>"
# auth_string = "Basic " + (base64.b64encode('{}:{}'.format(self.user, self.pswd).encode())).decode()
# auth_headers  = {
#			'Authorization' : auth_string,
#			'Content-Type' : 'application/json'
#      } 


jira_search_query = "(project = ABCD) AND status = NEW AND resolution in (Assigned, Open)"
jira_query_data = {
			'jql'        : jira_search_query,
			'maxResults' : max_results_shown,
}

jira_query_json_data = json.dumps(jira_query_json, indent=1, ensure_ascii=False).encode('utf8')
response = requests.post(jira_url, data=jira_query_json_data, headers=auth_headers)
response_json = response.json()
print response.status_code
print response_json
