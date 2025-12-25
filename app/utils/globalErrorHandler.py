from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class APIError(Exception):
    def __init__(self, msg: str = "Something went wrong", status: int = 500):
        self.msg = msg
        self.status = status

def globalErrorHandler(app: FastAPI):

    @app.exception_handler(Exception)
    async def errorHandler(request: Request, exc: Exception):
        # print("GlobalError")
        print(exc)
        return JSONResponse(
            status_code=500,
            content={
                "message": str(exc)
            }
        )
    
    @app.exception_handler(APIError)
    async def apiErrorhandler(request: Request, exc: APIError):
        # print("APIError")
        print(exc.status, exc.msg)
        return JSONResponse(
            status_code=exc.status,
            content={
                "message": str(exc.msg)
            }
        )