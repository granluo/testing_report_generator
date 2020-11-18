from github import Github
import datetime
import issue_model

class GithubRepo():

    def __init__(self, access_token, repo):
        self.client = Github(access_token)
        self.set_repo(repo)
        self.cur_time = datetime.datetime.now()

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

    def get_runs_of_workflows_for_json(self, event):
        workflows = self.get_workflows()
        columns = ['Workflow', self.cur_time.strftime("%m/%d")]
        contents = []
        
        for workflow in workflows:
            print(workflow.name)
            runs = workflow.get_runs(event = event)
            # if runs is not empty, then the first run will be get.
            for run in runs:
                run_result = {workflow.name: "[{}]({})".format(run.conclusion, run.html_url)}
                contents.append(run_result)

                #print (run.created_at.strftime("%m/%d/%Y, %H:%M:%S") + " " + run.conclusion)
                break
        return (columns, contents)

class JsonGenerator():

    def __init__(self, title, repo_client):
        self.report = issue_model.report(title = title)
        self.client = repo_client

    def set_description(self, description):
        self.report.description = description




def main():
    repo = GithubRepo('TOKEN', 'firebase/firebase-ios-sdk')
    repo.get_runs_of_workflows_for_json("schedule")
    
if __name__ == "__main__":
    main()

