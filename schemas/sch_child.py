from datetime import date
from pydantic import BaseModel
from typing import List, Optional
from schemas import sch_parent

class BaseChild(BaseModel):
    parent_id : str
    account_id : str
    img_profile : str
    fullname : str
    gender : str
    religion : str
    place_of_birth : str
    date_of_birth : date
    address : str
    village : str
    district : str
    city : str
    province : str
    relation : str

    class Config():
        orm_mode = True

class UpdateChild(BaseModel):
    child_id : str
    parent_id : Optional[str]
    account_id : str
    img_profile : Optional[str]
    fullname : Optional[str]
    gender : Optional[str]
    religion : Optional[str]
    place_of_birth : Optional[str]
    date_of_birth : Optional[date]
    address : Optional[str]
    village : Optional[str]
    district : Optional[str]
    city : Optional[str]
    province : Optional[str]
    relation : Optional[str]
    updated_by : str

    class Config():
        orm_mode = True

class ChildID(BaseModel):
    child_id : str

    class Config():
        orm_mode = True

class ChildData(BaseModel):
    child_id : str
    fullname : str

    class Config():
        orm_mode = True

class ChildWithParent(BaseChild):
    parent_data : sch_parent.ShowParent

    class Config():
        orm_mode = True

class InsertedChild(BaseChild):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True