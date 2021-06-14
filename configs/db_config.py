from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from configs import app_config

""" SQLALCHEMY_DATABASE_URL =  'postgresql://juniusvariant@127.0.0.1:5432/bacajakarta_db'

engine =  create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() """
conf = app_config.Settings()

app_mode = conf.APP_MODE

if app_mode == 'Development':
    SQLALCHEMY_DATABASE_URL =  "postgresql+asyncpg://juniusvariant@127.0.0.1:5432/bacajakarta_db"
if app_mode == 'Production':
    SQLALCHEMY_DATABASE_URL =  "postgresql://usthyfbohhvykd:2ff06dd828917f5f8f0fef027d11d4337bef1815a91a84b176a0f86ae44b6377@ec2-35-171-250-21.compute-1.amazonaws.com:5432/depk1bbdajorbf"

engine =  create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()