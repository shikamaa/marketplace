from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from models import Order, Product
from schemas import PagParams
from data import get_session, async_ssn

SessionDepURL = Annotated[AsyncSession, Depends(get_session)]
PaginationParamsURL = Annotated[PagParams, Depends(PagParams)]

router = APIRouter()
#response_model
@router.get("/orders")
async def get_orders(session: SessionDepURL,
                     pagination: PaginationParamsURL,
                     ):
    query = (
        select(Order).limit(pagination.limit).offset(pagination.offset)
    )
    if query is None:
        raise HTTPException(status_code=404, description="No orders found")
    res = (await session.execute(query)).scalars().all()
    
    return res