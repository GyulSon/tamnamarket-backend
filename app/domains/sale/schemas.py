from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ClassificationResult(BaseModel):
    category: str

class SaleAdCreateRequest(BaseModel):
    product_id: int
    voice_text: str

class GeneratedAdText(BaseModel):
    title: str
    final_description: str

class PriceRecommendRequest(BaseModel):
    product_id: int

class PriceRecommendResponse(BaseModel):
    recommended_price: int

class SaleAdDetail(BaseModel):
    product_id: int
    title: str
    price: int
    images: List[str]
    voice_url: str
    final_description: str
