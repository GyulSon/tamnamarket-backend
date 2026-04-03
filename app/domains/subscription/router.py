from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse
from app.domains.subscription.schemas import FarmerSummary
from app.core.database import get_db
from app.domains.subscription.models import Subscription
from app.domains.users.models import Seller, SellerImage
from app.common.utils import get_base64_encoded_file

router = APIRouter()

@router.get("/farmer", response_model=BaseResponse[List[FarmerSummary]])
async def get_subscribed_farmers(
    buyer_id: int,
    db: Session = Depends(get_db)
):
    """
    구독 중인 농부 조회 API (실제 데이터 및 Base64 프로필)
    """
    # 구독 테이블과 농부 테이블 JOIN
    results = db.query(Seller, SellerImage)\
                .join(Subscription, Subscription.seller_id == Seller.seller_id)\
                .outerjoin(SellerImage, Seller.seller_id == SellerImage.seller_id)\
                .filter(Subscription.buyer_id == buyer_id)\
                .all()
    
    farmer_list = []
    for seller, seller_img in results:
        profile_data = get_base64_encoded_file(seller_img.image_path if seller_img else "")
        
        farmer_list.append(
            FarmerSummary(
                seller_id=seller.seller_id,
                name=seller.name or "무명 농부",
                profile_img=profile_data,
                residence=seller.residence or "제주특별자치도"
            )
        )
        
    return BaseResponse(isSuccess=True, content=farmer_list)
