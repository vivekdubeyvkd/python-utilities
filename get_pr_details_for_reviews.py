import requests
import json
import sys
import os
from datetime import datetime, timedelta

'''
  Script Name  : get_pr_details_for_reviews.py
  Purpose      : Utility to find PR details mentioned below:
                    # All PRs n last 1 year
                    # Find PR URL, PR Author
                    # Number of files changed, added or deleted
                    # Number of commits
                    # Number of comments and commenters
                    # PR creation, Last update and PR merged date
  Author       : Vivek Dubey
'''

def get_pull_requests(BASE_URL, headers, prTimeLine):
    response = requests.get(f"{BASE_URL}/pulls?state=all&since={prTimeLine}", headers=headers)
    return response.json()

def check_and_print_pr_details(BASE_URL, headers, pr, outputFilePath, reviewerOutputFilePath, commenterOutputFilePathObject, TARGET_BRANCH_PATTERN):
    pr_number = pr['number']
    author = pr['user']['login']
    prCreationDate = pr['created_at']
    prMergedDate = pr['merged_at']
    lastPrUpdateDate = pr['updated_at']
    prClosedDate = pr['closed_at']
    targetBranch = pr['base']['ref']
    sourceBranch = pr['head']['ref']
    otherPrDetails = get_pr_details(BASE_URL, headers, pr_number)
    changedFiles = otherPrDetails['changed_files']
    # Get lines of code from the pull request
    additions = otherPrDetails['additions']
    deletions = otherPrDetails['deletions']
    linesChanged = additions + deletions

    # check if merged or closed directly without merge
    if prMergedDate == None and prClosedDate != None:
        pass
    elif prMergedDate == None:
        # this section filters out open PRs, if you want to list open PRs as well, then in that case remove this elif section
        return
    else:
        pass

    # get commits
    commits = get_pr_commits(BASE_URL, headers, pr_number)
    #for commit in commits:
    #    print(f"Commit: {commit['sha']}")

    # get comments
    comments = get_pr_comments(BASE_URL, headers, pr_number)

    # get reviews
    reviews = get_pr_reviews(BASE_URL, headers, pr_number)
    #print(reviews)

    # print PR details
    # need PRs only for Pearl for now

    if TARGET_BRANCH_PATTERN.lower() in targetBranch.lower():
        #print(f"\nPR URL: {pr['html_url']}")
        #outputFilePath.write(f"\nPR URL: {pr['html_url']}\n")
        #print(f"PR Author: {author}")
        #outputFilePath.write(f"PR Author: {author}\n")
        #print(f"Target Branch: {targetBranch}, Source Branch: {sourceBranch}")
        #outputFilePath.write(f"Target Branch: {targetBranch}, Source Branch: {sourceBranch}\n")
        #print(f"PR Creation Date: {prCreationDate}")
        #outputFilePath.write(f"PR Creation Date: {prCreationDate}\n")
        #print(f"Last PR Update Date: {lastPrUpdateDate}")
        #outputFilePath.write(f"Last PR Update Date: {lastPrUpdateDate}\n")
        #print(f"PR Merged Date: {prMergedDate}")
        #outputFilePath.write(f"PR Merged Date: {prMergedDate}\n")
        #print(f"Changed Files: {changedFiles}")
        #outputFilePath.write(f"Changed Files: {changedFiles}\n")
        #print(f"Lins of Code Changed: {linesChanged}")
        #outputFilePath.write(f"Lins of Code Changed: {linesChanged}\n")
        #print(f"   Lines added : {additions}, Lines deleted : {deletions}")
        #outputFilePath.write(f"   Lines added : {additions}, Lines deleted : {deletions}\n")
        #print(f"Number of commits: {len(commits)}")
        #outputFilePath.write(f"Number of commits: {len(commits)}\n")
        #if comments:
            #print(f"Number of comments: {len(comments)}")
            #outputFilePath.write(f"Number of comments: {len(comments)}\n")
        #else:
        #    print(f"Number of comments: 0")
            #outputFilePath.write(f"Number of comments: 0\n")

        # print all comments
        commentString = ""
        for comment in comments:
                #print(f"   Commentor: {comment['user']['login']}, Comment Date: {comment['created_at']}, Comment: {comment['body']}")
                if commentString:
                    commentString = commentString + "#" + comment['user']['login'] + " " + comment['created_at'] + " " + repr(comment['body'])
                else:
                    commentString = comment['user']['login'] + " " + comment['created_at'] + " " + repr(comment['body'])
                commenterOutputFilePathObject.write(f"{comment['user']['login']}, {pr['html_url']}, {author}, {targetBranch}, {sourceBranch}, {prCreationDate}, {lastPrUpdateDate}, {prMergedDate}, {changedFiles}, {linesChanged}, {additions}, {deletions}, {len(commits)}, {comment['created_at']}, {repr(comment['body'])}\n")
        outputFilePath.write(f"{pr['html_url']}, {author}, {targetBranch}, {sourceBranch}, {prCreationDate}, {lastPrUpdateDate}, {prMergedDate}, {changedFiles}, {linesChanged}, {additions}, {deletions}, {len(commits)}, {len(comments)}, {commentString}\n")          

        # print review and write to file
        for review in reviews:
            reviewerOutputFilePath.write(f"{review['user']['login']}, {pr['html_url']}, {author}, {targetBranch}, {sourceBranch}, {prCreationDate}, {lastPrUpdateDate}, {prMergedDate}, {changedFiles}, {linesChanged}, {additions}, {deletions}, {len(commits)}, {review['submitted_at']}, {repr(review['body'])}\n")          

