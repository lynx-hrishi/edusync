from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import JSONResponse
from app.services.registerService import registerUserService, saveUserPreferenceService
from app.services.loginUserService import loginUserService
from app.utils.responseUtils import successResponse, errorResponse
import json

router = APIRouter()

async def registerUser(payload: str = Form(...)):
    try:
        user = registerUserService(payload)
        if "error" in user:
            return errorResponse(error=user["error"], status_code=user["status"])
        elif user:
            return successResponse(message="User registered successfully", status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def loginUser(request: Request, payload: str = Form(...)):
    try:
        user = loginUserService(payload)
        if isinstance(user, dict):
            return errorResponse(error=user["error"], status_code=user["status"])
        elif user: 
            # Add session data
            data = json.loads(payload)
            request.session["user_email"] = data.get("email")
            request.session["user_id"] = user
            return successResponse(message="User logged in successfully", data={"redirect_url": "/dashboard"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def logout(request: Request):
    request.session.clear()
    return successResponse(message="Logged out successfully")