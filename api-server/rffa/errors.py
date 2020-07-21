from typing import Any, Optional

from fastapi import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse




class ErrorResponse(BaseModel):
    error_code: int
    message: str
    detail: Optional[Any]


class RFFAHTTPError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = 1000
    message = 'Unknown server error'
    headers: Optional[Any] = None

    def __init__(self, detail: Any = None):
        self.detail = detail

    @property
    def body(self):
        return ErrorResponse(
            error_code=self.error_code,
            message=self.message,
            detail=self.detail
        )

    @classmethod
    def response_model(cls):
        model = create_model(
            cls.__name__ + 'Response',
            __base__=ErrorResponse,
        )

        model.Config.schema_extra = {
            "example": {
                'error_code': cls.error_code,
                "message": cls.message,
            }
        }

        return model

    def json_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content=self.body.dict(exclude_none=True),
            headers=self.headers,
        )


class InvalidRequestError(RFFAHTTPError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = 1001
    message = 'Invalid request body'


