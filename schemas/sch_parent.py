from enum import Enum
from datetime import date
from uuid import UUID
from utils.asForm import as_form, form_body
from pydantic import BaseModel
from typing import List, Optional

class gender(str, Enum):
    male='M'
    female='F'
    other='O'

class religion(str, Enum):
    islam='I'
    christian='C'
    protestan='P'
    budhist='B'
    hindi='H'
    other='O'

class parentRelation(str, Enum):
    father='F'
    mother='M'
    teacher='T'
    mentor='MT'

class childRelation(str, Enum):
    child='C'
    student='S'

class BaseParent(BaseModel):
    account_id : str
    img_profile : str
    fullname : str
    gender : gender
    religion : religion
    place_of_birth : str
    date_of_birth : date
    address : str
    village : str
    district : str
    city : str
    province : str
    relation : parentRelation

    class Config():
        orm_mode = True
        use_enum_values = True

@as_form
class InsertParent(BaseModel):
    account_id : str
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

@as_form
class UpdateParent(BaseModel):
    account_id : Optional[str]
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

class ShowParent(BaseModel):
    account_id : UUID
    fullname : str
    img_profile : str
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

class ParentID(BaseModel):
    parent_id : str

    class Config():
        orm_mode = True

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

@as_form
class InsertChild(BaseModel):
    parent_id : str
    account_id : str
    fullname : str
    gender : gender
    religion : religion
    place_of_birth : str
    date_of_birth : date
    address : str
    village : str
    district : str
    city : str
    province : str
    relation : childRelation

    class Config():
        orm_mode = True
        use_enum_values = True

@as_form
class UpdateChild(BaseModel):
    parent_id : Optional[str]
    account_id : str
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

class ParentWithChild(BaseParent):
    child_data : List[ChildData] = []
    class Config():
        orm_mode = True

class InsertedParent(BaseParent):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedParent(ShowParent):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True

class ChildWithParent(BaseChild):
    parent_data : ShowParent
    class Config():
        orm_mode = True

class InsertedChild(BaseChild):
    information: str = 'Insert Data Success.'
    class Config():
        orm_mode = True

class UpdatedChild(ShowParent):
    information: str = 'Updating Data Success.'
    class Config():
        orm_mode = True