from fastapi import APIRouter
from doctor.api.api_v1.endpoints import users, login, dummy_doctor


api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, tags=['login'])
api_router.include_router(dummy_doctor.router, tags=['Dummy Doctor'])
