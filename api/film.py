import aiofiles
from aiofiles.base import AiofilesContextManager
from asyncpg.exceptions import UniqueViolationError
from core.dependencies.database import get_repository
from pathlib import Path
from pprint import pprint
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from internal.models.film import FilmBase, FilmCreate, FilmJoined
from internal.repository.film_repository import FilmRepository
from fastapi.responses import JSONResponse, StreamingResponse

router = APIRouter(prefix="/films", tags=['films'])

router.mount('', 'front', 'front')
templates = Jinja2Templates(directory='front')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users", auto_error=True)


@router.get("", response_model=list[FilmJoined])
async def film_list(request: Request): # noqa
    return templates.TemplateResponse('index.html', {"request": request})
    
    # film_list = await film_repo.get()
    # return film_list


# @router.get("/{id}",
#             response_model=FilmJoined)
# async def film_one(id: int,
#                    film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
#     fetched_film = await film_repo.get_one(id)
#     if fetched_film is None:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": "not found"}
#         )

#     return fetched_film


# @router.post("",
#              status_code=status.HTTP_201_CREATED)
# async def create_film(new_film: FilmCreate,
#                       film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa

#     try:
#         await film_repo.create(new_film)
#         film_repo.logger.info(f"Создан фильм под названием: {new_film.title}")
#     except UniqueViolationError:
#         film_repo.logger.info(f"Фильм под названием {new_film.title} уже существует") # noqa
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"message": "Film already exists"}
#         )

#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content={"success": "created"}
#     )


# @router.delete("/{id}")
# async def delete_film(id: int,
#                       film_repo: FilmRepository = Depends(get_repository(FilmRepository))): # noqa
#     try:
#         deleted = await film_repo.delete(id)
#     except Exception as e:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={"message": f"error {e}"}
#         )

#     if deleted is None:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"error": "No such film"}
#         )

#     return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={"message": f"Deleted {id}"}
#         )

def ranged(
        file,
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
):
    consumed = 0

    file.seek(start)
    while True:
        # Смотрим длину запрашиваемых байтов в файле
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        # Отправленные байты
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


async def open_file(request: Request) -> tuple:
    path = Path('test/videoplayback.mp4')
    file = path.open('rb')
    file_size = path.stat().st_size
    chunk = 10 ** 6

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        # Очищаем длину запрашиваемого контента
        content_range = content_range.strip().lower()
        pprint(content_range)
        # Получаем длину
        content_ranges = content_range.split('=')[-1]
        # Получаем начальную длину и конечную
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        # Проверяем, что запрашиваемый чанк не выходит за начало файла
        range_start = max(0, int(range_start)) if range_start else 0
        # Проверяем, что запрашиваемый чанк не выходит за конец файла
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

        range_start = content_range.split('=')[-1].split('-')[0]
        range_end = min(int(range_start) + chunk, file_size - 1)

        print(range_start, range_end)

    return file, status_code, content_length, headers


# @router.get("/fake")
# async def fake(request: Request) -> StreamingResponse:
#     file, status_code, content_length, headers = await open_file(request)

#     response = StreamingResponse(
#         file,
#         media_type='video/mp4',
#         status_code=status_code
#     )

#     response.headers.update({
#         'Accept-Ranges': 'bytes',
#         'Content-Length': str(content_length),
#         **headers
#     })
    # print(file, status_code, content_length, headers)
    # return response

@router.get("/fake")
async def fake(request: Request):
    range_header = request.headers.get('range', None)
    if not range_header:
        return JSONResponse("bad q", 400)
    chunk_size = 10 ** 6
    file = Path("test/video.mp4")
    file_size = file.stat().st_size
    start = max(0, int(range_header.strip().split('=')[-1].split('-')[0]))

    end = min(start + chunk_size, file_size - 1)
    content_length = end + 1 - start

    file = read_chunk('test/video.mp4', start, content_length)

    headers = {
        "Accept-Range": 'bytes',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': f"{content_length}",
        'Content-Type': 'video/mp4'
    }

    return StreamingResponse(
        file,
        status_code=206,
        headers=headers,
        media_type='video/mp4'
    )


def read_chunk(file_name: str, start: int, length: int):
    with open(file_name, 'rb') as file:
        file.seek(start)
        data = file.read(length)
        yield data
