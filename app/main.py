from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.domains.items.router import router as items_router
from app.domains.audio.router import router as audio_router
from app.domains.sales.router import router as sales_router
from app.domains.vision.router import router as vision_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://goormthon-3.goorm.training",  # 프론트엔드 배포 주소 (확인 필요)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file mount (local storage setup)
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/voices", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Expose Base API Routers
app.include_router(items_router, prefix=f"{settings.API_V1_STR}/items", tags=["Items - 기능 1, 4"])
app.include_router(audio_router, prefix=f"{settings.API_V1_STR}/audio", tags=["Audio - 기능 2, 3"])
app.include_router(sales_router, prefix=f"{settings.API_V1_STR}/sales", tags=["Sales - 기능 5, 6"])
app.include_router(vision_router, prefix="/api/sale", tags=["Vision - 이미지 분석 분기"])

@app.get("/")
def check_health():
    return {"status": "ok", "message": "Welcome to TamnaMarket Backend API!"}
