import asyncio
import time


# I/O-bound task (simulating waiting for something like a web request or file read)
async def io_bound_task():
    print("Starting I/O-bound task...")
    await asyncio.sleep(2)  # Simulate I/O operation with a delay
    print("I/O-bound task complete.")

# CPU-bound task (simulating a computationally intensive task)
def cpu_bound_task():
    print("Starting CPU-bound task...")
    result = 0
    for i in range(100000000):  # Reduced the loop size for demonstration purposes
        result += i
    print(f"CPU-bound task complete with result: {result}")

# Main function to run both tasks
async def main():
    # Schedule the I/O-bound task
    io_task = asyncio.create_task(io_bound_task())

    # Run the CPU-bound task in a separate thread
    await asyncio.to_thread(cpu_bound_task)

    # Wait for the I/O-bound task to complete
    await io_task

# Run the event loop
asyncio.run(main())
