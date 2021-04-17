from datetime import datetime, timedelta
from internal.models.user import UserBase
from zoneinfo import ZoneInfo
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from core.dependencies.database import get_repository
from internal.repository.user_repository import UserRepository


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/users", auto_error=True)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

tz = ZoneInfo('Europe/Moscow')
valid_time = datetime.now(tz) - timedelta(hours=1)


async def auth_required(token: str = Depends(oauth2_schema),
                        user_repo: UserRepository = Depends(get_repository(UserRepository))) -> bool: # noqa
    user = await user_repo.get_by_token(token)
    if (user is None) or (user.valid_to < valid_time):
        return False
    return True


def password_verified(password: str, db_user: UserBase) -> bool:
    return pwd_context.verify(password, db_user.password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
