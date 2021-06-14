from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, DateTime, Text
from sqlalchemy_utils import UUIDType
import datetime
from configs.db_config import Base


class About(Base):
    __tablename__ = 'abouts'

    id = Column(UUIDType(binary=False),primary_key=True,index=True)
    description = Column(Text, nullable=True)
    about_type = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(String, default='System')
    updated_at = Column(DateTime, default=datetime.datetime.now())
    updated_by = Column(String, nullable=True)