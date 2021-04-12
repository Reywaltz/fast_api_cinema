from asyncpg.connection import Connection
from pkg.logger import logger


class BaseRepository:
    def __init__(self, db: Connection, logger: logger.Logger) -> None:
        self.db = db
        self.logger = logger
