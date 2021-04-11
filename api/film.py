from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from internal.models.film import FilmBase, FilmCreate
from internal.repository import film_repository
from asyncpg.exceptions import UniqueViolationError
from core.dependencies import database

router = APIRouter()

@router.get("/film", response_model=list[FilmBase])
async def film_list(film_repo = Depends(database.get_repository(film_repository.FilmRepository))):
    film_list = await film_repo.get()
    return film_list

@router.post("/film", status_code=201)
async def create_film(new_film: FilmCreate, 
                      film_repo = Depends(database.get_repository(film_repository.FilmRepository))):
    try:
        await film_repo.create(new_film)
    except UniqueViolationError:
        return JSONResponse(
                status_code=400, 
                content={"message": "Item already exists"}
            )

    return JSONResponse(200, {"success": "created"})
