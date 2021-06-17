from typing import List, Optional

from sqlalchemy import update, extract
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.booklet import Booklet
import datetime
import calendar

class bookletDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_booklet(self, period: datetime.date, description: str, icon: str, banner: str, color: str) -> Booklet:
        new_booklet = Booklet(period = period, description = description, icon = icon, banner = banner, color = color)
        self.db_session.add(new_booklet)
        await self.db_session.flush()
        return new_booklet

    async def update_booklet(self, booklet_id: str, period: Optional[datetime.date], description: Optional[str], 
    icon: Optional[str], banner: Optional[str], color: Optional[str], updated_by: str):
        datenow = datetime.datetime.now()
        q = update(Booklet).where(Booklet.id == booklet_id)
        if period:
            q = q.values(period=period)
        if description:
            q = q.values(description=description)
        if icon:
            q = q.values(icon=icon)
        if banner:
            q = q.values(banner=banner)
        if color:
            q = q.values(color=color)
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def get_booklet_data(self, booklet_id: str):
        q = await self.db_session.execute(select(Booklet).where(Booklet.id == booklet_id, Booklet.is_active == True))
        return q.scalar()

    async def get_all_booklets(self) -> List[Booklet]:
        q = await self.db_session.execute(select(Booklet).order_by(Booklet.period))
        return q.scalars().all()

    async def get_booklet_thisyear(self) -> List[Booklet]:
        year_now = datetime.datetime.now().year

        q = await self.db_session.execute(select(Booklet).where( extract('year', Booklet.period) == year_now))
        return q.scalars().all()

    async def get_booklet_thisyear_bymonth(self, month: int) -> List[Booklet]:
        year_now = datetime.datetime.now().year

        num_days = calendar.monthrange(year_now, month)[1]
        start_date = datetime.date(year_now, month, 1)
        end_date = datetime.date(year_now, month, num_days)

        q = await self.db_session.execute(select(Booklet).where(Booklet.period >= start_date, Booklet.period <= end_date))
        return q.scalars().all()