from configs.db_config import SessionLocal
from crud.dal_account import accountDAL


async def get_account_dal():
    async with SessionLocal() as session:
        async with session.begin():
            yield accountDAL(session)