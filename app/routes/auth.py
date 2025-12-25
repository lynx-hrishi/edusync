from fastapi import APIRouter, HTTPException, Request
from app.models import LoginRequest, RegisterRequest, User
from app.controllers.authControllers import registerUser, loginUser

router = APIRouter()

router.post("/login")(loginUser)
router.post("/register")(registerUser)

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}
