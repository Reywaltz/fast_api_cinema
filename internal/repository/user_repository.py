from internal.models.user import UserBase, UserCreate
from internal.repository.base import BaseRepository


class UserRepository(BaseRepository):
    select_by_username_query = "SELECT * FROM users where username=$1"
    insert_query = "INSERT INTO users (username, password, access_token, valid_to)\
                    values ($1, $2, $3, $4)"
    update_token_query = "UPDATE users SET access_token=$1, valid_to=$2\
                          WHERE id=$3"

    async def get_one(self, username: str) -> UserBase:
        user = await self.db.fetchrow(self.select_by_username_query, username)
        if user is not None:
            return UserBase(**user)
        return None

    async def insert(self, new_user: UserCreate):
        try:
            await self.db.fetch(self.insert_query,
                                new_user.username,
                                new_user.password,
                                new_user.access_token,
                                new_user.valid_to)
        except Exception as e:
            print(e)

    async def update(self, user: UserBase):
        try:
            await self.db.fetch(self.update_token_query,
                                user.access_token,
                                user.valid_to,
                                user.id)
        except Exception as e:
            print(e)
