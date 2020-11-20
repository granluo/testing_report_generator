from github import Github
from pytz import timezone
import pytz
import json
import datetime
import issue_model

EVENT = 'schedule'
SKIP_TESTS = ['performance-integration-tests','performance']
TIME_ZONE = 'US/Pacific'

class GithubClient():

    def __init__(self, access_token, repo):
        self.client = Github(access_token)
        self.set_repo(repo)

    def set_repo(self, new_repo):
        self.repo = self.client.get_repo(new_repo)

    def get_open_issues_by_label(self, label):
        issue_label = self.repo.get_label(label)
        issues = self.repo.get_issues( 
                state = 'open',
                sort='created',
                direction='asc',
                labels=[issue_label])
        return issues

    def get_workflows(self):
       return self.repo.get_workflows()

    def handle_issue(self, title, markdown_body, issue_label, testing_failed):
        labels = [issue_label]
        issues = self.repo.get_issues(labels=labels, state='open')
        if issues.totalCount == 0:
            if testing_failed:
                self.repo.create_issue(title=title, body=markdown_body, labels=[issue_label])
        else:
            first_issue = issues[0]
            if testing_failed:
                first_issue.create_comment(body=markdown_body)
            else:
                first_issue.create_comment(body='All tests passed. Issue closed.')
                first_issue.edit(state='closed')
            if issues.totalCount > 1:
                for issue in issues[1:]:
                    issue.edit(state='closed')

class JsonGenerator():

    def __init__(self, title, repo_client, skip_workflows):
        self.report = issue_model.Report(title = title)
        self.client = repo_client
        self.cur_time = datetime.datetime.now()
        self.skip_tests = set(skip_workflows)

    def set_description(self, description):
        self.report.description = description

    def get_runs_of_workflows_for_json(self, involve_successful_run = False):
        workflows = self.client.get_workflows()
        columns = ['Workflow']
        contents = []
        is_testing_failed = None
        
        for workflow in workflows:
            print(workflow.name)
            if workflow.name in self.skip_tests:
                print(" workflow {} is skipped.".format(workflow.name))
                continue
            runs = workflow.get_runs()
            # if runs is not empty, then the first run will be get.
            for run in runs:
                created_time = run.created_at.astimezone(timezone(TIME_ZONE)).strftime("%m/%d")
                if created_time not in columns:
                    columns.append(created_time)
                run_result = {'Workflow':workflow.name, created_time: "[{}]({})".format(run.conclusion, run.html_url)}
                if run.conclusion != 'success': 
                    if is_testing_failed is None:
                        is_testing_failed = True
                    contents.append(run_result)
                elif involve_successful_run:
                    contents.append(run_result)
                break
        if is_testing_failed is None:
            is_testing_failed = False
        return columns, contents, is_testing_failed
    def create_and_add_table(self, table_name, columns, contents):
       new_table = issue_model.Table(table_name= table_name, column_names = columns, contents=contents)
       self.report.add_table(new_table) 

    def generate_json(self, file_name = None):
       columns, contents, is_testing_failed = self.get_runs_of_workflows_for_json()
       self.create_and_add_table("Nightly All Workflow Report", columns, contents)
       if file_name is not None:
           self.report.convert_to_json(file_name)
       output = self.report.convert_to_json()
       return output, is_testing_failed
        
    def generate_markdown(self):
        json_body, is_testing_failed= self.generate_json()
        comment = json.loads(json_body)

        text = []
        text.append('# ' + comment.get('title'))
        text.append(comment.get('description', 'Failures are detected:'))

        separator = ' | '
        divider = '------------'
        for result in comment.get('test_results'):
            text.append('## ' + result.get('table_name'))
            columns = result.get('column_names')
            text.append(separator.join(columns))
            text.append(separator.join([divider for i in range(len(columns))]))
            for content in result.get('contents'):
                row = ['']
                for column in columns:
                    row.append(content.get(column, ''))
                row.append('')
                text.append(separator.join(row))

        return '\n'.join(text), is_testing_failed


def main():
    repo = GithubClient('token', 'granluo/testing_report_generator')
    json_generator = JsonGenerator('testing title', repo)
    markdown_body, testing_failed = json_generator.generate_markdown()
    repo.handle_issue("Title", markdown_body, 'Nightly-testing', testing_failed)
    print(json_generator.generate_json('sample.json'))
    
if __name__ == "__main__":
    main()

