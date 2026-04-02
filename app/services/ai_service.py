from google.genai import Client
from google.genai import types
from PIL import Image
import os
from typing import List, Optional
from app.core.config import settings

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
            prompt = (
                "너는 제주도 농산물 판별 전문가야. 이 사진 속의 제주 특산물(감귤류, 고사리, 땅콩, 당근)을 분류해줘. "
                "결과는 반드시 '한라봉', '천혜향', '레드향', '감귤', '고사리', '땅콩', '당근' 중 하나로만 대답해. "
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

    def generate_ad_text(self, category: str, stt_texts: List[str]) -> tuple:
        """
        4단계: AI 판매글 초안 작성
        """
        try:
            combined_context = "\n".join(stt_texts)
            prompt = (
                f"너는 제주도 직거래 플랫폼의 전문 마케터야. 아래 품종과 농부의 설명을 바탕으로 "
                f"소비자의 마음을 흔드는 제목과 상세 판매글 상세 내용을 작성해줘.\n\n"
                f"품종: {category}\n"
                f"농부의 설명 요약:\n{combined_context}\n\n"
                f"제목: [여기에 제목]\n"
                f"내용: [여기에 상세 내용]"
            )
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=prompt
            )
            full_text = response.text.strip()
            title = "신선한 제주 농산물"
            description = full_text
            if "제목:" in full_text and "내용:" in full_text:
                parts = full_text.split("내용:")
                title = parts[0].replace("제목:", "").strip()
                description = parts[1].strip()
            return title, description
        except Exception as e:
            return "상품 판매합니다", "맛있는 농산물입니다."

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
