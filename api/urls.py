from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from models import Order
from data import get_session, async_ssn

SessionDep1 = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter()

@router.get("/orders")
async def get_orders(session: SessionDep1):
    query = (
        select(Order)
    )
    if query is None:
        raise HTTPException(status_code=404, description="No orders found")
    res = (await session.execute(query)).scalars().all()
    
    return res
