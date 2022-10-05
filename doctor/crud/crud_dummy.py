import uuid
from typing import Any, List

from doctor.crud.base import CRUDBase
from doctor.models.usermodel import DummyDoctor
from doctor.schemas.user import UserDummyCreate, UserDummyUpdate

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select



class CRUDDummy(CRUDBase[DummyDoctor, UserDummyCreate, UserDummyUpdate]):

    async def create_dummydoctor(self, db: Session, *, obj_in: UserDummyCreate, user_id: str) -> DummyDoctor:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_dummy(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[DummyDoctor]:

        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create_dummydoctors(self, db: Session, *, dummy_list: List[UserDummyCreate], user_id: str):
        bulk = []
        for dummy in dummy_list:
            obj_in_data = jsonable_encoder(dummy)
            db_obj = self.model(**obj_in_data, user_id=user_id)
            bulk.append(db_obj)
        
        db.add_all(bulk)
        await db.commit()
        return bulk


dummydoctor = CRUDDummy(DummyDoctor)
