import sys
import os
import json
import requests
import re

'''
  Script Name : add_comments_using_jira_search_query_to_ira_tickets.py
  Purpose     : This utility lists JIRA based on input JIRA search query and updates the JIRA with custom input comment provided by the user.
                It works as follows:
                1. Scans all open issues based on input JIRA search query
                2. Parses scan results to list all JIRAs
                3. Finds JIRA defect Key/ID for every JIRA issue found in scan result
                4. Updated the JIRA ticket using custom input comment
  Author      : Vivek Dubey
'''

# Update the JIRA API URL as per your JIRA instance URL
JIRA_API_URL = 'https://api.jira.com/rest/api/2/search'

def call_jira_api(requestType, apiURL, headers, payloadData, jiraUser, jiraPwd):
    try:
        # if you want to use a service user named service_user_name, replace service_user_name with your service user name in below line
        if jiraUser == "service_user_name":
            r = requests.request(requestType, url = apiURL, params = payloadData,  auth=(jiraUser, jiraPwd))
        else: 
            r = requests.request(requestType, url = apiURL, params = payloadData,  headers={'Authorization': 'Bearer {}'.format(jiraPwd)})
        jsonData = r.json()
        if "errors" in jsonData:
            print(jsonData['errors'])
        else:
            return jsonData
    except Exception as ex:
            print(ex)

def call_jira_post_api(apiURL, payloadData, jiraUser, jiraPwd):
    try:
        # if you want to use a service user named service_user_name, replace service_user_name with your service user name in below line
        if jiraUser == "service_user_name":
            r = requests.post(url = apiURL, json = payloadData,  auth=(jiraUser, jiraPwd))
        else:    
            r = requests.post(url = apiURL, json = payloadData,  headers={'Authorization': 'Bearer {}'.format(jiraPwd)})
        jsonData = r.json()
        if "errors" in jsonData:
            print(jsonData['errors'])
        else:
            return jsonData
    except Exception as ex:
            print(ex)

def updateJiraComment(jiraComment, jiraIssue, jiraUser, jiraPwd):
    apiURL = "https://api.jira.com/rest/api/2/issue/" + jiraIssue + "/comment"
    print(jiraComment)
    #jsonPayload =  {
    #    "type":"mention",
    #    "body": "[Auto Comment]" + jiraComment
    #}
    jsonPayload =  {
        "type":"mention",
        "body": jiraComment
    }    
    call_jira_post_api(apiURL, jsonPayload, jiraUser, jiraPwd)

def update_jira_with_custom_comments(queryString, customJiraComment, jiraUser, jiraPwd):
    headers = {
        "Accept": "application/json"
    }
    print("\nInput JIRA Query: " + queryString)
    startAt = 0
    total = 1
    maxResults = 100
    allJiraJsonData = []
    query = {
        'jql': queryString,
        'startAt' : startAt,
        'maxResults': maxResults
    }
    while startAt <= total:
        jsonData = call_jira_api('GET', JIRA_API_URL, headers, query, jiraUser, jiraPwd)
        allJiraJsonData += jsonData['issues']
        startAt += maxResults
        total = jsonData['total']

    for issue in allJiraJsonData:
        jiraSummary = issue["fields"]["summary"]
        print(issue["key"])
        # call update JIRA comment function to add custom comments
        updateJiraComment(customJiraComment, issue["key"], jiraUser, jiraPwd)        

def validateScriptArgs(scriptArgs):
    if scriptArgs and len(scriptArgs) == 4:
        return "valid"
    else:
        return

def main(scriptArgs):
    if validateScriptArgs(scriptArgs):
        inputJiraQuery = scriptArgs[0]
        inputJIRAComment = scriptArgs[1]
        # service user name as 3rd input parameter to script
        jiraUser = scriptArgs[2]
        # password for service user as password or JIRA personal access token for other normal users to avoid SSO push for each rest API call in cases where JIRA instance is integrated with SSO push
        jiraPwd = scriptArgs[3]
        if inputJiraQuery and inputJIRAComment:
            update_jira_with_custom_comments(inputJiraQuery, inputJIRAComment, jiraUser, jiraPwd)
        else:
            print("++++++++++++++++++++++++++++++++++++ ERROR ++++++++++++++++++++++++++++++++++++")
            print("Invalid input parameters passed , kindly check and rerun ..... exiting ....") 
            print("Script to be run as:")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
            print("      python3 add_comments_using_jira_search_query_to_ira_tickets.py [JIRA Search Query for Target JIRA tickets] [Custom Input Comment] [JIRA Username] [JIRA password]")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")             
    else:
        print("++++++++++++++++++++++++++++++++++++ ERROR ++++++++++++++++++++++++++++++++++++")
        print("Invalid input parameters passed , kindly check and rerun ..... exiting ....") 
        print("Script to be run as:")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
        print("      python3 add_comments_using_jira_search_query_to_ira_tickets.py [JIRA Search Query for Target JIRA tickets] [Custom Input Comment] [JIRA Username] [JIRA password]")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 

if __name__ == "__main__":
    scriptArgs = sys.argv[1:]
    main(scriptArgs)
