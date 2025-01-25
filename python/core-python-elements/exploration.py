
import asyncio

async def a():
    for i in range(10):
        print("here")
        yield i



async def main():
    async for item in a():
        print(item)

asyncio.run(main())
