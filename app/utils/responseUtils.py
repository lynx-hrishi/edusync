from fastapi.responses import JSONResponse
from datetime import datetime

def successResponse(data=None, message="Success", status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "message": message
        }
    )

def errorResponse(error="Something went wrong", status_code=500):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "data": None,
            "error": error
        }
    )