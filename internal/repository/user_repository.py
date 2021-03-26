from uuid import uuid4

from internal.models.user import UserCreate
from internal.repository.base import BaseRepository


class UserRepository(BaseRepository):
    insert_query = """INSERT INTO users (username, password, access_token) VALUES (:username, :password, :access_token) returning id, username, password, access_token"""    
    async def create(self, user: UserCreate):
        try:
            tmp = user.dict()
            tmp["access_token"] = str(uuid4())
            new_user = await self.db.fetch_one(query=self.insert_query, values=tmp)
            return UserCreate(**new_user)
        except Exception as e:
            print(e)
            self.db.force_rollback()
