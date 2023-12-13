import pymongo


async def validate_file(filename, filesize, get_config_field):
    file_extension = filename.split('.')[-1] if "." in filename else None
    valid_extension = file_extension in get_config_field("file_upload.extensions")
    valid_filesize = filesize <= get_config_field("file_upload.filesize_max")
    return valid_extension and valid_filesize, file_extension


async def add_text_task(user_id, text, get_config_field):
    try:
        mongo_uri = get_config_field("")
        database_name = ""

        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]

        texts_collection = db["texts"]
        result = texts_collection.insert_one({"user_id": user_id, "text": text})

        client.close()

        return {"status": "success"}
    except Exception as e:
        print("Error in add_text_task:", str(e))
        return {"status": "error"}
