from typing import List

from pydantic import BaseModel


class DataResponse(BaseModel):
    status_code: int = 200
    success: bool = True
    result: BaseModel | None = None
    error: BaseModel | str | None = None
