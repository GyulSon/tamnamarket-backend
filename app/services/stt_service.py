import json
import requests
from openai import OpenAI
from app.core.config import settings
import os

class STTService:
    def __init__(self):
        # 제준님의 API 키와 설정을 환경 변수에서 로드
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.clova_invoke_url = settings.CLOVA_INVOKE_URL
        self.clova_secret_key = settings.CLOVA_SECRET_KEY
        self.boosting_json_path = "app/assets/boosting.json"

        # 제준님표 제주 사투리 대조군 (Few-shot)
        self.few_shot_examples = [
            {"d": "무사 경 하맨?", "s": "왜 그렇게 하니?"},
            {"d": "제주도 바당은 잘도 곱다양.", "s": "제주도 바다는 정말 예쁘네요."},
            {"d": "호끔만 기둘려 봅서.", "s": "조금만 기다려 보세요."},
            {"d": "어멍 아방 다 편안 하우꽈?", "s": "어머니 아버지 모두 편안 하십니까?"},
            {"d": "오늘 날씨가 잘도 좋구게.", "s": "오늘 날씨가 정말 좋네요."},
            {"d": "이거 하영 먹으쿠과?", "s": "이거 많이 먹을까요?"},
            {"d": "혼저옵서예. 맛좋은 문게 이수다.", "s": "어서 오세요. 맛있는 문어가 있습니다."},
            {"d": "폭싹 속았수다. 게메이.", "s": "정말 수고 많으셨습니다. 그러게요."},
            {"d": "도새기 괴기 맛이 제라진디양.", "s": "돼지고기 맛이 아주 끝내주네요."},
            {"d": "무신 거옌 고람디 모르쿠게.", "s": "무슨 말인지 도무지 모르겠어요."},
            {"d": "맨도롱 홀 때 호로록 드십서.", "s": "따뜻할 때 얼른 드세요."},
            {"d": "감저 하영 캐느라 욕봤수다.", "s": "고구마 많이 캐느라 고생하셨습니다."},
            {"d": "지실이 잘도 잘 됐구게.", "s": "감자 농사가 정말 잘 되었네요."},
            {"d": "몸 건강히 잘 이십서게.", "s": "몸 건강히 잘 계세요."},
            {"d": "게난 말이우다. 어떵 하리까?", "s": "그러게 말입니다. 어떻게 할까요?"}
        ]

    def transcribe_and_translate(self, audio_path: str):
        """음성 파일 -> CLOVA STT(부스팅) -> GPT 번역 실행"""
        
        # 1. CLOVA STT 호출 (키워드 부스팅 적용)
        boosting_words = []
        try:
            if os.path.exists(self.boosting_json_path):
                with open(self.boosting_json_path, 'r', encoding='utf-8') as f:
                    boosting_data = json.load(f)
                boosting_words = [item['words'] for item in boosting_data]
        except Exception as e:
            print(f"부스팅 파일 로드 중 에러: {e}")

        headers = {"X-CLOVASPEECH-API-KEY": self.clova_secret_key}
        payload = {
            "language": "ko-KR",
            "completion": "sync",
            "model": "high_accuracy",
            "boostings": [{"words": ", ".join(boosting_words[:100])}], # 성능을 위해 일부 로드 (필요시 조정 가능)
            "fullText": True
        }

        with open(audio_path, 'rb') as f:
            files = {
                'media': f,
                'params': (None, json.dumps(payload), 'application/json')
            }
            endpoint = f"{self.clova_invoke_url.rstrip('/')}/recognizer/upload"
            response = requests.post(endpoint, headers=headers, files=files, timeout=300)
        
        res_json = response.json()
        raw_text = res_json.get('text', "")
        
        if not raw_text:
            return None, None

        # 2. GPT-4o 번역 호출 (Few-shot 적용)
        example_str = "\n".join([f"{i+1}. 방언: {ex['d']} -> 표준어: {ex['s']}" for i, ex in enumerate(self.few_shot_examples)])
        
        system_prompt = (
            "너는 제주도 방언을 현대 표준어로 일대일 대응하는 전문 번역 엔진이야.\n"
            "문맥상 제주 방언으로 판단되는 부분은 제공된 예시를 바탕으로 번역하고, "
            "나머지는 자연스러운 한국어 문장으로 다듬어서 출력해.\n\n"
            f"### 번역 예시:\n{example_str}"
        )
        
        gpt_res = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 제주 사투리를 표준어로 번역해: {raw_text}"}
            ],
            temperature=0.3
        )
        
        translated_text = gpt_res.choices[0].message.content
        return raw_text, translated_text

# 싱글톤 인스턴스
stt_service = STTService()
