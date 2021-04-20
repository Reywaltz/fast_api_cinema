from internal.models.core import CoreModel, IDMixCoreModel
from typing import Union


class FilmBase(CoreModel):
    title: str
    year: str
    length: str
    score: float
    poster: str
    frame: list[str]
    plot: str
    video: str


class FilmJoined(FilmBase, IDMixCoreModel):
    director: list[Union[str, None]]
    genre: list[Union[str, None]]
    award: list[Union[str, None]]
    actor: list[Union[str, None]]
    country: list[Union[str, None]]


class FilmCreate(FilmBase):
    director: list[Union[int, None]]
    genre: list[Union[int, None]]
    award: list[Union[int, None]]
    actor: list[Union[int, None]]
    country: list[Union[int, None]]
