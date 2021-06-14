from pydantic import BaseModel
from typing import Optional
from utils.asForm import as_form


class BaseAbout(BaseModel):
    description: str
    about_type: str
    class Config():
        orm_mode = True

@as_form
class InsertAbout(BaseAbout):
    description: Optional[str]
    about_type: Optional[str]
    class Config():
        orm_mode = True

@as_form
class UpdateAbout(BaseModel):
    description: Optional[str]
    updated_by: str
    class Config():
        orm_mode = True

class InsertedAbout(InsertAbout):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedAbout(UpdateAbout):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True