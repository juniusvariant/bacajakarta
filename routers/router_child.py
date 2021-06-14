from typing import List, Optional
import shutil

from fastapi import APIRouter,status, Depends, File, UploadFile, Form

from utils import oauth2
from configs.db_config import SessionLocal
from crud.dal_child import childDAL
from models.child import Child
from dependencies.dpd_child_dal import get_child_dal
from schemas import sch_parent, sch_account

router = APIRouter()
img_location = 'media/img_profile/childs_img_profile/'

@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=sch_parent.InsertedChild)
async def create_child(child_input: sch_parent.InsertChild = Depends(sch_parent.InsertChild.as_form), 
child_profile: Optional[UploadFile] = File(None), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):

        async with SessionLocal() as session:
            async with session.begin():
                child_dal = childDAL(session)

                with open(img_location + child_profile.filename, 'wb') as image:
                    shutil.copyfileobj(child_profile.file, image)
    
                img_url =  str(img_location + child_profile.filename)

                return await child_dal.create_child(
                    child_input.account_id, child_input.parent_id, img_url, child_input.fullname, child_input.gender, 
                    child_input.religion, child_input.place_of_birth, child_input.date_of_birth, child_input.address, 
                    child_input.village, child_input.district, child_input.city, child_input.province, child_input.relation
                )


@router.get("/find/{child_id}", status_code=status.HTTP_200_OK, response_model=sch_parent.ChildWithParent)
async def find_child_id(child_id: str, child_dal: childDAL = Depends(get_child_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    return await child_dal.get_child_data(child_id)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[sch_parent.ChildWithParent])
async def get_all_childs(child_dal: childDAL = Depends(get_child_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)) -> List[Child]:
    return await child_dal.get_all_childs()


@router.put("/update/{child_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_parent.UpdatedChild)
async def update_child_data(child_id, child_input: sch_parent.UpdateChild = Depends(sch_parent.UpdateChild.as_form), 
child_dal: childDAL = Depends(get_child_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            child_dal = childDAL(session)

            await child_dal.update_child(
                child_id, child_input.account_id, 
                child_input.fullname, child_input.gender, 
                child_input.religion, child_input.place_of_birth, child_input.date_of_birth, child_input.address, 
                child_input.village, child_input.district, child_input.city, child_input.province, 
                child_input.relation, child_input.updated_by
                )

            return await child_dal.get_child_data(child_id)


@router.put("/updatephoto/{child_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_parent.UpdatedChild)
async def update_child_profile_image(child_id: str, updated_by: str = Form(...), child_profile: UploadFile = File(...), 
child_dal: childDAL = Depends(get_child_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            child_dal = childDAL(session)

            with open(img_location + child_profile.filename, 'wb') as image:
                    shutil.copyfileobj(child_profile.file, image)
    
            img_url = str(img_location + child_profile.filename)

            await child_dal.update_child_photo(
                child_id, img_url, updated_by
                )

            return await child_dal.get_child_data(child_dal)