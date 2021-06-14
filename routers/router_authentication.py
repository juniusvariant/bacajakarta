from models import account
from fastapi import APIRouter, Depends, status, HTTPException
from configs import db_config, app_config
from sqlalchemy.orm import Session
from utils.hashing import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from utils import token, oauth2
from schemas import sch_account, sch_auth

from dependencies.dpd_account_dal import get_account_dal
from crud.dal_account import accountDAL

router = APIRouter()
get_db = db_config.get_db
config_setting = app_config.Settings()

@router.post('/login', status_code=status.HTTP_200_OK, response_model=sch_auth.Token)
async def login(auth_request: OAuth2PasswordRequestForm = Depends(), account_dal: accountDAL = Depends(get_account_dal)):
    email_check = await account_dal.check_account_email(auth_request.username)
    
    if not email_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Account Not Found')
    
    account_password = await account_dal.get_account_password(auth_request.username)
    if not Hash.verify(auth_request.password, account_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Incorrect Password ')
    # generate JWT token
    access_token_expires = timedelta(minutes=config_setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": auth_request.username}, expires_delta=access_token_expires
    )
    results = {
        "access_token": access_token, 
        "token_type": "bearer",
        "expired_in": config_setting.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "user_info": account_password
    }

    return results

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=sch_account.InsertedAccount)
async def create_user(account_input: sch_account.BaseAccount):
    async with db_config.SessionLocal() as session:
        async with session.begin():
            account_dal = accountDAL(session)
            
            email_check = await account_dal.check_account_email(account_input.email)
            if email_check:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Taken.")

            return await account_dal.create_account(account_input.username, account_input.email, account_input.password)