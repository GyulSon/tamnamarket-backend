from pydantic import BaseModel
from typing import List

class FarmerSummary(BaseModel):
    seller_id: int
    name: str
    profile_img: str
    residence: str

class SubscribedFarmers(BaseModel):
    farmers: List[FarmerSummary]
