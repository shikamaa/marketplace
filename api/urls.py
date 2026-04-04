from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, sql, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from models import Order, Product, User
from schemas import PagParams, UserSchema, ProductSchema, AddProductSchema, AddUserSchema
from data import get_session, async_ssn

SessionDep = Annotated[AsyncSession, Depends(get_session)]
PagDep = Annotated[PagParams, Depends(PagParams)]

router = APIRouter()

@router.get("/")
def idx():
    return { "Message": "Hello" }

@router.get("/products/count", description="Return count of products",)
async def products_count(session: SessionDep,):
    count_query = select(sql.func.count()).select_from(Product)

    res = (await session.execute(count_query)).scalar()
    if res is None:
        raise HTTPException("No products found")
    
    return res

@router.get("/products", response_model = list[ProductSchema])
async def get_pag_products(session: SessionDep, 
                        pagination: PagDep) -> list[ProductSchema]:
    query = (
        select(Product).
        limit(pagination.limit).
        offset(pagination.offset)
    )
    res = (await session.execute(query)).scalars().all()
    if res is None:
         raise HTTPException(status_code=404,description="Products not found")
    
    return res


@router.get("/products/search", response_model=list[ProductSchema]) 
async def get_like_products(session: SessionDep, product: str) -> list[ProductSchema]:
    desired = f"%{product}%" 
    q = select(Product).where(Product.name.ilike(desired))
    return (await session.execute(q)).scalars().all()
    
@router.get("/products/{id}", response_model=ProductSchema, description="Returns a product if it exists")
async def get_specific_product(session: SessionDep, id: int):
    query = select(Product).where(Product.id == id)
    
    res = (await session.execute(query)).scalar_one_or_none()
    
    if res is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    return res


async def return_similar_products(session: SessionDep):
    pass

@router.post("/products", description="Creates a product")
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

@router.post("/orders")
async def create_order(session: SessionDep, ):
    pass

@router.post("/review")
async def create_order():
    pass
