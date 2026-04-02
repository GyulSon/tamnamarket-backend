from pydantic import BaseModel

class OrderCreate(BaseModel):
    product_id: int
    buyer_id: int

class OrderResponseInfo(BaseModel):
    order_id: int
    status: str
