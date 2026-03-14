from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from dotenv import load_dotenv
from os import getenv
load_dotenv()

async_ngn = create_async_engine(getenv("CONN_STRING"),echo=True)

from models import Base

async_ssn = async_sessionmaker(async_ngn, expire_on_commit=False,class_=AsyncSession)

async def get_session():
    async with async_ssn() as session:
        yield session

