from configs.db_config import SessionLocal
from crud.dal_mission import missionDAL


async def get_mission_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield missionDAL(session)