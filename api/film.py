from asyncpg.exceptions import UniqueViolationError
from fastapi.params import Header
from core.dependencies.database import get_repository
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from internal.models.film import FilmCreate, FilmJoined
from internal.repository.film_repository import FilmRepository
from fastapi.responses import JSONResponse, StreamingResponse
from api.additions import additions

router = APIRouter(prefix='/films', tags=['films'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users", auto_error=True)


@router.get("/", response_model=list[FilmJoined])
async def film_list(film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    film_list = await film_repo.get()
    return film_list


@router.get("/{id}",
            response_model=FilmJoined)
async def film_one(id: int,
                   film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
    fetched_film = await film_repo.get_one(id)
    if fetched_film is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "not found"}
        )

    return fetched_film


@router.post("/",
             status_code=status.HTTP_201_CREATED)
async def create_film(new_film: FilmCreate,
                      film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa

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


# TODO поменять путь по фильму в зависимости от выбранного качества
@router.get("/{id}/{newid}")
async def fake(id: int, newid: int, range: str = Header(None)):
    if not range:
        return JSONResponse({"status": "bad request"}, 400)

    file_size = additions.get_file_size('test/video.mp4')
    start, end, content_length = additions.count_headers(range, file_size)
    file = additions.read_chunk('test/video.mp4', start, content_length)
    headers = additions.get_range_headers(start,
                                          end,
                                          content_length,
                                          file_size)

    return StreamingResponse(
        file,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=headers,
        media_type='video/mp4'
    )
