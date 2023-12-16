from Task_management_system.mongodb.startup import DATABASE_NAME
from Task_management_system.mongodb.mongo_utils import add_text
from Task_management_system.app_config.task_manager import task_manager
from sanic import response

db = DATABASE_NAME

async def route_get_task_status(request):
    try:
        # Получение id задачи из запроса
        task_id = request.args.get("task_id")

        # Получение статуса и причины неудачи из TaskManager
        task_status, failure_reason = task_manager.get_task_status(task_id)

        return response.json({
            "task_id": task_id,
            "status": task_status,
            "failure_reason": failure_reason
        })

    except Exception as err:
        return response.json({"error": str(err)}, status=500)
async def route_add_text(request):
    try:
        text_add = request.body.decode('utf-8')

        await add_text(db, text_add)

        return response.json({
            "message": "Text added successfully",
            "added_text": text_add,
        })

    except Exception as err:
        return response.json({"error": str(err)}, status=500)
