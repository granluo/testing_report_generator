import os
import sys
import json
from github import Github



def main():
    markdown = create_markdown()
    print(markdown)
    create_github_issue(body=markdown)


def create_markdown():
    ISSUE_COMMENT = os.getenv("INPUT_COMMENT")
    issue = json.loads(ISSUE_COMMENT)

    text = []
    text.append('# ' + issue.get('title'))
    text.append(issue.get('description', 'Failures are detected:'))

    separator = ' | '
    divider = '------------'
    for result in issue.get('test_results'):
        text.append('## ' + result.get('table_name'))
        colunms = result.get('colunm_names')
        text.append(separator.join(colunms))
        text.append(separator.join([divider for i in range(len(colunms))]))
        for content in result.get('contents'):
            row = ['']
            for colunm in colunms:
                row.append(content.get(colunm, ''))
            row.append('')
            text.append(separator.join(row))

    return '\n'.join(text)


def create_github_issue(body):
    TOKEN = os.getenv("INPUT_TOKEN")
    REPO_OWNER = os.getenv("INPUT_REPO_OWNER")
    REPO_NAME = os.getenv("INPUT_REPO_NAME")
    ISSUE_TITLE = os.getenv("INPUT_TITLE")
    ISSUE_LABEL = os.getenv("INPUT_LABEL")

    g = Github(TOKEN)
    repo = g.get_repo(REPO_OWNER + '/' + REPO_NAME)
    repo.create_issue(title=ISSUE_TITLE, body=body, labels=[ISSUE_LABEL])


# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 
