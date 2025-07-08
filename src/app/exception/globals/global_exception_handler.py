from fastapi import Request, FastAPI, logger
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime
from fastapi.responses import JSONResponse
from src.app.exception.model import ErrorDetail


async def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        details = []
        for error in exc.errors():
            details.append(
                {
                    "loc": error.get("loc", ["unknown"]),
                    "msg": error.get("msg", "Unknown validation error"),
                    "type": error.get("type", "validation_error"),
                }
            )

        # Obtener la ruta de la solicitud actual como instance
        instance = f"request:{request.url.path}"

        error = ErrorDetail(
            type="https://api.file-track/errors/validation-error",
            title="Validation Error",
            status=422,
            detail="Error en la validación de datos de entrada",
            details=details,
            instance=instance,
            timestamp=datetime.now().isoformat(),
        )

        return JSONResponse(status_code=422, content=error.model_dump())

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Obtener la ruta de la solicitud actual como instance
        instance = f"request:{request.url.path}"

        error = ErrorDetail(
            type="https://api.file-track/errors/http-error",
            title="HTTP Error",
            status=exc.status_code,
            detail=(
                str(exc.detail)
                if isinstance(exc.detail, str)
                else "Error en la solicitud"
            ),
            details=exc.detail if not isinstance(exc.detail, str) else None,
            instance=instance,
            timestamp=datetime.now().isoformat(),
        )

        return JSONResponse(status_code=exc.status_code, content=error.model_dump())

    @app.exception_handler(AttributeError)
    async def attribute_error_handler(request: Request, exc: AttributeError):
        # Obtener la ruta de la solicitud actual como instance
        instance = f"request:{request.url.path}"

        error = ErrorDetail(
            type="https://api.file-track/errors/implementation-error",
            title="Implementation Error",
            status=500,
            detail="Error en la implementación del servicio",
            details=str(exc),
            instance=instance,
            timestamp=datetime.now().isoformat(),
        )

        logger.error(f"AttributeError: {exc}", exc_info=True)

        return JSONResponse(status_code=500, content=error.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Obtener la ruta de la solicitud actual como instance
        instance = f"request:{request.url.path}"

        error = ErrorDetail(
            type="https://api.file-track/errors/server-error",
            title="Server Error",
            status=500,
            detail="Se produjo un error interno del servidor",
            details=str(exc) if app.debug else None,
            instance=instance,
            timestamp=datetime.now().isoformat(),
        )

        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(status_code=500, content=error.model_dump())
