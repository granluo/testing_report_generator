import os
import sys
import json
from github import Github
import json_generator


repo_client = json_generator.GithubClient(os.getenv("INPUT_TOKEN"), os.getenv("INPUT_REPO"))
json_generator = json_generator.JsonGenerator('testing title', repo_client)
repo_client. generate_issue(title, json_body, issue_label):
print(json_generator.generate_json('sample.json'))
