from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_audio():
    return {"message": "Audio route working"}
