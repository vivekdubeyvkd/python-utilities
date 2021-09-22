import sys
import json
import requests

'''
    usage:
    python create_jira.py "[jira summary]" "[jira description]" "[assign jira to user]" "[jira rest api user]" "[jira rest api user password]"
'''

JIRA_ROOT_URL = "[yout root jira]"
JIRA_API_URL = JIRA_ROOT_URL + '/rest/api/2/issue/'

def callApi(apiURL, payloadData, jiraUser, jiraPwd):
  try:
      r = requests.post(url = apiURL, json = payloadData,  auth=(jiraUser, jiraPwd))
      
      jsonData = r.json()
      if "errors" in jsonData:
         print(jsonData['errors'])
      else:  
        return jsonData
  except Exception as ex:
      print(ex)

def createJira(summary, description, assignTo, jiraUser, jiraPwd):
    # you can chage the issuetype in jsonPayload as per your requirement like Task, bug etc 
    jsonPayload =   {
    "fields":
        {
            "project":{"key": "QBWG"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"},
            "customfield_111111": {"yourKey": "your Value"},
            "customfield_111112": {"yourKey": "your Value"},
            "customfield_111112":  {"yourValue": "your Value"},
            "assignee": {"name": assignTo},
            "components" : [{"yourKey" : "yourValue"}]
        }
    }
    jsonData = callApi(JIRA_API_URL, jsonPayload, jiraUser, jiraPwd)
    if jsonData and "key" in jsonData:
        print(" JIRA is => " + JIRA_ROOT_URL + "/browse/" + jsonData['key'])
        print("")

def validateArgs(scriptArgs):
    if scriptArgs and len(scriptArgs) == 5:
        return "valid"
    else:
        return

def main(scriptArgs):
    if validateArgs(scriptArgs):
        summary = scriptArgs[0]
        description = scriptArgs[1]
        assignTo = scriptArgs[2]
        jiraUser = scriptArgs[3]
        jiraPwd = scriptArgs[4]
        # create a new jira
        createJira(summary, description, assignTo, jiraUser, jiraPwd)
    else:
        print("invalid args, please check and rerun again .......")

if __name__ == "__main__":
    scriptArgs = sys.argv[1:]
    main(scriptArgs)
