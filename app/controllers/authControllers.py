from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import JSONResponse
from app.services.registerService import registerUserService, saveUserPreferenceService
from app.services.loginUserService import loginUserService
import json

router = APIRouter()

async def registerUser(payload: str = Form(...)):
    try:
        user = registerUserService(payload)
        if user:
            return JSONResponse(
                content={"message": "User registered successfully"},
                status_code=201
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def loginUser(request: Request, payload: str = Form(...)):
    try:
        user = loginUserService(payload)
        if user:
            # Add session data
            data = json.loads(payload)
            request.session["user_email"] = data.get("email")
            request.session["user_id"] = user
            return {"message": "User Logged in successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}