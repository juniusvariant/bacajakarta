from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username: str
    password: str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config():
        orm_mode = True

class TokenData(BaseModel):
    email: Optional[str] = None

    class Config():
        orm_mode = True