from google.genai import Client
from google.genai import types
from PIL import Image
import os
from typing import List, Optional
from app.core.config import settings

from app.common.constants import ALLOWED_CATEGORIES

class AIService:
    def __init__(self):
        # 제준님의 API 키를 사용하여 클라이언트 초기화
        self.client = Client(api_key=settings.GEMINI_API_KEY)

    def classify_product(self, image_path: str) -> str:
        """
        1단계: 품종 분석 (Gemini 3.1 Flash-Lite)
        """
        try:
            img = Image.open(image_path)
            categories_str = ", ".join([f"'{c}'" for c in ALLOWED_CATEGORIES])
            prompt = (
                f"너는 제주도 농산물 판별 전문가야. 사진 속의 제주 특산물을 분류해줘.\n"
                f"결과는 반드시 {categories_str} 중 하나로만 대답해.\n"
                "설명 없이 단어만 출력해."
            )
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=[prompt, img],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="medium")
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"AI 분석 중 에러 발생: {e}")
            return "분류 에러"

    def generate_ad_text(self, category: str, weight: str, harvest_date: str, taste: str, message: str) -> tuple:
        """
        3단계: 4가지 답변을 바탕으로 전문적인 판매글 생성
        """
        try:
            prompt = (
                f"너는 제주도 농산물 직거래 플랫폼의 전문 마케터야. 아래 농부의 답변을 바탕으로 "
                f"신뢰감 있고 구매 욕구를 자극하는 판매글을 작성해줘.\n\n"
                f"1. 품종: {category}\n"
                f"2. 무게: {weight}\n"
                f"3. 수확일: {harvest_date}\n"
                f"4. 맛의 특징: {taste}\n"
                f"5. 농부의 한마디: {message}\n\n"
                f"### 작성 가이드:\n"
                f"- 제목은 반드시 '[품종] [무게]' 형식을 포함해야 하며, 20자 이내로 짧고 강렬하게 작성해.\n"
                f"- **상세 내용**: 인사말이나 서론('안녕하세요' 등)은 완전히 생략하고, 바로 상품의 특징을 3~5문장 내외로 간결하게 설명해.\n"
                f"- 수확 정보와 맛의 특징만 담은 담백하고 신뢰감 있는 문체를 사용해.\n"
                f"- **중요**: 서론이나 인사말 없이 바로 '제목:'과 '내용:' 항목만 출력해.\n\n"
                f"제목: [여기에 제목]\n"
                f"내용: [여기에 상세 내용]"
            )
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=prompt
            )
            full_text = response.text.strip()
            
            # 기본값 설정
            title = f"제주 {category} {weight}"
            description = full_text
            
            if "제목:" in full_text and "내용:" in full_text:
                parts = full_text.split("내용:")
                title = parts[0].replace("제목:", "").strip()
                # 제목이 너무 길면 자름 (DB 에러 방지)
                if len(title) > 50:
                    title = title[:47] + "..."
                description = parts[1].strip()
            
            return title, description
        except Exception as e:
            return f"제주 {category} {weight}", "맛있는 농산물입니다."

    def recommend_price(self, category: str, description: Optional[str] = "") -> int:
        """
        5단계: 적정 가격 추천 (AI 분석)
        """
        try:
            prompt = (
                f"너는 제주도 농산물 유통 전문가야. 아래 품종과 상품 정보를 바탕으로 "
                f"1kg당 적정 온라인 직거래 판매 가격(원)을 추천해줘. "
                f"결과는 '15000' 처럼 숫자만 출력해.\n\n"
                f"품종: {category}\n"
                f"상태 설명: {description}"
            )
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=prompt
            )
            price_text = response.text.strip().replace(",", "").replace("원", "")
            # 숫자가 아닐 경우를 대비한 파싱
            import re
            numbers = re.findall(r'\d+', price_text)
            if numbers:
                return int(numbers[0])
            return 15000 # 기본값
        except Exception as e:
            print(f"가격 추천 중 에러: {e}")
            return 12000

# 싱글톤 인스턴스
ai_service = AIService()
