from fastapi import APIRouter
from typing import List

from app.common.schemas import BaseResponse
from app.domains.subscription.schemas import FarmerSummary

router = APIRouter()

@router.get("/farmer", response_model=BaseResponse[List[FarmerSummary]])
async def get_subscribed_farmers(buyer_id: int):
    """
    구독 중인 농부 조회 API
    """
    return BaseResponse(
        isSuccess=True,
        content=[
            FarmerSummary(
                seller_id=1,
                name="귀농달인",
                profile_img="/static/images/profile.jpg",
                residence="제주시 애월읍"
            )
        ]
    )
