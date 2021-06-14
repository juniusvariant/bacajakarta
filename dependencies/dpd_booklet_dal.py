from configs.db_config import SessionLocal
from crud.dal_booklet import bookletDAL


async def get_booklet_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield bookletDAL(session)