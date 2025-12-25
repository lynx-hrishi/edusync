from fastapi import APIRouter, HTTPException, Request
from app.models import LoginRequest, RegisterRequest, User
from app.controllers.login_controller import registerUser, loginUser

router = APIRouter()

router.post("/login")(loginUser)
router.post("/register")(registerUser)

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

@router.get("/session")
async def check_session(request: Request):
    if request.session.get("is_authenticated"):
        return {
            "authenticated": True,
            "user_email": request.session.get("user_email")
        }
    return {"authenticated": False}