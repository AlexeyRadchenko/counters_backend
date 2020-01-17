import asyncio
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable, DropTable
from settings import config

async def create_tables(engine, tables):
    async with engine.acquire() as conn:
        for table in tables:
            await conn.execute(CreateTable(table))

async def drop_tables(engine, tables):
    async with engine.acquire() as conn:
        for table in tables:
            await conn.execute(DropTable(table))

async def insert_values(engine, table, **kwargs):
    async with engine.acquire() as conn:
        await conn.execute(table.insert().values(**kwargs))

async def init_db_engine(app=None, in_app=True):
    engine = await create_engine(
        user=config['postgres']['user'],
        database=config['postgres']['database'],
        host=config['postgres']['host'],
        password=config['postgres']['password']
    )
    if in_app:
        app['db'] = engine
    else:
        return engine

async def close_db_engine(app=None, in_app=True, engine=None):
    if in_app:
        app['db'].close()
        await app['db'].wait_closed()
        del app['db']
    else:
        engine.close()
        await engine.wait_closed()
