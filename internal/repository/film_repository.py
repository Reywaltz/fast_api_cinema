from asyncpg.exceptions import UniqueViolationError

import asyncpg

from internal.models.film import FilmBase
from internal.repository.base import BaseRepository


base_fields = "title, description, film_path, poster_path"
insert_fields = "id, " + base_fields

class FilmRepository(BaseRepository):
    select_query = "SELECT * FROM film"
    select_one_query = "SELECT * FROM film WHERE title=$1"
    create_query = f"INSERT INTO film ({base_fields}) values ($1, $2, $3, $4)"

    async def get(self):
        film_list = await self.db.fetch(self.select_query)
        return film_list

    async def create(self, new_film: FilmBase):
        film_list = await self.db.fetch(self.select_one_query, new_film.title)
        try:
            pr_statement = await self.db.prepare(self.create_query)
            film = await pr_statement.fetch(
                    new_film.title, 
                    new_film.description, 
                    new_film.film_path,
                    new_film.poster_path
                )
        except UniqueViolationError as e:
            raise UniqueViolationError