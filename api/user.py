from fastapi import APIRouter, Depends
from internal.models import user
from internal.repository import user_repository
from core.dependencies import database

router = APIRouter()

@router.post("/user")
async def create_user(new_user: user.UserCreate,
                      user_repo: user_repository.UserRepository = Depends(database.get_repository(user_repository.UserRepository))):
    created_user = await user_repo.create(user=new_user)
    return new_user