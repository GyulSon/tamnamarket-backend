from fastapi import APIRouter

from app.common.schemas import BaseResponse
from app.domains.farmer.schemas import FarmerProfileDetail

router = APIRouter()

@router.get("/profile", response_model=BaseResponse[FarmerProfileDetail])
async def get_farmer_profile(seller_id: int):
    """
    농부 프로필 상세 조회 API
    """
    return BaseResponse(
        isSuccess=True,
        content=FarmerProfileDetail(
            seller_id=1,
            name="김농부",
            experience="감귤 재배 20년",
            repurchase_rate=85.5,
            total_sales=1200,
            images=["/static/images/p1.jpg"]
        )
    )
