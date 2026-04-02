from fastapi import APIRouter, File, UploadFile, Body
from typing import List
import uuid
import os

from app.common.schemas import BaseResponse
from app.domains.sale.schemas import (
    ClassificationResult, GeneratedAdText, PriceRecommendResponse, SaleAdDetail
)

router = APIRouter()

@router.post("/classification", response_model=BaseResponse[ClassificationResult])
async def analyze_image(file: UploadFile = File(...)):
    """
    품종 분석 API
    """
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("static/images", filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return BaseResponse(
        isSuccess=True, 
        content=ClassificationResult(category="감귤 테스트 결과")
    )

@router.post("/image", response_model=BaseResponse[None])
async def upload_product_image(files: List[UploadFile] = File(...)):
    """
    상품 사진 업로드 API (최대 3장)
    """
    return BaseResponse(isSuccess=True, content=None)

@router.post("/text", response_model=BaseResponse[GeneratedAdText])
async def create_sale_text(
    product_id: int = Body(...),
    voices: List[UploadFile] = File(...)
):
    """
    음성 기반 게시물 작성 AI API (4개 파일 중 3개 분석, 1개 저장)
    """
    return BaseResponse(
        isSuccess=True, 
        content=GeneratedAdText(title="추천 제목", final_description="AI가 작성한 상세 내용")
    )

@router.post("/price", response_model=BaseResponse[PriceRecommendResponse])
async def recommend_price(product_id: int = Body(..., embed=True)):
    """
    적정가 추천 API
    """
    return BaseResponse(
        isSuccess=True, 
        content=PriceRecommendResponse(recommended_price=15000)
    )

@router.get("/salead", response_model=BaseResponse[SaleAdDetail])
async def get_sale_detail(product_id: int):
    """
    판매 글 상세 조회 API
    """
    return BaseResponse(
        isSuccess=True,
        content=SaleAdDetail(
            product_id=product_id,
            title="테스트 상품",
            price=15000,
            images=["/static/images/test1.jpg"],
            voice_url="/static/audio/test.webm",
            final_description="상세 설명입니다."
        )
    )
