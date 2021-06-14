from typing import List

from fastapi import APIRouter,status, Depends


from utils import oauth2
from configs.db_config import SessionLocal
from crud.dal_about import aboutDAL
from models.about_app import About
from dependencies.dpd_about_dal import get_about_dal
from schemas import sch_about, sch_account

router = APIRouter()


@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=sch_about.InsertedAbout)
async def create_about(about_input: sch_about.InsertAbout):
    async with SessionLocal() as session:
        async with session.begin():
            about_dal = aboutDAL(session)
            return await about_dal.create_about(about_input.description, about_input.about_type)


@router.get("/find/{about_type}", status_code=status.HTTP_200_OK, response_model=sch_about.BaseAbout)
async def find_account(about_type, about_dal: aboutDAL = Depends(get_about_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    return await about_dal.get_about_data(about_type)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[sch_about.BaseAbout])
async def get_all_abouts(about_dal: aboutDAL = Depends(get_about_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)) -> List[About]:
    return await about_dal.get_all_abouts()

        
@router.put("/update/{about_type}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_about.UpdatedAbout)
async def update_about_data(about_type, about_input: sch_about.UpdateAbout = Depends(sch_about.UpdateAbout.as_form), 
about_dal: aboutDAL = Depends(get_about_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            about_dal = aboutDAL(session)
            await about_dal.update_about(about_type, about_input.description, about_input.updated_by)

            return await about_dal.get_about_data(about_type)