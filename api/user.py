from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from core.dependencies.database import get_repository
from fastapi import APIRouter, Depends
from fastapi.param_functions import Form
from fastapi.responses import JSONResponse
from internal.models.user import UserBase, UserCreate
from internal.repository.user_repository import UserRepository

from api.additions.additions import (auth_required, hash_password,
                                     password_verified)

router = APIRouter(prefix='/users', tags=['users'])

tz = ZoneInfo('Europe/Moscow')


@router.post("/signup", status_code=201)
async def sign_up(username: str = Form(...),
                  password: str = Form(...),
                  user_repo: UserRepository = Depends(get_repository(UserRepository))): # noqa
    check_user = await user_repo.get_one(username)
    if check_user is not None:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exists"}
        )
    password_hash = hash_password(password)
    new_user = UserCreate(username=username,
                          password=password_hash,
                          access_token=str(uuid4()),
                          valid_to=datetime.now(tz) + timedelta(hours=1))
    await user_repo.insert(new_user)
    return JSONResponse(
        status_code=201,
        content={"message": "created"}
    )


@router.post("")
async def login(username: str = Form(...),
                password: str = Form(...),
                user_repo: UserRepository = Depends(get_repository(UserRepository))): # noqa
    cur_user = await user_repo.get_one(username)
    if (cur_user is None) or not (password_verified(password, cur_user)):
        return JSONResponse(
            status_code=404,
            content={"message": "Wrong user or password"}
        )
    cur_user.access_token = str(uuid4())
    cur_user.valid_to = datetime.now(tz) + timedelta(hours=1)
    await user_repo.update(cur_user)
    return JSONResponse(
        status_code=200,
        content={"access_token": cur_user.access_token}
    )


@router.get("", response_model=list[UserBase])
async def get_users(user_repo: UserRepository = Depends(get_repository(UserRepository)), # noqa
                    authorized: bool = Depends(auth_required)):
    if authorized:
        users = await user_repo.get_all()
        return users
    else:
        return JSONResponse(
            status_code=401,
            content={"message": "no auth"}
        )
