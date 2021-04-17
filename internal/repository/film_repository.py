from asyncpg.exceptions import UniqueViolationError
from internal.models.film import FilmBase, FilmCreate
from internal.repository.base import BaseRepository

base_fields = "title, description, film_path, poster_path"
all_fields = "id, " + base_fields


class FilmRepository(BaseRepository):
    select_query = f"SELECT {all_fields} FROM film"
    select_one_query = f"SELECT {all_fields} FROM film WHERE id=$1"
    create_query = f"INSERT INTO film ({base_fields}) VALUES ($1, $2, $3, $4)"
    delete_query = "DELETE FROM film WHERE id=$1 RETURNING id"
    update_query = "UPDATE film SET title=$1, description=$2, film_path=$3, poster_path=$4 WHERE id=$5" # noqa

    async def get(self) -> list[FilmBase]:
        film_list = await self.db.fetch(self.select_query)
        return film_list

    async def get_one(self, id: int) -> FilmBase:
        pr_statement = await self.db.prepare(self.select_one_query)
        film = await pr_statement.fetchrow(id)
        if film is None:
            return
        return FilmBase(**film)

    async def create(self, new_film: FilmCreate):
        try:
            pr_statement = await self.db.prepare(self.create_query)
            await pr_statement.fetch(
                new_film.title,
                new_film.description,
                new_film.film_path,
                new_film.poster_path
            )

        except UniqueViolationError:
            raise UniqueViolationError

    async def delete(self, id: int):
        try:
            deleted = await self.db.fetchrow(self.delete_query, id)
            return deleted
        except Exception as e:
            print(e)
            raise e

    async def update(self, updated_film: FilmBase):
        pr_statement = await self.db.prepare(self.update_query)
        await pr_statement.fetch(
            updated_film.title,
            updated_film.description,
            updated_film.film_path,
            updated_film.poster_path,
            updated_film.id
        )
