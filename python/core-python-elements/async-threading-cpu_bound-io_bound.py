import asyncio


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

# Run the event loop
asyncio.run(main())



# Summary of Mechanism:
# The CPU-bound task runs in a separate thread using asyncio.to_thread(), where it holds the GIL
# most of the time for executing Python bytecode. However, Python periodically releases the GIL
# (e.g., after a certain number of bytecode instructions). During these brief moments, the event loop
# can acquire the GIL and execute pending tasks (moving them from ready queue to call stack - the awaited coroutine)
# "I/O-bound task complete". This allows both tasks to make progress concurrently.

# If the task is CPU-bound, it's generally better to use synchronous programming or run CPU-bound tasks in separate threads or processes.
# Async programming is most beneficial for I/O-bound tasks, not CPU-bound ones.

