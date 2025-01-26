import asyncio
import aiohttp
import pprint

class WebCrawler:

    def __init__(self, url_list, rate_limiting_per_second=5, retries=[2, 5, 10], max_concurrent_connections=5):
        self.url_list = url_list
        self.retries = retries
        self.rate_limit_interval = 1.0 / rate_limiting_per_second
        self.semaphore = asyncio.Semaphore(max_concurrent_connections)
        self.lock = asyncio.Lock()
        self.next_allowed_time_request = None


    async def crawl_the_web(self):
        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in self.url_list:

                async with self.semaphore:
                    tasks.append(asyncio.create_task(self._process_url(url, session)))

            results = await asyncio.gather(*tasks, return_exceptions=True)

        results_dict = {}
        for url, result in zip(self.url_list, results):
            results_dict[url] = result

        return results_dict


    async def _process_url(self, url, session):
        for attempt in range(1, len(self.retries) +1):
            await self._rate_limit()

            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()


            except aiohttp.ClientError as e:
                await asyncio.sleep(self.retries[attempt - 1])

                if attempt == len(self.retries):
                    return {f"Error: In attempt {attempt}, with URL {url}"}

    async def _rate_limit(self):
        async with self.lock:
            if self.next_allowed_time_request is None:  # Set it the first time _rate_limit is called
                self.next_allowed_time_request = asyncio.get_event_loop().time()

            current_time = asyncio.get_event_loop().time()
            print("request acquired the lock in time: " + str(current_time ))
            spare = self.next_allowed_time_request - current_time
            waiting_time = max(0, spare)
            await asyncio.sleep(waiting_time) if waiting_time > 0 else None
            self.next_allowed_time_request += self.rate_limit_interval



if __name__ == "__main__":
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/2",
        "https://jsonplaceholder.typicode.com/todos/3",
        "https://jsonplaceholder.typicode.com/todos/3",
        "https://jsonplaceholder.typicode.com/todos/3",
        "https://jsonplaceholder.typicode.com/todos/3",
        "https://jsonplaceholder.typicode.com/todos/4",
        "https://jsonplaceholder.typicode.com/todos/5",
        "https://jsonplaceholder.typicode.com/todos/5",
        "https://jsonplaceholder.typicode.com/todos/7",
        "https://jsonplaceholder.typicode.com/todos/8",
        "https://jsonplaceholder.typicode.com/todos/8",
        "https://jsonplaceholder.typicode.com/todos/8",
        "https://jsonplaceholder.typicode.com/todos/8",
        "https://jsonplaceholder.typicode.com/todos/8",

    ]

    scraper = WebCrawler(urls)
    results = asyncio.run(scraper.crawl_the_web())
    pprint.pprint(results)

