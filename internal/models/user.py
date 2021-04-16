from datetime import datetime

from internal.models.core import CoreModel, IDMixCoreModel


class UserCreate(CoreModel):
    username: str
    password: str
    access_token: str
    valid_to: datetime


class UserBase(IDMixCoreModel, UserCreate):
    pass
