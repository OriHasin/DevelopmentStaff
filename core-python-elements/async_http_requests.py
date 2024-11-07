"""
    1. **Overview of aiohttp**:
       - `aiohttp` is an asynchronous HTTP client-server library designed for high-performance web interactions.
       - It leverages Python's `async` and `await` syntax, allowing non-blocking operations, which makes it efficient for I/O-bound tasks like network communication.


    2. **ClientSession and Context Managers**:
       - `aiohttp.ClientSession` is the primary interface for making HTTP requests.
       - **Why `ClientSession`?**
         - Manages a pool of connections to reuse TCP connections for efficiency.
         - Handles session-wide settings like headers, cookies, and connection persistence.
       - **Usage with `async with`**:
         - `async with aiohttp.ClientSession() as session`:
           - The `__aenter__` method asynchronously initializes the session.
           - The `__aexit__` method asynchronously closes the session, releasing all associated resources.
         - This `async with` syntax ensures that session setup and teardown are managed properly, without blocking the event loop.


    3. **Request Handling**:
       - Each request method (`session.get`, `session.post`, etc.) returns a context manager that represents the request operation.
       - **Using `async with session.get(...)`**:
         - When calling `session.get`, it does not immediately contain the response data; instead, it initiates the request.
         - `async with session.get(...) as response`:
           - `__aenter__` here waits until the server response is available, then returns a `ClientResponse` object.
           - `__aexit__` handles cleanup, like closing the response object, to free resources after the response data has been processed.


    4. **ClientResponse Object**:
       - `ClientResponse` represents the HTTP response returned from a server.
       - **Response Lifecycle**:
         - When a request is made with `await session.get(...)`, it initiates an async connection.
         - `ClientResponse` does not initially contain the response body; instead, it provides an interface for retrieving the data when it becomes available.
         - Accessing response content, e.g., `await response.text()`, is asynchronous because:
           - Response data may be received in chunks over the network.
           - `await response.text()` reads and decodes the data asynchronously. """


import aiohttp
import asyncio
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/trigger", methods=['GET'])
async def send_requests():
    urls = ['https://www.example.com',
            'https://www.example4.com',
            'https://www.example3.com']

    async with aiohttp.ClientSession() as session:
        tasks = [process_request(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
        print(len(results))

    return jsonify(results), 200


async def process_request(url, session):
    try:
        async with session.get(url) as response:
            text = await response.text()
            return {"url": url, "status_code": response.status, "text": text}
    except Exception as e:
        return {"url": url, "error": str(e)}




if __name__ == '__main__':
    app.run()