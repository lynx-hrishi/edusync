from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.learning import router as learning_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(learning_router, prefix="/api", tags=["Learning"])

@app.get("/")
async def root():
    return {"message": "EduSync API is running"}