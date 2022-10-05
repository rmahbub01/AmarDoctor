from doctor.core.config import settings
from doctor.crud.crud_utility import user
from doctor.db import base
from doctor.db.base_class import Base
from doctor.db.session import engine
from doctor.schemas.user import UserCreateBase
from sqlalchemy.orm import Session
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)


    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



    users = await user.get_by_mobile(db, mobile=settings.FIRST_USER_MOBILE)
    if not users:
        user_in = UserCreateBase(
            full_name=settings.FIRST_SUPERUSER,
            gender=settings.FIRST_SUPERUSER_GENDER,
            mobile=settings.FIRST_SUPERUSER_MOBILE,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_admin=True
        )
        await user.create(db, obj_in=user_in)
    await db.close()
