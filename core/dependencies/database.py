from typing import Callable

from asyncpg.connection import Connection
from fastapi import Depends, Request
from internal.repository.base import BaseRepository
from pkg.logger import logger

logger = logger.Logger.new_logger('file_log')


def get_database(request: Request) -> Connection:
    return request.app.state._db


def get_repository(RepoType: BaseRepository) -> Callable:
    def get_repo(db: Connection = Depends(get_database)):
        return RepoType(db, logger)
    return get_repo
