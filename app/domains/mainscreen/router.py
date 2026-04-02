from fastapi import APIRouter

router = APIRouter()

@router.get("/content")
async def get_main_content():
    """
    전체 판매 글 조회 API
    """
    return {"message": "전체 메인 콘텐츠"}

@router.get("/filter")
async def filter_content():
    """
    상품별 판매 글 필터링 API
    """
    return {"message": "필터링된 결과 조회"}
