from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.sale.models import Product
from app.domains.users.models import Seller
from app.domains.mainscreen.schemas import MainContentItem

router = APIRouter()

@router.get("/content", response_model=BaseResponse[List[MainContentItem]])
async def get_main_content(
    buyer_id: int,
    db: Session = Depends(get_db)
):
    """
    전체 판매 글 조회 API (진짜 DB 연동)
    """
    # 1. Product와 Seller를 JOIN하여 필요한 정보 추출
    results = db.query(Product, Seller).join(Seller, Product.seller_id == Seller.seller_id).all()
    
    content_list = []
    for product, seller in results:
        content_list.append(
            MainContentItem(
                product_id=product.product_id,
                title=product.title or "제목 없음",
                price=product.price or 0,
                thumbnail="/static/images/sample.jpg", # 이미지 테이블 연동 필요
                seller_name=seller.name or "무명 농부",
                category=product.category or "기타"
            )
        )
    
    return BaseResponse(
        isSuccess=True,
        content=content_list
    )

@router.get("/filter", response_model=BaseResponse[List[MainContentItem]])
async def filter_content(
    buyer_id: int, 
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    상품별 판매 글 필터링 API
    """
    query = db.query(Product, Seller).join(Seller, Product.seller_id == Seller.seller_id)
    if category:
        query = query.filter(Product.category == category)
        
    results = query.all()
    content_list = []
    for product, seller in results:
        content_list.append(
            MainContentItem(
                product_id=product.product_id,
                title=product.title or "제목 없음",
                price=product.price or 0,
                thumbnail="/static/images/sample.jpg",
                seller_name=seller.name or "무명 농부",
                category=product.category or "기타"
            )
        )
        
    return BaseResponse(isSuccess=True, content=content_list)
