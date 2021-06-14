from typing import List

from fastapi import APIRouter,status, Depends


from utils import oauth2
from configs.db_config import SessionLocal
from crud.dal_account import accountDAL
from models.account import Account
from dependencies.dpd_account_dal import get_account_dal
from schemas import sch_account

router = APIRouter()


@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=sch_account.InsertedAccount)
async def create_user(account_input: sch_account.BaseAccount):
    async with SessionLocal() as session:
        async with session.begin():
            account_dal = accountDAL(session)
            return await account_dal.create_account(account_input.username, account_input.email, account_input.password)


@router.get("/find/{account_id}", status_code=status.HTTP_200_OK, response_model=sch_account.ShowAccount)
async def find_account(account_id: str, account_dal: accountDAL = Depends(get_account_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    return await account_dal.get_account_data(account_id)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[sch_account.ShowAccount])
async def get_all_accounts(account_dal: accountDAL = Depends(get_account_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)) -> List[Account]:
    return await account_dal.get_all_accounts() 

        
@router.put("/update/{account_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_account.UpdatedAccount)
async def update_account_data(account_id, account_input: sch_account.UpdateAccount = Depends(sch_account.UpdateAccount.as_form), 
account_dal: accountDAL = Depends(get_account_dal), current_user: sch_account.UpdateAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            account_dal = accountDAL(session)
            await account_dal.update_account(account_id, account_input.username, account_input.email, account_input.password, account_input.updated_by)

            return await account_dal.get_account_data(account_id)