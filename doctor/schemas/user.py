from typing import Optional, List
import uuid
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime

##########################
# for dummy doctor
########################
# this UserDummy is albo usredummycreate , Update base schema
class UserDummyBase(BaseModel):
    full_name : Optional[str] = None
    degree : Optional[str] = None
    specialities : Optional[str] = None
    chamber : Optional[str] = None
    address : Optional[str] = None
    visiting_hour : Optional[str] = None
    contact_number : Optional[str] = None


class UserDummyCreate(UserDummyBase):
    pass

class UserDummyUpdate(UserDummyBase):
    pass

class UserDummy(UserDummyBase):
    id : uuid.UUID
    user_id : uuid.UUID

    class Config:
        orm_mode = True

class UserDummyApi(UserDummy):
    pass


#User Schemas
class UserBase(BaseModel):
    #personal info 
    full_name : Optional[str] = None
    gender : Optional[str] = None
    mobile : Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin : bool = False
    is_superuser : bool = False
    created_on : Optional[datetime]

    @validator('full_name')
    def name_validator(cls, v):
        if v == None or v.strip() == '':
            raise ValueError('Name is not valid!')
        return v 
    
    @validator('mobile')
    def mobile_validator(cls, v):
        if len(v)==11 and isinstance(int(v), int):
            return v
        raise ValueError('The number format is invalid. Use numbers like 017xxxxxxxx')



class UserCreateBase(UserBase):
    full_name : str
    gender : str
    mobile : str
    email: Optional[EmailStr]=None
    password : str 

    @validator('password')
    def password_validator(cls, v):
        if len(v)<5:
            raise ValueError('Password must be equal or greater than 5 characters')
        return v

    
class UserUpdateBase(UserBase):
    full_name : Optional[str] = None
    email: Optional[EmailStr] = None
    password : Optional[str] = None

#update user password schema
class UserChangePassword(BaseModel):
    password : str

    @validator('password')
    def password_validator(cls, v):
        if len(v)<5:
            raise ValueError('Password must be equal or greater than 5 characters')
        return v


class UserInDBBase(UserBase):
    id : Optional[uuid.UUID] = None
    # dummydoctor : List[UserDummy] = []


    class Config:
        orm_mode = True

#for additional info returned by api
class UserApi(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password : str
