from typing import List, Optional
import shutil

from fastapi import APIRouter,status, Depends, File, UploadFile, Form

from utils import oauth2
from configs.db_config import SessionLocal
from crud.dal_booklet import bookletDAL
from models.booklet import Booklet
from dependencies.dpd_booklet_dal import get_booklet_dal
from schemas import sch_booklet, sch_account

router = APIRouter()
banner_location = 'media/img_booklet/img_banner/'
icon_location = 'media/img_booklet/img_icon/'

@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=sch_booklet.InsertedBooklet)
async def create_booklet(booklet_input: sch_booklet.InsertBooklet = Depends(sch_booklet.InsertBooklet.as_form), 
booklet_banner: Optional[UploadFile] = File(None), booklet_icon: Optional[UploadFile] = File(None),
current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):

        async with SessionLocal() as session:
            async with session.begin():
                booklet_dal = bookletDAL(session)

                with open(banner_location + booklet_banner.filename, 'wb') as banner:
                    shutil.copyfileobj(booklet_banner.file, banner)

                with open(icon_location + booklet_icon.filename, 'wb') as icon:
                    shutil.copyfileobj(booklet_icon.file, icon)
    
                banner_url =  str(banner_location + booklet_banner.filename)
                icon_url =  str(icon_location + booklet_icon.filename)

                return await booklet_dal.create_booklet(
                    booklet_input.period, booklet_input.description, icon_url, banner_url, booklet_input.color
                )


@router.get("/find-month/{month}", status_code=status.HTTP_200_OK, response_model=List[sch_booklet.BaseBooklet])
async def find_parent_id(month, booklet_dal: bookletDAL = Depends(get_booklet_dal), 
current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user))->List[Booklet]:
    return await booklet_dal.get_booklet_thisyear_bymonth(month)


@router.get("/all-thisyear", status_code=status.HTTP_200_OK, response_model=List[sch_booklet.BaseBooklet])
async def get_all_booklet_thisyear(booklet_dal: bookletDAL = Depends(get_booklet_dal), 
current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)) -> List[Booklet]:
    return await booklet_dal.get_booklet_thisyear()


@router.put("/update/{booklet_id}", status_code=status.HTTP_202_ACCEPTED, response_model=sch_booklet.UpdatedBooklet)
async def update_booklet_data(booklet_id, booklet_input: sch_booklet.UpdateBooklet = Depends(sch_booklet.UpdateBooklet.as_form), 
booklet_banner: Optional[UploadFile] = File(None), booklet_icon: Optional[UploadFile] = File(None), 
booklet_dal: bookletDAL = Depends(get_booklet_dal), current_user: sch_account.BaseAccount = Depends(oauth2.get_current_user)):
    async with SessionLocal() as session:
        async with session.begin():
            booklet_dal = bookletDAL(session)

            with open(banner_location + booklet_banner.filename, 'wb') as banner:
                shutil.copyfileobj(booklet_banner.file, banner)

            with open(icon_location + booklet_icon.filename, 'wb') as icon:
                shutil.copyfileobj(booklet_icon.file, icon)

            banner_url =  str(banner_location + booklet_banner.filename)
            icon_url =  str(icon_location + booklet_icon.filename)

            await booklet_dal.update_booklet(
                booklet_id, booklet_input.date, booklet_input.description, icon_url, banner_url, 
                booklet_input.color, booklet_input.updated_by
                )

            return await booklet_dal.get_booklet_data(booklet_id)