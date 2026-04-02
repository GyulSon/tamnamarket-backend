from fastapi import APIRouter

from app.common.schemas import BaseResponse
from app.domains.order.schemas import OrderCreate, OrderResponseInfo

router = APIRouter()

@router.post("/product", response_model=BaseResponse[OrderResponseInfo])
async def purchase_product(order_data: OrderCreate):
    """
    농산물 구매 API
    """
    return BaseResponse(
        isSuccess=True, 
        content=OrderResponseInfo(order_id=101, status="결제 대기")
    )