def get_all_prs(BASE_URL, headers, prTimeLine, TARGET_BRANCH_PATTERN):
    page = 1
    prs = []
    outputFilePathVal = "author_pr_details.csv"
    reviewerOutputFilePathVal = "review_pr_details.csv"
    commenterOutputFilePathVal = "review_details_with_comments.csv"
    if os.path.isfile(outputFilePathVal):
        os.remove(outputFilePathVal)
    if os.path.isfile(reviewerOutputFilePathVal):
        os.remove(reviewerOutputFilePathVal)    
    outputFilePathObject = open(outputFilePathVal, "a")
    outputFilePathObject.write(f"PR URL, PR Author, Target Branch, Source Branch, PR Creation Date, Last PR Update Date, PR Merged Date, Number of Changed Files, Total Lines Changed, Lines Added, Lined Deleted, Number of Commits, Number of Comments, Comment Details\n")    
    outputFilePathObject.close()
    reviewerOutputFilePathObject = open(reviewerOutputFilePathVal, "a")
    reviewerOutputFilePathObject.write(f"PR Reviewer, PR URL, PR Author, Target Branch, Source Branch, PR Creation Date, Last PR Update Date, PR Merged Date, Number of Changed Files, Total Lines Changed, Lines Added, Lined Deleted, Number of Commits, Review Date, Review Details\n")    
    reviewerOutputFilePathObject.close()
    commenterOutputFilePathObject = open(commenterOutputFilePathVal, "a")
    commenterOutputFilePathObject.write(f"PR Reviewer, PR URL, PR Author, Target Branch, Source Branch, PR Creation Date, Last PR Update Date, PR Merged Date, Number of Changed Files, Total Lines Changed, Lines Added, Lined Deleted, Number of Commits, Comment Date, Comment Msg\n") 
    commenterOutputFilePathObject.close()    
    while True:
        url = f"{BASE_URL}/pulls?state=all&per_page=100&page={page}&since={prTimeLine}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            break
        for pr in data:
            #prs.append(pr)
            if TARGET_BRANCH_PATTERN in pr['base']['ref']:
                outputFilePathObject = open(outputFilePathVal, "a")
                reviewerOutputFilePathObject = open(reviewerOutputFilePathVal, "a")
                commenterOutputFilePathObject = open(commenterOutputFilePathVal, "a")
                check_and_print_pr_details(BASE_URL, headers, pr, outputFilePathObject, reviewerOutputFilePathObject, commenterOutputFilePathObject, TARGET_BRANCH_PATTERN)
                outputFilePathObject.close()
                reviewerOutputFilePathObject.close()
                commenterOutputFilePathObject.close()
        page += 1
    #return prs

def get_pr_comments(BASE_URL, headers, pr_number):
    response = requests.get(f"{BASE_URL}/pulls/{pr_number}/comments", headers=headers)
    return response.json()

