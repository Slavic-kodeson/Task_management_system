# from sanic import json
# from motor.motor_asyncio import AsyncIOMotorClient
#
#
# motor_client = AsyncIOMotorClient("mongodb://localhost:27017")
# database_name = "tasks_collection"
# database = motor_client[database_name]

from functions.tasks import add_text_task, add_file_task, remove_text_task, register_website, validate_file
from aiohttp import web


async def route_add_text(request):
    try:
        data = await request.json()
        print("Request data:", data)

        result = await add_text_task(data.get("user_id"), data.get("text"))

        if result.get("status") == "success":
            return web.json_response({"status": "Task added successfully"})
        else:
            return web.json_response({"status": "Task failed"}, status=500)
    except Exception as e:
        print("Error processing request:", str(e))
        return web.json_response({"status": "Error processing request"}, status=500)


async def route_add_file(request):
    try:
        data = await request.post()
        user_id = data.get("user_id")
        file = data.get("file")

        file_valid, file_extension = await validate_file(file.filename, len(file.file.read()))
        if not file_valid:
            return web.json_response({"status": "Invalid file"})

        result = await add_file_task(user_id, file.file.read(), file.filename)

        if result.get("status") == "success":
            return web.json_response({"status": "Task added successfully"})
        else:
            return web.json_response({"status": "Task failed"}, status=500)
    except Exception as e:
        print("Error processing request:", str(e))
        return web.json_response({"status": "Error processing request"}, status=500)


async def route_remove_text(request):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        document_id = data.get("document_id")

        result = await remove_text_task(user_id, document_id)

        # Check the result and construct the response accordingly
        if result.get("status") == "success":
            return web.json_response({"status": "Task removed successfully"})
        elif result.get("status") == "not found":
            return web.json_response({"status": "Document not found"}, status=404)
        else:
            return web.json_response({"status": "Task failed"}, status=500)
    except Exception as e:
        print("Error processing request:", str(e))
        return web.json_response({"status": "Error processing request"}, status=500)


async def route_register_website(request):
    try:
        data = await request.json()
        website_name = data.get("website_name")

        result = await register_website(website_name)

        if result.get("status") == "success":
            return web.json_response({"website_id": result.get("website_id")})
        else:
            return web.json_response({"status": "Failed to register website"}, status=500)
    except Exception as e:
        print("Error processing request:", str(e))
        return web.json_response({"status": "Error processing request"}, status=500)
