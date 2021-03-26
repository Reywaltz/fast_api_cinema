from typing import Callable

from internal.repository.base import BaseRepository
from databases import Database
from fastapi import Depends
from pkg.logger import logger
from fastapi import Request

logger = logger.Logger.new_logger('file_log')

def get_database(request: Request) -> Database:
    return request.app.state._db

def get_repository(RepoType: BaseRepository) -> Callable:
    def get_repo(db: Database = Depends(get_database)):
        return RepoType(db, logger)
    return get_repo
