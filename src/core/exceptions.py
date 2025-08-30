from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    status_code: int = 400
    default_code: str = "error"
    default_detail: str = "Something went wrong."

    def __init__(
        self,
        detail: str | None = None,
        code: str | None = None,
        values: dict[str, Any] | None = None,
        status_code: int | None = None,
    ):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code
        self.values = values or {}
        self.status_code = status_code or self.status_code

        super().__init__(self.detail)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register exception handlers for the FastAPI application.
    """

    @app.exception_handler(APIException)
    async def _handle_api_exceptions(request: Request, exc: APIException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "code": exc.code,
                "variables": exc.values,
            },
        )
