from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from auth import create_access_token, authenticate_user, get_current_user
from models import UserCreate, LoginUser, Pet
from crud import *
from database import users_collection
from frontend import router as frontend_router  # Importa el router desde frontend.py
from auth import*
# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Virtual Pet API",
    description="Una API para gestionar mascotas virtuales, donde puedes crear, actualizar y eliminar mascotas.",
    version="1.0.0",
)

# Configuración de OAuth2 para la autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

# Incluye las rutas del frontend
app.include_router(frontend_router)

# Rutas de la API
@app.post("/register/", summary="Registrar un nuevo usuario", description="Permite registrar un nuevo usuario con un nombre de usuario y una contraseña.")
def register(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = {"username": user.username, "hashed_password": hashed_password, "role": "ROLE_USER", "pets": []}
    users_collection.insert_one(user_dict)
    return {"msg": "User registered successfully"}

@app.post("/login/", summary="Iniciar sesión", description="Permite a los usuarios autenticarse y obtener un token JWT.")
def login(user: LoginUser):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": authenticated_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/pets/", summary="Crear una nueva mascota", description="Crea una nueva mascota y la asocia al usuario autenticado.")
async def create_new_pet(pet: Pet, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    create_pet(pet, user)
    return {"msg": "Pet created successfully"}

@app.get("/pets/", summary="Listar las mascotas", description="Lista todas las mascotas del usuario autenticado.")
async def list_user_pets(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    pets = get_user_pets(user)
    return pets

@app.put("/pets/{pet_name}", summary="Actualizar una mascota", description="Actualiza la información de una mascota específica.")
async def update_user_pet(pet_name: str, pet: Pet, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    updated_pet = update_pet(pet_name, pet, user)
    return updated_pet

@app.delete("/pets/{pet_name}", summary="Eliminar una mascota", description="Elimina una mascota específica del usuario autenticado.")
async def delete_user_pet(pet_name: str, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    delete_pet(pet_name, user)
    return {"msg": "Pet deleted successfully"}

# Personalización del esquema de seguridad en Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Virtual Pet API",
        version="1.0.0",
        description="API para gestionar mascotas virtuales.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
