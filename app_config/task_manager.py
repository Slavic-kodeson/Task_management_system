import asyncio

class TaskManager:
    def __init__(self):
        self.task_queue = asyncio.Queue()

    async def process_tasks(self):
        while True:
            task = await self.task_queue.get()
            try:
                await task()
            except Exception as e:
                print(f"Error processing task: {e}")
            finally:
                self.task_queue.task_done()

    async def add_task(self, task):
        await self.task_queue.put(task)
