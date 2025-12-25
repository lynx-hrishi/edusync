from fastapi import APIRouter, HTTPException, Form
from app.models import LoginRequest, RegisterRequest
from app.services.registerService import registerUserService

router = APIRouter()

async def registerUser(payload: str = Form(...)):
    try:
        user = registerUserService(payload)
        if user:
            return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
