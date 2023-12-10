import pymongo


async def validate_file(filename, filesize, get_config_field):
    file_extension = filename.split('.')[-1] if "." in filename else None
    valid_extension = file_extension in get_config_field("file_upload.extensions")
    valid_filesize = filesize <= get_config_field("file_upload.filesize_max")
    return valid_extension and valid_filesize, file_extension


async def add_text_task(user_id, text, get_config_field):
    try:
        mongo_uri = get_config_field("database.mongodb.uri")
        database_name = "your_database_name"

        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]

        texts_collection = db["texts"]
        result = texts_collection.insert_one({"user_id": user_id, "text": text})

        client.close()

        return {"status": "success"}
    except Exception as e:
        print("Error in add_text_task:", str(e))
        return {"status": "error"}


async def add_file_task(user_id, file_data, filename, get_config_field):
    try:
        mongo_uri = get_config_field("database.mongodb.uri")
        database_name = "your_database_name"

        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]

        files_collection = db["files"]
        result = files_collection.insert_one({"user_id": user_id, "file_data": file_data, "filename": filename})

        client.close()

        return {"status": "success"}
    except Exception as e:
        print("Error in add_file_task:", str(e))
        return {"status": "error"}


async def remove_text_task(user_id, document_id, get_config_field):
    try:
        mongo_uri = get_config_field("database.mongodb.uri")
        database_name = "your_database_name"

        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]

        texts_collection = db["texts"]
        result = texts_collection.delete_one({"_id": pymongo.ObjectId(document_id), "user_id": user_id})

        client.close()

        return {"status": "success"} if result.deleted_count > 0 else {"status": "not found"}
    except Exception as e:
        print("Error in remove_text_task:", str(e))
        return {"status": "error"}


async def register_website(website_name, get_config_field):
    try:
        mongo_uri = get_config_field("database.mongodb.uri")
        database_name = "your_database_name"

        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]

        websites_collection = db["websites"]
        existing_website = websites_collection.find_one({"name": website_name})
        if existing_website:
            return {"status": "error", "message": "Website name already registered"}

        result = websites_collection.insert_one({"name": website_name})

        client.close()

        return {"status": "success", "website_id": str(result.inserted_id)}
    except Exception as e:
        print("Error in register_website:", str(e))
        return {"status": "error", "message": "Internal server error"}
