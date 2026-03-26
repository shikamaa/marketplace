from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from dotenv import load_dotenv
from os import getenv
from contextlib import asynccontextmanager
from data import async_ngn, async_ssn, get_session
from models import Base, Product
from schemas import AddProductSchema, ProductSchema, PagParams
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc, func, sql
#from asyncio import run as async_run
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

#app = FastAPI(dependencies=[Depends(get_query_token)])

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_ngn.begin() as conn:
        print(Base.metadata.tables)
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

from urls import router
app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
