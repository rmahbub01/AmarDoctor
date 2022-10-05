from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, DateTime, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from doctor.db.base_class import Base
from datetime import datetime
import uuid

# this model is for our registered doctors
class UserDoctor(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)

    #personal details
    full_name = Column(String, index=True)
    gender = Column(String)

    #personal info
    email = Column(String, unique=True, index=True, nullable=False)
    nid_passport = Column(String, unique=True, index=True, nullable=False)
    #bmdc is doctor registration number giver by Bangladesh gov.
    bmdc = Column(String, unique=True, nullable=False, index=True)

    #credentials
    hashed_password = Column(String,  nullable=False)

    #permissions
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.now)

# when a UserDoctor model will be created this DoctorDetails model must be created
# this model is for additional information about doctor
class DoctorDetails(Base):
    #about the doctor
    doctor = relationship('UserDoctor', backref=backref("child", uselist=False))
    doctor_title = Column(String, index=True, nullable=True)
    doctor_type = Column(String, index=True, nullable=True)
    dateofbirth = Column(DateTime, nullable=True)
    district = Column(String, index=True, nullable=True)
    doctor_details = Column(String, nullable=True)
