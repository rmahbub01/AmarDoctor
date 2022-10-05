from datetime import timedelta
from typing import Any

from doctor.api import deps
from doctor.core import security
from doctor.core.config import settings
from doctor.core.security import get_password_hash
from doctor.crud.crud_utility import user
from doctor.models.usermodel import User
from doctor.schemas.token import Token, TokenPayload
from doctor.schemas.user import UserBase, UserCreateBase, UserUpdateBase, UserChangePassword
from doctor.schemas.msg import Msg
from doctor.schemas.token import Token, TokenPayload

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from starlette.responses import RedirectResponse, Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.base import SecurityBase
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError

from doctor.helper.email import *

router = APIRouter()



@router.post("/login/access-token", response_model=Token)
async def login_access_token(response : Response, db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    users = await user.authenticate(
        db, mobile=form_data.username, password=form_data.password
    )
    if not users:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not await user.is_active(users):
        raise HTTPException(status_code=400, detail="Inactive User")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await security.create_access_token(
            users.id, expires_delta=access_token_expires
        )
    response.set_cookie(
            "Authorization",
            value=f"Bearer {access_token}",
            domain=settings.SERVER_HOST.split('/')[-1],
            httponly=True,
            expires=access_token_expires,
        )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/logout")
async def logout(response:Response):
    response.delete_cookie("Authorization")
    return {'success':'User logged out successfully.'}


@router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(request:Request, email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    users = await user.get_by_email(db, email=email)

    if not users:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = await generate_password_reset_token(email=email)
    await send_reset_password_email(email_to=users.email, email=email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@router.post("/change_password/", response_model=Msg)   
async def change_password(db: Session = Depends(deps.get_db), new_password: UserChangePassword = Body(...), current_user : User = Depends(deps.get_current_active_user)) -> Any:
    """
    Reset password
    """
    
    hashed_password = await get_password_hash(new_password.password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    await db.commit()
    return {"msg": "Password updated successfully"}


@router.post("/reset-password", response_model=Msg)
async def reset_password(db: Session = Depends(deps.get_db), new_password: UserChangePassword = Body(...), current_user : User = Depends(deps.get_current_active_user)) -> Any:
    """
    Reset password
    """
    
    hashed_password = await get_password_hash(new_password.password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    await db.commit()
    return {"msg": "Password updated successfully"}
