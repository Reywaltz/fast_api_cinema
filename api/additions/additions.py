from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from core.dependencies.database import get_repository
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from internal.models.user import UserBase
from internal.repository.user_repository import UserRepository
from passlib.context import CryptContext

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


def read_chunk(file_name: str, start: int, length: int):
    with open(file_name, 'rb') as file:
        file.seek(start)
        data = file.read(length)
        yield data


def count_headers(range, file_size, chunk_size=10**6) -> tuple[int, int, int]:
    start = max(0, int(range.strip().split('=')[-1].split('-')[0]))
    end = min(start + chunk_size, file_size - 1)
    content_length = end + 1 - start

    return start, end, content_length


def get_range_headers(start: int,
                      end: int,
                      content_length: int,
                      file_size: int) -> dict:
    headers = {
        'Accept-Range': 'bytes',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': f'{content_length}',
        'Content-Type': 'video/mp4'
    }
    return headers


def get_file_size(file_name: str) -> int:
    file = Path(file_name)
    file_size = file.stat().st_size
    return file_size
