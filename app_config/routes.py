from sanic import response
from sanic import Unauthorized
import uuid
from authentication import functionality
from redisdb.redis_utils import (delete_text_by_id, add_text_with_id,
                                 add_file_with_id, update_task_status,
                                 check_user_token, check_task_status)
import mongodb.mongo_utils as mongo_db
import redisdb.redis_utils as redis_db
import utils.route_signature as routes_sign
from utils.permissions_utils import check_user_permission
from utils.raise_utils import json_response
from utils.auth_hash import generate_user_id
from utils.token_utils import generate_auth_user_pack, generate_registration_code


async def add_text(request):
    user_data = await get_user_data(request)

    if user_data is None:
        return json_response(401, description=f"User not Authenticated.")

    body = request.body

    if not body:
        return json_response(400, description=f"Empty text provided.")

    text_add = body.decode('utf-8')
    text_id = str(uuid.uuid4())

    await add_text_with_id(request.app.ctx.redis, text_id, text_add)

    return json_response(200, {
        "task_id": text_id,
        "message": "Text add task enqueued successfully",
        "added_text": text_add,
    })


async def add_file(request):
    user_data = await get_user_data(request)

    if user_data is None:
        return json_response(401, description=f"User not Authenticated.")

    file_field = request.files.get('file')

    if file_field is None:
        return json_response(400, description=f"No file provided.")

    file_content = file_field.body
    file_id = str(uuid.uuid4())

    await add_file_with_id(request.app.ctx.redis, file_id, file_content)

    return json_response(200, {
        "task_id": file_id,
        "message": "File add task enqueued successfully",
    })


async def get_task_status(request, task_id):
    user_data = await get_user_data(request)

    if user_data is None:
        return json_response(401, description="User not authenticated.")

    # # Check if the user has permission to get task status (you might need to implement this function)
    # if not check_user_permission(user_data):
    #     return json_response(403, description="Insufficient permissions.")

    try:
        task_status = await check_task_status(request.app.ctx.redis, task_id)
        return json_response(200, {"task_id": task_id, "status": task_status})
    except Exception as e:
        return json_response(500, description=f"Failed to get task status: {str(e)}")


async def find_text_by_id(request, task_id):
    user_data = await get_user_data(request)

    if user_data is None:
        return json_response(401, description=f"User not Authenticated.")

    result = await request.app.ctx.redis.hget("text_collection", task_id)

    if result:
        return response.json({
            "text_id": task_id,
            "text": result,
        })
    else:
        return json_response(404, description="Text not found")


async def delete_text(request, text_id):
    user_data = await get_user_data(request)

    if user_data is None:
        return json_response(401, description=f"User not Authenticated.")

    await delete_text_by_id(request.app.ctx.redis, text_id)

    return response.json({
        "message": f"Text with id {text_id} deleted successfully",
    })


async def route_add_text(request):
    return await add_text(request)


async def route_delete_text(request, text_id):
    return await delete_text(request, text_id)


async def add_file_route(request):
    return await add_file(request)


async def route_get_text(request, task_id):
    return await find_text_by_id(request, task_id)


async def route_get_task_status(request, task_id):
    return await get_task_status(request, task_id)


async def add_response_headers(_, responses):
    responses.headers["Accept"] = "application/json"


async def get_user_data(request):
    user_id = request.headers.get('user_id')
    session_id = request.headers.get('session_id')
    token = request.headers.get('token')

    if user_id is None or session_id is None or token is None:
        raise Unauthorized("User Not Authorized")

    user_data = await check_user_token(request.app.ctx.redis, user_id, session_id, token)

    return user_data


async def login_route(request):
    user_data: dict = request.json

    if not functionality.validate_schema_login_route(user_data):
        return json_response(400, description=f"Provided fields are not Valid.")

    sanic_ref = request.route.ctx.refsanic.ctx

    user_id = generate_user_id(user_data)
    user_signature = {"id": user_id}

    user_exist = await mongo_db.exists_user(sanic_ref.mongo, user_signature)
    if not user_exist:
        return json_response(401, description=f'User was not found.')

    token, session_id = generate_auth_user_pack()
    await redis_db.remember_user_session(sanic_ref.redis, token, user_id, session_id)

    return json_response(200, token=token, session_id=session_id, user_id=user_id, description=f"Success.")


async def create_registration_code_route(request):
    user_data: dict = request.json

    if not functionality.validate_schema_create_reg_code(user_data):
        return json_response(400, description=f"Provided fields are not Valid.")

    sanic_ref = request.route.ctx.refsanic.ctx

    is_good = await check_user_permission(routes_sign.CreateRegistrationCode(sanic_ref=sanic_ref,
                                                                             user_data=user_data))
    if not is_good:
        return json_response(401, description=f"You dont have access.")

    reg_code = generate_registration_code()

    await redis_db.insert_registration_code(sanic_ref.redis, reg_code, user_data.get("role"))

    new_token = await functionality.update_user_token(
        user_id=user_data["user_id"],
        session_id=user_data["session_id"],
        redis_db=sanic_ref.redis)

    return json_response(200, token=new_token, code=reg_code, description="Registered.")


async def check_registration_code_route(request):
    user_data: dict = request.json

    if not functionality.validate_schema_registration_code(user_data):
        return json_response(400, description=f"Provided fields are not Valid.")

    sanic_ref = request.route.ctx.refsanic.ctx

    if not await redis_db.find_registration_code(sanic_ref.redis, user_data.get("register_code")):
        return json_response(401, description=f"Not valid code.")

    return json_response(200, description=f"Valid Code.")


async def register_route(request):
    user_data: dict = request.json

    if not functionality.validate_schema_registration_route(user_data):
        return json_response(400, description=f"Provided fields are not valid.")

    sanic_ref = request.route.ctx.refsanic.ctx
    user_id, user_data = generate_user_id(user_data, get_user=True)

    user_role = await check_user_permission(
        routes_sign.RegisterAccount(sanic_ref=sanic_ref, user_data=user_data)
    )

    if not user_role:
        return json_response(401, description=f"You are not granted, to do so.")

    user_signature = {
        "email": user_data.get("email"),
        "login": user_data.get("login")
    }

    user_exist = await mongo_db.exists_user(sanic_ref.mongo, user_signature)
    if user_exist:
        return json_response(401, description=f"Email address or login is being used by another user.")

    user_data["role"] = user_role

    await mongo_db.register_user(sanic_ref.mongo, user_data)
    await redis_db.remove_registration_code(sanic_ref.redis, user_data.get("registration_code"))

    return json_response(200, description=f"Registered successfully.")


async def patch_user_route(request):
    user_data: dict = request.json

    if not functionality.validate_schema_patch_user(user_data):
        return json_response(400, description=f"Provided fields are not valid.")

    sanic_ref = request.route.ctx.refsanic.ctx

    can_user_change_settings = await check_user_permission(
        routes_sign.SettingsAccount(sanic_ref=sanic_ref, user_data=user_data)
    )

    if not can_user_change_settings:
        return json_response(401, description=f"You are not valid.")

    await mongo_db.replace_settings(mongo_db, user_data["user_id"], user_data["settings"])

    new_token = await functionality.update_user_token(
        user_id=user_data["user_id"],
        session_id=user_data["session_id"],
        redis_db=sanic_ref.redis)

    return json_response(200, token=new_token, description=f"Success.")
