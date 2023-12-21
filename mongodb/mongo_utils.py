from gridfs import GridFS


async def exists_user(mongo_db, search) -> bool:
    result = await mongo_db["users"].find_one(search, {"id": 1})
    return result is not None


async def insert_registration_code(mongo_db, reg_code, permissions):
    await mongo_db["register_codes"].insert_one({
        "code": reg_code,
        "permissions": permissions
    })


async def find_registration_code(mongo_db, reg_code):
    response = await mongo_db["register_codes"].find_one({"code": reg_code}, {"_id": 0, "code": 1})
    return response


async def replace_settings(mongo_db, user_id, new_settings):
    await mongo_db["users"].replace_one({"id": user_id}, {"$set": new_settings})


async def check_permissions(mongo_db, requested_permissions: dict):
    permission = await mongo_db["users"].find_one(requested_permissions, {"id": 1})
    return permission is not None


async def register_user(mongo_db, user_data) -> None:
    await mongo_db["users"].insert_one({
        "login": user_data.get("login"),
        "password": user_data.get("password"),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "id": user_data.get("id"),
        "telegram": None,
        "logs_access": user_data.get("permissions")
    })


async def add_text_with_id(mongo_db, text_id, text) -> None:
    try:
        print(f"Adding text with id {text_id}: {text}")
        users_collection = mongo_db["users"]
        await users_collection.insert_one({"task_id": text_id, "text": text})
        print(f"Text with id {text_id} added successfully")
    except Exception as e:
        print(f"Error adding text with id {text_id}: {str(e)}")
        raise


async def add_file_with_id(mongo_db, file_id, file_content):
    try:
        print(f"Adding file with id {file_id}")
        fs = GridFS(mongo_db, collection="users")
        file_id = fs.put(file_content, filename=file_id)
        print(f"File with id {file_id} added successfully")
    except Exception as e:
        print(f"Error adding file with id {file_id}: {str(e)}")
        raise
