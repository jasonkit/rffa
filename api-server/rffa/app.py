from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from rffa.errors import InvalidRequestError, RFFAHTTPError

app = FastAPI(
    title='refined:FFA API',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(RFFAHTTPError)
def rffa_http_error_handler(request, exception: RFFAHTTPError):
    return exception.json_response()


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(
        request, exception: RequestValidationError):
    return InvalidRequestError(exception.errors()).json_response()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )

    http_validation_error = (
        openapi_schema['components']["schemas"]['HTTPValidationError']
    )

    http_validation_error['properties'] = {
        "error_code": {
            "title": "Error code",
            "type": "integer",
        },
        "message": {
            "title": "Message",
            "type": "string",
        },
        **http_validation_error['properties'],
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore
