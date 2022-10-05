from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from doctor.core.config import settings
from doctor.db import base
from doctor.db.base_class import Base
from doctor.crud.crud_utility import user


# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    