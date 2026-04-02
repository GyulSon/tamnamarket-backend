import logging
from app.core.config import settings

# 로깅 설정
logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        """
        알리고(Aligo) 또는 쿨SMS(CoolSMS) 등의 API 키가 있을 경우 
        환경 변수에서 불러와 초기화합니다.
        """
        self.is_ready = False 

    def send_order_notification(self, phone: str, product_name: str):
        """
        [6단계 구현] 구매 발생 시 판매자에게 알림 문자 발송 (Mock)
        """
        message = f"[{settings.PROJECT_NAME}] 새 주문이 발생했습니다! 상품: {product_name}"
        
        # 실제 API 연동이 되어있지 않으므로 로그로 대체
        print(f"\n[SMS 전송 시뮬레이션]")
        print(f"수신번호: {phone}")
        print(f"내용: {message}")
        print("========================\n")
        
        return True

# 싱글톤 인스턴스
sms_service = SMSService()
