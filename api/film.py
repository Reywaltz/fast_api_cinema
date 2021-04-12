from asyncpg.exceptions import UniqueViolationError
from core.dependencies.database import get_repository
from fastapi import APIRouter, Depends, status
from internal.models.film import FilmBase, FilmCreate
from internal.repository.film_repository import FilmRepository
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/films", response_model=list[FilmBase])
async def film_list(film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    film_list = await film_repo.get()
    return film_list


@router.get("/films/{id}",
            response_model=FilmBase)
async def film_one(id: int,
                   film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    fetched_film = await film_repo.get_one(id)
    if fetched_film is None:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "not found"}
            )

    return fetched_film


@router.post("/films",
             status_code=status.HTTP_201_CREATED)
async def create_film(new_film: FilmCreate,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    try:
        await film_repo.create(new_film)
    except UniqueViolationError:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Film already exists"}
            )

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": "created"}
        )


@router.delete("/films/{id}")
async def delete_film(id: int,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    try:
        deleted = await film_repo.delete(id)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"error {e}"}
        )

    if deleted is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "No such film"}
        )

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Deleted {id}"}
        )


@router.put("/films/{id}")
async def update_film(id: int,
                      updated_film: FilmCreate,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa

    updated_film = FilmBase(id=id, **updated_film.dict())
    try:
        updated = await film_repo.update(updated_film)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"error {e}"}
        )

    if updated is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"No such film with id:{id}"}
        )

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Updated:{id}"}
        )
