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
from asyncio import run as async_run

from sqlalchemy.exc import SQLAlchemyError
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_ngn.begin() as conn:
        print(Base.metadata.tables)
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
PagDep = Annotated[PagParams, Depends(PagParams)]

from urls import router

@app.get("/")
def idx():
    return { "Message": "Hello" }

@app.get("/products/count",description="Return count of products",)
async def products_count(session: SessionDep,):
    count_query = select(sql.func.count()).select_from(Product)

    res = (await session.execute(count_query)).scalar()
    if res is None:
        raise HTTPException("No products found")
    
    return res

@app.get("/products", response_model = list[ProductSchema])
async def get_pag_products(session: SessionDep, 
                        pagination: PagDep) -> list[ProductSchema]:
    query = (
        select(Product).
        limit(pagination.limit).
        offset(pagination.offset)
    )
    res = (await session.execute(query)).scalars().all()
    if res is None:
         raise HTTPException(status_code=404,description="Product not found")
    
    return res
 
@app.get("/products/{id}", response_model=ProductSchema, description="Returns a product if it exists")
async def get_specific_product(session: SessionDep, id: int):
    query = select(Product).where(Product.id == id)
    
    res = (await session.execute(query)).scalar_one_or_none()
    
    if res is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return res
#/products/search?q={str}
@app.get("/products/like/{str}", response_model=list[ProductSchema]) 
async def ilike_products(session: SessionDep, product: str) -> list[ProductSchema]:
    desired_products = f"%{product}"
    
    query = select(Product).where((Product.name.like(desired_products)))
    #query = select(Product.where.ilike())
    res = (await session.execute(query)).scalars().all()
    if res is None:
        raise HTTPException(status_code=404, detail="No match found")
    return res
    
@app.get("/products/{id}/similar")
async def return_similar_products(session: SessionDep):
    pass

@app.post("/products", description="Creates a product")
async def add_product(input_data: AddProductSchema,session: SessionDep):

    new_product = Product(
        name = input_data.name,
        description = input_data.description,
        status = input_data.status
    )
    session.add(new_product)
    await session.commit()
    
    await session.refresh(new_product)
    return {"Product added sucessfully": True}

@app.post("/orders")
async def create_order(session: SessionDep, ):
    pass

@app.post("/review")
async def create_order():
    pass

if __name__ == "__main__":
    uvicorn.run(app)
