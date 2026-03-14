from pydantic import BaseModel, Field, ConfigDict, AfterValidator, ValidationError
from typing import Annotated
from models import PRODUCT_NAME_LEN

class AddProductSchema(BaseModel):
    name : str
    description: str = Field(default="")
    status: bool = Field(default=True)
    
class ProductSchema(AddProductSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)  
  
class PagParams(BaseModel):
    limit: int = Field(default=100, ge=0, le=100, description="records displayed on the page")
    offset: int = Field(default=0, ge=0, le=100, description="max offset of records")

