from configs.db_config import SessionLocal
from crud.dal_child import childDAL


async def get_child_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield childDAL(session)