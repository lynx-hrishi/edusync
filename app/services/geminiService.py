import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_response(self, user_message: str, system_prompt: str = None):
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {user_message}"
            else:
                full_prompt = user_message
                
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

def get_gemini_service():
    return GeminiService()