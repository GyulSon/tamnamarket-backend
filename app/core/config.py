import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "TamnaMarket Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@127.0.0.1:3306/tamnamarket")

settings = Settings()
