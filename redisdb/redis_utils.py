async def remember_user_session(redis_db, token, user_id, session_id, expire_in_seconds=900):
    await redis_db.setex(user_id, expire_in_seconds, f"{session_id},{token}")


async def find_registration_code(redis_db, reg_code):
    response = await redis_db.get(reg_code)
    return response


async def remove_registration_code(redis_db, reg_code):
    await redis_db.delete(reg_code)


async def insert_registration_code(redis_db, reg_code: str, user_type: str, expire_in_seconds=900) -> None:
    await redis_db.setex(reg_code, expire_in_seconds, user_type)


async def check_user_token(redis_db, user_id, session_id, token):
    response = await redis_db.get(user_id)
    return session_id in response and token in response
