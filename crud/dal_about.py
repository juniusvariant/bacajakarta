from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.about_app import About
import datetime

class aboutDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_about(self, description: str, about_type: str) -> About:
        new_about = About(description=description,about_type=about_type)
        self.db_session.add(new_about)
        await self.db_session.flush()
        return new_about

    async def update_about(self, description: Optional[str], about_type: str, updated_by: str):
        datenow = datetime.datetime.now()
        q = update(About).where(About.about_type == about_type)
        if description:
            q = q.values(description=description)
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def get_all_abouts(self) -> List[About]:
        q = await self.db_session.execute(select(About).order_by(About.about_type))
        return q.scalars().all()

    async def get_about_data(self, about_type: str):
        q = await self.db_session.execute(select(About).where(About.about_type == about_type, About.is_active == True))
        return q.scalar()