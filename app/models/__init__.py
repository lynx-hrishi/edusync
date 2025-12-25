from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    phone: str
    name: str

class SavePreferenceRequest(BaseModel):
    goals: List[str]
    preferences: List[str]
    experience: str

class CheckAnswerRequest(BaseModel):
    question_id: int
    chosen_option: str

class User(BaseModel):
    id: int
    email: str
    name: str
    phone: str

class Chapter(BaseModel):
    id: int
    title: str
    description: str

class Concept(BaseModel):
    id: int
    chapter_id: int
    title: str
    content: str

class Question(BaseModel):
    id: int
    concept_id: int
    question: str
    options: List[str]
    correct_answer: str

class LearningPath(BaseModel):
    user_id: int
    chapters: List[Chapter]
    progress: float