from fastapi import APIRouter, HTTPException, Request
from app.models import LoginRequest, RegisterRequest, User
from app.config.dbConnect import makeConnection, commitValues, closeConnection
from app.controllers.authControllers import registerUser, loginUser
from app.utils.responseUtils import successResponse, errorResponse

router = APIRouter()

@router.get("/learning-path")
async def get_learning_path(request: Request):
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result
        user_id = request.session.get("user_id")
        
        # Get user preference
        cursor.execute("SELECT experience FROM user_preference WHERE user_id = %s", (user_id,))
        pref_result = cursor.fetchone()
        experience = pref_result[0] if pref_result else None
        
        # Get total correct attempts
        cursor.execute("SELECT COALESCE(SUM(correct_attempts), 0) FROM progress WHERE user_id = %s", (user_id,))
        correct_result = cursor.fetchone()
        correct_attempts = int(correct_result[0]) if correct_result else 0
        
        # Get completed chapters count
        cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id = %s AND isCompleted = 1", (user_id,))
        completed_result = cursor.fetchone()
        completed_chapters = int(completed_result[0]) if completed_result else 0
        
        # Get latest chapter name
        cursor.execute("""
            SELECT c.chapter_name 
            FROM chapters c 
            JOIN progress p ON c.chapter_id = p.chapter_id 
            WHERE p.user_id = %s 
            ORDER BY c.chapter_id DESC 
            LIMIT 1
        """, (user_id,))
        latest_result = cursor.fetchone()
        latest_chapter_name = latest_result[0] if latest_result else None
            
        closeConnection(conn, cursor)
        
        return successResponse(data={
            "experience": experience,
            "correct_attempts": correct_attempts,
            "completed_chapters": completed_chapters,
            "latest_chapter_name": latest_chapter_name
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))