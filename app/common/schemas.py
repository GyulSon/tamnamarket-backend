from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    """
    모든 API 응답의 표준 형식
    - 성공 시: isSuccess=True, content에 데이터 포함
    - 실패 시: isSuccess=False, message에 에러 이유 기재
    """
    isSuccess: bool
    message: Optional[str] = None
    content: Optional[T] = None
