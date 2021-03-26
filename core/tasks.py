from fastapi import FastAPI
from databases import Database
# from internal.tasks import connect_to_db, close_db_connection

def create_start_app_handler(app: FastAPI):
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI):
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


async def connect_to_db(app: FastAPI) -> None:
    database = Database("postgresql://cinema:password@localhost:5432/fast_api_cinema", min_size=2, max_size=10)  # these can be configured in config as well

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        print(e)


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        print(e)