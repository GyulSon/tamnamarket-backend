from pydantic import BaseModel
from typing import List, Optional

class FarmerProfileDetail(BaseModel):
    seller_id: int
    name: str
    experience: str
    repurchase_rate: float
    total_sales: int
    images: List[str] # 최대 4장
