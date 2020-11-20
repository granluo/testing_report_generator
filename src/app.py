import os
import sys
import json
from github import Github
import json_generator


repo_client = json_generator.GithubClient(os.getenv("INPUT_TOKEN"), os.getenv("INPUT_REPO_NAME"))
skip_workflows = [] if os.getenv("INPUT_SKIP_WORKFLOWS") is None else os.getenv("INPUT_SKIP_WORKFLOWS").split(",")
json_generator = json_generator.JsonGenerator("Nightly Testing", repo_client, os.getenv("INPUT_SKIP_WORKFLOWS").split(","))
markdown_body, testing_failed = json_generator.generate_markdown()
repo_client.handle_issue(os.getenv("INPUT_TITLE"), markdown_body, os.getenv("INPUT_ISSUE_LABEL"), testing_failed)
print(markdown_body)
