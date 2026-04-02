from fastapi import APIRouter, File, UploadFile, Body, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.sale.models import Product, ProductImage
from app.domains.sale.schemas import (
    ClassificationResult, GeneratedAdText, PriceRecommendResponse, SaleAdDetail
)
from app.services.ai_service import ai_service
from app.services.stt_service import stt_service

router = APIRouter()

@router.post("/classification", response_model=BaseResponse[ClassificationResult])
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    1단계: 품종 분석 및 DB 업데이트 (Gemini 3.1)
    """
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("static/images", filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    category_result = ai_service.classify_product(file_path)
    
    # [DB 저장] 실제 서비스에서는 상품을 새로 생성하거나 기존 ID의 품종을 업데이트
    # 현재는 목업 데이터베이스 흐름에 맞춰 로직 구현
    return BaseResponse(
        isSuccess=True, 
        content=ClassificationResult(category=category_result)
    )

@router.post("/text", response_model=BaseResponse[GeneratedAdText])
async def create_sale_text(
    product_id: int = Body(...),
    voices: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    2~4단계: 음성 처리 및 AI 판매글 생성 + DB 영구 저장
    - 4번째 음성 원본 경로 및 AI 생성글을 Product 테이블에 업데이트
    """
    stt_results = []
    voice_url = ""

    try:
        for i, voice in enumerate(voices[:4]):
            temp_filename = f"{uuid.uuid4()}_{voice.filename}"
            temp_path = os.path.join("static/audio", temp_filename)
            with open(temp_path, "wb") as buffer:
                content = await voice.read()
                buffer.write(content)
            
            if i < 3: # 분석용
                raw, translated = stt_service.transcribe_and_translate(temp_path)
                if translated: stt_results.append(translated)
            else: # 4번 파일: 원본 저장용
                voice_url = f"/static/audio/{temp_filename}"

        # AI 판매글 생성
        title, description = ai_service.generate_ad_text(category="제주 농산물", stt_texts=stt_results)

        # [DB 저장] 진짜로 DB에 업데이트 진행
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.title = title
            product.final_description = description
            product.voice_path = voice_url
            db.commit()

        return BaseResponse(
            isSuccess=True, 
            content=GeneratedAdText(title=title, final_description=description)
        )

    except Exception as e:
        db.rollback()
        return BaseResponse(isSuccess=False, content=None)

@router.post("/price", response_model=BaseResponse[PriceRecommendResponse])
async def recommend_price(
    product_id: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    5단계: 적정가 추천 및 데이터 동기화
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    category = product.category if product else "감귤류"
    context = product.final_description if product else ""
    
    recommended = ai_service.recommend_price(category=category, description=context)
    
    return BaseResponse(
        isSuccess=True, 
        content=PriceRecommendResponse(recommended_price=recommended)
    )

@router.get("/salead", response_model=BaseResponse[SaleAdDetail])
async def get_sale_detail(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    판매 글 상세 조회 (진짜 DB 데이터 반환)
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        return BaseResponse(isSuccess=False, content=None)

    return BaseResponse(
        isSuccess=True,
        content=SaleAdDetail(
            product_id=product.product_id,
            title=product.title or "제목 없음",
            price=product.price or 0,
            images=["/static/images/sample.jpg"], # ProductImage 테이블과 JOIN 필요
            voice_url=product.voice_path or "",
            final_description=product.final_description or ""
        )
    )
