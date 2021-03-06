from internal.models.core import CoreModel, IDMixCoreModel

class UserBase(CoreModel):
    username: str
    password: str
    access_token: str

class UserCreate(UserBase):
    pass