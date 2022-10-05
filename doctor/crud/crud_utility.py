import uuid
from typing import Any, Dict, Optional, Union

from doctor.core import security
from .base import CRUDBase

from doctor.models.usermodel import DummyDoctor, User
from doctor.schemas.token import Token, TokenPayload
from doctor.schemas.user import (UserBase, UserCreateBase, UserDummy,UserDummyApi, UserDummyBase, UserDummyCreate,UserUpdateBase)
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select


# CRUD functionalities for Normal User models
class CRUDUser(CRUDBase[User, UserCreateBase, UserUpdateBase]):
    async def get_by_mobile(self, db: Session, mobile: str) -> Optional[User]:
        query = select(User).where(User.mobile == mobile)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def create(self, db: Session, obj_in: UserCreateBase) -> User:
        db_obj = User(
            full_name=obj_in.full_name,
            gender=obj_in.gender,
            mobile=obj_in.mobile,
            email=obj_in.email,
            hashed_password= await security.get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_admin=obj_in.is_admin,
            is_superuser=obj_in.is_superuser,

        )
        # adding user to database
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: Session, db_obj: User, obj_in: Union[UserUpdateBase, Dict[str, Any]]) -> User:

        if isinstance(obj_in, dict):
            user_data = obj_in
        else:
            user_data = obj_in.dict(exclude_unset=True)
        if user_data['password']:
            hashed_password = await security.get_password_hash(
                user_data.get('password'))
            del user_data['password']
            user_data['hashed_password'] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=user_data)

    async def authenticate(self, db: Session, *, mobile: str, password: str) -> Optional[User]:
        users = await self.get_by_mobile(db, mobile=mobile)

        if not users:
            return None
        
        if not await security.verify_password(password, users.hashed_password):
            return None
        return users

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    async def is_admin(self, user: User) -> bool:
        return user.is_admin


user = CRUDUser(User)
