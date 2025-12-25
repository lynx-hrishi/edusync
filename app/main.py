from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes.auth import router as auth_router
from app.routes.learning import router as learning_router
from app.utils.globalErrorHandler import globalErrorHandler

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here", max_age=60 * 60 * 24)

globalErrorHandler(app)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(learning_router, prefix="/api", tags=["Learning"])

@app.get("/")
async def root():
    return {"message": "EduSync API is running"}