import asyncio

task_queue = asyncio.Queue()


async def process_tasks():
    while True:
        task = await task_queue.get()
        task_queue.task_done()
