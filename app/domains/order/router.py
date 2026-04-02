from fastapi import APIRouter

router = APIRouter()

@router.post("/product")
async def purchase_product():
    """
    농산물 구매 API
    """
    return {"message": "구매 절차가 완료되었습니다."}
