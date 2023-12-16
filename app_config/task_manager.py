import asyncio

class TaskManager:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.task_statuses = {}  # Словарь для хранения статусов задач

    async def process_tasks(self):
        while True:
            task = await self.task_queue.get()
            task_id = task.__name__
            try:
                await task()
                self.task_statuses[task_id] = "DONE"
            except Exception as e:
                self.task_statuses[task_id] = "FAILED"
                self.task_statuses[task_id + "_failure_reason"] = str(e)
                print(f"Error processing task: {e}")
            finally:
                self.task_queue.task_done()

    async def add_task(self, task):
        task_id = task.__name__
        self.task_statuses[task_id] = "PENDING"  # Устанавливание статуса PENDING перед добавлением в очередь
        await self.task_queue.put(task)

    def get_task_status(self, task_id):
        # Получаем статус и причину неудачи (если есть) для задачи
        status = self.task_statuses.get(task_id, "UNKNOWN")
        failure_reason = self.task_statuses.get(task_id + "_failure_reason", None)
        return status, failure_reason

task_manager = TaskManager()
