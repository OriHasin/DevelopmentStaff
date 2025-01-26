import logging
import pprint
import time
logging.basicConfig(level=logging.INFO)
class TaskProcessor:

    def __init__(self, tasks):
        self.tasks = {task['id']: task for task in tasks}
        self.result = {}


    def process_tasks(self):
        start_time = time.time()

        for task in self.tasks.keys():
                self._process_task(task)

        end_time = time.time()
        logging.info(f"FINISH SYNCHRONOUS PROCESSING! TOTAL TIME : {end_time - start_time}")
        return self.result


    def _process_task(self, task_id):
        if task_id not in self.result.keys():
            task = self.tasks[task_id]
            dependencies = task['dependencies']

            for dep in dependencies:
                if dep not in self.result.keys():
                    self._process_task(dep)

            logging.info(f"Processing Task {task_id}, with processing time: {task['processing_time']} seconds.")
            time.sleep(task['processing_time'])
            logging.info(f"Finish processing task {task_id}")

            self.result[task_id] = "Complete"



if __name__ == "__main__":
    tasks = [
        {"id": "A", "dependencies": ["D"], "processing_time": 2},
        {"id": "B", "dependencies": ["A"], "processing_time": 3},
        {"id": "C", "dependencies": ["A"], "processing_time": 3},
        {"id": "D", "dependencies": [], "processing_time": 1},
    ]

    processor = TaskProcessor(tasks)
    pprint.pprint(processor.process_tasks())