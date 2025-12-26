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
        if isinstance(user, dict):
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
            request.session["user_id"] = user[0]
            request.session["username"] = user[1]
            
            # Check if user has preferences set
            from app.config.dbConnect import makeConnection, closeConnection
            connection_result = makeConnection()
            if connection_result:
                conn, cursor = connection_result
                cursor.execute("SELECT COUNT(*) FROM user_preference WHERE user_id = %s", (user[0],))
                has_preferences = cursor.fetchone()[0] > 0
                closeConnection(conn, cursor)
                
                redirect_url = "/dashboard" if has_preferences else "/preferences"
            else:
                redirect_url = "/preferences"  # Default to preferences if DB check fails
            
            return successResponse(message="User logged in successfully", data={"redirect_url": redirect_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def logout(request: Request):
    request.session.clear()
    return successResponse(message="Logged out successfully")