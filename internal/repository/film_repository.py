from internal.models.film import FilmBase
from internal.repository.base import BaseRepository


class FilmRepository(BaseRepository):
    select_query = "SELECT * FROM film"    
    async def get(self):
        film_list = await self.db.fetch_all(query=self.select_query)
        return film_list
        