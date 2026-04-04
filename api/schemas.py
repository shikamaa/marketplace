from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from sqlalchemy import Numeric

class AddProductSchema(BaseModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: bool = Field(default=True)
       
class ProductSchema(AddProductSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)  

class AddOrderSchema(BaseModel):
    quantity: int 
    price: float
  
class OrderSchema(BaseModel):
    id: int

class PagParams(BaseModel):
    limit: int = Field(default=100, ge=0, le=100, description="records displayed on the page")
    offset: int = Field(default=0, ge=0, le=100, description="max offset of records")

class AddUserSchema():
    username: str = Field()
    password: str
    
class UserSchema():
    id: Optional[int] 
    
    
    
    
    
