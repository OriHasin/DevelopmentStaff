import os

import requests
import pprint
import dotenv

dotenv.load_dotenv(".env")

class FileNode:
    def __init__(self, name, download_url):
        self.name = name
        self.download_url = download_url

    def __repr__(self):
        return f"name: {self.name}"


class DirNode:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.children = None
    def __repr__(self):
        return f"name: {self.name}, path: {self.path}, childs: {self.children}"






def get_repo_content(owner, repo, path="/"):
    URL = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(URL, headers={"Authorization": f"token {os.environ.get('TOKEN')}"}).json()
    current_level = []
    for element in response:
        if element["type"] == "file":
            current_level.append(FileNode(element["name"], element["download_url"]))
        elif element["type"] == "dir":
            curr_dir = DirNode(element["name"], element["path"])
            curr_dir.children = get_repo_content(owner, repo, element["path"])
            current_level.append(curr_dir)
    return current_level



if __name__ == '__main__':
    pprint.pprint(get_repo_content("OriHasin", "DevelopmentStaff"))