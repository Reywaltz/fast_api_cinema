from databases import Database
from pkg.logger import logger

class BaseRepository:
    def __init__(self, db: Database, logger: logger.Logger) -> None:
        self.db = db
        self.logger = logger