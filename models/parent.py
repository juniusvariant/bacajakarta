from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Date
from sqlalchemy_utils import URLType, UUIDType
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from configs.db_config import Base
from uuid import uuid4

if TYPE_CHECKING:
    from .account import Account
    from .child import Child

class Parent(Base):
    __tablename__ = 'parents'
    
    id = Column(UUIDType(binary=False), default=uuid4,primary_key=True,index=True)
    account_id = Column(UUIDType(binary=False), ForeignKey('accounts.id'), index=True)
    img_profile = Column(URLType, nullable=True)
    fullname = Column(String)
    gender = Column(String)
    religion = Column(String)
    place_of_birth = Column(String)
    date_of_birth = Column(Date)
    address = Column(String)
    village = Column(String)
    district = Column(String)
    city = Column(String)
    province = Column(String)
    relation = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(String, default='System')
    updated_at = Column(DateTime, default=datetime.datetime.now())
    updated_by = Column(String, nullable=True)

    account = relationship('Account', back_populates='parent')
    child = relationship('Child', back_populates='parent')
