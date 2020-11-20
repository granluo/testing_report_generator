import os
import sys
import json
from github import Github
import json_generator

print(os.getenv())
repo_client = json_generator.GithubClient(os.getenv("INPUT_TOKEN"), os.getenv("INPUT_HOST_REPO"), os.getenv("INPUT_TARGET_REPO"))
json_generator = json_generator.JsonGenerator("Nightly Testing", repo_client, os.getenv("INPUT_SKIP_WORKFLOWS").split(","))
markdown_body, testing_failed = json_generator.generate_markdown(os.getenv("INPUT_JSON_REPORT"))
repo_client.handle_issue(os.getenv("INPUT_TITLE"), markdown_body, os.getenv("INPUT_LABEL"), testing_failed)
print(markdown_body)
