from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from configs import app_config
import cloudinary

cloudinary.config(
  cloud_name = 'hmpytvwgr',  
  api_key = '229795342785883',  
  api_secret = 'W3i1u18j5I3ibIa9mkWqvEQLhKU'  
)

conf = app_config.Settings()

app_mode = conf.APP_MODE

if app_mode == 'Development':
    SQLALCHEMY_DATABASE_URL =  "postgresql+asyncpg://juniusvariant@127.0.0.1:5432/bacajakarta_db"
if app_mode == 'Production':
    SQLALCHEMY_DATABASE_URL =  "postgresql+asyncpg://ajztaysnlmequx:5a74575cbe487d3b158b32d545e0197d701b189a6bdc67ddd92d84244ca03aea@ec2-35-171-250-21.compute-1.amazonaws.com:5432/d26hsji8et19k2"

engine =  create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()