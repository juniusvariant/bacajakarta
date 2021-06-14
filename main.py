from fastapi_offline import FastAPIOffline
from fastapi import FastAPI
from configs import app_config
from models import account, parent, child, about_app
from configs.db_config import engine
from routers import router_account, router_authentication, router_child, router_parent, router_utils

conf = app_config.Settings()

""" user.Base.metadata.create_all(bind=engine)
participant.Base.metadata.create_all(bind=engine) """

tags_metadata = conf.METADATA
inet_mode = conf.INET_MODE

if inet_mode == 'Offline':
    app = FastAPIOffline(openapi_tags=tags_metadata)
if inet_mode == 'Online':
    app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router_authentication.router, tags=['Auth End-Point'], prefix = '/auth')
app.include_router(router_utils.router, tags=['Utils End-Point'], prefix = '/utils')
app.include_router(router_account.router, tags=['Accounts End-Point'], prefix= '/accounts')
app.include_router(router_parent.router, tags=['Parents End-Point'], prefix = '/parent')
app.include_router(router_child.router, tags=['Childs End-Point'], prefix = '/child')

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(account.Base.metadata.create_all)
        await conn.run_sync(parent.Base.metadata.create_all)
        await conn.run_sync(child.Base.metadata.create_all)
        await conn.run_sync(about_app.Base.metadata.create_all)
