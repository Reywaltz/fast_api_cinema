from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from core.dependencies.database import get_repository
from fastapi import APIRouter, Depends
from fastapi.param_functions import Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from internal.models.user import UserCreate
from internal.repository.user_repository import UserRepository
from passlib.context import CryptContext

router = APIRouter(prefix='/users', tags=['user'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users", auto_error=True)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


@router.post("/signup", status_code=201)
async def sign_up(username: str = Form(...),
                  password: str = Form(...),
                  user_repo: UserRepository = Depends(get_repository(UserRepository))):
    check_user = await user_repo.get_one(username)
    if check_user is not None:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exists"}
        )
    password_hash = pwd_context.hash(password)
    new_user = UserCreate(username=username,
                          password=password_hash,
                          access_token=str(uuid4()),
                          valid_to=datetime.now(ZoneInfo("Europe/Moscow")) + timedelta(hours=1))
    await user_repo.insert(new_user)
    return JSONResponse(
        status_code=201,
        content={"message": "created"}
    )


@router.post("")
async def login(username: str = Form(...),
                password: str = Form(...),
                user_repo: UserRepository = Depends(get_repository(UserRepository))):
    cur_user = await user_repo.get_one(username)
    if (cur_user is None) or not (pwd_context.verify(password, cur_user.password)):
        return JSONResponse(
            status_code=404,
            content={"message": "Wrong user or password"}
        )
    cur_user.access_token = str(uuid4())
    cur_user.valid_to = datetime.now(ZoneInfo("Europe/Moscow")) + timedelta(hours=1)
    await user_repo.update(cur_user)
    return JSONResponse(
        status_code=200,
        content={"message": "authed"}
    )
