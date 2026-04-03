from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse
from app.domains.farmer.schemas import FarmerProfileDetail
from app.core.database import get_db
from app.domains.users.models import Seller, SellerImage
from app.common.utils import get_base64_encoded_file

router = APIRouter()

@router.get("/profile", response_model=BaseResponse[FarmerProfileDetail])
async def get_farmer_profile(
    seller_id: int,
    db: Session = Depends(get_db)
):
    """
    농부 프로필 상세 조회 API (실제 데이터 및 Base64 이미지)
    """
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        return BaseResponse(isSuccess=False, message="농부를 찾을 수 없습니다.", content=None)
    
    # 이미지 조회
    seller_img = db.query(SellerImage).filter(SellerImage.seller_id == seller_id).first()
    image_data = get_base64_encoded_file(seller_img.image_path if seller_img else "")

    return BaseResponse(
        isSuccess=True,
        content=FarmerProfileDetail(
            seller_id=seller.seller_id,
            name=seller.name or "무명 농부",
            experience=seller.experience or "경력 정보 없음",
            repurchase_rate=seller.repurchase_rate or 0.0,
            total_sales=seller.total_sales or 0,
            images=[image_data] if image_data else []
        )
    )
