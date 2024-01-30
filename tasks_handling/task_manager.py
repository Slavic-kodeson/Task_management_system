from tasks_handling.tasks_queue import task_queue
from redisdb.redis_utils import update_task_status, add_text_with_id


class TaskManager:
    def __init__(self, redis):
        self.redis = redis

    async def process_tasks(self):
        while True:
            task = await task_queue.queue.get()
            await self.execute_task(task)

    async def execute_task(self, task):
        task_type = task.get("type")
        task_id = task.get("task_id")
        redis_db = task.get("redis_db", self.redis)

        try:
            print(f"Processing task with task_id: {task_id}")
            await update_task_status(redis_db, task_id, "IN PROGRESS", None)

            if task_type == "add_text":
                await add_text_with_id(redis_db, task_id, task["text"])

        except Exception as e:
            print(f"Processing failed for task_id {task_id}: {str(e)}")
            await update_task_status(redis_db, task_id, "FAILED", str(e))
        else:
            print(f"Processing successful for task_id {task_id}")
            await update_task_status(redis_db, task_id, "DONE", None)
