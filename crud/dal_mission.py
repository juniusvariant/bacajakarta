from typing import List, Optional

from sqlalchemy import update, extract
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.mission import Mission
import datetime
import calendar

class missionDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_mission(self, booklet_id: str, mission_date: datetime.date, task: str, mission_type: str, 
    description: str, icon: str, color: str, tags: List[str], is_for: str) -> Mission:
        new_mission = Mission(booklet_id = booklet_id, mission_date = mission_date, task = task, mission_type = mission_type, 
        description = description, icon = icon, color = color, tags = tags, is_for = is_for
        )
        self.db_session.add(new_mission)
        await self.db_session.flush()
        return new_mission

    async def update_mission(self, mission_id: str, booklet_id: str, mission_date: Optional[datetime.date], 
    task: Optional[str], mission_type: Optional[str], description: Optional[str], icon: Optional[str], 
    color: Optional[str], tags: Optional[List[str]], is_for: str, updated_by: str):
        datenow = datetime.datetime.now()
        q = update(Mission).where(Mission.id == mission_id, Mission.booklet_id == booklet_id)
        if mission_date:
            q = q.values(mission_date=mission_date)
        if task:
            q = q.values(task=task)
        if mission_type:
            q = q.values(mission_type=mission_type)
        if description:
            q = q.values(description=description)
        if icon:
            q = q.values(icon=icon)
        if color:
            q = q.values(color=color)
        if tags:
            q = q.values(tags=tags)
        if is_for:
            q = q.values(is_for=is_for)
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def get_all_missions(self) -> List[Mission]:
        q = await self.db_session.execute(select(Mission).order_by(Mission.mission_date))
        return q.scalars().all()

    async def get_booklet_thisyear(self) -> List[Mission]:
        year_now = datetime.datetime.now().year

        q = await self.db_session.execute(select(Mission).where( extract('year', Mission.mission_date) == year_now))
        return q.scalars().all()

    async def get_booklet_thisyear_bymonth(self, booklet_id: str, month: int) -> List[Mission]:
        year_now = datetime.datetime.now().year

        num_days = calendar.monthrange(year_now, month)[1]
        start_date = datetime.date(year_now, month, 1)
        end_date = datetime.date(year_now, month, num_days)

        q = await self.db_session.execute(select(Mission).where(Mission.booklet_id == booklet_id, 
        Mission.mission_date >= start_date, Mission.mission_date <= end_date))
        return q.scalars().all()