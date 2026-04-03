from fastapi import APIRouter, File, UploadFile, Depends, Request
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.sale.models import Product, ProductImage
from app.domains.sale.schemas import (
    ClassificationResultDetail, GeneratedAdText, PriceRecommendResponse, SaleAdDetail, SaleImageUploadRequest, SaleAdCreateRequest, PriceRecommendRequest
)
from app.services.ai_service import ai_service
from app.services.stt_service import stt_service
from app.common.constants import ALLOWED_CATEGORIES

router = APIRouter()

@router.post("/classification", response_model=BaseResponse[ClassificationResultDetail])
async def classify_product(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    1단계: 품종 분석 및 신규 상품 생성
    - Gemini Vision으로 품종 분석
    - DB에 새로운 Product 레코드 생성
    - 첫 번째 이미지(img1)로 현재 분석한 사진 저장
    """
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("static/images", filename)
    db_path = f"/static/images/{filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    category_result = ai_service.classify_product(file_path)
    
    # [검증] 7종 품종에 해당하지 않는 경우 실패 반환
    if category_result not in ALLOWED_CATEGORIES:
        return BaseResponse(isSuccess=False, content=None)
    
    # [DB 저장] 고정된 판매자 ID(1번)로 상품 초기 생성
    new_product = Product(
        seller_id=1,
        category=category_result,
        is_selling=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # [이미지 저장] 첫 번째 이미지로 품종 분류 시 사용한 사진 등록
    prod_img = ProductImage(
        product_id=new_product.product_id,
        img1=db_path
    )
    db.add(prod_img)
    db.commit()
        
    return BaseResponse(
        isSuccess=True, 
        content=ClassificationResultDetail(product_id=new_product.product_id, category=category_result)
    )

@router.post("/image", response_model=BaseResponse[dict])
async def upload_product_images(
    product_id: int,
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    2단계: 상품 사진 3장 추가 등록 (img2, img3, img4)
    - 1단계(품종 분류)에서 사용한 사진이 img1이 됨
    """
    image_paths = []
    for img in images[:3]: # 3장만 처리
        filename = f"{uuid.uuid4()}_{img.filename}"
        path = os.path.join("static/images", filename)
        with open(path, "wb") as buffer:
            content = await img.read()
            buffer.write(content)
        image_paths.append(f"/static/images/{filename}")
    
    # 3장이 안 될 경우 빈 문자열로 채움
    while len(image_paths) < 3:
        image_paths.append("")

    # 기존 ProductImage(1단계에서 생성됨)를 찾아 img2~4 업데이트
    prod_img = db.query(ProductImage).filter(ProductImage.product_id == product_id).first()
    if not prod_img:
        # 혹시 없을 경우를 대비해 생성 (원칙상 1단계에서 생성되어야 함)
        prod_img = ProductImage(product_id=product_id)
        db.add(prod_img)
    
    prod_img.img2 = image_paths[0]
    prod_img.img3 = image_paths[1]
    prod_img.img4 = image_paths[2]
    
    db.commit()
    
    return BaseResponse(isSuccess=True, content={"message": "추가 이미지 3장 업로드 완료"})

@router.post("/text", response_model=BaseResponse[GeneratedAdText])
async def create_sale_text(
    product_id: int,
    voices: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    3단계: 음성 처리 및 AI 판매글 생성 + DB 업데이트
    """
    stt_answers = ["", "", "", ""]
    voice_url = ""

    try:
        # [1] 상품 존재 여부 선체크
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            print(f"❌ [에러] 상품 ID {product_id}를 찾을 수 없습니다.")
            return BaseResponse(isSuccess=False, message="상품을 찾을 수 없습니다.", content=None)

        print(f"🎙️ [시작] 상품 {product_id} 음성 처리 중... (파일 개수: {len(voices)})")
        
        for i, voice in enumerate(voices[:4]):
            try:
                temp_filename = f"{uuid.uuid4()}_{voice.filename}"
                temp_path = os.path.join("static/audio", temp_filename)
                
                # 디렉토리 다시 한 번 체크 (안전빵)
                if not os.path.exists("static/audio"):
                    os.makedirs("static/audio")

                with open(temp_path, "wb") as buffer:
                    content = await voice.read()
                    buffer.write(content)
                
                print(f"   - {i+1}번 파일 저장 성공: {temp_path}")

                # STT & 번역 실행
                raw, translated = stt_service.transcribe_and_translate(temp_path)
                if translated:
                    stt_answers[i] = translated
                    print(f"   - {i+1}번 번역 결과: {translated}")
                else:
                    print(f"   - ⚠️ {i+1}번 번역 실패 (STT 결과 없음)")
                
                if i == 3 or (i == len(voices)-1): # 마지막 파일 또는 4번 파일을 대표 음성으로 함
                    voice_url = f"/static/audio/{temp_filename}"
            except Exception as file_err:
                print(f"   - ❌ {i+1}번 파일 처리 중 개별 에러: {file_err}")

        # [2] AI 판매글 생성
        category = product.category if product else "제주 농산물"
        print(f"✍️ [AI 생성 중] 카테고리: {category}")

        title, description = ai_service.generate_ad_text(
            category=category,
            weight=stt_answers[0] or "무게 정보 없음",
            harvest_date=stt_answers[1] or "최근 수확",
            taste=stt_answers[2] or "뛰어난 맛",
            message=stt_answers[3] or "전달 사항 없음"
        )

        print(f"✅ [완료] 제목 생성 결과: {title}")

        # [3] DB 업데이트 (DB 에러 방지를 위해 최종 텍스트 길이 제한)
        product.title = title[:250] if title else f"제주 {category} 상품"
        product.final_description = description
        product.voice_path = voice_url
        product.price = 23000  # 기본 추천 가격 미리 세팅 (0원 방지)
        db.commit()

        return BaseResponse(
            isSuccess=True, 
            content=GeneratedAdText(title=title, final_description=description)
        )

    except Exception as e:
        db.rollback()
        import traceback
        print(f"🔥 [CRITICAL 에러] /api/sale/text 처리 도중 전체 실패: {e}")
        traceback.print_exc() # 상세 에러 스택 파악용
        return BaseResponse(isSuccess=False, message=str(e), content=None)

    except Exception as e:
        db.rollback()
        return BaseResponse(isSuccess=False, content=None)

@router.post("/price", response_model=BaseResponse[PriceRecommendResponse])
async def recommend_price(
    req: PriceRecommendRequest,
    db: Session = Depends(get_db)
):
    """
    4단계: 적정가 추천 (23,000원 하드코딩)
    """
    FIXED_PRICE = 23000
    
    product = db.query(Product).filter(Product.product_id == req.product_id).first()
    if product:
        product.price = FIXED_PRICE
        db.commit()
    
    return BaseResponse(
        isSuccess=True, 
        content=PriceRecommendResponse(product_id=req.product_id, recommended_price=FIXED_PRICE)
    )

from app.common.utils import get_base64_encoded_file

@router.get("/salead", response_model=BaseResponse[SaleAdDetail])
async def get_sale_detail(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    5단계: 판매 글 상세 조회 (실제 데이터 및 Base64 이미지/음성)
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return BaseResponse(isSuccess=False, message="상품을 찾을 수 없습니다.", content=None)

    # 이미지 JOIN
    prod_img = db.query(ProductImage).filter(ProductImage.product_id == product_id).first()
    image_data_list = []
    
    if prod_img:
        for img_path in [prod_img.img1, prod_img.img2, prod_img.img3, prod_img.img4]:
            if img_path:
                encoded = get_base64_encoded_file(img_path)
                if encoded: image_data_list.append(encoded)

    voice_data = ""
    if product.voice_path:
        voice_data = get_base64_encoded_file(product.voice_path)

    return BaseResponse(
        isSuccess=True,
        content=SaleAdDetail(
            product_id=product.product_id,
            title=product.title or "제목 없음",
            price=product.price or 0, # 여기 0이 나오는 이유는 아직 4단계(가격 추천)를 안 거쳤기 때문일 수 있습니다.
            images=image_data_list,
            voice_url=voice_data,
            final_description=product.final_description or ""
        )
    )
