# ==========================================================
# Asynchronous Programming in Python
# ==========================================================
# In Python, asynchronous programming is handled using asyncio,
# a library for writing asynchronous code using async/await.
# Python also introduces Futures, a concept used for dealing
# with values that are computed asynchronously.

# ==========================================================
# Async/Await in Python
# ==========================================================
# The asyncio library allows Python to handle asynchronous I/O
# operations, such as file or network operations, in an efficient
# manner. You define asynchronous functions with async def,
# and use await to wait for the result of asynchronous operations.

# Example of async/await usage:

import asyncio

async def fetch_data():
    await asyncio.sleep(2)  # Simulating an asynchronous I/O operation
    print("Data fetched successfully!")

async def main():
    print("Start")
    await fetch_data()
    print("End")

# Running the async example
asyncio.run(main())

# Explanation:
# async def is used to define an asynchronous function (fetch_data).
# The await keyword pauses the execution until asyncio.sleep(2) finishes,
# simulating an I/O operation.

# ==========================================================
# Futures in Python
# ==========================================================
# A Future represents a result that is not yet available but
# will be at some point. You typically work with Futures when
# dealing with concurrent tasks in Python, like in concurrent.futures.

# Example using Futures:

async def task():
    await asyncio.sleep(2)
    return "Task completed!"

async def main_with_future():
    future = asyncio.ensure_future(task())  # Creates a Future for the task
    print("Waiting for task...")
    result = await future  # Waits for the task to complete
    print(result)

# Running the future example
asyncio.run(main_with_future())

# Explanation:
# asyncio.ensure_future is used to create a Future for the task.
# await future waits until the task completes and retrieves the result.
