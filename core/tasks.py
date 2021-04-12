import os

import asyncpg
from fastapi import FastAPI


def create_start_app_handler(app: FastAPI):
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI):
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


async def connect_to_db(app: FastAPI) -> None:
    try:
        database = await asyncpg.connect(os.getenv("DB_URL"))
        app.state._db = database
    except Exception as e:
        print(e)


async def close_db_connection(app: FastAPI) -> None:
    try:
        app.state._db.terminate()
    except Exception as e:
        print(e)
