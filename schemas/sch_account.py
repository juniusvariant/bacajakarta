from pydantic import BaseModel, EmailStr
from typing import Optional
from utils.asForm import as_form

class AccountID(BaseModel):
    account_id: str
    class Config():
        orm_mode = True

class BaseAccount(BaseModel):
    username: str
    email: EmailStr
    password: str
    class Config():
        orm_mode = True

class ShowAccount(BaseModel):
    username: str
    email: EmailStr
    class Config():
        orm_mode = True 

@as_form
class UpdateAccount(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    updated_by: str
    class Config():
        orm_mode = True

class InsertedAccount(ShowAccount):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedAccount(ShowAccount):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True