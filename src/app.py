import os
import sys
import json
from github import Github
import json_generator


repo_client = json_generator.GithubClient('1d95f4b4d680e937987334ebc0d109d4a39ff038', 'granluo/testing_report_generator')#(os.getenv("INPUT_TOKEN"), os.getenv("INPUT_REPO"))
json_generator = json_generator.JsonGenerator('testing title', repo_client)
markdown_body, testing_failed = json_generator.generate_markdown()
repo_client.handle_issue("Title", markdown_body, 'Nightly-testing', testing_failed)
print(markdown_body)
