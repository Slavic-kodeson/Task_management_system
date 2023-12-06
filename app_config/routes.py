from sanic import json
from motor.motor_asyncio import AsyncIOMotorClient


motor_client = AsyncIOMotorClient("mongodb://localhost:27017")
database_name = "tasks_collection" 
database = motor_client[database_name]


async def route_add_text(request):
    try:
        raw_body = request.body
        text_add = raw_body.decode('utf-8')

        result = await database.text_collection.insert_one({"text": text_add})

        return json({"message": "Text added successfully", "added_text": text_add, "mongo_id": str(result.inserted_id)})

    except Exception as err:
        return json({"error": str(err)}, 500)


def route_add_file(request):
    pass


def route_remove_text(request):
    pass
