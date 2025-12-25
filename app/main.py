from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes.auth import router as auth_router
from app.routes.learning import router as learning_router
from app.routes.userRoutes import router as user_router
from app.utils.globalErrorHandler import globalErrorHandler

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/Template")

# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key="your-secret-key-here", 
    max_age=60 * 60 * 24,
    same_site="lax",
    https_only=False
)

globalErrorHandler(app)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(learning_router, prefix="/api", tags=["Learning"])
app.include_router(user_router, prefix="/api", tags=["User"])
 
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def get_dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.get("/roadmap")
async def get_roadmap(request: Request):
    return templates.TemplateResponse("Roadmap.html", {"request": request})

@app.get("/profile")
async def get_profile(request: Request):
    return templates.TemplateResponse("Profile.html", {"request": request})

@app.get("/login")
async def get_profile(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@app.get("/register")
async def get_profile(request: Request):
    return templates.TemplateResponse("Register.html", {"request": request})