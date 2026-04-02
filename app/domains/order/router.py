from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.order.models import Order
from app.domains.order.schemas import OrderCreate, OrderResponseInfo
from app.services.sms_service import sms_service

router = APIRouter()

@router.post("/product", response_model=BaseResponse[OrderResponseInfo])
async def purchase_product(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    6단계: 농산물 구매 및 DB 영구 저장 + 판매자 알림 전송 API
    """
    try:
        # [DB 저장] 진짜로 주문 레코드 생성 (SQLAlchemy INSERT)
        new_order = Order(
            product_id=order_data.product_id,
            buyer_id=order_data.buyer_id
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        # 판매자에게 실제 SMS 알림 발송 (Twilio)
        sms_service.send_order_notification(
            phone="010-4872-3270", 
            product_name=f"상품 ID {order_data.product_id}"
        )
        
        return BaseResponse(
            isSuccess=True, 
            content=OrderResponseInfo(order_id=new_order.order_id, status="결제 및 주문 기록 완료")
        )

    except Exception as e:
        db.rollback()
        print(f"주문 중 에러: {e}")
        return BaseResponse(isSuccess=False, content=None)
