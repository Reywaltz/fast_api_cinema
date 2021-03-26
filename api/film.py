from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from internal.models import film
from internal.repository import film_repository
from core.dependencies import database

router = APIRouter()

@router.get("/film", response_model=list[film.FilmBase])
async def film_list(film_repo = Depends(database.get_repository(film_repository.FilmRepository))):
    film_list = await film_repo.get()
    return film_list


@router.get("/film/get")
async def film_get():
    film_file = open("front_cinema/FlixGo-Online-Movies-Template/Workshop_ пишем первый проект на FastAPI.mp4", mode="rb")
    return StreamingResponse(film_file, media_type="video/mp4")