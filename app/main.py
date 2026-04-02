from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings

# SQLAlchemy relationship 문자열 resolve를 위해 모든 모델을 라우터보다 먼저 임포트
from app.domains.users.models import Seller, SellerImage, Buyer  # noqa: F401
from app.domains.sale.models import Product, ProductImage, Wishlist  # noqa: F401
from app.domains.subscription.models import Subscription  # noqa: F401
from app.domains.order.models import Order  # noqa: F401

from app.domains.sale.router import router as sale_router
from app.domains.mainscreen.router import router as mainscreen_router
from app.domains.subscription.router import router as subscription_router
from app.domains.farmer.router import router as farmer_router
from app.domains.order.router import router as order_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://goormthon-3.goorm.training",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 스태틱 파일 설정 (이미지 저장 등)
if not os.path.exists("static/images"):
    os.makedirs("static/images")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록 (API 명세서 기준)
app.include_router(sale_router, prefix="/api/sale", tags=["Sale - 판매 글"])
app.include_router(mainscreen_router, prefix="/api/mainscreen", tags=["MainScreen - 메인 화면"])
app.include_router(subscription_router, prefix="/api/subscription", tags=["Subscription - 구독"])
app.include_router(farmer_router, prefix="/api/farmer", tags=["Farmer - 농부"])
app.include_router(order_router, prefix="/api/order", tags=["Order - 주문/구매"])

@app.get("/")
def check_health():
    return {"status": "ok", "message": "탐라장터 API가 정상 작동 중입니다."}
