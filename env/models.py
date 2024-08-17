
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    hashed_password: Optional[str] = None
    role: str = "ROLE_USER"

class Pet(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    color: Optional[str] = None
    mood: Optional[str] = "Happy"
    energy_level: Optional[int] = 100

class LoginUser(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Firulais",
                "type": "Perro",
                "color": "Marrón",
                "mood": "Excited",
                "energy_level": 80
            }
        }