from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TamnaMarket Backend"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    DATABASE_URL: str = "sqlite:///./tamnamarket.db"

    class Config:
        env_file = ".env"

settings = Settings()
