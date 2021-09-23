import sys
import json
import requests
import os

'''
  Script Name : get_github_users_without_public_email.py
  Purpose     : To get all users on a GitHub org who has not updated their public email on their GitHub profile
  Usage       : to be run as
                [python/python3] get_github_users_without_public_email.py [your GitHub org] [github user to be used for rest api calls] [GitHub PAT for github user to be used for rest api calls]
                GitHub PAT => GitHub personal access token with appropriate access in place to work with GitHub rest API calls
                # script ignores the GitHub users in suspended state
                
                ** First test this script in some testing environment to see how it behaves and then only start using it on any PROD environment **
                
  Author      : Vivek Dubey
  Copyright   : Intuit Inc @ 2021
'''

OUTPUT_FILE_PATH = "github_user_with_no_public_email.csv"
GITHUB_API_URL = 'https://api.github.com//api/v3/orgs/'

def call_api(apiURL, githubUser, githubPwd):
    try:
        r = requests.get(url = apiURL,  auth=(githubUser, githubPwd))
        jsonData = r.json()
        if "documentation_url" in jsonData:
            print(jsonData)
            raise
        else:
            return jsonData
    except Exception as ex:
        print(ex)

def checkUsersPublicEmail(userJson, githubUser, githubPwd):
    userApiURL = userJson['url']
    userSpecificJSON = call_api(userApiURL, githubUser, githubPwd)
    OUTPUT_FILE = open(OUTPUT_FILE_PATH, "a")
    if userSpecificJSON and "suspended_at" not in userSpecificJSON:
        if  userSpecificJSON["email"]:
            #print(userSpecificJSON["login"] + " " + userSpecificJSON["email"])
            OUTPUT_FILE.write(userSpecificJSON["login"] + "," + userSpecificJSON["email"] + "\n")
        else:
            #print(userSpecificJSON["login"] + " " + "")
            OUTPUT_FILE.write(userSpecificJSON["login"] + "," +  "\n")
        OUTPUT_FILE.close()

def validateScriptArgs(scriptArgs):
    if scriptArgs and len(scriptArgs) == 3:
        return "valid"
    else:
        return

def main(scriptArgs):
    if validateScriptArgs(scriptArgs):
        githubOrg = scriptArgs[0]
        githubUser = scriptArgs[1]
        githubPwd = scriptArgs[2]
        # check and delete output file if it exists
        if os.path.exists(OUTPUT_FILE_PATH):
            os.remove(OUTPUT_FILE_PATH)
        # get GitHUb users without public email on a GitHub org
        # you can update the range in below for loop based on user size on your GitHub org 
        for counter in range(1,21):
            apiURL =  GITHUB_API_URL + githubOrg + '/members?page='+ str(counter) +'&par_page=100'
            orgUserJson = call_api(apiURL, githubUser, githubPwd)
            if orgUserJson:
                for userGenericJson in orgUserJson:
                    checkUsersPublicEmail(userGenericJson,githubUser, githubPwd)
    else:
        print("invalid script args, please check and rerun again .......")

if __name__ == "__main__":
    scriptArgs = sys.argv[1:]
    main(scriptArgs)
