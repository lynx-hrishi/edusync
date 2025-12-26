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

@router.get("/profile")
async def get_profile(request: Request):
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result
        user_id = request.session.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="User not logged in")
        
        # Get user basic info
        cursor.execute("SELECT username, email, age FROM users WHERE user_id = %s", (user_id,))
        user_result = cursor.fetchone()
        if not user_result:
            raise HTTPException(status_code=404, detail="User not found")
        
        username, email, age = user_result
        
        # Get user preference
        cursor.execute("SELECT goals, preference, experience FROM user_preference WHERE user_id = %s", (user_id,))
        pref_result = cursor.fetchone()
        goals, preference, experience = pref_result if pref_result else (None, None, None)
        
        # Get total solved questions (correct attempts)
        cursor.execute("SELECT COALESCE(SUM(correct_attempts), 0) FROM progress WHERE user_id = %s", (user_id,))
        total_solved = int(cursor.fetchone()[0])
        
        # Get total attempts
        cursor.execute("SELECT COALESCE(SUM(total_attempts), 0) FROM progress WHERE user_id = %s", (user_id,))
        total_attempts = int(cursor.fetchone()[0])
        
        # Get completed chapters count
        cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id = %s AND isCompleted = 1", (user_id,))
        completed_chapters = int(cursor.fetchone()[0])
        
        # Get total chapters
        cursor.execute("SELECT COUNT(*) FROM chapters")
        total_chapters = int(cursor.fetchone()[0])
        
        # Calculate accuracy
        accuracy = round((total_solved / total_attempts * 100), 1) if total_attempts > 0 else 0
        
        # Get recent activity (last 5 chapters worked on)
        cursor.execute("""
            SELECT c.chapter_name, p.correct_attempts, p.total_attempts
            FROM chapters c 
            JOIN progress p ON c.chapter_id = p.chapter_id 
            WHERE p.user_id = %s AND p.total_attempts > 0
            ORDER BY p.progress_id DESC 
            LIMIT 5
        """, (user_id,))
        recent_activity = [{
            "chapter_name": row[0],
            "correct_attempts": int(row[1]),
            "total_attempts": int(row[2]),
            "accuracy": round((int(row[1]) / int(row[2]) * 100), 1) if int(row[2]) > 0 else 0
        } for row in cursor.fetchall()]
        
        closeConnection(conn, cursor)
        
        return successResponse(data={
            "user": {
                "username": username,
                "email": email,
                "age": age
            },
            "preferences": {
                "goals": goals,
                "preference": preference,
                "experience": experience
            },
            "stats": {
                "total_solved": total_solved,
                "total_attempts": total_attempts,
                "accuracy": accuracy,
                "completed_chapters": completed_chapters,
                "total_chapters": total_chapters,
                "completion_rate": round((completed_chapters / total_chapters * 100), 1) if total_chapters > 0 else 0
            },
            "recent_activity": recent_activity
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chapter-progress")
async def get_chapter_progress(request: Request):
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result
        user_id = request.session.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="User not logged in")
        
        # Get all chapters with their progress
        cursor.execute("""
            SELECT c.chapter_id, c.chapter_name, 
                   COALESCE(SUM(p.total_attempts), 0) as total_attempts,
                   COALESCE(SUM(p.correct_attempts), 0) as correct_attempts,
                   MAX(COALESCE(p.isCompleted, 0)) as is_completed,
                   COUNT(concepts.concept_id) as total_concepts,
                   COUNT(CASE WHEN cp.isCompleted = 1 THEN 1 END) as completed_concepts
            FROM chapters c
            LEFT JOIN progress p ON c.chapter_id = p.chapter_id AND p.user_id = %s
            LEFT JOIN concepts ON c.chapter_id = concepts.chapter_id
            LEFT JOIN concept_progress cp ON concepts.concept_id = cp.concept_id 
                AND cp.user_id = %s AND cp.chapter_id = c.chapter_id
            GROUP BY c.chapter_id, c.chapter_name
            ORDER BY c.chapter_id
        """, (user_id, user_id))
        
        chapters = cursor.fetchall()
        chapter_progress = []
        
        for chapter in chapters:
            chapter_id, chapter_name, total_attempts, correct_attempts, is_completed, total_concepts, completed_concepts = chapter
            
            # Convert to int
            total_attempts = int(total_attempts)
            correct_attempts = int(correct_attempts)
            total_concepts = int(total_concepts)
            completed_concepts = int(completed_concepts)
            
            # Calculate progress percentage based on concepts completed
            if total_concepts > 0:
                concept_progress = (completed_concepts / total_concepts) * 100
            else:
                concept_progress = 0
            
            # Calculate accuracy
            accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
            
            # Determine overall progress (weighted: 70% concept completion + 30% accuracy)
            if total_attempts > 0:
                overall_progress = (concept_progress * 0.7) + (accuracy * 0.3)
            else:
                overall_progress = concept_progress
            
            chapter_progress.append({
                "chapter_id": chapter_id,
                "chapter_name": chapter_name,
                "progress_percentage": round(overall_progress, 1),
                "concept_progress": round(concept_progress, 1),
                "accuracy": round(accuracy, 1),
                "total_attempts": total_attempts,
                "correct_attempts": correct_attempts,
                "completed_concepts": completed_concepts,
                "total_concepts": total_concepts,
                "is_completed": bool(is_completed),
                "status": "completed" if is_completed else ("in_progress" if total_attempts > 0 else "not_started")
            })
        
        closeConnection(conn, cursor)
        
        return successResponse(data={
            "chapters": chapter_progress
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))