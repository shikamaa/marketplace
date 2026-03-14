from pydantic import BaseModel, Field, ConfigDict

class AddProductSchema(BaseModel):
    name: str = Field(default=None)
    price: int | None 
    count: int | None
       
class ProductSchema(AddProductSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)  
  

class PagParams(BaseModel):
    limit: int = Field(default=100, ge=0, le=100, description="records displayed on the page")
    offset: int = Field(default=0, ge=0, le=100, description="max offset of records")
