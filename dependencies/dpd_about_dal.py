from configs.db_config import SessionLocal
from crud.dal_about import aboutDAL


async def get_about_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield aboutDAL(session)