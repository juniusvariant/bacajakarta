from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.child import Child
import datetime

class childDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_child(self, account_id : str, parent_id : str, img_profile : str, fullname : str, gender : str, 
    religion : str, place_of_birth : str, date_of_birth : datetime.date, address : str, village : str, district : str, 
    city : str, province : str, relation : str) -> Child:
        new_parent = Child(account_id = account_id, parent_id = parent_id, img_profile = img_profile, fullname = fullname, gender = gender, 
        religion = religion, place_of_birth = place_of_birth, date_of_birth = date_of_birth, address = address, 
        village = village, district = district, city = city, province = province, relation = relation)
        self.db_session.add(new_parent)
        await self.db_session.flush()
        return new_parent

    async def update_child(self, child_id : str, parent_id: Optional[str], account_id : Optional[str], img_profile : Optional[str], 
    fullname : Optional[str], gender : Optional[str], religion : Optional[str], place_of_birth : Optional[str], 
    date_of_birth : Optional[datetime.date], address : Optional[str], village : Optional[str], district : Optional[str], 
    city : Optional[str], province : Optional[str], relation : Optional[str], updated_by: str):
        datenow = datetime.datetime.now()
        q = update(Child).where(Child.id == child_id)
        q = q.values(parent_id=parent_id)
        if account_id:
            q = q.values(account_id=account_id)
        if img_profile:
            q = q.values(img_profile=img_profile)
        if fullname:
            q = q.values(fullname=fullname)
        if gender:
            q = q.values(gender=gender)
        if religion:
            q = q.values(religion=religion)
        if place_of_birth:
            q = q.values(place_of_birth=place_of_birth)
        if date_of_birth:
            q = q.values(date_of_birth=date_of_birth)
        if address:
            q = q.values(address=address)
        if village:
            q = q.values(village=village)
        if district:
            q = q.values(district=district)
        if city:
            q = q.values(city=city)
        if province:
            q = q.values(province=province)
        if relation:
            q = q.values(relation=relation)
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def update_child_photo(self, child_id: str, img_profile : str, updated_by: str):
        datenow = datetime.datetime.now()
        q = update(Child).where(Child.id == child_id)
        q = q.values(img_profile = img_profile)
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def get_all_childs(self) -> List[Child]:
        q = await self.db_session.execute(select(Child).order_by(Child.id))
        return q.scalars().all()

    async def get_child_data(self, child_id: str):
        q = await self.db_session.execute(select(Child).where(Child.id == child_id, Child.is_active == True))
        return q.scalar()