from fastapi import APIRouter

router = APIRouter()

@router.get("/profile")
async def get_farmer_profile():
    """
    농부 프로필 상세 조회 API
    """
    return {"message": "농부 프로필 데이터"}
