from internal.models.core import CoreModel, IDMixCoreModel
from typing import Optional

class FilmBase(CoreModel, IDMixCoreModel):
    title: str
    path: str
    poster: Optional[str]
