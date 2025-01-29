import asyncio
import os
import time
import aiohttp
import dotenv
import pprint

dotenv.load_dotenv(".env")


async def get_repo_content(owner, repo, path="/"):
    async with aiohttp.ClientSession() as session:
        return await _get_repo_content(session, owner, repo, path)


async def _get_repo_content(session, owner, repo, path="/"):
    async def _process_data(element):
        if element["type"] == "file":
            return {"type": element["type"], "name": element["name"]}

        elif element["type"] == "dir":
            return {"children": await _get_repo_content(session, owner, repo, element["path"]), "path": element["path"],
                    "type": element["type"], "name": element["name"]}


    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    async with session.get(url, headers={"Authorization": f"token {os.environ.get('TOKEN')}"}) as response:
        data = await response.json()

    current_level = [asyncio.create_task(_process_data(element)) for element in data]
    results = await asyncio.gather(*current_level)

    return results






if __name__ == '__main__':
    start_time = time.monotonic()
    pprint.pprint(asyncio.run(get_repo_content("OriHasin", "DevelopmentStaff")))
    end_time = time.monotonic()
    print(f"Total Execution Time: {end_time - start_time} seconds")