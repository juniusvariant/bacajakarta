from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.sql.expression import null
from sqlalchemy_utils import EmailType, UUIDType
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from configs.db_config import Base
from uuid import uuid4

if TYPE_CHECKING:
    from .parent import Parent
    from .child import Child

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(UUIDType(binary=False), default=uuid4 ,primary_key=True,index=True)
    username = Column(String)
    email = Column(EmailType)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(String, default='System')
    updated_at = Column(DateTime, default=datetime.datetime.now())
    updated_by = Column(String, nullable=True)

    parent = relationship('Parent', back_populates='account')
    child = relationship('Child', back_populates='account')