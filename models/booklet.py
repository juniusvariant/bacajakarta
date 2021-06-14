from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, DateTime, Date, Text
from sqlalchemy_utils import URLType, UUIDType, ColorType
import datetime
from configs.db_config import Base


class Booklet(Base):
    __tablename__ = 'booklets'

    id = Column(UUIDType(binary=False),primary_key=True,index=True)
    period = Column(Date, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(URLType, nullable=True)
    banner = Column(URLType, nullable=True)
    color = Column(ColorType, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(String, default='System')
    updated_at = Column(DateTime, default=datetime.datetime.now())
    updated_by = Column(String, nullable=True)