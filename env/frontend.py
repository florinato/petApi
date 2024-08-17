from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/manage_pets", response_class=HTMLResponse)
async def manage_pets(request: Request):
    return templates.TemplateResponse("manage_pets.html", {"request": request})

# main.py
from fastapi import FastAPI
from frontend import router as frontend_router

app = FastAPI()

app.include_router(frontend_router)  # Incluye las rutas del frontend