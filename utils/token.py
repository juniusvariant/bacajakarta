from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from schemas import sch_auth
from configs import app_config, db_config
from sqlalchemy.orm import Session
from fastapi import Depends

config_setting = app_config.Settings()
get_db = db_config.get_db

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=config_setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config_setting.SECRET_KEY, algorithm=config_setting.ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception, db: Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, config_setting.SECRET_KEY, algorithms=[config_setting.ALGORITHM])
        input_email: str = payload.get("sub")
        if input_email is None:
            raise credentials_exception
        token_data = sch_auth.TokenData(email=input_email)
    except JWTError:
        raise credentials_exception