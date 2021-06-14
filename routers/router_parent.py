from typing import List, Optional
import shutil

from fastapi import APIRouter,status, Depends, File, UploadFile, Form

from utils import oauth2
from configs.db_config import SessionLocal
from crud.dal_parent import parentDAL
from models.parent import Parent
from dependencies.dpd_parent_dal import get_parent_dal
from schemas import sch_parent, sch_account

router = APIRouter()
img_location = 'media/img_profile/parents_img_profile/'

@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=sch_parent.InsertedParent)
async def create_parent(parent_input: sch_parent.InsertParent = Depends(sch_parent.InsertParent.as_form), 
parent_profile: Optional[UploadFile] = File(None), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):

        async with SessionLocal() as session:
            async with session.begin():
                parent_dal = parentDAL(session)

                with open(img_location + parent_profile.filename, 'wb') as image:
                    shutil.copyfileobj(parent_profile.file, image)
    
                img_url =  str(img_location + parent_profile.filename)

                return await parent_dal.create_parent(
                    parent_input.account_id, img_url, parent_input.fullname, parent_input.gender, 
                    parent_input.religion, parent_input.place_of_birth, parent_input.date_of_birth, parent_input.address, 
                    parent_input.village, parent_input.district, parent_input.city, parent_input.province, parent_input.relation
                )


@router.get("/find/{parent_id}", status_code=status.HTTP_200_OK, response_model=sch_parent.ShowParent)
async def find_parent_id(parent_id: str, parent_dal: parentDAL = Depends(get_parent_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    return await parent_dal.get_parent_data(parent_id)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[sch_parent.ShowParent])
async def get_all_parents(parent_dal: parentDAL = Depends(get_parent_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)) -> List[Parent]:
    return await parent_dal.get_all_parents() 


@router.put("/update/{parent_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_parent.UpdatedParent)
async def update_parent_data(parent_id, parent_input: sch_parent.UpdateParent = Depends(sch_parent.UpdateParent.as_form), 
parent_dal: parentDAL = Depends(get_parent_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            parent_dal = parentDAL(session)

            await parent_dal.update_parent(
                parent_id, parent_input.account_id, 
                parent_input.fullname, parent_input.gender, 
                parent_input.religion, parent_input.place_of_birth, parent_input.date_of_birth, parent_input.address, 
                parent_input.village, parent_input.district, parent_input.city, parent_input.province, 
                parent_input.relation, parent_input.updated_by
                )

            return await parent_dal.get_parent_data(parent_id)


@router.put("/updatephoto/{parent_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_parent.UpdatedParent)
async def update_parent_profile_image(parent_id: str, updated_by: str = Form(...), parent_profile: UploadFile = File(...), 
parent_dal: parentDAL = Depends(get_parent_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            parent_dal = parentDAL(session)

            with open(img_location + parent_profile.filename, 'wb') as image:
                    shutil.copyfileobj(parent_profile.file, image)
    
            img_url = str(img_location + parent_profile.filename)

            await parent_dal.update_parent_photo(
                parent_id, img_url, updated_by
                )

            return await parent_dal.get_parent_data(parent_id)