from fastapi import APIRouter

router = APIRouter()

@router.get("/farmer")
async def get_subscribed_farmers():
    """
    구독 중인 농부 조회 API
    """
    return {"message": "구독 농부 리스트"}
