from fastapi import APIRouter
from typing import List

from app.common.schemas import BaseResponse
from app.domains.mainscreen.schemas import MainContentItem

router = APIRouter()

@router.get("/content", response_model=BaseResponse[List[MainContentItem]])
async def get_main_content(buyer_id: int):
    """
    전체 판매 글 조회 API
    """
    return BaseResponse(
        isSuccess=True,
        content=[
            MainContentItem(
                product_id=1,
                title="상품 1",
                price=10000,
                thumbnail="/static/images/test1.jpg",
                seller_name="홍길동",
                category="한라봉"
            )
        ]
    )

@router.get("/filter", response_model=BaseResponse[List[MainContentItem]])
async def filter_content(buyer_id: int, category: str = None):
    """
    상품별 판매 글 필터링 API
    """
    return BaseResponse(isSuccess=True, content=[])