def get_pr_commits(BASE_URL, headers, pr_number):
    response = requests.get(f"{BASE_URL}/pulls/{pr_number}/commits", headers=headers)
    return response.json()

def get_pr_reviews(BASE_URL, headers, pr_number):
    response = requests.get(f"{BASE_URL}/pulls/{pr_number}/reviews", headers=headers)
    return response.json()    

def get_pr_details(BASE_URL, headers, pr_number):
    response = requests.get(f"{BASE_URL}/pulls/{pr_number}", headers=headers)
    return response.json()    

def validateScriptArgs(scriptArgs):
    if scriptArgs and len(scriptArgs) == 4:
        return "valid"
    else:
        return

def main(scriptArgs):
    if validateScriptArgs(scriptArgs):
        # GitHub Org
        OWNER = scriptArgs[0]
        REPO = scriptArgs[1]
        # branch to target
        TARGET_BRANCH_PATTERN = scriptArgs[2]
        # GitHub personal access token
        TOKEN = scriptArgs[3]

        # Header for authorization
        headers = {
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Calculate the date 1 year ago
        # you can update the days in below line as per your choice to get PR details over a period of time
        one_year_ago = (datetime.now() - timedelta(days=365)).isoformat()

        # Base URL for the GitHub API
        # update the GitHub API details as per your GitHub API URL for hosted GitHub enterprise instances
        BASE_URL = f"https://api.github.com/api/v3/repos/{OWNER}/{REPO}"

        # get all pull requests
        #pull_requests = get_pull_requests(BASE_URL, headers, one_year_ago)
        pull_requests = get_all_prs(BASE_URL, headers, one_year_ago, TARGET_BRANCH_PATTERN)

        '''
        # loop over each PR object to get the details
        for pr in pull_requests:
            pr_number = pr['number']
            author = pr['user']['login']
            prCreationDate = pr['created_at']
            prMergedDate = pr['merged_at']
            lastPrUpdateDate = pr['updated_at']
            targetBranch = pr['base']['ref']
            sourceBranch = pr['head']['ref']
            otherPrDetails = get_pr_details(BASE_URL, headers, pr_number)
            changedFiles = otherPrDetails['changed_files']
            # Get lines of code from the pull request
            additions = otherPrDetails['additions']
            deletions = otherPrDetails['deletions']
            linesChanged = additions + deletions

            # get commits
            commits = get_pr_commits(BASE_URL, headers, pr_number)
            #for commit in commits:
            #    print(f"Commit: {commit['sha']}")

            # get comments
            comments = get_pr_comments(BASE_URL, headers, pr_number)

            # get reviews
            #reviews = get_pr_reviews(BASE_URL, headers, pr_number)
            #print(reviews)

            # print PR details
            # need PRs only for Pearl for now
            if 'Pearl' in targetBranch:
                print(f"\nPR URL: {pr['html_url']}")
                print(f"PR Author: {author}")
                print(f"Target Branch: {targetBranch}, Source Branch: {sourceBranch}")
                print(f"PR Creation Date: {prCreationDate}")
                print(f"Last PR Update Date: {lastPrUpdateDate}")
                print(f"PR Merged Date: {prMergedDate}")
                print(f"Changed Files: {changedFiles}")
                print(f"Lins of Code Changed: {linesChanged}")
                print(f"   Lines added : {additions}, Lines deleted : {deletions}")
                print(f"Number of commits: {len(commits)}")
                if comments:
                    print(f"Number of comments: {len(comments)}")
                else:
                    print(f"Number of comments: 0")

                # print all comments
                for comment in comments:
                    print(f"   Commentor: {comment['user']['login']}, Comment Date: {comment['created_at']}, Comment: {comment['body']}")
            '''
    else:
        print("\n+++++++++++++++++++++++++++++++ ERROR ++++++++++++++++++++++++++++++++++++++++")
        print("Invalid number of input parameters passed to script, kindly check and rerun ... exiting ...")
        print("+++++++++++++++++++++++++++++++ ERROR ++++++++++++++++++++++++++++++++++++++++\n")             

if __name__ == "__main__":
    scriptArgs = sys.argv[1:]
    main(scriptArgs)
