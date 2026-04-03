from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.users.models import Seller
from app.domains.mainscreen.schemas import MainContentItem
from app.domains.sale.models import Product, ProductImage
from app.common.utils import get_base64_encoded_file

router = APIRouter()

@router.get("/content", response_model=BaseResponse[List[MainContentItem]])
async def get_main_content(
    buyer_id: int,
    db: Session = Depends(get_db)
):
    """
    전체 판매 글 조회 API (실제 이미지 데이터 포함)
    """
    # 1. Product, Seller, ProductImage를 JOIN하여 실제 데이터 추출
    results = db.query(Product, Seller, ProductImage)\
                .join(Seller, Product.seller_id == Seller.seller_id)\
                .outerjoin(ProductImage, Product.product_id == ProductImage.product_id)\
                .all()
    
    content_list = []
    for product, seller, prod_img in results:
        # DB에 저장된 img1 경로를 Base64로 변환
        thumbnail_data = get_base64_encoded_file(prod_img.img1 if prod_img else "")
        
        content_list.append(
            MainContentItem(
                product_id=product.product_id,
                title=product.title or "제목 없음",
                price=product.price or 0,
                thumbnail=thumbnail_data,
                seller_name=seller.name or "무명 농부",
                category=product.category or "기타"
            )
        )
    
    return BaseResponse(isSuccess=True, content=content_list)

@router.get("/filter", response_model=BaseResponse[List[MainContentItem]])
async def filter_content(
    buyer_id: int, 
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    상품별 판매 글 필터링 API (실제 이미지 데이터 포함)
    """
    query = db.query(Product, Seller, ProductImage)\
               .join(Seller, Product.seller_id == Seller.seller_id)\
               .outerjoin(ProductImage, Product.product_id == ProductImage.product_id)
    
    if category:
        query = query.filter(Product.category == category)
        
    results = query.all()
    content_list = []
    for product, seller, prod_img in results:
        thumbnail_data = get_base64_encoded_file(prod_img.img1 if prod_img else "")
        
        content_list.append(
            MainContentItem(
                product_id=product.product_id,
                title=product.title or "제목 없음",
                price=product.price or 0,
                thumbnail=thumbnail_data,
                seller_name=seller.name or "무명 농부",
                category=product.category or "기타"
            )
        )
        
    return BaseResponse(isSuccess=True, content=content_list)
