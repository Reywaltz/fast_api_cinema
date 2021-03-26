from pydantic import BaseModel

class CoreModel(BaseModel):
    pass

class IDMixCoreModel(BaseModel):
    id: int