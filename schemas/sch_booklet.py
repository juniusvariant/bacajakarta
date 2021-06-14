from pydantic import BaseModel, color
from typing import Optional
from utils.asForm import as_form
from datetime import date


class BaseBooklet(BaseModel):
    period = date
    description = str
    icon = str
    banner = str
    color = color
    class Config():
        orm_mode = True

@as_form
class InsertBooklet(BaseBooklet):
    icon = Optional[str]
    banner = Optional[str]
    class Config():
        orm_mode = True

@as_form
class UpdateBooklet(BaseBooklet):
    icon = Optional[str]
    banner = Optional[str]
    updated_by: str
    class Config():
        orm_mode = True

class InsertedBooklet(InsertBooklet):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedBooklet(UpdateBooklet):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True