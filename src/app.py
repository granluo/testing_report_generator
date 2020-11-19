import os
import sys
import json
from github import Github


def main():
    ISSUE_COMMENT = os.getenv("INPUT_COMMENT")
    TOKEN = os.getenv("INPUT_TOKEN")
    REPO_NAME = os.getenv("INPUT_REPO_NAME")
    ISSUE_TITLE = os.getenv("INPUT_TITLE")
    ISSUE_LABEL = os.getenv("INPUT_LABEL")

    markdown, report_error = create_markdown(ISSUE_COMMENT)
    print(markdown)

    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)
    labels = [ISSUE_LABEL]
    issues = repo.get_issues(labels=labels, state='open')
    if issues.totalCount == 0:
        if report_error:
            repo.create_issue(title=ISSUE_TITLE, body=markdown, labels=[ISSUE_LABEL])
    else:
        first_issue = issues[0]
        if report_error:
            first_issue.create_comment(body=markdown)
        else:
            first_issue.create_comment(body='All tests passed. Issue closed.')
            first_issue.edit(state='closed')
        if issues.totalCount > 1:
            for issue in issues[1:]:
                issue.edit(state='closed')


def create_markdown(json_comment):
    comment = json.loads(json_comment)

    text = []
    text.append('# ' + comment.get('title'))
    text.append(comment.get('description', ''))

    separator = ' | '
    divider = '------------'
    for result in comment.get('test_results'):
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

    return ['\n'.join(text), True]


# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 
