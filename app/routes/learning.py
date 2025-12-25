from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.models import SavePreferenceRequest, CheckAnswerRequest, Chapter, Concept, Question, LearningPath
from typing import List
from app.controllers.authControllers import saveUserPreferenceService
from app.config.dbConnect import makeConnection, closeConnection, commitValues
from app.utils.responseUtils import successResponse, errorResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/Template")

@router.post("/save-preference")
async def saveUserPreference(request: Request, payload: str = Form(...)):
    try:
        user = saveUserPreferenceService(request, payload)
        if user:
            return successResponse(message="User preference saved successfully", status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/chapters")
async def get_chapters():
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result

        cursor.execute("SELECT * FROM chapters")
        chapters = cursor.fetchall()

        chapters_data = []
        for i in chapters:
            cursor.execute("SELECT * FROM concepts where chapter_id = %s", (i[0],))
            concepts = cursor.fetchall()
            chapters_data.append({
                "id": i[0],
                "title": i[1],
                "description": i[2],
                "concepts": concepts
            })
        
        closeConnection(conn, cursor)
        return successResponse(data={"chapters": chapters_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @router.get("/concepts/{chapter_id}")
# async def get_concepts(chapter_id: int):
#     concepts = [c for c in concepts_db if c["chapter_id"] == chapter_id]
#     if not concepts:
#         raise HTTPException(status_code=404, detail="No concepts found for this chapter")
#     return {"concepts": concepts}

# @router.get("/concept/{concept_id}")
# async def get_concept(concept_id: int):
#     concept = next((c for c in concepts_db if c["id"] == concept_id), None)
#     if not concept:
#         raise HTTPException(status_code=404, detail="Concept not found")
#     return {"concept": concept}

# @router.get("/test-concept/{concept_id}")
# async def test_concept(concept_id: int):
#     questions = [q for q in questions_db if q["concept_id"] == concept_id]
#     if not questions:
#         raise HTTPException(status_code=404, detail="No questions found for this concept")
#     return {"questions": questions}

# @router.post("/check-answer")
# async def check_answer(request: CheckAnswerRequest):
#     question = next((q for q in questions_db if q["id"] == request.question_id), None)
#     if not question:
#         raise HTTPException(status_code=404, detail="Question not found")
    
#     is_correct = question["correct_answer"] == request.chosen_option
#     return {
#         "correct": is_correct,
#         "correct_answer": question["correct_answer"],
#         "explanation": "Well done!" if is_correct else f"The correct answer is: {question['correct_answer']}"
#     }

# @router.get("/check-mastery/{chapter_id}")
# async def check_mastery(chapter_id: int):
#     chapter = next((c for c in chapters_db if c["id"] == chapter_id), None)
#     if not chapter:
#         raise HTTPException(status_code=404, detail="Chapter not found")
    
#     return {
#         "chapter_id": chapter_id,
#         "mastery_level": 75.0,
#         "completed_concepts": 3,
#         "total_concepts": 5,
#         "status": "Good Progress"
#     }

# @router.get("/ask-hint/{question_id}")
# async def ask_hint(question_id: int):
#     question = next((q for q in questions_db if q["id"] == question_id), None)
#     if not question:
#         raise HTTPException(status_code=404, detail="Question not found")
    
#     hints = {
#         1: "Think about what stores data in programming",
#         2: "Consider what makes code reusable"
#     }
    
#     return {
#         "question_id": question_id,
#         "hint": hints.get(question_id, "Try to think about the key concepts related to this topic")
#     }