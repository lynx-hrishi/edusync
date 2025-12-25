from fastapi import APIRouter, HTTPException
from app.models import LoginRequest, RegisterRequest, User

router = APIRouter()

# Mock database
users_db = []
user_id_counter = 1

@router.post("/login")
async def login(request: LoginRequest):
    user = next((u for u in users_db if u["email"] == request.email), None)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        },
        "token": f"mock_token_{user['id']}"
    }

@router.post("/register")
async def register(request: RegisterRequest):
    global user_id_counter
    
    if any(u["email"] == request.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": user_id_counter,
        "email": request.email,
        "password": request.password,
        "phone": request.phone,
        "name": request.name
    }
    
    users_db.append(new_user)
    user_id_counter += 1
    
    return {
        "message": "Registration successful",
        "user": {
            "id": new_user["id"],
            "email": new_user["email"],
            "name": new_user["name"]
        }
    }