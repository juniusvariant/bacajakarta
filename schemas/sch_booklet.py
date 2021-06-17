from pydantic import BaseModel, color
from typing import List, Optional
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

class BaseMission(BaseModel):
    booklet_id = str
    mission_date = date
    task = str
    mission_type = str
    description = str
    icon = str
    color = str
    tags = List[str]
    is_for = str
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

@as_form
class InsertMission(BaseMission):
    icon = Optional[str]
    color = Optional[str]
    tags = Optional[List[str]]
    class Config():
        orm_mode = True

@as_form
class UpdateMission(BaseMission):
    icon = Optional[str]
    color = Optional[str]
    tags = Optional[List[str]]
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

class InsertedMission(InsertMission):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedMission(UpdateMission):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True