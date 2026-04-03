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
        [6단계 구현] 구매 발생 시 판매자에게 알림 문자 발송 (Twilio 연동)
        """
        import httpx
        import base64

        message = f"[{settings.PROJECT_NAME}] 새 주문이 발생했습니다! 상품: {product_name}"
        
        # 번호 포맷팅 (010-xxxx-xxxx -> +8210xxxxxxxx)
        clean_phone = "".join(filter(str.isdigit, phone))
        if clean_phone.startswith("0"):
            clean_phone = "+82" + clean_phone[1:]
        
        # 트윌리오 API 호출
        # 환경변수 미설정 시 안전하게 실패 처리
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            print("SMS 발송 실패: TWILIO 환경변수가 설정되지 않았습니다.")
            return False

        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        data = {
            "To": clean_phone,
            "From": settings.TWILIO_FROM_NUMBER,
            "Body": message
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, data=data, auth=auth)
                if response.status_code == 201:
                    print(f"SMS 발송 성공: {phone}")
                    return True
                else:
                    print(f"SMS 발송 실패: {response.status_code}, {response.text}")
                    return False
        except Exception as e:
            print(f"SMS 발송 중 예외 발생: {e}")
            return False

# 싱글톤 인스턴스
sms_service = SMSService()
