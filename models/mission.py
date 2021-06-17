from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, DateTime, Date, Text, ARRAY, ForeignKey
from sqlalchemy_utils import URLType, UUIDType, ColorType
from sqlalchemy.orm import relationship
import datetime
from configs.db_config import Base

if TYPE_CHECKING:
    from .booklet import Booklet

class Mission(Base):
    __tablename__ = 'missions'

    id = Column(UUIDType(binary=False), primary_key=True, index=True)
    booklet_id = Column(UUIDType(binary=False), ForeignKey('booklets.id'), index=True)
    mission_date = Column(Date, unique=True, index=True)
    task = Column(Text)
    mission_type = Column(String, index=True)
    description = Column(Text, nullable=True)
    icon = Column(URLType, nullable=True)
    color = Column(ColorType, nullable=True)
    tags = Column(ARRAY(String))
    is_for = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(String, default='System')
    updated_at = Column(DateTime, default=datetime.datetime.now())
    updated_by = Column(String, nullable=True)

    tastHeader = relationship('Booklet', back_populates='taskDetail')
