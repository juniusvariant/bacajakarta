from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from utils.hashing import Hash

from models.account import Account
import datetime

class accountDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_account(self, username: str, email: str, password: str) -> Account:
        new_user = Account(username=username,email=email, password=Hash.bcrypt(password))
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_account(self, account_id: str, username: Optional[str], email: Optional[str], password: Optional[str], updated_by: str):
        datenow = datetime.datetime.now()
        q = update(Account).where(Account.id == account_id)
        if username:
            q = q.values(username=username)
        if email:
            q = q.values(email=email)
        if password:
            q = q.values(password=Hash.bcrypt(password))
        q = q.values(updated_by = updated_by)
        q = q.values(updated_at = datenow)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def get_all_accounts(self) -> List[Account]:
        q = await self.db_session.execute(select(Account).order_by(Account.id))
        return q.scalars().all()

    async def get_account_data(self, account_id: str):
        q = await self.db_session.execute(select(Account).where(Account.id == account_id, Account.is_active == True))
        return q.scalar()

    async def check_account_email(self, account_email: str):
        q = await self.db_session.execute(select(Account).where(Account.email == account_email, Account.is_active == True))
        return q.scalar()

    async def get_account_password(self, account_email: str):
        q = await self.db_session.execute(select(Account.password).where(Account.email == account_email, Account.is_active == True))
        return q.scalar()