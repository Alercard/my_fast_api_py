from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# creamos el middleware para manejo de errores
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    # metodo que se ejecutara para detectar los errores errores
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            # ejecutamos la siguiente llamada
            return await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": str(e)
                }
            )