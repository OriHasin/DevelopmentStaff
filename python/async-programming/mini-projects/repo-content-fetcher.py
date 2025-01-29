import os
import requests
import dotenv
import pprint
import time

dotenv.load_dotenv(".env")


def get_repo_content(owner, repo, path="/"):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers={"Authorization": f"token {os.environ.get('TOKEN')}"}).json()
    current_level = []

    for element in response:

        if element["type"] == "file":
            current_level.append({"type": element["type"], "name": element["name"]})

        elif element["type"] == "dir":
            curr_dir = {"children": get_repo_content(owner, repo, element["path"]), "path": element["path"], "type": element["type"], "name": element["name"]}
            current_level.append(curr_dir)

    return current_level


if __name__ == '__main__':
    start_time = time.monotonic()
    pprint.pprint(get_repo_content("OriHasin", "DevelopmentStaff"))
    end_time = time.monotonic()
    print(f"Total Execution Time: {end_time - start_time} seconds")
