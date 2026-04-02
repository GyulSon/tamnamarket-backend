from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_sales():
    return {"message": "Sales route working"}
