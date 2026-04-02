import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "TamnaMarket Backend"
    
    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # [1단계] AI 비전 인식용 (Gemini 3.1)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # [2, 4단계] STT 번역 및 게시글 작성용 (OpenAI)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # [2단계] 고정밀 음성 추출용 (Clova Speech)
    CLOVA_SECRET_KEY: str = os.getenv("CLOVA_SECRET_KEY")
    CLOVA_INVOKE_URL: str = os.getenv("CLOVA_INVOKE_URL")

    # [6단계] 트윌리오 실시간 문자 발송용
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER")

settings = Settings()
