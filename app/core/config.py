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

settings = Settings()
