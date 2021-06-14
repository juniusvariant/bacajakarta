from configs.db_config import SessionLocal
from crud.dal_parent import parentDAL


async def get_parent_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield parentDAL(session)