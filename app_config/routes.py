from database.mongodb.startup import DATABASE_NAME
from database.mongodb.mongo_utils import add_text
from sanic import response

db = DATABASE_NAME


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
