from fastapi import APIRouter, HTTPException
from app.models import LoginRequest, RegisterRequest, User
from app.controllers.login_controller import registerUser
router = APIRouter()

# Mock database
users_db = []
user_id_counter = 1

# router.post("/login")

router.post("/register")(registerUser)