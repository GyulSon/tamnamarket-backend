import base64
import os

def get_base64_encoded_file(file_path: str) -> str:
    """파일을 읽어 Base64 데이터 URL로 변환"""
    if not file_path:
        return ""
        
    try:
        # 실제 로컬 경로로 변환 (DB에는 /static/... 로 저장됨)
        true_path = file_path.lstrip("/")
        if not os.path.exists(true_path):
            return ""
            
        with open(true_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode("utf-8")
            
        # 확장자에 따른 mime type 설정
        ext = file_path.split(".")[-1].lower()
        mime_type = "image/jpeg"
        if ext in ["png"]: mime_type = "image/png"
        elif ext in ["webp"]: mime_type = "image/webp"
        elif ext in ["webm"]: mime_type = "audio/webm"
        elif ext in ["mp3"]: mime_type = "audio/mpeg"
        elif ext in ["m4a"]: mime_type = "audio/mp4"
        
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"Base64 인코딩 에러: {e}")
        return ""
