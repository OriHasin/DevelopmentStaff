import asyncio
import logging
import pprint
import time

logging.basicConfig(level=logging.INFO)


class TaskProcessor:

    def __init__(self, tasks, maximum_concurrent_tasks=5):
        self.tasks = {task['id']: task for task in tasks}
        self.conditions = {task['id']: asyncio.Condition() for task in tasks}
        self.semaphore = asyncio.Semaphore(maximum_concurrent_tasks)
        self.lock = asyncio.Lock()      # not really needed, just demonstrate using best practices shared access
        self.result = {}


    async def process_tasks(self):
        start_time = time.time()

        coros = [asyncio.create_task(self._process_task(task)) for task in self.tasks.keys()]
        await asyncio.gather(*coros, return_exceptions=True)

        end_time = time.time()
        logging.info(f"FINISH ASYNCHRONOUS PROCESSING! TOTAL TIME : {end_time - start_time}")
        return self.result


    async def _process_task(self, task_id):
        task = self.tasks[task_id]
        dependencies = task['dependencies']

        for dep in dependencies:
            if dep not in self.result.keys():
                async with self.conditions[dep]:
                    logging.info(f"task {task_id} acquired the lock for dep {dep}, and now going to release it for waiting")
                    await self.conditions[dep].wait()
                    logging.info(f"task {task_id} acquired the lock for dep {dep}, for more processing here, going to finish")

        async with self.semaphore:

            logging.info(f"Processing Task {task_id}, with processing time: {task['processing_time']} seconds.")
            await asyncio.sleep(task['processing_time'])
            logging.info(f"Finish processing task {task_id}")

            async with self.lock:   # not really need here, because only writing to a shared state with unique key
                self.result[task_id] = "Complete"

            async with self.conditions[task_id]:
                self.conditions[task_id].notify_all()



if __name__ == "__main__":
    tasks = [
        {"id": "A", "dependencies": ["D"], "processing_time": 2},
        {"id": "B", "dependencies": ["A"], "processing_time": 3},
        {"id": "C", "dependencies": ["A"], "processing_time": 3},
        {"id": "D", "dependencies": [], "processing_time": 1},
    ]

    processor = TaskProcessor(tasks)
    pprint.pprint(asyncio.run(processor.process_tasks()))