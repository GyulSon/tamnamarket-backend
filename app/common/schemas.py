from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    """
    모든 API 응답의 표준 형식
    isSuccess: 성공 여부 (True/False)
    content: 실제 데이터 (실패 시 None)
    """
    isSuccess: bool
    content: Optional[T] = None
