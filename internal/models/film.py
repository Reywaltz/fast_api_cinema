from internal.models.core import CoreModel, IDMixCoreModel
from typing import Optional

class FilmBase(CoreModel, IDMixCoreModel):
    title: str
    description: str
    film_path: str
    poster_path: Optional[str]

class FilmCreate(CoreModel):
    title: str
    description: str
    film_path: str
    poster_path: Optional[str]
