from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user import router as user_router
from api.film import router as film_router
from core import tasks


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.add_event_handler("startup", tasks.create_start_app_handler(app))
app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))


app.include_router(user_router, prefix="/api")
app.include_router(film_router, prefix="/api")
