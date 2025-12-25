from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.models import SavePreferenceRequest, CheckAnswerRequest, Chapter, Concept, Question, LearningPath
from typing import List
from app.controllers.authControllers import saveUserPreferenceService
from app.config.dbConnect import makeConnection, closeConnection, commitValues
from app.utils.responseUtils import successResponse, errorResponse
from app.services.geminiService import get_gemini_service

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
            cursor.execute("SELECT concept_id, concept_name FROM concepts where chapter_id = %s", (i[0],))
            concepts = cursor.fetchall()
            print(concepts)
            data = {
                "id": i[0],
                "title": i[1],
                "description": i[2],
                "concepts": []
            }
            for i in concepts:
                data["concepts"].append({
                    "concept_id": i[0],
                    "concept_name": i[1]
                })
            chapters_data.append(data)
        
        closeConnection(conn, cursor)
        return successResponse(data={"chapters": chapters_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/concepts/{chapter_id}/{concept_id}")
async def get_concepts(chapter_id: int, concept_id: int):
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result

        cursor.execute("SELECT * FROM concepts WHERE chapter_id = %s and concept_id = %s", (chapter_id, concept_id))
        concept_details = cursor.fetchone()
        # print(concept_details)
        concept = {
            "concept_id": concept_details[0],
            "chapter_id": concept_details[1],
            "concept_name": concept_details[2],
            "concept_desc": concept_details[3]
        }
        # print(concept)
        closeConnection(conn, cursor)
        return successResponse(data={"concept": concept})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/test-concept/{chapter_id}/{concept_id}")
async def test_concept(request: Request, chapter_id: int, concept_id: int):
    try:
        connection_result = makeConnection()
        if connection_result is None:
            raise Exception("Database connection failed")
        
        conn, cursor = connection_result

        cursor.execute("SELECT * FROM concepts WHERE chapter_id = %s and concept_id = %s", (chapter_id, concept_id))
        concept_details = cursor.fetchone()

        cursor.execute("SELECT preference, experience FROM user_preference where user_id = %s", (request.session.get("user_id"), ))
        user_data = cursor.fetchone()
        user_preference = user_data[0]
        user_experience = user_data[1]

        prompt_preference = {
            "Prefer more concise explanation": "Be more detailed when explaining the concepts",
            "Prefer more example savvy": "Be more detailed when explaining the concepts",
            "Prefer more pracice questions": "User needs more questions to solve"
        }

        print(concept_details, user_experience, user_preference, prompt_preference[user_preference])

        demo_question = {
            "question": "What is a linked list?",
            "options": ["A data structure", "A programming language", "A database system", "None of the above"],
            "correct_answer": "A data structure",
            "explanation": "A linked list is a linear data structure in which elements are stored in nodes, each containing a value and a reference to the next node."
        }

        prompt = f"""
        You are a tutor for data structures.
        Topic: {concept_details[2]}
        Difficulty: {user_experience}
        Student Preference: {prompt_preference[user_preference]}
        Generate {"5" if user_preference == "Prefer more pracice questions" else "3"} MCQ with 4 options and specify the correct option index and a short explanation.

        Instructions:
        - Your job is to return a JSON response with a structure as of question, options as an array, correct_option and an explaination.
        - Based on the user experience, ask questions which can help grow the student.

        Example:
        {demo_question}
        """

        # gemini = get_gemini_service()
        # res = gemini.generate_response(system_prompt=prompt)
        # print(res)



        # return successResponse(data={"questions": res})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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