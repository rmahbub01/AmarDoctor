from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from doctor.db.base_class import Base
from datetime import datetime


class User(Base):
    # id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    #relationship
    dummydoctor = relationship('DummyDoctor', back_populates='users')

    #personal details
    full_name = Column(String, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    mobile = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, default=None, unique=True)


    #credentials
    hashed_password = Column(String, nullable=False)

    #permissions
    is_active = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    created_on = Column(DateTime, default=datetime.now())


# dummy doctors model for creating doctors to show the viewers
class DummyDoctor(Base):
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    #relationship
    user_id = Column(String, ForeignKey('user.id'))
    users = relationship('User', back_populates='dummydoctor')

    #doctor details
    full_name = Column(String, nullable=False, index=True)
    degree = Column(String, nullable=True)
    specialities = Column(String, nullable=False, index=True)
    chamber = Column(String, nullable=True, index=True)
    address = Column(String, nullable=True, index=True)
    visiting_hour = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)