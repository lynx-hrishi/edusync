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
        print(user_id)

        # Get user preference
        cursor.execute("SELECT experience FROM user_preference WHERE user_id = %s", (user_id,))
        user_preference = cursor.fetchone()
        experience = user_preference[0] if user_preference else None
        print(experience)

        # Get total correct attempts
        cursor.execute("SELECT correct_attempts FROM progress WHERE user_id = %s", (user_id,))
        total_correct = cursor.fetchone()
        correct_attempts = total_correct[0] if total_correct[0] else 0
        print(correct_attempts)

        # Get completed chapters count
        cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id = %s AND isCompleted = 1", (user_id,))
        completed_count = cursor.fetchone()
        completed_chapters = completed_count[0] if completed_count else 0
        print(completed_chapters)

        # Get latest chapter name (highest chapter_id with progress)
        cursor.execute("""
            SELECT c.chapter_name 
            FROM chapters c 
            JOIN progress p ON c.chapter_id = p.chapter_id 
            WHERE p.user_id = %s 
            ORDER BY c.chapter_id DESC 
            LIMIT 1
        """, (user_id,))
        latest_chapter = cursor.fetchone()
        latest_chapter_name = latest_chapter[0] if latest_chapter else None
        print(latest_chapter_name)

        closeConnection(conn, cursor)
        
        return successResponse(data={
            "user_preference": experience,
            "correct_attempts": correct_attempts,
            "completed_chapters": completed_chapters,
            "latest_chapter_name": latest_chapter_name
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))