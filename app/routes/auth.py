from fastapi import APIRouter, HTTPException, Request
from app.models import LoginRequest, RegisterRequest, User
from app.controllers.authControllers import registerUser, loginUser
from app.utils.responseUtils import successResponse, errorResponse

router = APIRouter()

router.post("/login")(loginUser)
router.post("/register")(registerUser)

# @router.get("/logout")
# async def logout(request: Request):
#     request.session.clear()
#     return successResponse(message="Logged out successfully")
