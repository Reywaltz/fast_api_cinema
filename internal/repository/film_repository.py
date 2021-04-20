from asyncpg.exceptions import UniqueViolationError
from internal.models.film import FilmBase, FilmCreate, FilmJoined
from internal.repository.base import BaseRepository

base_film_fields = "title, year, length, score, poster, frame, plot, video"
all_film_fields = "id, " + base_film_fields


class FilmRepository(BaseRepository):
    select_query = "select film.id, film.title, film.year,\
                    film.length, film.score, film.poster,\
                    film.frame, film.plot, film.video,\
                    array_agg(DISTINCT director.name) as director,\
                    array_agg(DISTINCT genre.name) as genre,\
                    array_agg(DISTINCT award.name) as award,\
                    array_agg(DISTINCT actor.name) as actor,\
                    array_agg(DISTINCT country.name) as country from film\
                    left join film_genre ON film_genre.film_id = film.id\
                    left join genre ON genre.id = film_genre.genre_id\
                    left join film_director ON film_director.film_id = film.id\
                    left join director on director.id = film_director.director_id\
                    left join film_award ON film_award.film_id = film.id\
                    left join award ON award.id = film_award.award_id\
                    left join film_actor ON film_actor.film_id = film.id\
                    left join actor on actor.id = film_actor.actor_id\
                    left join film_country ON film_country.film_id = film.id\
                    left join country on country.id = film_country.country_id\
                    group by film.id" # noqa

    select_one_query = "select film.id, film.title, film.year,\
                    film.length, film.score, film.poster,\
                    film.frame, film.plot, film.video,\
                    array_agg(DISTINCT director.name) as director,\
                    array_agg(DISTINCT genre.name) as genre,\
                    array_agg(DISTINCT award.name) as award,\
                    array_agg(DISTINCT actor.name) as actor,\
                    array_agg(DISTINCT country.name) as country from film\
                    left join film_genre ON film_genre.film_id = film.id\
                    left join genre ON genre.id = film_genre.genre_id\
                    left join film_director ON film_director.film_id = film.id\
                    left join director on director.id = film_director.director_id\
                    left join film_award ON film_award.film_id = film.id\
                    left join award ON award.id = film_award.award_id\
                    left join film_actor ON film_actor.film_id = film.id\
                    left join actor on actor.id = film_actor.actor_id\
                    left join film_country ON film_country.film_id = film.id\
                    left join country on country.id = film_country.country_id\
                    where film.id=$1\
                    group by film.id" # noqa

    create_film_query = f"INSERT INTO film ({base_film_fields})\
                         VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id"
    create_film_award_query = "INSERT INTO film_award VALUES ($1, $2)"
    create_film_genre_query = "INSERT INTO film_genre VALUES ($1, $2)"
    create_film_actor_query = "INSERT INTO film_actor VALUES ($1, $2)"
    create_film_country_query = "INSERT INTO film_country VALUES ($1, $2)"
    create_film_director_query = "INSERT INTO film_director VALUES ($1, $2)"

    delete_query = "DELETE FROM film WHERE id=$1 RETURNING id"
    update_query = "UPDATE film SET title=$1, description=$2, film_path=$3, poster_path=$4 WHERE id=$5" # noqa

    async def get(self) -> list[FilmJoined]:
        film_list = await self.db.fetch(self.select_query)
        return film_list

    async def get_one(self, id: int) -> FilmJoined:
        pr_one_film = await self.db.prepare(self.select_one_query)
        film = await pr_one_film.fetchrow(id)
        if film is None:
            return
        return FilmJoined(**film)

    async def create(self, new_film: FilmCreate):
        pr_create_film = await self.db.prepare(self.create_film_query)
        pr_create_film_award = await self.db.prepare(self.create_film_award_query) # noqa
        pr_create_film_actor = await self.db.prepare(self.create_film_actor_query) # noqa
        pr_create_film_genre = await self.db.prepare(self.create_film_genre_query) # noqa
        pr_create_film_country = await self.db.prepare(self.create_film_country_query) # noqa
        pr_create_film_director = await self.db.prepare(self.create_film_director_query) # noqa
        try:
            async with self.db.transaction():
                res = await pr_create_film.fetchrow(
                    new_film.title,
                    new_film.year,
                    new_film.length,
                    new_film.score,
                    new_film.poster,
                    new_film.frame,
                    new_film.plot,
                    new_film.video
                )
                film_id = res[0]

                for award in new_film.award:
                    if award is not None:
                        await pr_create_film_award.fetch(
                            film_id,
                            award
                        )

                for actor in new_film.actor:
                    if actor is not None:
                        await pr_create_film_actor.fetch(
                            film_id,
                            actor
                        )

                for country in new_film.country:
                    if country is not None:
                        await pr_create_film_country.fetch(
                            film_id,
                            country
                        )

                for genre in new_film.genre:
                    if genre is not None:
                        await pr_create_film_genre.fetch(
                            film_id,
                            genre
                        )

                for director in new_film.director:
                    if director is not None:
                        await pr_create_film_director.fetch(
                            film_id,
                            director
                        )

        except Exception as e:
            print(e)

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
