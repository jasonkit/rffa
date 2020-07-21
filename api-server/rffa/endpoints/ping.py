from fastapi import status
from pydantic import BaseModel, Field

from rffa.app import app


class PingResponse(BaseModel):
    result: str = Field('pong', const=True, title='pong',
                        description='Always be `pong`')

    class Config:
        schema_extra = {
            "example": {
                'result': 'pong'
            }
        }


@app.get(
    '/ping',
    description='Health check',
    status_code=status.HTTP_200_OK,
    response_model=PingResponse,
)
def ping():
    return {
        'result': 'pong'
    }
