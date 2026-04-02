from pydantic import BaseModel
from typing import List

class MainContentItem(BaseModel):
    product_id: int
    title: str
    price: int
    thumbnail: str
    seller_name: str
    category: str

class MainContentList(BaseModel):
    items: List[MainContentItem]
