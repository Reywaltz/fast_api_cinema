from asyncpg.exceptions import UniqueViolationError
from core.dependencies.database import get_repository
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from internal.models.film import FilmBase, FilmCreate
from internal.repository.film_repository import FilmRepository
from starlette.responses import JSONResponse

from api.additions.additions import auth_required

router = APIRouter(prefix="/films", tags=['films'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users", auto_error=True)


@router.get("", response_model=list[FilmBase],)
async def film_list(film_repo: FilmRepository = Depends(get_repository(FilmRepository))) -> list[FilmBase]: # noqa
    film_list = await film_repo.get()
    return film_list


@router.get("/{id}",
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


@router.post("",
             status_code=status.HTTP_201_CREATED)
async def create_film(new_film: FilmCreate,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository)), # noqa
                      authorized: bool = Depends(auth_required)):
    if not authorized:
        return JSONResponse(
            status_code=401,
            content={"message": "no auth"}
        )
    try:
        await film_repo.create(new_film)
        film_repo.logger.info(f"Создан фильм под названием: {new_film.title}")
    except UniqueViolationError:
        film_repo.logger.info(f"Фильм под названием {new_film.title} уже существует") # noqa
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Film already exists"}
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"success": "created"}
    )


@router.delete("/{id}")
async def delete_film(id: int,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository)), # noqa
                      authorized: bool = Depends(auth_required)):
    if not authorized:
        return JSONResponse(
            status_code=401,
            content={"message": "no auth"}
        )
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


@router.put("/{id}")
async def update_film(id: int,
                      updated_film: FilmCreate,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository)), # noqa
                      authorized: bool = Depends(auth_required)):
    if not authorized:
        return JSONResponse(
                status_code=401,
                content={"message": "no auth"}
            )
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
