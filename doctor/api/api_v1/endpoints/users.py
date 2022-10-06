from typing import Any, List, Union, Optional
from doctor.api import deps
from doctor.core.config import settings
from doctor.crud.crud_dummy import dummydoctor
from doctor.crud.crud_utility import user
from doctor.db.init_db import init_db
from doctor.models.usermodel import User
from doctor.schemas.token import Token, TokenPayload
from doctor.schemas.user import (UserApi, UserBase, UserCreateBase,
                                 UserUpdateBase)
from fastapi import APIRouter, Body, Depends, HTTPException, Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from doctor.helper.email import *



router = APIRouter()


@router.get("/read_users", response_model=List[UserApi])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await user.get_multi(db, skip=skip, limit=limit)
    return users



@router.post("/create_user", response_model=UserApi)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreateBase,
    background_tasks : BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    users = await user.get_by_mobile(db, mobile=user_in.mobile)
    if users:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    users = await user.create(db, obj_in=user_in)

    if settings.EMAILS_ENABLED and user_in.email:
        #email will be sent in the background
        background_tasks.add_task(send_new_account_email, email_to=user_in.email, username=user_in.email, password=user_in.password)

    return users


@router.patch("/update/me", response_model=UserApi)
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(None),
    email:Optional[EmailStr]= Body(None),
    password: str = Body(None),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdateBase(**current_user_data)

    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    users = await user.update(db, db_obj=current_user, obj_in=user_in)
    return users


@router.get("/me", response_model=UserApi)
async def read_user_me(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=UserApi)
async def create_user_open(
    *,
    background_tasks : BackgroundTasks,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(...),
    gender: str = Body(...),
    mobile: str = Body(...),
    email : EmailStr = Body(...),
    password: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    users = await user.get_by_mobile(db, mobile=mobile) or await user.get_by_email(db, email)
    if users:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system",
        )
    user_in = UserCreateBase(
        full_name=full_name,gender=gender, mobile=mobile, password=password, email=email)

    users = await user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        #email will be sent in the background
        background_tasks.add_task(send_new_account_email, email_to=user_in.email, username=user_in.mobile, password=user_in.password)

    return users


@router.get("/{user_id}", response_model=UserApi)
async def read_user_by_id(
    user_id: str,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    users = await user.get(db, id=user_id)
    if users == current_user:
        return users
    if not user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return users


@router.patch("/update/{user_id}", response_model=UserApi)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: UserUpdateBase,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    users = await user.get(db, id=user_id)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    users = await user.update(db, db_obj=users, obj_in=user_in)
    return users
