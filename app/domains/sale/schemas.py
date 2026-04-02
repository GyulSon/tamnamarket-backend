from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ClassificationResultDetail(BaseModel):
    product_id: int
    category: str

class SaleImageUploadRequest(BaseModel):
    product_id: int

class SaleAdCreateRequest(BaseModel):
    product_id: int

class GeneratedAdText(BaseModel):
    title: str
    final_description: str

class PriceRecommendRequest(BaseModel):
    product_id: int

class PriceRecommendResponse(BaseModel):
    product_id: int
    recommended_price: int

class SaleAdDetail(BaseModel):
    product_id: int
    title: str
    price: int
    images: List[str]
    voice_url: str
    final_description: str
