from fastapi import APIRouter, File, UploadFile
import uuid
import os

router = APIRouter()

@router.post("/classification")
async def analyze_image(file: UploadFile = File(...)):
    """
    프론트엔드로부터 이미지를 받아 분석 결과를 문자열로 반환하는 API
    """
    # 임시로 파일을 저장할 경로 설정 (static/images 디렉토리가 main.py에 설정되어 있음)
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("static/images", filename)
    
    # 이미지 파일 저장
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    # TODO: 추후 Gemini Vision 등의 이미지 분석 로직 추가
    return {"result": "테스트 성공입니다."}
